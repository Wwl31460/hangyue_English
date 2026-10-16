// 无头渲染验收：复用 app:// 协议加载打包后的 dist，检查 #root 有内容且无致命报错
const { app, BrowserWindow, protocol } = require('electron');
const path = require('path');

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

app.whenReady().then(() => {
  const distDir = path.join(__dirname, '..', 'release', 'win-unpacked', 'resources', 'app.asar', 'dist');

  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(distDir, rel || 'index.html') });
  });

  const win = new BrowserWindow({
    show: false,
    width: 430,
    height: 880,
    webPreferences: { contextIsolation: true, nodeIntegration: false },
  });

  const errors = [];
  win.webContents.on('console-message', (e) => {
    if (e.type === 'error') errors.push(e.message);
  });
  win.webContents.on('did-fail-load', (e, code, desc) => errors.push('did-fail-load: ' + code + ' ' + desc));

  win.loadURL('app://localhost/index.html').then(() => {
    setTimeout(async () => {
      try {
        const html = await win.webContents.executeJavaScript(
          "document.getElementById('root') ? document.getElementById('root').innerHTML.length : -1"
        );
        const title = await win.webContents.executeJavaScript("document.querySelector('h1') ? document.querySelector('h1').innerText : '(no h1)'");
        const hasBackBar = await win.webContents.executeJavaScript(
          "!!Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('回到背单词'))"
        );
        console.log('ROOT_HTML_LEN=' + html);
        console.log('H1=' + title);
        console.log('HAS_BACKBAR=' + hasBackBar);
        console.log('ERRORS=' + (errors.length ? errors.join(' | ') : 'none'));
        app.quit();
      } catch (e) {
        console.log('EVAL_ERROR=' + e.message);
        app.quit();
      }
    }, 2500);
  });
});
