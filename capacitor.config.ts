import type { CapacitorConfig } from '@capacitor/cli';

// 航悦英语 · 移动端（Android）壳配置
// 说明：这是一层 WebView 壳，界面与桌面版完全共用同一份 dist 产物，
// 因此手机/平板与电脑上的功能、数据（Supabase 云同步）天然一致。
const config: CapacitorConfig = {
  appId: 'com.hangyue.english',
  appName: '航悦英语',
  webDir: 'dist',
  // 让 WebView 的源为 https://localhost —— 安全上下文，
  // Web Audio、crypto.randomUUID、wss 语音合成都才能正常工作。
  server: {
    androidScheme: 'https',
  },
  android: {
    // 允许用 Chrome 远程调试 WebView（开发排查用，不影响正常使用）
    webContentsDebuggingEnabled: true,
    // 在线朗读（Edge 语音）必须伪装成 Edge 浏览器：微软服务端会校验 UA 里有没有 "Edg/"
    // 安卓 WebView 原生 UA 不带这个标记，握手会被直接拒绝，表现就是「完全没声音」。
    // 桌面版在 electron/main.cjs 里做了同样的事，这里补齐安卓端。
    overrideUserAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36 Edg/143.0.0.0',
  },
};

export default config;
