import { useMemo, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { words } from '../data/words';
import { grades, gradeById, unitTitles, GradeStage } from '../data/grades';
import { Word } from '../types';
import { useProgress } from '../lib/progress';
import { speak } from '../lib/tts';
import { recognizeOnce, speechRecognitionSupported, speakPassed, normWord, editDistance } from '../lib/speech';

// 题型
export type QType = 'choice' | 'spelling' | 'fill' | 'speak';
const TYPE_META: Record<QType, { label: string; icon: string; desc: string }> = {
  choice: { label: '四选一', icon: '🔘', desc: '看中文，选出正确单词' },
  spelling: { label: '拼写', icon: '✍️', desc: '看中文，写出完整单词' },
  fill: { label: '填空', icon: '🧩', desc: '补全缺字母的单词' },
  speak: { label: '发音', icon: '🎤', desc: '朗读单词，判断是否读对' },
};

interface Q {
  word: Word;
  type: QType;
  options?: string[]; // choice
  answerIdx?: number; // choice
  mask?: string; // fill：缺字母的占位，如 h_lp
  missing?: string; // fill：被遮住的字母（按顺序）
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// 为某词生成四选一选项（优先同单元 → 同年级 → 全部词表）
function buildChoices(w: Word, unitWords: Word[], gid: string): string[] {
  const sameUnit = unitWords.filter(
    (x) => x.id !== w.id && x.word.toLowerCase() !== w.word.toLowerCase(),
  );
  const sameGrade = words.filter(
    (x) =>
      x.grade === gid &&
      x.id !== w.id &&
      x.word.toLowerCase() !== w.word.toLowerCase() &&
      !sameUnit.some((s) => s.id === x.id),
  );
  const rest = words.filter(
    (x) =>
      x.id !== w.id &&
      x.word.toLowerCase() !== w.word.toLowerCase() &&
      !sameUnit.some((s) => s.id === x.id) &&
      !sameGrade.some((s) => s.id === x.id),
  );
  const pool = [...sameUnit, ...sameGrade, ...rest];
  const distract = shuffle(pool).slice(0, 3).map((x) => x.word);
  return shuffle([w.word, ...distract]);
}

// 生成填空遮罩：遮住 1~2 个字母（不遮首字母），返回占位串与被遮字母
function buildMask(word: string): { mask: string; missing: string } {
  const len = word.length;
  const blanks = len <= 3 ? 1 : 2;
  const candidates: number[] = [];
  for (let i = 1; i < len; i++) candidates.push(i); // 不遮首字母
  const positions = shuffle(candidates).slice(0, blanks).sort((a, b) => a - b);
  let mask = '';
  for (let i = 0; i < len; i++) mask += positions.includes(i) ? '_' : word[i];
  const missing = positions.map((p) => word[p]).join('');
  return { mask, missing };
}

// 依据所选题型，为单元单词逐个分配一道题（轮转，保证各题型都出现）
function buildQuestions(list: Word[], types: QType[], gid: string): Q[] {
  return list.map((w, i) => {
    const type = types[i % types.length];
    const q: Q = { word: w, type };
    if (type === 'choice') {
      const opts = buildChoices(w, list, gid);
      q.options = opts;
      q.answerIdx = opts.indexOf(w.word);
    } else if (type === 'fill') {
      const { mask, missing } = buildMask(w.word);
      q.mask = mask;
      q.missing = missing;
    }
    return q;
  });
}

// ============ 主组件 ============
export default function Test() {
  const { gid, uid } = useParams();
  const nav = useNavigate();
  const p = useProgress();
  const stage = gid ? gradeById[gid] : undefined;

  // 1) 未选年级：年级选择
  if (!gid || !stage) {
    return <GradePick nav={nav} p={p} />;
  }

  // 2) 已选年级、未选单元：单元选择
  if (!uid) {
    return <UnitPick gid={gid} nav={nav} p={p} />;
  }

  // 3) 已选单元：配置 + 答题 + 评分
  return <UnitTest gid={gid} uid={Number(uid)} nav={nav} p={p} />;
}

// ---- 年级选择 ----
function GradePick({ nav, p }: { nav: (s: string) => void; p: ReturnType<typeof useProgress> }) {
  const SECTION_ORDER: GradeStage['section'][] = ['小学', '初中', '高中'];
  const countOf = (id: string) => words.filter((w) => w.grade === id).length;
  // 某年级的单元总数 / 已测试单元数（用于年级卡片展示进度，无需点进单元即可看到）
  const unitsOf = (id: string) => new Set(words.filter((w) => w.grade === id).map((w) => w.unit ?? 0)).size;
  const testedOf = (id: string) =>
    Object.keys(p.unitScores).filter((k) => k.startsWith(`${id}:`)).length;
  return (
    <div className="page pb-6 pt-4">
      <h1 className="text-xl font-extrabold text-brand-900">章节测试</h1>
      <p className="mt-1 text-xs text-slate-400">选择年级，按单元测试并评分。每个单词权重相同，满分 100 分。</p>
      <div className="mt-4 space-y-5">
        {SECTION_ORDER.map((sec) => (
          <div key={sec}>
            <div className="section-title">{sec}</div>
            <div className="mt-2 grid grid-cols-2 gap-3">
              {grades
                .filter((g) => g.section === sec)
                .map((g) => {
                  const tested = testedOf(g.id);
                  const total = unitsOf(g.id);
                  return (
                    <button
                      key={g.id}
                      onClick={() => nav(`/vocab/test/grade/${g.id}`)}
                      className="group flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-3 text-left transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-soft active:scale-[0.98]"
                    >
                      <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-brand-50 text-3xl">
                        {g.emoji}
                      </span>
                      <div className="min-w-0">
                        <div className="truncate text-sm font-bold text-brand-900">{g.label}</div>
                        <div className="text-xs text-slate-500">{countOf(g.id)} 个词</div>
                        <div className="mt-0.5 text-[11px] text-brand-500">已测 {tested}/{total} 单元</div>
                      </div>
                      <span className="ml-auto text-slate-300 transition group-hover:translate-x-0.5">›</span>
                    </button>
                  );
                })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---- 单元选择 ----
function UnitPick({ gid, nav, p }: { gid: string; nav: (s: string) => void; p: ReturnType<typeof useProgress> }) {
  const stage = gradeById[gid];
  const gradeWords = words.filter((w) => w.grade === gid);
  const units = [...new Set(gradeWords.map((w) => w.unit ?? 0))].sort((a, b) => a - b);
  const titleOf = (u: number) => unitTitles[gid]?.[u];
  // 本册完成情况汇总：无需点进单元即可看到已测/已掌握进度
  const total = units.length;
  const tested = units.filter((u) => p.getUnitScore(`${gid}:${u}`)).length;
  const mastered = units.filter((u) => p.getUnitScore(`${gid}:${u}`)?.passed).length;
  return (
    <div className="page pb-6 pt-4">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-50 text-3xl">{stage.emoji}</span>
        <div>
          <h1 className="text-xl font-extrabold text-brand-900">{stage.label} · 测试</h1>
          <p className="text-xs text-slate-500">选择单元开始测试</p>
        </div>
      </div>

      {/* 完成情况汇总：已测 / 已掌握 */}
      <div className="mt-4 grid grid-cols-3 gap-2">
        <div className="rounded-2xl bg-slate-50 p-3 text-center">
          <div className="text-xl font-extrabold text-brand-700">{tested}/{total}</div>
          <div className="text-[11px] text-slate-500">已测试</div>
        </div>
        <div className="rounded-2xl bg-emerald-50 p-3 text-center">
          <div className="text-xl font-extrabold text-emerald-600">{mastered}/{total}</div>
          <div className="text-[11px] text-slate-500">已掌握（≥60）</div>
        </div>
        <div className="rounded-2xl bg-amber-50 p-3 text-center">
          <div className="text-xl font-extrabold text-amber-600">{total - tested}</div>
          <div className="text-[11px] text-slate-500">未测试</div>
        </div>
      </div>

      <div className="mt-4 space-y-2.5">
        {units.map((u) => {
          const n = gradeWords.filter((w) => w.unit === u).length;
          const m = p.getUnitMistakes(`${gid}:${u}`).length;
          const sc = p.getUnitScore(`${gid}:${u}`);
          return (
            <button
              key={u}
              onClick={() => nav(`/vocab/test/grade/${gid}/unit/${u}`)}
              className="group flex w-full items-center gap-3 rounded-2xl border border-slate-200 bg-white p-3.5 text-left transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-soft active:scale-[0.98]"
            >
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-brand-50 text-lg font-extrabold text-brand-700">
                {u}
              </span>
              <div className="min-w-0">
                <div className="text-sm font-bold text-brand-900">Unit {u}</div>
                <div className="truncate text-xs text-slate-500">{titleOf(u) ?? `第 ${u} 单元`} · {n} 个词</div>
              </div>
              {/* 测试状态徽标：未测试 / 已掌握（得分）/ 未完成（得分） */}
              {sc ? (
                sc.passed ? (
                  <span className="ml-auto mr-1 rounded-full bg-emerald-100 px-2 py-0.5 text-[10px] font-semibold text-emerald-600">
                    ✓ {sc.score}分
                  </span>
                ) : (
                  <span className="ml-auto mr-1 rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold text-amber-600">
                    ✗ {sc.score}分
                  </span>
                )
              ) : (
                <span className="ml-auto mr-1 rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-400">
                  未测试
                </span>
              )}
              {m > 0 && (
                <span className="rounded-full bg-rose-100 px-2 py-0.5 text-[10px] font-semibold text-rose-600">
                  {m} 错词
                </span>
              )}
              <span className="text-slate-300 transition group-hover:translate-x-0.5">›</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ---- 配置 + 答题 + 评分 ----
function UnitTest({ gid, uid, nav, p }: { gid: string; uid: number; nav: (s: string) => void; p: ReturnType<typeof useProgress> }) {
  const stage = gradeById[gid];
  const key = `${gid}:${uid}`;
  const unitWords = useMemo(() => words.filter((w) => w.grade === gid && w.unit === uid), [gid, uid]);

  const [step, setStep] = useState<'config' | 'run' | 'result'>('config');
  const [types, setTypes] = useState<QType[]>(['choice', 'spelling', 'fill', 'speak']);
  const [qs, setQs] = useState<Q[]>([]);
  const [idx, setIdx] = useState(0);
  const [results, setResults] = useState<(boolean | null)[]>([]);
  const [isRetest, setIsRetest] = useState(false);

  const total = qs.length || unitWords.length; // 本次测试词数（重测时=错词数）
  const weight = total > 0 ? 100 / total : 0; // 每词分值

  if (unitWords.length === 0) {
    return (
      <div className="page pb-6 pt-10 text-center">
        <div className="text-5xl">📭</div>
        <h1 className="mt-3 text-xl font-extrabold text-brand-900">本单元暂无单词</h1>
        <p className="mt-2 text-sm text-slate-500">{stage.label} · Unit {uid} 还没有录入单词，先去其他单元试试～</p>
        <button onClick={() => nav(`/vocab/test/grade/${gid}`)} className="btn-primary mt-5 w-full">返回选单元</button>
      </div>
    );
  }

  // 开始一次测试（target 为本次要测的词列表，retest 标记是否为重测）
  const beginTest = (target: Word[], retest: boolean) => {
    if (target.length === 0 || types.length === 0) return;
    setIsRetest(retest);
    setQs(buildQuestions(target, types, gid));
    setResults(new Array(target.length).fill(null));
    setIdx(0);
    setStep('run');
  };

  // 完整单元测试
  const startFull = () => beginTest(unitWords, false);

  // 重测本单元错词
  const startRetest = () => {
    const m = p
      .getUnitMistakes(key)
      .map((id) => words.find((w) => w.id === id))
      .filter(Boolean) as Word[];
    beginTest(m, true);
  };

  const onAnswered = (correct: boolean) => {
    setResults((prev) => {
      const next = prev.slice();
      next[idx] = correct;
      return next;
    });
  };

  const next = () => {
    if (idx + 1 >= qs.length) finish();
    else setIdx(idx + 1);
  };

  const finish = () => {
    const testedIds = qs.map((q) => q.word.id);
    const correctIds = qs.map((q, i) => (results[i] ? q.word.id : '')).filter(Boolean);
    // 按单元记录错题：完整测试直接以未通过的词作为本单元错词集；重测则移除本次答对的、保留未测到的旧错词
    p.recordUnitTest(key, testedIds, correctIds, isRetest);
    // 同时写入全局错词本（供“错词本”页统一复习）
    qs.forEach((q, i) => {
      if (!results[i]) p.addMistake(q.word.id);
    });
    const correctCount = results.filter(Boolean).length;
    const score = Math.round(correctCount * weight);
    // 记录本单元成绩（保留最好分、标记是否通过），用于单元列表统一展示状态与得分
    p.recordUnitScore(key, { score, lastTested: new Date().toISOString().slice(0, 10) });
    p.addStars(Math.round(score / 10));
    setStep('result');
  };

  // 评分结果
  if (step === 'result') {
    const correctCount = results.filter(Boolean).length;
    const score = Math.round(correctCount * weight);
    const pct = score;
    const grade = score >= 90 ? 'A' : score >= 80 ? 'B' : score >= 70 ? 'C' : score >= 60 ? 'D' : '不及格';
    const gradeColor = score >= 80 ? 'text-emerald-600' : score >= 60 ? 'text-amber-600' : 'text-rose-500';
    const remaining = p.getUnitMistakes(key).length; // 本次记录后该单元剩余错词
    return (
      <div className="page pb-6 pt-8">
        <div className="card animate-fadeup text-center">
          <div className="text-5xl">{remaining === 0 ? '🏆' : '🎉'}</div>
          <h1 className="mt-3 text-2xl font-extrabold text-brand-900">{isRetest && remaining === 0 ? '错词全部掌握！' : '测试完成'}</h1>
          <p className="mt-1 text-xs text-slate-500">
            {stage.label} · Unit {uid} · {isRetest ? '重测' : `共 ${total} 词`}
          </p>

          <div className={`mt-4 text-6xl font-extrabold ${gradeColor}`}>{score}</div>
          <div className="text-sm text-slate-500">满分 100 分 · 得分率 {pct}%</div>
          <div className="mt-3 inline-block rounded-full bg-slate-100 px-4 py-1 text-sm font-bold text-slate-700">
            等级 {grade}
          </div>

          <p className="mt-2 text-xs text-slate-400">
            本次成绩已记录到单元列表（历史最佳 {p.getUnitScore(key)?.score ?? score} 分）
          </p>

          <div className="mt-4 h-3 w-full overflow-hidden rounded-full bg-slate-100">
            <div className={`h-full rounded-full transition-all ${score >= 60 ? 'bg-gradient-to-r from-emerald-400 to-emerald-600' : 'bg-gradient-to-r from-rose-400 to-rose-600'}`} style={{ width: `${pct}%` }} />
          </div>

          <div className="mt-4 grid grid-cols-3 gap-2">
            <Stat label="答对" value={correctCount} color="text-emerald-600" />
            <Stat label="答错" value={total - correctCount} color="text-rose-500" />
            <Stat label="得星" value={Math.round(score / 10)} color="text-amber-500" />
          </div>

          {isRetest && remaining === 0 ? (
            <p className="mt-3 rounded-2xl bg-emerald-50 px-3 py-2 text-sm font-medium text-emerald-700">
              🎊 本单元错词已全部测对，已从错题本移除！
            </p>
          ) : isRetest ? (
            <p className="mt-3 text-xs text-slate-400">本单元还剩 {remaining} 个错词，学完后可再次重测。</p>
          ) : (
            <p className="mt-3 text-xs text-slate-400">每词 {weight.toFixed(1)} 分（100÷{total}），未通过的词已存入本单元错题本，可重测。</p>
          )}

          <div className="mt-5 grid grid-cols-2 gap-3">
            <button onClick={startFull} className="btn-primary w-full">🔄 再来一次</button>
            {remaining > 0 && (
              <button onClick={startRetest} className="rounded-2xl border border-rose-300 bg-rose-50 py-3 text-sm font-semibold text-rose-600">
                🔁 重测错词（{remaining}）
              </button>
            )}
            <button onClick={() => nav(`/vocab/test/grade/${gid}`)} className="btn-accent w-full">
              选其他单元
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 答题
  if (step === 'run') {
    const q = qs[idx];
    const answered = results[idx] !== null;
    const correctCount = results.filter(Boolean).length;
    return (
      <div className="page pb-6 pt-4">
        <div className="flex items-center justify-between text-sm">
          <span className="font-semibold text-brand-800">第 {idx + 1} / {total} 题</span>
          <span className="text-slate-400">已对 {correctCount} · 每词 {weight.toFixed(1)} 分</span>
        </div>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-100">
          <div className="h-full rounded-full bg-gradient-to-r from-brand-600 to-brand-800 transition-all" style={{ width: `${((idx + 1) / total) * 100}%` }} />
        </div>

        <QuestionCard key={idx} q={q} answered={answered} onAnswered={onAnswered} />

        {answered && (
          <button onClick={next} className="btn-primary mt-4 w-full">
            {idx + 1 >= total ? '查看成绩 🏁' : '下一题 →'}
          </button>
        )}
      </div>
    );
  }

  // 配置题型
  const mistakeWords = p.getUnitMistakes(key).map((id) => words.find((w) => w.id === id)).filter(Boolean) as Word[];
  return (
    <div className="page pb-6 pt-4">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-brand-50 text-3xl">{stage.emoji}</span>
        <div>
          <h1 className="text-xl font-extrabold text-brand-900">{stage.label} · Unit {uid}</h1>
          <p className="text-xs text-slate-500">{unitWords.length} 个词 · 每个词 {weight.toFixed(1)} 分，满分 100</p>
        </div>
      </div>

      {mistakeWords.length > 0 && (
        <div className="card mt-4 border-rose-200 bg-rose-50">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-bold text-rose-700">🔁 本单元有 {mistakeWords.length} 个错词</div>
              <div className="text-xs text-rose-500">学完后可以只重测这些错词</div>
            </div>
            <button onClick={startRetest} className="rounded-2xl bg-rose-500 px-4 py-2 text-sm font-semibold text-white active:scale-[0.98]">
              重测错词
            </button>
          </div>
        </div>
      )}

      <div className="card mt-4">
        <div className="section-title">选择测试题型</div>
        <p className="mt-1 text-xs text-slate-400">可多选，每词随机分配一种题型（轮转保证都考到）。</p>
        <div className="mt-3 space-y-2">
          {(Object.keys(TYPE_META) as QType[]).map((t) => {
            const on = types.includes(t);
            return (
              <button
                key={t}
                onClick={() => setTypes((prev) => (prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]))}
                className={`flex w-full items-center gap-3 rounded-2xl border px-3.5 py-3 text-left transition active:scale-[0.99] ${
                  on ? 'border-brand-400 bg-brand-50' : 'border-slate-200 bg-white'
                }`}
              >
                <span className="text-2xl">{TYPE_META[t].icon}</span>
                <div className="min-w-0">
                  <div className="text-sm font-bold text-brand-900">{TYPE_META[t].label}</div>
                  <div className="text-xs text-slate-500">{TYPE_META[t].desc}</div>
                </div>
                <span className={`ml-auto grid h-6 w-6 place-items-center rounded-full text-sm ${on ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-300'}`}>
                  {on ? '✓' : ''}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="card mt-3 text-xs text-slate-500">
        📊 评分规则：共 {unitWords.length} 个单词，每个单词权重相同（{weight.toFixed(1)} 分），总分 100 分。每词答对得分，答错不得分；未通过的词存入本单元错题本，全部测对后自动移除。
      </div>

      <button onClick={startFull} disabled={types.length === 0} className="btn-primary mt-4 w-full disabled:opacity-40">
        🚀 开始测试（{types.length} 种题型）
      </button>
    </div>
  );
}

// ---- 单题卡片 ----
function QuestionCard({ q, answered, onAnswered }: { q: Q; answered: boolean; onAnswered: (c: boolean) => void }) {
  const meta = TYPE_META[q.type];
  const head = (
    <div className="mb-3 flex items-center gap-2">
      <span className="rounded-full bg-brand-100 px-2.5 py-0.5 text-xs font-bold text-brand-700">{meta.icon} {meta.label}</span>
    </div>
  );

  return (
    <div className="card mt-4 animate-fadeup">
      {head}
      {q.type === 'choice' && <ChoiceQ q={q} answered={answered} onAnswered={onAnswered} />}
      {q.type === 'spelling' && <SpellingQ q={q} answered={answered} onAnswered={onAnswered} />}
      {q.type === 'fill' && <FillQ q={q} answered={answered} onAnswered={onAnswered} />}
      {q.type === 'speak' && <SpeakQ q={q} answered={answered} onAnswered={onAnswered} />}
    </div>
  );
}

// 四选一：看中文，选英文单词
function ChoiceQ({ q, answered, onAnswered }: { q: Q; answered: boolean; onAnswered: (c: boolean) => void }) {
  const [picked, setPicked] = useState<number | null>(null);
  const pick = (i: number) => {
    if (answered) return;
    setPicked(i);
    onAnswered(i === q.answerIdx);
  };
  return (
    <>
      <div className="text-sm text-slate-500">选出正确的英文单词：</div>
      <div className="mt-1 text-2xl font-extrabold text-brand-900">{q.word.meaning}</div>
      {q.word.phonetic && <div className="mt-0.5 text-xs text-slate-400">{q.word.phonetic}</div>}
      <div className="mt-3 space-y-2">
        {q.options!.map((opt, i) => {
          let cls = 'border-slate-200 bg-white hover:border-brand-300';
          if (answered) {
            if (i === q.answerIdx) cls = 'border-emerald-400 bg-emerald-50 text-emerald-700';
            else if (i === picked) cls = 'border-rose-400 bg-rose-50 text-rose-700';
            else cls = 'border-slate-200 bg-white opacity-60';
          }
          return (
            <button
              key={i}
              disabled={answered}
              onClick={() => pick(i)}
              className={`w-full rounded-2xl border px-4 py-3 text-left text-lg font-semibold transition active:scale-[0.99] ${cls}`}
            >
              <span className="mr-2 text-slate-400">{String.fromCharCode(65 + i)}.</span>
              {opt}
            </button>
          );
        })}
      </div>
      {answered && (
        <div className={`mt-3 rounded-2xl px-4 py-2 text-sm font-medium ${picked === q.answerIdx ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
          {picked === q.answerIdx ? '✅ 回答正确！' : `❌ 正确答案：${q.word.word}`}
        </div>
      )}
    </>
  );
}

// 拼写：看中文（含首字母提示），写出完整单词
function SpellingQ({ q, answered, onAnswered }: { q: Q; answered: boolean; onAnswered: (c: boolean) => void }) {
  const [val, setVal] = useState('');
  const hint = q.word.word[0] + ' '.repeat(q.word.word.length - 1).replace(/ /g, ' _');
  const submit = () => {
    if (answered) return;
    const target = normWord(q.word.word);
    const got = normWord(val);
    // 容错：完全相等，或编辑距离 ≤ 1（允许一个字母误差）
    const ok = got === target || editDistance(got, target) <= 1;
    onAnswered(ok);
  };
  return (
    <>
      <div className="text-sm text-slate-500">根据中文写出单词：</div>
      <div className="mt-1 text-2xl font-extrabold text-brand-900">{q.word.meaning}</div>
      <div className="mt-1 text-xs text-slate-400">提示（首字母）：<span className="font-mono tracking-widest">{hint}</span></div>
      <input
        autoFocus
        value={val}
        disabled={answered}
        onChange={(e) => setVal(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && submit()}
        placeholder="输入英文拼写"
        className="mt-3 w-full rounded-2xl border-2 border-slate-200 px-4 py-3 text-lg font-semibold outline-none focus:border-brand-400"
      />
      {!answered && (
        <button onClick={submit} className="btn-primary mt-3 w-full">提交</button>
      )}
      {answered && (
        <div className={`mt-3 rounded-2xl px-4 py-2 text-sm font-medium ${normWord(val) === normWord(q.word.word) || editDistance(normWord(val), normWord(q.word.word)) <= 1 ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
          {normWord(val) === normWord(q.word.word) || editDistance(normWord(val), normWord(q.word.word)) <= 1
            ? `✅ 正确！${q.word.word}`
            : `❌ 正确答案：${q.word.word}`}
        </div>
      )}
    </>
  );
}

// 填空：看中文 + 缺字母的单词，缺哪格就在哪格填（原位输入）
function FillQ({ q, answered, onAnswered }: { q: Q; answered: boolean; onAnswered: (c: boolean) => void }) {
  const word = q.word.word;
  const mask = q.mask || '';
  // 找出被遮住的字母下标（按出现顺序对应缺失字母）
  const positions = mask.split('').map((c, i) => (c === '_' ? i : -1)).filter((i) => i >= 0);
  const [filled, setFilled] = useState<string[]>(() => positions.map(() => ''));
  const refs = useRef<(HTMLInputElement | null)[]>([]);

  const submit = () => {
    if (answered) return;
    const joined = filled.join('');
    const ok = normWord(joined) === normWord(q.missing || '');
    onAnswered(ok);
  };

  return (
    <>
      <div className="text-sm text-slate-500">补全单词（缺哪格就在哪格填）：</div>
      <div className="mt-1 text-2xl font-extrabold text-brand-900">{q.word.meaning}</div>
      <div className="mt-3 flex flex-wrap items-center gap-1.5">
        {word.split('').map((ch, i) => {
          const bi = positions.indexOf(i);
          if (bi >= 0) {
            // 缺失位：原位小输入框
            return (
              <input
                key={i}
                ref={(el) => {
                  refs.current[bi] = el;
                }}
                autoFocus={bi === 0}
                maxLength={1}
                value={filled[bi]}
                disabled={answered}
                onChange={(e) => {
                  const v = e.target.value.replace(/[^a-zA-Z]/g, '').slice(-1);
                  setFilled((prev) => {
                    const n = prev.slice();
                    n[bi] = v;
                    return n;
                  });
                  if (v && bi < positions.length - 1) refs.current[bi + 1]?.focus();
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') submit();
                  if (e.key === 'Backspace' && !filled[bi] && bi > 0) refs.current[bi - 1]?.focus();
                }}
                className="h-12 w-10 rounded-xl border-2 border-brand-300 text-center text-xl font-bold uppercase text-brand-800 outline-none focus:border-brand-500"
              />
            );
          }
          // 已知字母：直接显示
          return (
            <span key={i} className="px-0.5 text-3xl font-extrabold text-slate-700">
              {ch}
            </span>
          );
        })}
      </div>
      {!answered && (
        <button onClick={submit} className="btn-primary mt-3 w-full">提交</button>
      )}
      {answered && (
        <div className={`mt-3 rounded-2xl px-4 py-2 text-sm font-medium ${normWord(filled.join('')) === normWord(q.missing || '') ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
          {normWord(filled.join('')) === normWord(q.missing || '')
            ? `✅ 正确！${q.word.word}`
            : `❌ 缺少的是「${q.missing}」→ ${q.word.word}`}
        </div>
      )}
    </>
  );
}

// 发音测试：给单词，朗读，判断是否读对
function SpeakQ({ q, answered, onAnswered }: { q: Q; answered: boolean; onAnswered: (c: boolean) => void }) {
  const supported = speechRecognitionSupported();
  const [listening, setListening] = useState(false);
  const [recognized, setRecognized] = useState(''); // 识别出的文本（用于回显“读错的内容”）
  const [hint, setHint] = useState(''); // 识别失败/网络提示
  const [passed, setPassed] = useState<boolean | null>(null);

  const judge = (ok: boolean) => {
    if (answered) return;
    setPassed(ok);
    onAnswered(ok);
  };

  const record = async () => {
    if (answered || listening) return;
    setListening(true);
    setHint('正在聆听…请大声朗读');
    setRecognized('');
    setPassed(null);
    try {
      const text = await recognizeOnce('en-GB', 6000);
      const ok = speakPassed(text, q.word.word);
      setRecognized(text.trim());
      setHint(ok ? '✓ 识别一致，自动通过' : '✗ 识别结果与目标不符');
      judge(ok);
    } catch (e: any) {
      const msg = e?.message || 'error';
      // 中国大陆环境常见：浏览器内置识别走 Google 服务器被墙 → network / not-allowed
      if (msg === 'network' || msg === 'not-allowed' || msg === 'service-not-allowed') {
        setHint('自动语音识别在本网络不可用（多为无法连接识别服务），请用下方手动判定。');
      } else if (msg === 'no-result' || msg === 'timeout') {
        setHint('没听清，请重试或用下方手动判定。');
      } else {
        setHint('识别失败，请用下方手动判定。');
      }
    } finally {
      setListening(false);
    }
  };

  return (
    <>
      <div className="text-sm text-slate-500">大声朗读下面的单词：</div>
      <div className="mt-1 flex items-center justify-between">
        <div className="text-4xl font-extrabold text-brand-900">{q.word.word}</div>
        <button onClick={() => speak(q.word.word, { rate: 0.8 })} className="btn-ghost !py-2 text-sm">🔊 听示范</button>
      </div>
      {q.word.phonetic && <div className="mt-0.5 text-xs text-slate-400">{q.word.phonetic}</div>}

      {!answered && (
        <div className="mt-4">
          <button
            onClick={record}
            disabled={listening}
            className={`w-full rounded-2xl py-3.5 text-lg font-semibold text-white transition active:scale-[0.99] ${listening ? 'animate-pulse bg-rose-500' : 'bg-brand-600'}`}
          >
            {listening ? '🎤 录音中…' : '🎤 开始朗读（自动判分）'}
          </button>

          {/* 自动识别时回显读到的内容，读错也能看到 */}
          {recognized && (
            <div className="mt-3 rounded-2xl bg-slate-50 px-4 py-2 text-sm">
              <span className="text-slate-400">识别到：</span>
              <span className="font-semibold text-slate-700">「{recognized}」</span>
              <span className="ml-1 text-xs text-slate-400">（目标：{q.word.word}）</span>
            </div>
          )}
          {hint && <p className="mt-2 text-center text-xs text-slate-500">{hint}</p>}

          {/* 手动判定兜底：任何环境下都能完成发音测试 */}
          <div className="mt-3 flex gap-3">
            <button onClick={() => judge(true)} className="flex-1 rounded-2xl border border-emerald-300 bg-emerald-50 py-2.5 text-sm font-semibold text-emerald-700">✅ 读对了</button>
            <button onClick={() => judge(false)} className="flex-1 rounded-2xl border border-rose-300 bg-rose-50 py-2.5 text-sm font-semibold text-rose-700">❌ 没读对</button>
          </div>
          <p className="mt-2 text-center text-[11px] text-slate-400">自动判分需联网识别服务；若不可用，家长/老师可手动判定。</p>
        </div>
      )}

      {answered && passed !== null && (
        <div className={`mt-3 rounded-2xl px-4 py-2 text-sm font-medium ${passed ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
          {passed ? '✅ 发音通过！' : '❌ 这次没通过，再练练～'}
        </div>
      )}
    </>
  );
}

function Stat({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="rounded-2xl bg-slate-50 p-3 text-center">
      <div className={`text-2xl font-extrabold ${color}`}>{value}</div>
      <div className="mt-1 text-xs text-slate-500">{label}</div>
    </div>
  );
}
