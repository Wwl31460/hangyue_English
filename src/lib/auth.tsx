// auth.tsx —— 账号体系（React 版）
//
// 后端已从 Supabase 换成国内可达的托管云服务（见 lib/cloud.ts）。云服务自带登录不支持
// 「用户名 + 密码」，所以账号表由我们自己的服务端函数来管，App 只调这几个函数：
//   hy_create_student    老师后台建号（老师口令在服务端校验）；同名即改密码
//   hy_login             用户名 + 密码登录，成功后返回一张 180 天有效的票据(token)
//   hy_restore           重开 App 时拿本地票据向云端核对登录态
//   hy_logout            登出，作废票据
//   hy_load/save_progress 学习进度读写（凭票据，不认用户名）
// 本地只存票据和用户名，密码本身不落地。
import {
  createContext,
  useContext,
  useEffect,
  useCallback,
  useRef,
  useState,
  ReactNode,
} from 'react';
import { callRpc } from './rpc';
import type { ProgressData } from './progress';

// 同步状态：local=未登录仅本地；loading=拉取中；saving=保存中；saved=已同步；error=同步失败
export type SyncState = 'local' | 'loading' | 'saving' | 'saved' | 'error';

interface AuthUser {
  id: string; // 用户名的规范化形式
  name: string; // 显示名（用户名的原始写法）
  role: string; // teacher / student
}

interface AuthCtx {
  user: AuthUser | null;
  ready: boolean; // 是否已确认登录态（首屏未确认前不要闪烁登录按钮）
  syncState: SyncState;
  // 老师给当前账号开放的年级 id 列表；null = 不限制（全部内容可学）
  scope: string[] | null;
  canOpen: (gradeId: string) => boolean; // 这个年级是否已开放
  refreshScope: () => Promise<void>; // 重新拉一次范围（老师刚改完时用）
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  // 老师后台用：老师口令 + 用户名 + 密码创建（或重置）学生账号
  createStudent: (username: string, password: string, pin: string) => Promise<{ isNew: boolean }>;
  loadRemote: () => Promise<ProgressData | null>;
  saveRemote: (data: ProgressData) => Promise<void>;
}

const Ctx = createContext<AuthCtx | null>(null);

const TOKEN_KEY = 'hy-token'; // 登录票据
const NAME_KEY = 'hy-name'; // 用户名缓存（断网时也能显示名字）
const SCOPE_KEY = 'hy-scope'; // 老师给这个账号开放的年级范围（缓存一份，断网也能显示锁）

// 调服务端函数的统一封装在 lib/rpc.ts（老师后台也用它，避免两份实现走偏）

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [ready, setReady] = useState(false);
  const [syncState, setSyncState] = useState<SyncState>('local');
  const tokenRef = useRef(''); // 当前票据，随登录/登出变化

  // 老师开放的年级范围：null = 全部可学。初值取本机缓存，断网时也能显示锁。
  const [scope, setScope] = useState<string[] | null>(() => {
    try {
      const raw = localStorage.getItem(SCOPE_KEY);
      const v = raw ? JSON.parse(raw) : null;
      return Array.isArray(v) && v.length > 0 ? (v as string[]) : null;
    } catch {
      return null;
    }
  });

  const applyScope = useCallback((s: unknown) => {
    const list = Array.isArray(s) && s.length > 0 ? (s as string[]) : null;
    setScope(list);
    try {
      if (list) localStorage.setItem(SCOPE_KEY, JSON.stringify(list));
      else localStorage.removeItem(SCOPE_KEY);
    } catch {
      /* 存不下不影响使用 */
    }
  }, []);

  // 登录后拉一次范围。失败就沿用本机缓存——既不误锁学生，也不擅自放开。
  const loadScope = useCallback(async () => {
    if (!tokenRef.current) {
      applyScope(null);
      return;
    }
    try {
      const r = await callRpc('hy_my_scope', { p_token: tokenRef.current });
      if (r?.ok) applyScope(r.scope);
    } catch {
      /* 网络问题忽略 */
    }
  }, [applyScope]);

  // 进入页面：拿本地票据向云端核对一次，确认是否仍是登录态
  useEffect(() => {
    let active = true;
    (async () => {
      const token = localStorage.getItem(TOKEN_KEY) || '';
      if (!token) {
        if (active) setReady(true);
        return;
      }
      tokenRef.current = token;
      try {
        const r = await callRpc('hy_restore', { p_token: token });
        if (!active) return;
        if (r?.ok) {
          localStorage.setItem(NAME_KEY, r.displayName);
          setUser({ id: r.username, name: r.displayName, role: r.role });
          void loadScope();
        } else {
          // 票据真的失效了（过期/被登出）：清掉，回到未登录
          localStorage.removeItem(TOKEN_KEY);
          localStorage.removeItem(NAME_KEY);
          tokenRef.current = '';
        }
      } catch {
        // 只是网络不通而已，不能把登录态清掉——先用本地缓存的用户名顶着，联网后自动恢复
        const cached = localStorage.getItem(NAME_KEY);
        if (active && cached) setUser({ id: cached, name: cached, role: '' });
      } finally {
        if (active) setReady(true);
      }
    })();
    return () => {
      active = false;
    };
  }, [loadScope]);

  const login = useCallback(async (username: string, password: string) => {
    const r = await callRpc('hy_login', { p_username: username, p_password: password });
    if (!r) throw new Error('登录服务没有返回结果，请稍后重试。');
    if (!r.ok) throw new Error(r.error || '登录失败，请重试。');
    tokenRef.current = r.token;
    localStorage.setItem(TOKEN_KEY, r.token);
    localStorage.setItem(NAME_KEY, r.displayName);
    setUser({ id: r.username, name: r.displayName, role: r.role });
    await loadScope();
  }, [loadScope]);

  const logout = useCallback(async () => {
    const token = tokenRef.current;
    tokenRef.current = '';
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(NAME_KEY);
    setUser(null);
    setSyncState('local');
    applyScope(null); // 登出后不再受上一个账号的范围影响
    // 本地已经算登出了；作废服务端票据失败也不影响使用（票据会自然过期）
    if (token) {
      try {
        await callRpc('hy_logout', { p_token: token });
      } catch {
        /* 忽略 */
      }
    }
  }, [applyScope]);

  const createStudent = useCallback(async (username: string, password: string, pin: string) => {
    const r = await callRpc('hy_create_student', {
      p_pin: pin,
      p_username: username,
      p_password: password,
    });
    if (!r?.ok) throw new Error(r?.error || '添加失败，请重试。');
    return { isNew: !!r.isNew };
  }, []);

  // 从云端拉取当前账号的完整进度；没登录/云端还没记录都返回 null
  const loadRemote = useCallback(async (): Promise<ProgressData | null> => {
    if (!tokenRef.current) return null;
    setSyncState('loading');
    const r = await callRpc('hy_load_progress', { p_token: tokenRef.current });
    if (!r?.ok) {
      setSyncState('error');
      throw new Error(r?.error || '读取云端进度失败');
    }
    setSyncState('saved');
    return (r.data as ProgressData) ?? null;
  }, []);

  // 把整份进度保存到云端；未登录直接返回（不写库）
  const saveRemote = useCallback(async (data: ProgressData) => {
    if (!tokenRef.current) return;
    setSyncState('saving');
    const r = await callRpc('hy_save_progress', {
      p_token: tokenRef.current,
      p_data: data as unknown as Record<string, unknown>,
    });
    if (!r?.ok) {
      setSyncState('error');
      throw new Error(r?.error || '保存到云端失败');
    }
    setSyncState('saved');
  }, []);

  // 未登录 = 不限制（离线随便学）；登录后按老师设置的范围来
  const canOpen = useCallback(
    (gradeId: string) => !user || scope === null || scope.includes(gradeId),
    [user, scope],
  );

  const api: AuthCtx = {
    user,
    ready,
    syncState,
    scope,
    canOpen,
    refreshScope: loadScope,
    login,
    logout,
    createStudent,
    loadRemote,
    saveRemote,
  };
  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAuth(): AuthCtx {
  const c = useContext(Ctx);
  if (!c) throw new Error('useAuth 必须在 AuthProvider 内使用');
  return c;
}
