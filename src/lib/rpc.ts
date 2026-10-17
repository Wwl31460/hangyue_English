// 云端函数调用的统一入口
// 约定：所有 hy_* 函数都返回单个 jsonb 对象 { ok, ... }，失败时给中文 error。
// 网络异常（断网、超时）统一翻译成一句人话，调用方直接展示即可。
import { cloud, networkHint } from './cloud';

export async function callRpc(name: string, args: Record<string, unknown> = {}): Promise<any> {
  let res: any;
  try {
    // SDK 不传 schema 泛型时 rpc 的参数类型会被推成 never，这里按实际用法放开类型
    const db = cloud.database as any;
    res = await db.rpc(name, args);
  } catch (e) {
    throw new Error(networkHint(e));
  }
  if (res?.error) throw new Error(networkHint(res.error));
  // 函数返回 jsonb 对象时直接拿到对象；返回集合时兜底取第一条
  return Array.isArray(res?.data) ? (res.data[0] ?? null) : res.data;
}
