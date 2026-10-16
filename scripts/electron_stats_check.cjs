// 学习统计端到端验证：往本机存档塞入历史数据（含旧格式），
// 打开真实打包产物进「我的」页，看统计数字是否算对。
const { app, BrowserWindow, protocol, session } = require('electron');
const path = require('path');

const EDGE_UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/143.0.3650.75 Safari/537.36 Edg/143.0.3650.75';
app.userAgentFallback = EDGE_UA;
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true, supportFetchAPI: true, stream: true } },
]);

const DIST = process.env.CHECK_DIST || path.join(__dirname, '..', 'dist');
const hardTimer = setTimeout(() => { console.log('STEP: HARD_TIMEOUT'); app.exit(9); }, 60000);

function dayKey(offset) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

// 造数据：
//   今天      words10 readings1(满分) minutes15 → 10 星
//   昨天      words4  bonus1            minutes20 → 2+1 = 3 星
//   3 天前    【旧格式】数值 18 = 分钟             → 迁移后 0 星（只有时长）
//   5 天前    words2                              → 1 星
// 期望：累计 14.0 星 / 积分 1 / 连续 2 天 / 7 天区间 单词16 听读1 学习天3 获星14.0
const today = dayKey(0);
const seed = {
  daily: { date: today, words: 10, readings: 1, minutes: 15, readingIds: ['r1'], bonus: 0 },
  history: {
    [today]: { date: today, words: 10, readings: 1, minutes: 15, readingIds: ['r1'], bonus: 0 },
    [dayKey(-1)]: { date: dayKey(-1), words: 4, readings: 0, minutes: 20, readingIds: [], bonus: 1 },
    [dayKey(-3)]: 18, // ← 旧格式：直接是分钟数
    [dayKey(-5)]: { date: dayKey(-5), words: 2, readings: 0, minutes: 5, readingIds: [], bonus: 0 },
  },
  mistakeIds: [],
  hardIds: [],
  learnedIds: [],
  completedReadings: [],
  readingScores: { r1: 100 },
  readingRecordScores: {},
  readingAudio: {},
  unitMistakes: {},
  unitScores: {},
  settings: { defaultRate: 1, voiceName: null },
};

app.whenReady().then(async () => {
  session.defaultSession.setUserAgent(EDGE_UA);
  protocol.registerFileProtocol('app', (request, callback) => {
    let rel = request.url.replace(/^app:\/\//, '').split('#')[0].split('?')[0];
    rel = rel.replace(/^\/+/, '').replace(/^localhost\//, '').replace(/^\.\//, '');
    callback({ path: path.join(DIST, rel || 'index.html') });
  });

  const win = new BrowserWindow({ show: false, webPreferences: { contextIsolation: true, nodeIntegration: false } });
  await win.loadURL('app://localhost/index.html');
  // 写入存档后进入「我的」
  await win.webContents.executeJavaScript(
    `localStorage.setItem('k12en:progress', ${JSON.stringify(JSON.stringify(seed))}); location.hash = '#/me';`,
  );
  await win.webContents.reload();
  await new Promise((r) => setTimeout(r, 1500));
  await win.webContents.executeJavaScript(`location.hash = '#/me'`);
  await new Promise((r) => setTimeout(r, 1200));

  const text = await win.webContents.executeJavaScript(
    `(() => {
       const cards = [...document.querySelectorAll('.card')];
       const c = cards.find((el) => el.textContent.includes('学习统计'));
       return c ? c.innerText : 'NOT_FOUND |' + document.body.innerText.slice(0, 400);
     })()`,
  );
  console.log('---「学习统计」卡片内容---');
  console.log(text);
  console.log('--- 返回栏检查（首页不应出现）---');
  const homeBar = await win.webContents.executeJavaScript(
    `(async () => {
       location.hash = '#/';
       await new Promise((r) => setTimeout(r, 400));
       const has = document.body.innerText.includes('返回首页');
       location.hash = '#/me';
       await new Promise((r) => setTimeout(r, 400));
       const hasMe = document.body.innerText.includes('返回首页');
       return JSON.stringify({ 首页出现返回栏: has, 我的页出现返回栏: hasMe });
     })()`,
  );
  console.log(homeBar);

  const expected = { 累计星星: '14', 积分: '1', 连续: '2 天', 单词: '16', 听读: '1', 学习天数: '3' };
  console.log('E2E_EXPECT: ' + JSON.stringify(expected));

  clearTimeout(hardTimer);
  app.exit(0);
});
