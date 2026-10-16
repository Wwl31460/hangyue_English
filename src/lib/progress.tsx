import { createContext, useContext, useEffect, useRef, ReactNode, useState } from 'react';
import { load, save } from './storage';
import { useAuth } from './auth';
import { setPreferredVoice } from './tts';

// 学习进度与奖励（本地存储）
export interface DailyStat {
  date: string;
  words: number;
  readings: number;
  minutes: number;
  readingIds: string[]; // 今日完成的听读材料 id（仅首次听到，用于今日听读得分）
  bonus: number; // 当日额外奖励星（小测 / 单元测试）
}
export interface Settings {
  defaultRate: number; // 默认语速
  voiceName: string | null; // 默认发音人
}

// 单元测试成绩：记录每单元最好成绩与通过状态（key = "grade:unit"）
export interface UnitScore {
  score: number; // 最好成绩（满分 100）
  passed: boolean; // 是否达到及格线（>=60）
  attempts: number; // 累计测试次数
  lastTested: string; // 最近一次测试日期 YYYY-MM-DD
}

export interface ProgressData {
  daily: DailyStat; // 今日（实时）
  history: Record<string, DailyStat>; // 每日学习记录（key = YYYY-MM-DD），周/月/三月/半年统计的数据源
  mistakeIds: string[];
  hardIds: string[]; // 困难单词本：记起来很困难的单词，可反复复习
  learnedIds: string[]; // 已学单词（在学习模块中学过），测试只从这里面抽
  completedReadings: string[];
  readingScores: Record<string, number>; // 每篇听读理解测试最好成绩（百分制），与录音分合计为本章总评
  readingRecordScores: Record<string, number>; // 每篇跟读录音系统自动评分（百分制，按朗读完整度估算），与测试分合计
  readingAudio: Record<string, string>; // 跟读整篇录音（base64 data URL），按 reading id 存，本地保留
  unitMistakes: Record<string, string[]>; // 按单元错题本：key = "grade:unit"，value = 未掌握的单词 id
  unitScores: Record<string, UnitScore>; // 单元测试成绩：key = "grade:unit"
  settings: Settings;
  currentGrade?: string; // 当前学习年级（云端同步“续学”用）
  currentUnit?: number; // 当前学习单元
}

interface ProgressCtx extends ProgressData {
  today: string;
  addStars: (n: number) => void;
  addMinutes: (n: number) => void;
  markWordStudied: () => void;
  markReadingDone: (id: string) => void;
  recordReadingScore: (id: string, percent: number) => void;
  getReadingScore: (id: string) => number | undefined;
  recordReadingRecord: (id: string, percent: number) => void;
  getReadingRecordScore: (id: string) => number | undefined;
  saveReadingAudio: (id: string, dataUrl: string) => void;
  getReadingAudio: (id: string) => string | undefined;
  addMistake: (id: string) => void;
  removeMistake: (id: string) => void;
  clearMistakes: () => void;
  isMistake: (id: string) => boolean;
  // 困难单词本
  addHard: (id: string) => void;
  removeHard: (id: string) => void;
  clearHard: () => void;
  isHard: (id: string) => boolean;
  addLearned: (id: string) => void;
  isLearned: (id: string) => boolean;
  isReadingDone: (id: string) => boolean;
  // 今日得分（满 10 星）= 背单词得分 + 听读得分
  todayWordStars: () => number;
  todayArticleStars: () => number;
  todayStars: () => number;
  // —— 学习统计（供「我的」页按 周/月/三月/半年 查看）——
  dayStars: (day: DailyStat) => number; // 某天获得的星星 = 学习星(单词≤5 + 听读≤5) + 奖励星
  totalStars: () => number; // 累计星星（全部历史 + 今天）
  totalPoints: () => number; // 积分 = 累计星星 ÷ 10 向下取整，可一直累加
  streakDays: () => number; // 连续学习天数（今天没学则从昨天往前数）
  dailySeries: (days: number) => DailyStat[]; // 近 N 天记录（含今天、按日期升序、无记录补 0）
  // 单元错题本：记录一次单元测试的结果
  // - 完整测试：直接以本次未通过的词作为该单元错词集
  // - 重测：保留未在本次重测中出现的旧错词，移除本次答对的，加入本次仍错的
  recordUnitTest: (key: string, testedIds: string[], correctIds: string[], isRetest: boolean) => void;
  getUnitMistakes: (key: string) => string[];
  clearUnitMistakes: (key: string) => void;
  updateSettings: (s: Partial<Settings>) => void;
  resetAll: () => void;
  setCurrent: (grade: string, unit: number) => void; // 记录“当前学习单元”，用于登录后续学
  // 单元测试成绩：记录/读取某单元最好成绩与通过状态
  recordUnitScore: (key: string, r: { score: number; lastTested: string }) => void;
  getUnitScore: (key: string) => UnitScore | undefined;
}

const KEY = 'progress';

function todayStr(): string {
  return new Date().toISOString().slice(0, 10);
}

// 生成 YYYY-MM-DD（本地时区，避免 toISOString 的时差问题）
function dayKey(d: Date): string {
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

function emptyDay(date: string): DailyStat {
  return { date, words: 0, readings: 0, minutes: 0, readingIds: [], bonus: 0 };
}

function fresh(): ProgressData {
  const t = todayStr();
  return {
    daily: emptyDay(t),
    history: {},
    mistakeIds: [],
    hardIds: [],
    learnedIds: [],
    completedReadings: [],
    readingScores: {},
    readingRecordScores: {},
    readingAudio: {},
    unitMistakes: {},
    unitScores: {},
    settings: { defaultRate: 1, voiceName: null },
    currentGrade: undefined,
    currentUnit: undefined,
  };
}

// 兼容旧数据：history 以前只存「当日分钟数」，这里统一升级为完整日记录
function migrateHistory(raw: unknown): Record<string, DailyStat> {
  const out: Record<string, DailyStat> = {};
  if (!raw || typeof raw !== 'object') return out;
  for (const [k, v] of Object.entries(raw as Record<string, unknown>)) {
    if (typeof v === 'number') {
      // 老格式：数值 = 分钟
      out[k] = { ...emptyDay(k), minutes: v };
    } else if (v && typeof v === 'object') {
      const o = v as Partial<DailyStat>;
      out[k] = {
        date: k,
        words: o.words ?? 0,
        readings: o.readings ?? 0,
        minutes: o.minutes ?? 0,
        readingIds: Array.isArray(o.readingIds) ? o.readingIds : [],
        bonus: o.bonus ?? 0,
      };
    }
  }
  return out;
}

// 补全可能缺失的字段（旧版本存档 / 云端数据）
function normalize(d: ProgressData): ProgressData {
  if (!Array.isArray(d.learnedIds)) d.learnedIds = [];
  if (!Array.isArray(d.hardIds)) d.hardIds = [];
  // 注意：readingScores 是对象（Record），不能用 Array.isArray 判断，
  // 否则每次启动都会被误判为“缺失”而清空，历史听读成绩全丢。
  if (!d.readingScores || typeof d.readingScores !== 'object') d.readingScores = {};
  if (!d.readingRecordScores || typeof d.readingRecordScores !== 'object') d.readingRecordScores = {};
  if (!d.readingAudio || typeof d.readingAudio !== 'object') d.readingAudio = {};
  if (!d.unitMistakes || typeof d.unitMistakes !== 'object') d.unitMistakes = {};
  if (!d.unitScores || typeof d.unitScores !== 'object') d.unitScores = {};
  d.history = migrateHistory(d.history);
  const t = todayStr();
  if (!d.daily || d.daily.date !== t) d.daily = emptyDay(t);
  else d.daily = { ...emptyDay(t), ...d.daily, date: t, readingIds: d.daily.readingIds ?? [], bonus: d.daily.bonus ?? 0 };
  return d;
}

// 跨天保护：App 一直开着时，今天的计数不会串到昨天
function rollover(d: ProgressData): ProgressData {
  const t = todayStr();
  return d.daily?.date === t ? d : { ...d, daily: emptyDay(t) };
}

// 今日数据每次改动都同步进 history（历史即统计数据源）
function syncDay(d: ProgressData, daily: DailyStat): ProgressData {
  return { ...d, daily, history: { ...d.history, [daily.date]: daily } };
}

// 某天获得的星星：学习星（单词 ≤5 + 听读 ≤5）+ 当日奖励星
function starsFor(day: DailyStat, quizScores: Record<string, number>, recScores: Record<string, number>): number {
  const w = (Math.min(day.words, 10) / 10) * 5;
  let best = 0;
  for (const id of day.readingIds ?? []) {
    const parts = [recScores[id], quizScores[id]].filter((x): x is number => x != null);
    if (parts.length) best = Math.max(best, parts.reduce((a, b) => a + b, 0) / parts.length);
  }
  const a = Math.min(1, best / 100) * 5;
  return Math.round((w + a + (day.bonus ?? 0)) * 10) / 10;
}

const Ctx = createContext<ProgressCtx | null>(null);

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<ProgressData>(() => {
    const loaded = load<ProgressData>(KEY, fresh());
    // 统一补全字段、迁移历史格式、必要时重置今日
    return normalize(loaded);
  });

  // —— 云端账号进度同步 ——
  const { ready, user, loadRemote, saveRemote } = useAuth();
  const loadedRef = useRef(false); // 本次登录是否已从云端拉取过（避免重复拉取）
  const skipSaveRef = useRef(false); // 刚拉完云端数据，先别立刻回写

  useEffect(() => {
    save(KEY, data);
  }, [data]);

  // 把「设置」里的发音人同步给朗读引擎：所有 speak() 调用自动使用，无需逐处传参。
  // 注意要在渲染期同步——子组件的 effect（预热读音）先于父组件 effect 执行，
  // 若放在 useEffect 里，子组件预热会用错音色，导致缓存对不上、点了还是要等。
  setPreferredVoice(data.settings.voiceName);

  // 登录成功后：用云端进度覆盖本地（实现换设备续学）；登出则标记下次重新拉取
  useEffect(() => {
    if (!ready) return;
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadRemote()
        .then((remote) => {
          if (!remote) return;
          const merged = normalize({ ...fresh(), ...remote });
          skipSaveRef.current = true; // 刚拉下来的数据无需立即回写
          setData(merged);
        })
        .catch(() => {
          /* 云端拉取失败不影响本地使用 */
        });
    }
    if (!user) loadedRef.current = false;
  }, [ready, user, loadRemote]);

  // 学习中改动进度：登录态下防抖保存到云端（未登录不写库）
  useEffect(() => {
    if (!ready || !user || !loadedRef.current) return;
    if (skipSaveRef.current) {
      skipSaveRef.current = false; // 跳过刚拉取后的那次多余写入
      return;
    }
    const t = setTimeout(() => {
      saveRemote(data).catch(() => {});
    }, 800);
    return () => clearTimeout(t);
  }, [data, ready, user, saveRemote]);

  const api: ProgressCtx = {
    ...data,
    today: todayStr(),
    // 奖励星（小测 / 单元测试）计入当日，统计页按天汇总
    addStars: (n) =>
      setData((d0) => {
        const d = rollover(d0);
        return syncDay(d, { ...d.daily, bonus: (d.daily.bonus ?? 0) + n });
      }),
    addMinutes: (n) =>
      setData((d0) => {
        const d = rollover(d0);
        return syncDay(d, { ...d.daily, minutes: d.daily.minutes + n });
      }),
    markWordStudied: () =>
      setData((d0) => {
        const d = rollover(d0);
        return syncDay(d, { ...d.daily, words: d.daily.words + 1 });
      }),
    markReadingDone: (id) =>
      setData((d0) => {
        const d = rollover(d0);
        if (d.completedReadings.includes(id)) return d;
        return syncDay({ ...d, completedReadings: [...d.completedReadings, id] }, {
          ...d.daily,
          readings: d.daily.readings + 1,
          readingIds: [...d.daily.readingIds, id],
        });
      }),
    addMistake: (id) =>
      setData((d) => (d.mistakeIds.includes(id) ? d : { ...d, mistakeIds: [...d.mistakeIds, id] })),
    removeMistake: (id) => setData((d) => ({ ...d, mistakeIds: d.mistakeIds.filter((x) => x !== id) })),
    clearMistakes: () => setData((d) => ({ ...d, mistakeIds: [] })),
    isMistake: (id) => data.mistakeIds.includes(id),
    addHard: (id) =>
      setData((d) => (d.hardIds.includes(id) ? d : { ...d, hardIds: [...d.hardIds, id] })),
    removeHard: (id) => setData((d) => ({ ...d, hardIds: d.hardIds.filter((x) => x !== id) })),
    clearHard: () => setData((d) => ({ ...d, hardIds: [] })),
    isHard: (id) => data.hardIds.includes(id),
    addLearned: (id) =>
      setData((d0) => {
        const d = rollover(d0);
        if (d.learnedIds.includes(id)) return d;
        return syncDay({ ...d, learnedIds: [...d.learnedIds, id] }, { ...d.daily, words: d.daily.words + 1 });
      }),
    isLearned: (id) => data.learnedIds.includes(id),
    isReadingDone: (id) => data.completedReadings.includes(id),
    recordReadingScore: (id, percent) =>
      setData((d0) => {
        const d = rollover(d0);
        const best = Math.max(d.readingScores[id] ?? 0, percent);
        const done = d.completedReadings.includes(id);
        const next = { ...d, readingScores: { ...d.readingScores, [id]: best } };
        if (done) return { ...next, daily: d.daily };
        return syncDay({ ...next, completedReadings: [...d.completedReadings, id] }, {
          ...d.daily,
          readings: d.daily.readings + 1,
          readingIds: [...d.daily.readingIds, id],
        });
      }),
    getReadingScore: (id) => {
      // 本章总评 = 录音分(系统自动) 与 理解测试分 的合计（各占一半，百分制）
      const rec = data.readingRecordScores[id];
      const quiz = data.readingScores[id];
      const parts = [rec, quiz].filter((x): x is number => x != null);
      return parts.length ? Math.round(parts.reduce((a, b) => a + b, 0) / parts.length) : undefined;
    },
    recordReadingRecord: (id, percent) =>
      setData((d) => ({
        ...d,
        readingRecordScores: { ...d.readingRecordScores, [id]: Math.max(d.readingRecordScores[id] ?? 0, percent) },
      })),
    getReadingRecordScore: (id) => data.readingRecordScores[id],
    saveReadingAudio: (id, dataUrl) =>
      setData((d) => {
        try {
          return { ...d, readingAudio: { ...d.readingAudio, [id]: dataUrl } };
        } catch {
          return d; // 超出本地存储配额时静默放弃，不阻断主流程
        }
      }),
    getReadingAudio: (id) => data.readingAudio[id],
    // 今日得分（满 10 星）＝ 背单词 5 星 + 听读 5 星（比例均衡）
    todayWordStars: () => (Math.min(data.daily.words, 10) / 10) * 5,
    todayArticleStars: () => {
      let best = 0;
      for (const id of data.daily.readingIds) {
        // 本章总评 = 录音分 + 测试分（只取已有的求平均），与列表展示一致
        const parts = [data.readingRecordScores[id], data.readingScores[id]].filter(
          (x): x is number => x != null,
        );
        if (parts.length) best = Math.max(best, parts.reduce((a, b) => a + b, 0) / parts.length);
      }
      return Math.min(1, best / 100) * 5;
    },
    todayStars: () => {
      const w = (Math.min(data.daily.words, 10) / 10) * 5;
      let best = 0;
      for (const id of data.daily.readingIds) {
        const parts = [data.readingRecordScores[id], data.readingScores[id]].filter(
          (x): x is number => x != null,
        );
        if (parts.length) best = Math.max(best, parts.reduce((a, b) => a + b, 0) / parts.length);
      }
      const a = Math.min(1, best / 100) * 5;
      return Math.min(10, Math.round((w + a) * 10) / 10);
    },

    // —— 学习统计 ——
    dayStars: (day) => starsFor(day, data.readingScores, data.readingRecordScores),
    totalStars: () =>
      Object.values(data.history).reduce(
        (sum, day) => sum + starsFor(day, data.readingScores, data.readingRecordScores),
        0,
      ),
    // 10 星 = 1 积分，可一直往上累计
    totalPoints: () =>
      Math.floor(
        Object.values(data.history).reduce(
          (sum, day) => sum + starsFor(day, data.readingScores, data.readingRecordScores),
          0,
        ) / 10,
      ),
    // 连续学习天数：有单词或听读记录的才算“学了”；今天还没学则从昨天起算，不打断连击
    streakDays: () => {
      const active = new Set(
        Object.values(data.history)
          .filter((day) => day.words > 0 || day.readings > 0)
          .map((day) => day.date),
      );
      const cur = new Date();
      if (!active.has(dayKey(cur))) cur.setDate(cur.getDate() - 1);
      let n = 0;
      while (active.has(dayKey(cur))) {
        n++;
        cur.setDate(cur.getDate() - 1);
      }
      return n;
    },
    // 近 N 天每日记录：按日期升序，没有记录的那天补 0
    dailySeries: (days) => {
      const out: DailyStat[] = [];
      const cur = new Date();
      cur.setDate(cur.getDate() - (days - 1));
      for (let i = 0; i < days; i++) {
        const k = dayKey(cur);
        out.push(k === data.daily.date ? data.daily : (data.history[k] ?? emptyDay(k)));
        cur.setDate(cur.getDate() + 1);
      }
      return out;
    },
    recordUnitTest: (key, testedIds, correctIds, isRetest) =>
      setData((d) => {
        const wrongNow = testedIds.filter((id) => !correctIds.includes(id));
        let next: string[];
        if (isRetest) {
          const prev = d.unitMistakes[key] || [];
          // 保留未在本次重测里出现的旧错词；本次测过的，答对则移除、答错则保留
          next = prev.filter((id) => !testedIds.includes(id)).concat(wrongNow);
        } else {
          next = wrongNow;
        }
        return { ...d, unitMistakes: { ...d.unitMistakes, [key]: next } };
      }),
    getUnitMistakes: (key) => data.unitMistakes[key] || [],
    clearUnitMistakes: (key) =>
      setData((d) => {
        const m = { ...d.unitMistakes };
        delete m[key];
        return { ...d, unitMistakes: m };
      }),
    updateSettings: (s) => setData((d) => ({ ...d, settings: { ...d.settings, ...s } })),
    resetAll: () => setData(fresh()),
    // 记录单元测试成绩：保留最好成绩，达到及格线即标记通过；累计测试次数
    recordUnitScore: (key, r) =>
      setData((d) => {
        const prev = d.unitScores?.[key];
        return {
          ...d,
          unitScores: {
            ...d.unitScores,
            [key]: {
              score: Math.max(prev?.score ?? 0, r.score),
              passed: (prev?.passed || false) || r.score >= 60,
              attempts: (prev?.attempts || 0) + 1,
              lastTested: r.lastTested,
            },
          },
        };
      }),
    getUnitScore: (key) => data.unitScores?.[key],
    setCurrent: (grade, unit) =>
      setData((d) =>
        d.currentGrade === grade && d.currentUnit === unit ? d : { ...d, currentGrade: grade, currentUnit: unit },
      ),
  };

  return <Ctx.Provider value={api}>{children}</Ctx.Provider>;
}

export function useProgress(): ProgressCtx {
  const c = useContext(Ctx);
  if (!c) throw new Error('useProgress 必须在 ProgressProvider 内使用');
  return c;
}
