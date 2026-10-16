// 多视口截图：用 Electron 内置 Chromium 按手机/平板/桌面尺寸渲染 dist，
// 直观验证响应式适配（手机窄栏不变、平板/桌面加宽居中）。
// 说明：单窗口 + 切 hash 的方式，比反复 loadURL 更稳。
const { app, BrowserWindow, protocol } = require('electron');
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const OUT = path.join(ROOT, 'shots');

const VIEWS = [
  { name: '1-phone', w: 390, h: 844 }, // 常见手机
  { name: '2-tablet-portrait', w: 768, h: 1024 }, // 平板竖屏
  { name: '3-tablet-landscape', w: 1024, h: 768 }, // 平板横屏
  { name: '4-desktop', w: 1440, h: 900 }, // 电脑
];

const ROUTES = [
  { key: 'home', hash: '/' },
  { key: 'vocab', hash: '/vocab' },
  { key: 'me', hash: '/me' },
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

app.commandLine.appendSwitch('disable-gpu');

app
  .whenReady()
  .then(async () => {
    // 与 electron/main.cjs 相同的 app:// 协议处理
    protocol.registerFileProtocol('app', (request, callback) => {
      let rel = request.url.replace(/^app:\/\//, '').split('#')[0].split('?')[0];
      rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
      callback({ path: path.join(DIST, rel || 'index.html') });
    });

    if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

    const win = new BrowserWindow({
      width: VIEWS[0].w,
      height: VIEWS[0].h,
      useContentSize: true,
      show: false,
      webPreferences: { contextIsolation: true },
    });

    await win.loadURL('app://localhost/index.html#/');
    await sleep(2000);

    for (const v of VIEWS) {
      win.setContentSize(v.w, v.h);
      await sleep(600);

      for (const r of ROUTES) {
        await win.webContents.executeJavaScript(
          `window.location.hash = ${JSON.stringify('#' + r.hash)}; true`,
        );
        await sleep(1300);

        const img = await win.webContents.capturePage();
        fs.writeFileSync(path.join(OUT, `${v.name}-${r.key}.png`), img.toPNG());

        // 量出内容列实际宽度，验证 .page 响应式是否生效
        const width = await win.webContents.executeJavaScript(
          `(() => { const el = document.querySelector('.page'); return el ? Math.round(el.getBoundingClientRect().width) : -1; })()`,
        );
        console.log(`shot ${v.name}-${r.key}  viewport=${v.w}x${v.h}  .page宽=${width}px`);
      }
    }

    console.log('ALL DONE');
    win.destroy();
    app.quit();
  })
  .catch((e) => {
    console.error(e);
    app.quit();
  });
