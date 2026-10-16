// cloud.ts —— 云端客户端（换成国内可达的托管云服务）
//
// 为什么换：原来的 Supabase 服务器在国内网络被阻断，登录、同步全都连不上。
// 现在用 WorkBuddy 云服务（endpoint 在国内可达），只做两件事：账号、学习进度。
//
// 下面的 endpoint / publishableKey 就是云服务开通后返回的 publicConfig，本身就是
// 可以放在前端代码里的公开配置（服务端会校验请求来源），真正的权限控制在数据库那一层。
import { createWorkBuddyCloud } from '@tencent-ai/workbuddy-cloud-sdk';

export const CLOUD_ENDPOINT = 'https://hangyue-english.app.workbuddy.host';
export const CLOUD_PUBLISHABLE_KEY =
  'wbpk_ax6EubsOCr5M7E3MzPNr23_96r7HJritKmoevSoc6w69ucURYYtri82';

// 全局唯一客户端实例：auth.tsx 的账号、进度同步都用它
export const cloud = createWorkBuddyCloud({
  endpoint: CLOUD_ENDPOINT,
  publishableKey: CLOUD_PUBLISHABLE_KEY,
});

/** 把各种网络异常统一翻译成用户能看懂的一句话 */
export function networkHint(err: unknown): string {
  const msg = String((err as any)?.message ?? err ?? '');
  if (/failed to fetch|networkerror|load failed|err_|timeout|abort|fetch failed/i.test(msg)) {
    return '连不上云端服务器（网络不通）。请检查网络后重试；也可以先返回首页离线使用，本机学习进度照常保存，等网络恢复后再登录同步。';
  }
  return msg || '云端请求失败，请稍后重试。';
}
