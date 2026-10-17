// 端到端验证这次改的四个功能（走真实桌面版路径：app:// + 真实 UI 操作）
//   1) 学生登录后能不能拿到老师设的内容范围
//   2) 未开放的年级是不是真的显示锁、数字对不对
//   3) 老师口令进后台能不能看到学生学习情况
//   4) 点开能不能看到每天学了多少
const { app, BrowserWindow, protocol } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const out = path.join(__dirname, '_teacher_e2e_result.txt');
const log = [];
const say = (s) => {
  log.push(s);
  fs.writeFileSync(out, log.join('\n') + '\n', 'utf8');
};

const hard = setTimeout(() => {
  say('HARD_TIMEOUT');
  app.exit(9);
}, 180000);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

app.whenReady().then(async () => {
  const distDir = path.join(__dirname, '..', 'dist');
  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '');
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(distDir, rel || 'index.html') });
  });

  const win = new BrowserWindow({ show: false, width: 420, height: 900, webPreferences: { contextIsolation: true } });
  const js = (code) => win.webContents.executeJavaScript(code);

  try {
    await win.loadURL('app://localhost/index.html');
    await sleep(1500);

    // ---------- 1. 学生登录，看有没有拿到范围 ----------
    await js('localStorage.clear(); location.hash = "#/login"; true');
    await sleep(1200);
    const loginRes = await js(`(async () => {
      const setVal = (el, v) => {
        Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set.call(el, v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
      };
      const ins = [...document.querySelectorAll('input')];
      if (ins.length < 2) return 'NO_INPUTS:' + ins.length;
      setVal(ins[0], '测试乙');
      setVal(ins[1], 'test123456');
      await new Promise(r => setTimeout(r, 200));
      [...document.querySelectorAll('button')].find(b => /登录/.test(b.textContent))?.click();
      for (let i = 0; i < 40; i++) {
        await new Promise(r => setTimeout(r, 400));
        const err = document.querySelector('.bg-rose-50');
        if (err && err.textContent.trim()) return 'ERROR: ' + err.textContent.trim();
        if (location.hash && location.hash !== '#/login') {
          await new Promise(r => setTimeout(r, 1200));
          return 'OK scope=' + (localStorage.getItem('hy-scope') || 'null');
        }
      }
      return 'TIMEOUT';
    })()`);
    say('1) 学生登录        : ' + loginRes);

    // ---------- 2. 未开放年级是否上锁 ----------
    await js('location.hash = "#/vocab"; true');
    await sleep(1500);
    const lockRes = await js(`(() => {
      const rows = [...document.querySelectorAll('button')].filter(b => /小学|初中|高中/.test(b.textContent));
      const locked = rows.filter(b => b.textContent.includes('🔒'));
      const open = rows.filter(b => !b.textContent.includes('🔒'));
      return '年级卡=' + rows.length + ' 上锁=' + locked.length + ' 可进=' + open.length
        + ' | 可进的是: ' + open.map(b => b.textContent.replace(/\\s+/g,' ').slice(0,18)).join(' / ');
    })()`);
    say('2) 年级列表        : ' + lockRes);

    // ---------- 3. 老师口令进后台看学习情况 ----------
    await js('location.hash = "#/teacher"; true');
    await sleep(1200);
    const teacherRes = await js(`(async () => {
      const setVal = (el, v) => {
        Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set.call(el, v);
        el.dispatchEvent(new Event('input', { bubbles: true }));
      };
      const pin = document.querySelector('input[type=password]');
      if (!pin) return 'NO_PIN_INPUT';
      setVal(pin, 'wwl31460');
      await new Promise(r => setTimeout(r, 200));
      [...document.querySelectorAll('button')].find(b => /进入/.test(b.textContent))?.click();
      for (let i = 0; i < 40; i++) {
        await new Promise(r => setTimeout(r, 400));
        const t = document.body.innerText;
        if (/已学/.test(t)) return 'OK ' + t.replace(/\\s+/g, ' ').slice(0, 200);
        const err = document.querySelector('.bg-rose-50');
        if (err && err.textContent.trim()) return 'ERROR: ' + err.textContent.trim();
      }
      return 'TIMEOUT body=' + document.body.innerText.replace(/\\s+/g,' ').slice(0, 120);
    })()`);
    say('3) 老师看学习情况  : ' + teacherRes);

    // ---------- 4. 点开某个学生看每日明细 ----------
    const detailRes = await js(`(async () => {
      const card = [...document.querySelectorAll('button')].find(b => /已学/.test(b.textContent));
      if (!card) return 'NO_STUDENT_CARD';
      card.click();
      for (let i = 0; i < 30; i++) {
        await new Promise(r => setTimeout(r, 400));
        const t = document.body.innerText;
        if (/每天学了多少/.test(t)) {
          const rows = [...document.querySelectorAll('div')].filter(d => /^\\d{4}-\\d{2}-\\d{2}$/.test(d.textContent.trim()));
          return 'OK 明细行=' + rows.length + ' | ' + t.replace(/\\s+/g, ' ').slice(0, 260);
        }
      }
      return 'TIMEOUT';
    })()`);
    say('4) 学生每日明细    : ' + detailRes);

    // ---------- 5. 内容范围编辑面板是否出来 ----------
    const scopeRes = await js(`(() => {
      const t = document.body.innerText;
      return '内容开放范围=' + /内容开放范围/.test(t) + ' 全部内容开放=' + /全部内容开放/.test(t)
        + ' 清除按钮=' + /清除这个学生/.test(t) + ' 年级格子=' + document.querySelectorAll('button').length;
    })()`);
    say('5) 授权编辑面板    : ' + scopeRes);
  } catch (e) {
    say('EXCEPTION: ' + e.message);
  } finally {
    clearTimeout(hard);
    app.exit(0);
  }
});
