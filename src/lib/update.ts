// update.ts —— 版本号 + 在线检查更新 + 一键下载安装
//
// 更新清单放在 GitHub 仓库根目录的 version.json。App 每次打开、以及
// 「我的 → 检查更新」都会去读一次；有新版本就弹提示，点一下就能下载安装。
//
// 仓库在国外，国内网络访问 raw.githubusercontent.com 经常被阻断（GitHub 主站也时好时坏），
// 所以下面准备了几个镜像地址**并发**去试，谁先通用谁；全都失败就当作「暂时查不到更新」，
// 静默跳过、绝不打扰使用。

import { Capacitor, registerPlugin } from '@capacitor/core';

/** 当前版本：发新版时这里和 android/app/build.gradle 的 versionCode 要一起改 */
export const APP_VERSION = '1.1';
export const APP_VERSION_CODE = 2;

export const REPO_SLUG = 'Wwl31460/hangyue_English';
export const REPO_URL = `https://github.com/${REPO_SLUG}`;

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

// 清单地址，并发尝试
const MANIFEST_URLS = [
  `https://raw.githubusercontent.com/${REPO_SLUG}/main/version.json`,
  `https://cdn.jsdelivr.net/gh/${REPO_SLUG}@main/version.json`,
  `https://github.com/${REPO_SLUG}/raw/main/version.json`,
];

const TIMEOUT_MS = 8000;

async function fetchManifest(url: string): Promise<RemoteVersion> {
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, { signal: ctl.signal, cache: 'no-store' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = (await res.json()) as RemoteVersion;
    if (!data || typeof data.versionCode !== 'number') throw new Error('清单格式不正确');
    return data;
  } finally {
    clearTimeout(timer);
  }
}

// 并发请求，取第一个成功的结果；全部失败返回 null
function firstSuccess<T>(tasks: Promise<T>[]): Promise<T | null> {
  return new Promise((resolve) => {
    let pending = tasks.length;
    let settled = false;
    for (const t of tasks) {
      t.then((v) => {
        if (!settled) {
          settled = true;
          resolve(v);
        }
      }).catch(() => {
        if (--pending === 0 && !settled) {
          settled = true;
          resolve(null);
        }
      });
    }
  });
}

/** 去仓库读最新版本清单；网络不通时返回 null */
export async function fetchLatestVersion(): Promise<RemoteVersion | null> {
  return firstSuccess(MANIFEST_URLS.map((u) => fetchManifest(u)));
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
