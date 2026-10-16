// auth.tsx —— 账号体系（React 版）
// 职责：
//  1) 维护登录态（user / ready），首次进入自动恢复会话；
//  2) 提供 login(username, password) / logout()；
//  3) 提供云端进度的读取与保存（loadRemote / saveRemote），由 progress.tsx 调用。
// 学生用“用户名 + 密码”登录；内部把用户名拼成「用户名@hangyue.local」去对接 Supabase，
// 所以后台建账号时邮箱要填「用户名@hangyue.local」。
import {
  createContext,
  useContext,
  useEffect,
  useCallback,
  useRef,
  useState,
  ReactNode,
} from 'react';
import { supabase } from './supabaseClient';
import type { ProgressData } from './progress';

// 同步状态：local=未登录仅本地；loading=拉取中；saving=保存中；saved=已同步；error=同步失败
export type SyncState = 'local' | 'loading' | 'saving' | 'saved' | 'error';

interface AuthUser {
  id: string;
  name: string; // 显示名（默认取邮箱前缀，即用户名）
}

interface AuthCtx {
  user: AuthUser | null;
  ready: boolean; // 是否已确认登录态（首屏未确认前不要闪烁登录按钮）
  syncState: SyncState;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  // 老师后台用：按“用户名 + 密码”创建学生账号（邮箱由系统自动生成，老师无需填写）
  createStudent: (username: string, password: string) => Promise<void>;
  loadRemote: () => Promise<ProgressData | null>;
  saveRemote: (data: ProgressData) => Promise<void>;
}

const Ctx = createContext<AuthCtx | null>(null);

// 把“用户名”转成 Supabase 登录邮箱（底层必须是一个邮箱，但老师/学生都不用手填）：
// - 纯英文/数字的用户名（如 xiaoming）→ 直接用 xiaoming@hangyue.local（后台可见、可读）
// - 含中文等非 ASCII（如 小明）→ 邮箱不能含中文，改用用户名的编码生成稳定且合法的邮箱
//   这样无论用户名是中文还是英文，登录时都能唯一对应到同一个账号。
function toLoginEmail(u: string): string {
  const name = String(u || '').trim();
  if (!name) return '';
  if (/^[\x20-\x7E]+$/.test(name)) return name + '@hangyue.local'; // 纯 ASCII（英文/数字/常用符号）
  return 'u_' + utf8ToBase64Url(name) + '@hangyue.local'; // 中文等：编码成合法邮箱
}

// UTF-8 字符串 → URL-safe Base64（浏览器/Electron 都有 btoa、TextEncoder）
function utf8ToBase64Url(s: string): string {
  const bytes = new TextEncoder().encode(s);
  let bin = '';
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// 取显示名：优先用创建时存的真用户名（中文/英文都行），否则退回邮箱前缀
function displayName(u: { email?: string | null; user_metadata?: Record<string, any> }): string {
  const meta = u.user_metadata || {};
  if (meta.username) return meta.username as string;
  if (meta.display_name) return meta.display_name as string;
  const email = u.email || '';
  return email.split('@')[0] || '同学';
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [ready, setReady] = useState(false);
  const [syncState, setSyncState] = useState<SyncState>('local');

  // 进入页面：先看本地有没有已登录的会话（刷新/重开自动恢复）
  useEffect(() => {
    let active = true;
    supabase.auth.getSession().then(({ data }) => {
      if (!active) return;
      const s = data.session;
      if (s?.user) setUser({ id: s.user.id, name: displayName(s.user) });
      setReady(true);
    });
    // 登录/登出/token 刷新都会触发，保持登录态最新
    const { data: sub } = supabase.auth.onAuthStateChange((_e, session) => {
      if (session?.user) setUser({ id: session.user.id, name: displayName(session.user) });
      else setUser(null);
    });
    return () => {
      active = false;
      sub.subscription.unsubscribe();
    };
  }, []);

  // 登录：学生用用户名+密码；成功后会触发上面的 onAuthStateChange，progress.tsx 自动拉取进度
  const login = useCallback(async (username: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email: toLoginEmail(username),
      password,
    });
    if (error) throw error;
  }, []);

  const logout = useCallback(async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  }, []);

  // 老师后台创建学生：用户名(中文/英文) + 密码；邮箱自动生成，昵称存真用户名
  const createStudent = useCallback(async (username: string, password: string) => {
    const email = toLoginEmail(username);
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: { username, display_name: username } },
    });
    if (error) throw error;
  }, []);

  // 从云端拉取当前用户的完整进度；未登录返回 null
  const loadRemote = useCallback(async (): Promise<ProgressData | null> => {
    const { data: sess } = await supabase.auth.getUser();
    const u = sess.user;
    if (!u) return null;
    setSyncState('loading');
    const { data, error } = await supabase
      .from('user_progress')
      .select('data')
      .eq('user_id', u.id)
      .maybeSingle();
    if (error) {
      setSyncState('error');
      throw error;
    }
    setSyncState('saved');
    return (data?.data as ProgressData) ?? null;
  }, []);

  // 把整份进度保存到云端；未登录直接返回（不写库）
  const saveRemote = useCallback(async (data: ProgressData) => {
    const { data: sess } = await supabase.auth.getUser();
    const u = sess.user;
    if (!u) return;
    setSyncState('saving');
    const { error } = await supabase.from('user_progress').upsert(
      {
        user_id: u.id,
        display_name: u.email ? u.email.split('@')[0] : null,
        current_grade: (data as any).currentGrade ?? null,
        current_unit: (data as any).currentUnit ?? null,
        data,
        updated_at: new Date().toISOString(),
      },
      { onConflict: 'user_id' },
    );
    if (error) {
      setSyncState('error');
      throw error;
    }
    setSyncState('saved');
  }, []);

  const api: AuthCtx = { user, ready, syncState, login, logout, createStudent, loadRemote, saveRemote };
  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAuth(): AuthCtx {
  const c = useContext(Ctx);
  if (!c) throw new Error('useAuth 必须在 AuthProvider 内使用');
  return c;
}
