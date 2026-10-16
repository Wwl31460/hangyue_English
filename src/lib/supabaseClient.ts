// supabaseClient.ts —— Supabase 客户端（React/Vite 工程用本地安装的 SDK）
// publishable / anon key 可公开放在前端；数据安全靠数据表的 Row Level Security（RLS）保证，
// 只允许本人读写自己的数据。切勿把 service_role key 放到前端！
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://cqasnjbpglubtgwgkjvq.supabase.co';
const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_wDA8VSM51Uwq_H5OB11jhA_q9EASA6Q';

// 供登录页做连通性自检用：云服务器在国内网络常被阻断，需要把"网络不通"和"密码错"分开告诉用户
export const CLOUD_HEALTH_URL = SUPABASE_URL + '/auth/v1/health';

// 全局唯一客户端实例，auth.tsx / 进度同步都用它。
// detectSessionInUrl=false：本 App 用 HashRouter，不解析 URL 里的认证回调，避免冲突。
export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: {
    persistSession: true,      // 登录态存本地，关掉再开仍可自动恢复
    autoRefreshToken: true,    // token 过期自动刷新
    detectSessionInUrl: false,
  },
});
