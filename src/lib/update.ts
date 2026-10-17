// update.ts —— 版本号 + 在线检查更新 + 一键下载安装
//
// 更新清单由**云端接口**（hy_latest_release 函数）下发，安装包放在国内站点上。
// 为什么不直接把 version.json 当静态文件抓：静态站不返回跨域头，App 里用 fetch 读它
// 会被浏览器直接拦掉；而云端接口是跨域可用的，安卓 WebView / 桌面版都能正常读到。
//
// 下载安装包本身不受跨域限制（安卓交给系统下载器，桌面版交给浏览器），所以二进制走静态站。

import { Capacitor, registerPlugin } from '@capacitor/core';
import { cloud } from './cloud';

/** 当前版本：发新版时这里和 android/app/build.gradle 的 versionCode 要一起改 */
export const APP_VERSION = '1.3';
export const APP_VERSION_CODE = 4;

/** 应用站点（更新说明页 + 安装包下载地址），国内直连可达 */
export const SITE_URL = 'https://hangyue-english.app.workbuddy.host';

export interface UpdateAsset {
  url: string; // 安装包下载直链
  fileName: string; // 存到手机上用的文件名
  size?: number; // 字节数，仅用于展示
}

export interface RemoteVersion {
  version: string;
  versionCode: number;
  notes?: string; // 更新说明，一行一条
  publishedAt?: string;
  android?: UpdateAsset;
  windows?: UpdateAsset;
}

/** 去云端读最新版本清单；网络不通、没发布过都返回 null（静默跳过，不打扰使用） */
export async function fetchLatestVersion(): Promise<RemoteVersion | null> {
  try {
    // SDK 不传 schema 泛型时 rpc 的参数类型会被推成 never，这里按实际用法放开类型
    const res: any = await (cloud.database as any).rpc('hy_latest_release', {});
    if (res?.error) return null;
    const data = Array.isArray(res?.data) ? res.data[0] : res.data;
    if (!data || typeof data.versionCode !== 'number') return null;
    return data as RemoteVersion;
  } catch {
    return null;
  }
}

/** 云端版本是否比本机新 */
export function isNewer(remote: RemoteVersion): boolean {
  return (remote.versionCode || 0) > APP_VERSION_CODE;
}

/** 取当前平台对应的安装包 */
export function assetForThisPlatform(remote: RemoteVersion): UpdateAsset | null {
  const platform = Capacitor.getPlatform();
  if (platform === 'android') return remote.android ?? null;
  const ua = typeof navigator !== 'undefined' ? navigator.userAgent : '';
  if (/Windows/i.test(ua)) return remote.windows ?? null;
  return remote.android ?? remote.windows ?? null;
}

// ————— 原生插件：交给系统下载器下载，下载完拉起系统安装界面 —————
// 实现见 android/app/src/main/java/com/hangyue/english/UpdaterPlugin.java
interface UpdaterPlugin {
  download(o: { url: string; fileName: string }): Promise<{ id: number }>;
  progress(o: { id: number }): Promise<{ status: string; received: number; total: number }>;
  install(o: { id: number }): Promise<void>;
  openUrl(o: { url: string }): Promise<void>;
}

const Updater = registerPlugin<UpdaterPlugin>('Updater');

export interface UpdateProgress {
  percent: number; // 0~100；总量未知时给 -1（显示不确定进度）
  phase: 'downloading' | 'installing';
}

/** 用系统浏览器打开链接（桌面版走这里，安卓下载失败时也降级到这里） */
export function openInBrowser(url: string): void {
  if (Capacitor.getPlatform() === 'android') {
    void Updater.openUrl({ url }).catch(() => undefined);
    return;
  }
  window.open(url, '_blank');
}

/**
 * 立即更新。
 * 安卓：系统下载器下载（通知栏有进度），下载完自动弹出安装界面。
 * 其它环境：交给系统浏览器下载。
 */
export async function startUpdate(
  asset: UpdateAsset,
  onProgress: (p: UpdateProgress) => void,
): Promise<void> {
  if (Capacitor.getPlatform() !== 'android') {
    openInBrowser(asset.url);
    onProgress({ percent: 100, phase: 'installing' });
    return;
  }

  const { id } = await Updater.download({ url: asset.url, fileName: asset.fileName });
  // 轮询下载进度：每 0.8 秒问一次，最多等 12 分钟
  for (let i = 0; i < 900; i++) {
    const st = await Updater.progress({ id });
    if (st.status === 'done') break;
    if (st.status === 'failed') throw new Error('下载失败，请检查网络后重试');
    onProgress({
      percent: st.total > 0 ? Math.round((st.received / st.total) * 100) : -1,
      phase: 'downloading',
    });
    await new Promise((r) => setTimeout(r, 800));
  }
  onProgress({ percent: 100, phase: 'installing' });
  await Updater.install({ id });
}

// ————— 手动检查更新的入口 —————
// 「我的」页只放一个按钮，真正的弹窗由 App 根部统一渲染，避免每个页面各写一份。
let manualHandler: (() => void) | null = null;

export function setManualCheckHandler(fn: (() => void) | null): void {
  manualHandler = fn;
}

export function triggerManualCheck(): void {
  manualHandler?.();
}
