// 端到端验证：走真实桌面版路径（app://localhost + 真实 UI 操作）完成一次登录，
// 用来确认「换后端后登录能不能通」——包括 app:// 这种非 http 来源是否被服务端放行。
const { app, BrowserWindow, protocol } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const out = path.join(__dirname, '_login_e2e_result.txt');
const hard = setTimeout(() => {
  fs.writeFileSync(out, 'HARD_TIMEOUT\n', 'utf8');
  app.exit(9);
}, 120000);

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
    await new Promise((r) => setTimeout(r, 1500));
    lines.push('origin        : ' + (await win.webContents.executeJavaScript('location.origin')));
    // 清掉可能残留的登录票据，保证是从头登录
    await win.webContents.executeJavaScript('localStorage.clear(); location.hash = "#/login"; true');
    await new Promise((r) => setTimeout(r, 1200));

    const script = `(async () => {
      const setVal = (el, v) => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
      };
      const inputs = [...document.querySelectorAll('input')];
      if (inputs.length < 2) return 'NO_INPUTS:' + inputs.length;
      setVal(inputs[0], '测试同学');
      setVal(inputs[1], 'test123456');
      await new Promise(r => setTimeout(r, 300));
      const btn = [...document.querySelectorAll('button')].find(b => /登录/.test(b.textContent));
      if (!btn) return 'NO_BUTTON';
      btn.click();
      for (let i = 0; i < 40; i++) {
        await new Promise(r => setTimeout(r, 500));
        const err = document.querySelector('.bg-rose-50');
        if (err && err.textContent && err.textContent.trim()) return 'ERROR: ' + err.textContent.trim();
        if (location.hash && location.hash !== '#/login') {
          await new Promise(r => setTimeout(r, 1500));
          return 'OK hash=' + location.hash + ' token=' + (localStorage.getItem('hy-token') ? 'saved' : 'MISSING')
            + ' page=' + document.body.innerText.replace(/\\s+/g, ' ').slice(0, 160);
        }
      }
      return 'STILL_ON_LOGIN';
    })()`;
    lines.push('login         : ' + (await win.webContents.executeJavaScript(script)));
  } catch (e) {
    lines.push('FAILED        : ' + String(e?.message || e));
  }
  clearTimeout(hard);
  fs.writeFileSync(out, lines.join('\n') + '\n', 'utf8');
  app.exit(0);
});
