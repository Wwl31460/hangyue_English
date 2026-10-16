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
import { cloud, networkHint } from './cloud';
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

// 调服务端函数：把返回统一成 {ok, ...} 的对象；网络异常抛中文提示
async function callRpc(name: string, args: Record<string, unknown>): Promise<any> {
  let res: any;
  try {
    // SDK 不传 schema 泛型时 rpc 的参数类型会被推成 never，这里按实际用法放开类型
    const db = cloud.database as any;
    res = await db.rpc(name, args);
  } catch (e) {
    throw new Error(networkHint(e));
  }
  if (res?.error) throw new Error(networkHint(res.error));
  // 函数返回单个 jsonb → 直接是对象；返回集合时补一个空数组兜底
  return Array.isArray(res?.data) ? (res.data[0] ?? null) : res.data;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [ready, setReady] = useState(false);
  const [syncState, setSyncState] = useState<SyncState>('local');
  const tokenRef = useRef(''); // 当前票据，随登录/登出变化

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
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const r = await callRpc('hy_login', { p_username: username, p_password: password });
    if (!r) throw new Error('登录服务没有返回结果，请稍后重试。');
    if (!r.ok) throw new Error(r.error || '登录失败，请重试。');
    tokenRef.current = r.token;
    localStorage.setItem(TOKEN_KEY, r.token);
    localStorage.setItem(NAME_KEY, r.displayName);
    setUser({ id: r.username, name: r.displayName, role: r.role });
  }, []);

  const logout = useCallback(async () => {
    const token = tokenRef.current;
    tokenRef.current = '';
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(NAME_KEY);
    setUser(null);
    setSyncState('local');
    // 本地已经算登出了；作废服务端票据失败也不影响使用（票据会自然过期）
    if (token) {
      try {
        await callRpc('hy_logout', { p_token: token });
      } catch {
        /* 忽略 */
      }
    }
  }, []);

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

  const api: AuthCtx = { user, ready, syncState, login, logout, createStudent, loadRemote, saveRemote };
  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useAuth(): AuthCtx {
  const c = useContext(Ctx);
  if (!c) throw new Error('useAuth 必须在 AuthProvider 内使用');
  return c;
}
