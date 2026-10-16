import { FormEvent, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { CLOUD_HEALTH_URL } from '../lib/supabaseClient';

// 探测云端是否可达。用 no-cors 只求"握手成功"——能把两种完全不同的原因分开：
//   连不上 → 是网络问题（服务器在国内网络常被阻断），再怎么输密码都没用；
//   连得上 → 才是账号密码的问题。
async function cloudReachable(): Promise<boolean> {
  try {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), 3500);
    await fetch(CLOUD_HEALTH_URL, { mode: 'no-cors', signal: ctl.signal, cache: 'no-store' });
    clearTimeout(timer);
    return true;
  } catch {
    return false;
  }
}

const NET_HELP =
  '连不上云端服务器：当前网络无法访问 Supabase（国内网络常被阻断）。请开启代理/VPN 后重试；' +
  '也可以先「返回首页」离线使用——本机学习进度照常保存，等网络恢复后再登录同步。';

// 登录页：学生用“用户名 + 密码”登录（账号由老师在后台设置）
export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const [probe, setProbe] = useState(false); // 正在探测云端连通性

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password) {
      setErr('请输入用户名和密码');
      return;
    }
    setBusy(true);
    setErr('');
    try {
      await login(username, password);
      nav('/'); // 登录成功回首页，进度会自动从云端加载
    } catch (e: any) {
      // 把 Supabase 的原始错误翻成中文，直接告诉用户卡在哪
      const msg = String(e?.message || '');
      const low = msg.toLowerCase();
      if (/not confirmed|email confirmation|confirm/i.test(low)) {
        setErr('登录失败：该账号还没激活。请在 Supabase 后台 Authentication → Users 里把此用户设为“已确认”，或关闭 Email 确认后重新添加。');
      } else if (/invalid|credentials/i.test(low)) {
        setErr('用户名或密码不正确。注意：在 Supabase 后台手动建的账号，其邮箱必须是「用户名@hangyue.local」；中文名请直接用 App 内「老师后台」添加最稳妥。');
      } else if (typeof navigator !== 'undefined' && navigator.onLine === false) {
        setErr('当前设备没有网络连接，无法登录。请连上网络后重试，或先离线使用。');
      } else {
        // 服务器都摸不到的话，就是网络问题而非账号问题。必须讲清楚，否则用户会一直以为密码错了
        setProbe(true);
        const reachable = await cloudReachable();
        setProbe(false);
        setErr(reachable ? '登录失败：' + (msg || '请稍后重试') : NET_HELP);
      }
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="page flex min-h-screen flex-col pb-10 pt-12">
      <div className="animate-fadeup">
        <div className="flex items-center gap-2">
          <span className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-brand-600 to-brand-800 text-xl shadow-soft">
            📖
          </span>
          <div>
            <h1 className="text-2xl font-extrabold tracking-tight text-brand-900">航悦英语</h1>
            <p className="text-xs text-slate-500">登录后进度自动保存到云端</p>
          </div>
        </div>
      </div>

      <form onSubmit={submit} className="card mt-8 animate-fadeup">
        <label className="section-title mb-0">用户名</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="老师给的用户名，如 xiaoming"
          autoComplete="username"
          className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
        />

        <label className="section-title mb-0 mt-4">密码</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="老师设置的密码"
          autoComplete="current-password"
          className="mt-2 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm outline-none focus:border-brand-400"
        />

        {err && <p className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-xs text-rose-600">{err}</p>}

        <button
          type="submit"
          disabled={busy}
          className="btn-primary mt-5 w-full !py-3 text-base disabled:opacity-60"
        >
          {busy ? (probe ? '正在检测网络…' : '登录中…') : '登录'}
        </button>
      </form>

      <p className="mt-4 text-center text-xs text-slate-400">
        账号由老师在 App 内的「老师后台」添加，用户名可以是中文或英文，自己无法注册。
      </p>

      <Link to="/" className="mt-auto pt-6 text-center text-sm text-brand-600">
        ← 返回首页（不登录也能先体验）
      </Link>
    </div>
  );
}
