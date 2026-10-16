// 验证桌面版最终产物：按 electron/main.cjs 完全相同的方式（app:// 特权协议）
// 加载 release/win-unpacked/resources/app.asar 里的页面，确认打包后的桌面版渲染正常。
const { app, BrowserWindow, protocol, session } = require('electron');
const path = require('path');

const ASAR = path.join(__dirname, '..', 'release', 'win-unpacked', 'resources', 'app.asar');
const DIST = path.join(ASAR, 'dist');

const EDGE_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0';
app.userAgentFallback = EDGE_UA;

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

app.commandLine.appendSwitch('disable-gpu');

app
  .whenReady()
  .then(async () => {
    session.defaultSession.setUserAgent(EDGE_UA);

    protocol.registerFileProtocol('app', (request, callback) => {
      let rel = request.url.replace(/^app:\/\//, '').split('#')[0].split('?')[0];
      rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
      callback({ path: path.join(DIST, rel || 'index.html') });
    });

    const win = new BrowserWindow({
      width: 430,
      height: 880,
      show: false,
      webPreferences: { contextIsolation: true },
    });

    await win.loadURL('app://localhost/index.html');
    await new Promise((r) => setTimeout(r, 2500));

    const info = await win.webContents.executeJavaScript(`(() => ({
      title: document.title,
      brand: document.body.innerText.includes('航悦英语'),
      hasPageColumn: !!document.querySelector('.page'),
      cardCount: document.querySelectorAll('.card').length,
      pageWidth: (() => { const e = document.querySelector('.page'); return e ? Math.round(e.getBoundingClientRect().width) : -1; })(),
      isSecureContext: window.isSecureContext,
    }))()`);

    console.log('桌面版（asar + app://）加载结果:', JSON.stringify(info, null, 2));
    win.destroy();
    app.quit();
  })
  .catch((e) => {
    console.error('加载失败:', e);
    app.quit();
  });
