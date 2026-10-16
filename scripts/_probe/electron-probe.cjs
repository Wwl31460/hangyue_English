// 用 Electron（Chromium）加载探测页，读出结果写到 result.txt
// 用法：electron scripts/_probe/electron-probe.cjs <url>
const { app, BrowserWindow } = require('electron');
const fs = require('node:fs');
const path = require('node:path');

const url = process.argv[2];
const outFile = path.join(__dirname, 'result.txt');

app.whenReady().then(async () => {
  const win = new BrowserWindow({
    show: false,
    webPreferences: { nodeIntegration: false, contextIsolation: true },
  });
  const lines = [];
  try {
    await win.loadURL(url);
    let result = null;
    for (let i = 0; i < 40; i++) {
      await new Promise((r) => setTimeout(r, 500));
      const st = await win.webContents
        .executeJavaScript('window.probeState || "running"')
        .catch(() => 'running');
      if (st === 'done') {
        result = await win.webContents.executeJavaScript('window.probeResult || ""');
        break;
      }
    }
    lines.push('URL      : ' + url);
    lines.push('origin   : ' + (await win.webContents.executeJavaScript('location.origin').catch(() => '?')));
    lines.push('RESULT   : ' + result);
  } catch (e) {
    lines.push('FAILED   : ' + String(e?.message || e));
  }
  fs.writeFileSync(outFile, lines.join('\n') + '\n', 'utf8');
  app.exit(0);
});
