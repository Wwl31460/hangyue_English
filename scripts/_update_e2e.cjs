// 端到端验证「检查更新」：走真实桌面版路径（app://localhost + 真实 UI），
// 看启动后能不能读到云端清单并弹出更新提示。
const { app, BrowserWindow, protocol } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const out = path.join(__dirname, '_update_e2e_result.txt');
const hard = setTimeout(() => {
  fs.writeFileSync(out, 'HARD_TIMEOUT\n', 'utf8');
  app.exit(9);
}, 90000);

app.whenReady().then(async () => {
  const distDir = path.join(__dirname, '..', 'dist');
  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(distDir, rel || 'index.html') });
  });

  const win = new BrowserWindow({
    show: false,
    webPreferences: { contextIsolation: true, nodeIntegration: false },
  });

  const lines = [];
  try {
    await win.loadURL('app://localhost/index.html');
    // 启动 2 秒后才检查更新，这里多等一会儿
    let found = '';
    for (let i = 0; i < 24; i++) {
      await new Promise((r) => setTimeout(r, 500));
      const t = await win.webContents.executeJavaScript('document.body.innerText');
      if (t.includes('发现新版本')) {
        found = t.replace(/\s+/g, ' ').slice(0, 220);
        break;
      }
    }
    lines.push('UPDATE_DIALOG : ' + (found || '（没有弹出更新提示）'));
  } catch (e) {
    lines.push('FAILED        : ' + String(e?.message || e));
  }
  clearTimeout(hard);
  fs.writeFileSync(out, lines.join('\n') + '\n', 'utf8');
  app.exit(0);
});
