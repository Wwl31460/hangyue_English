// Electron 主进程：加载本地构建（桌面双击打开）
const { app, BrowserWindow, protocol, session, shell } = require('electron');
const path = require('path');

// Edge 在线朗读服务（wss://speech.platform.bing.com）会校验 User-Agent：
// 必须包含 "Edg/" 才放行，否则握手直接 403。Electron 默认 UA 会被拒，
// 这里统一伪装成 Edge，确保真人语音可用（离线朗读仍走系统语音兜底）。
const EDGE_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0';
app.userAgentFallback = EDGE_UA;

// 注册特权协议：让打包后的 ES Module / 绝对路径在 file:// 下也能正常加载（避免白屏）
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

function createWindow() {
  const win = new BrowserWindow({
    width: 430,
    height: 880,
    minWidth: 360,
    minHeight: 640,
    backgroundColor: '#eef2f7',
    title: '航悦英语',
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // 「检查更新」时页面会 window.open 下载地址：交给系统默认浏览器处理，
  // 不要在应用里再弹一个窗口出来（那样用户既看不到下载、也没法另存）
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:/i.test(url)) {
      void shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  const devUrl = process.env.ELECTRON_RENDERER_URL;
  if (devUrl) {
    // 开发模式：加载 vite 本地服务
    win.loadURL(devUrl);
    return;
  }

  // 生产模式：通过 app:// 协议加载 dist（避免 file:// 下的模块脚本 CORS 白屏）
  win.loadURL('app://localhost/index.html');
}

app.whenReady().then(() => {
  const distDir = path.join(__dirname, '..', 'dist');

  // 会话级 UA 同样改为 Edge：渲染进程的 WebSocket 握手也走这里
  session.defaultSession.setUserAgent(EDGE_UA);

  protocol.registerFileProtocol('app', (request, callback) => {
    // 先去掉 #hash 与 ?query：HashRouter 换页后刷新时 URL 会带 #/xxx，
    // 若不过滤会被当成文件名，导致白屏 ERR_FILE_NOT_FOUND
    let rel = request.url.replace(/^app:\/\//, '').split('#')[0].split('?')[0];
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(distDir, rel || 'index.html') });
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
