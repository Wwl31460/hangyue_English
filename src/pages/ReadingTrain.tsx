import { ReactNode, useEffect, useMemo, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { readings } from '../data/readings';
import { useProgress } from '../lib/progress';
import { speak, speakSequence, stopSpeak, prefetchSpeech } from '../lib/tts';
import { useRecorder } from '../lib/recorder';
import { Reading, Sentence, questionUnits } from '../types';

export default function ReadingTrain() {
  const { id } = useParams();
  const nav = useNavigate();
  const p = useProgress();
  const material = readings.find((r) => r.id === id);

  const [cur, setCur] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loop, setLoop] = useState(false);
  const [rate, setRate] = useState(p.settings.defaultRate);
  const [aIdx, setAIdx] = useState<number | null>(null);
  const [bIdx, setBIdx] = useState<number | null>(null);
  const [showQuiz, setShowQuiz] = useState(false);
  const [allPlaying, setAllPlaying] = useState(false); // 听全文状态

  useEffect(() => () => stopSpeak(), [nav]);

  const sentences = useMemo(() => material?.sentences ?? [], [material]);
  const voiceName = p.settings.voiceName;

  // 进页面先预热前几句，首次连播也能无缝衔接
  useEffect(() => {
    if (sentences.length === 0) return;
    prefetchSpeech(
      sentences.map((s) => s.text),
      { name: voiceName, rate },
      4,
    );
  }, [sentences, voiceName, rate]);

  if (!material) return <div className="p-6 text-slate-500">未找到材料。</div>;

  // 单句朗读（点“读这句”或切句时用）
  function speakAt(i: number) {
    speak(sentences[i].text, {
      rate,
      name: voiceName,
      onstart: () => setPlaying(true),
      onend: () => setPlaying(false),
    });
  }

  // 连续播放：全部交给 speakSequence —— 句子按音频时间轴排布，句间没有空档
  function play() {
    const hasAB = aIdx !== null && bIdx !== null;
    const from = hasAB ? Math.min(aIdx as number, bIdx as number) : cur;
    const to = hasAB ? Math.max(aIdx as number, bIdx as number) : loop ? cur : sentences.length - 1;
    setCur(from);
    setPlaying(true);
    speakSequence(
      sentences.map((s) => s.text),
      {
        from,
        to,
        loop: hasAB || loop,
        rate,
        name: voiceName,
        onIndex: (i) => setCur(i),
        onDone: () => setPlaying(false),
      },
    );
  }

  // 暂停：直接停掉已排入的音频（无缝播放器由时间轴统一调度，停了就不会再往下读）
  function toggle() {
    if (playing) {
      stopSpeak();
      setPlaying(false);
    } else {
      play();
    }
  }

  function prev() {
    stopSpeak();
    setPlaying(false);
    setCur((c) => Math.max(0, c - 1));
  }
  function next() {
    stopSpeak();
    setPlaying(false);
    setCur((c) => Math.min(sentences.length - 1, c + 1));
  }
  // 听全文：把整篇小故事作为一段朗读，便于先通读再逐句练
  function toggleStory() {
    if (allPlaying) {
      stopSpeak();
      setAllPlaying(false);
      return;
    }
    speak(material!.story, {
      rate,
      name: voiceName,
      onstart: () => setAllPlaying(true),
      onend: () => setAllPlaying(false),
    });
  }

  return (
    <div className="page pb-6 pt-5">
      <button
        onClick={() => {
          stopSpeak();
          nav('/listen');
        }}
        className="text-sm text-slate-500"
      >
        ← 返回
      </button>

      <div className="mt-2">
        <h1 className="text-xl font-extrabold text-brand-900">{material.title}</h1>
        <div className="text-xs text-slate-500">
          {material.level} · {material.topic} · {material.duration}
        </div>
      </div>

      {/* 故事全文：先通读整篇小故事 */}
      <div className="card mt-4 animate-fadeup">
        <div className="flex items-center justify-between">
          <div className="section-title mb-0">故事全文</div>
          <button
            onClick={toggleStory}
            className="rounded-full bg-brand-600 px-3 py-1.5 text-xs font-medium text-white transition active:scale-95"
          >
            {allPlaying ? '⏸ 停止' : '📖 听全文'}
          </button>
        </div>
        <p className="mt-3 text-[15px] leading-7 text-slate-700">{material.story}</p>
      </div>

      {/* 播放器 */}
      <div className="card mt-4 animate-fadeup overflow-hidden !p-0">
        <div className="bg-gradient-to-br from-brand-600 to-brand-900 p-5">
          <p className="text-lg font-semibold leading-relaxed text-white">{sentences[cur].text}</p>
          {sentences[cur].zh && (
            <p className="mt-1.5 min-h-[2.5rem] text-sm leading-relaxed text-white/80">{sentences[cur].zh}</p>
          )}
          <div className="mt-4 flex items-center justify-center gap-5">
            <button
              onClick={prev}
              className="grid h-12 w-12 place-items-center rounded-full bg-white/15 text-xl text-white backdrop-blur transition active:scale-95"
            >
              ⏮
            </button>
            <button
              onClick={toggle}
              className="grid h-16 w-16 place-items-center rounded-full bg-white text-2xl text-brand-800 shadow-soft transition active:scale-95"
            >
              {playing ? '⏸' : '▶'}
            </button>
            <button
              onClick={next}
              className="grid h-12 w-12 place-items-center rounded-full bg-white/15 text-xl text-white backdrop-blur transition active:scale-95"
            >
              ⏭
            </button>
          </div>
        </div>

        <div className="space-y-3 p-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setLoop((l) => !l)}
              className={`chip ${loop ? 'chip-on' : 'chip-off'}`}
            >
              🔁 单句循环
            </button>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500">语速</span>
              <input
                type="range"
                min={0.5}
                max={1.2}
                step={0.1}
                value={rate}
                onChange={(e) => setRate(parseFloat(e.target.value))}
                className="w-24 accent-brand-600"
              />
              <span className="w-9 text-sm font-semibold text-brand-700">{rate}x</span>
            </div>
          </div>

          <div className="flex items-center justify-between rounded-2xl bg-accent-50 px-3 py-2">
            <div className="flex gap-2">
              <button onClick={() => setAIdx(cur)} className="chip !bg-white !py-1 text-accent-700 ring-1 ring-accent-200">
                设A ({aIdx !== null ? aIdx + 1 : '-'})
              </button>
              <button onClick={() => setBIdx(cur)} className="chip !bg-white !py-1 text-accent-700 ring-1 ring-accent-200">
                设B ({bIdx !== null ? bIdx + 1 : '-'})
              </button>
              {(aIdx !== null || bIdx !== null) && (
                <button
                  onClick={() => {
                    setAIdx(null);
                    setBIdx(null);
                  }}
                  className="chip !bg-slate-100 !py-1 text-slate-500"
                >
                  清除
                </button>
              )}
            </div>
            <span className="text-xs font-medium text-accent-700">AB 复读</span>
          </div>
        </div>
      </div>

      {/* 整篇跟读：保存整篇文章录音（不是单句） */}
      <ArticleReadAloud materialId={material.id} sentences={sentences} />

      {/* 理解小测（成绩计入今日得分，点开前在列表可见） */}
      <div className="mt-5">
        <button onClick={() => setShowQuiz((v) => !v)} className="btn-primary w-full">
          📝 理解小测
        </button>
      </div>

      {showQuiz && <QuizPanel material={material} onClose={() => setShowQuiz(false)} />}
    </div>
  );
}

// 整篇跟读录音：点“开始录音”后按句子顺序朗读（读一句换下一句），读完点“停止录音”；
// 停止后出现“试听”按钮，试听满意再点“提交”保存整篇录音；
// 提交后出现“回顾录音”按钮，可回放整篇录音供老师/家长检查作业，并显示系统自动评分。
function ArticleReadAloud({ materialId, sentences }: { materialId: string; sentences: Sentence[] }) {
  const p = useProgress();
  const rec = useRecorder();
  const [cur, setCur] = useState(0);
  // idle 未录 / rec 录音中 / review 待提交（可试听） / done 已提交（可回放、看评分）
  const [phase, setPhase] = useState<'idle' | 'rec' | 'review' | 'done'>(
    p.getReadingAudio(materialId) ? 'done' : 'idle',
  );
  const [recordScore, setRecordScore] = useState<number | null>(
    () => p.getReadingRecordScore(materialId) ?? null,
  );
  const [savedUrl, setSavedUrl] = useState<string | null>(() => p.getReadingAudio(materialId) ?? null);
  const [submitting, setSubmitting] = useState(false);

  // 隐藏音频元素 + 播放状态：供“试听 / 回顾录音”按钮复用
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playingAudio, setPlayingAudio] = useState(false);
  const togglePlay = (src: string | null) => {
    const a = audioRef.current;
    if (!a || !src) return;
    if (!a.paused) {
      a.pause();
      setPlayingAudio(false);
      return;
    }
    a.src = src;
    a.currentTime = 0;
    a.play()
      .then(() => setPlayingAudio(true))
      .catch(() => setPlayingAudio(false));
  };

  // 估算朗读时长（约每秒 2.2 个词），用于按录音时长自动评分
  const estSec = useMemo(() => {
    const words = sentences.reduce((n, s) => n + s.text.split(/\s+/).length, 0);
    return Math.max(3, words / 2.2);
  }, [sentences]);

  const blobToDataUrl = (b: Blob) =>
    new Promise<string>((resolve, reject) => {
      const r = new FileReader();
      r.onload = () => resolve(r.result as string);
      r.onerror = reject;
      r.readAsDataURL(b);
    });

  // 系统自动评分：用录音时长占估算朗读时长的比例衡量“有没有读完整”，满分 100
  const scoreOf = (dur: number) => Math.max(0, Math.min(100, Math.round((dur / estSec) * 100)));

  const startRec = () => {
    rec.reset();
    setCur(0);
    setPlayingAudio(false);
    rec.start();
    setPhase('rec');
  };

  const stopRec = () => {
    rec.stop();
    setPhase('review');
  };

  const submit = async () => {
    if (!rec.blob) return;
    setSubmitting(true);
    try {
      const url = await blobToDataUrl(rec.blob);
      const sc = scoreOf(rec.duration);
      p.saveReadingAudio(materialId, url);
      p.recordReadingRecord(materialId, sc);
      setSavedUrl(url);
      setRecordScore(sc);
      setPhase('done');
    } catch {
      /* 保存失败不影响继续重录 */
    } finally {
      setSubmitting(false);
    }
  };

  const reRecord = () => {
    if (audioRef.current && !audioRef.current.paused) audioRef.current.pause();
    setPlayingAudio(false);
    rec.reset();
    setCur(0);
    setPhase('idle');
  };

  const goNext = () => setCur((c) => Math.min(sentences.length - 1, c + 1));

  return (
    <div className="card mt-4 animate-fadeup">
      <div className="flex items-center justify-between">
        <span className="section-title mb-0">整篇跟读</span>
        {phase === 'done' && <span className="text-xs text-emerald-600">✓ 已保存</span>}
      </div>

      {/* 句子按顺序显示，当前句高亮：读一句、换下一句 */}
      <div className="mt-3 space-y-1.5">
        {sentences.map((s, i) => (
          <div
            key={s.id}
            className={`flex w-full items-start gap-2 rounded-xl px-3 py-2 text-left text-sm transition ${
              i === cur ? 'bg-brand-50 font-semibold text-brand-800' : 'text-slate-600'
            }`}
          >
            <span
              className={`mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full text-[11px] ${
                i === cur ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-400'
              }`}
            >
              {i + 1}
            </span>
            <span>{s.text}</span>
          </div>
        ))}
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        {phase === 'idle' && (
          <button onClick={startRec} className="btn-accent !py-2.5">
            ● 开始录音
          </button>
        )}

        {phase === 'rec' && (
          <>
            <button
              onClick={stopRec}
              className="animate-pulse rounded-2xl bg-rose-500 px-5 py-2.5 font-semibold text-white"
            >
              ■ 停止录音 {rec.duration.toFixed(1)}s
            </button>
            <button onClick={goNext} className="btn-ghost !py-2.5">
              下一句 ▶
            </button>
          </>
        )}

        {/* 停止后：先“试听”，满意再“提交” */}
        {phase === 'review' && (
          <>
            <button onClick={() => togglePlay(rec.audioUrl)} className="btn-accent !py-2.5">
              {playingAudio ? '⏸ 停止试听' : '🎧 试听'}
            </button>
            <button onClick={reRecord} className="btn-ghost !py-2.5">
              重录
            </button>
            <button onClick={submit} disabled={submitting} className="btn-primary !py-2.5">
              {submitting ? '保存中…' : '提交'}
            </button>
          </>
        )}

        {/* 提交后：出现“回顾录音”，供检查作业 */}
        {phase === 'done' && (
          <>
            <button onClick={() => togglePlay(savedUrl)} className="btn-accent !py-2.5">
              {playingAudio ? '⏸ 停止回顾' : '🎧 回顾录音'}
            </button>
            <button onClick={reRecord} className="btn-ghost !py-2.5">
              重录
            </button>
          </>
        )}
      </div>

      <audio ref={audioRef} onEnded={() => setPlayingAudio(false)} className="hidden" />

      {phase === 'review' && (
        <p className="mt-2 text-xs text-slate-500">🎧 先点“试听”听一遍，满意再点“提交”。</p>
      )}

      {phase === 'done' && (
        <div className="mt-3 rounded-xl bg-amber-50 p-3">
          <div className="mt-1 text-sm font-medium text-amber-800">
            🤖 系统评分：{recordScore != null ? `${recordScore} 分` : '—'}
          </div>
        </div>
      )}
    </div>
  );
}

function QuizPanel({ material, onClose }: { material: Reading; onClose: () => void }) {
  const p = useProgress();
  // 每题作答状态：选择题存 choice 下标；抠空题存每个空的下标数组
  const [resp, setResp] = useState<Array<{ choice?: number | null; blanks?: (number | null)[] }>>(() =>
    material.questions.map((q) => (q.type === 'cloze' ? { blanks: q.blanks.map(() => null) } : { choice: null })),
  );
  const [checked, setChecked] = useState(false);
  const rewardedRef = useRef(false);

  // 计分单元：选择题=1，抠空题=空的数量；正确单元数用于打分
  const totalUnits = material.questions.reduce((n, q) => n + questionUnits(q), 0);
  const correctUnits = material.questions.reduce((n, q, i) => {
    const r = resp[i];
    if (q.type === 'choice') return n + (r?.choice === q.answer ? 1 : 0);
    return n + q.blanks.filter((b, bi) => r?.blanks?.[bi] === b.answer).length;
  }, 0);
  const pct = totalUnits > 0 ? Math.round((correctUnits / totalUnits) * 100) : 0;
  // 本章总评 = 本次测试分 + 前面的跟读录音分（两者合计，见 progress.getReadingScore）
  const recScore = p.getReadingRecordScore(material.id);
  const chapterTotal = p.getReadingScore(material.id);

  const setChoice = (qi: number, oi: number) =>
    setResp((prev) => {
      const n = [...prev];
      n[qi] = { choice: oi };
      return n;
    });
  const setBlank = (qi: number, bi: number, oi: number) =>
    setResp((prev) => {
      const n = [...prev];
      const cur = n[qi]?.blanks ? [...(n[qi].blanks as (number | null)[])] : [];
      cur[bi] = oi;
      n[qi] = { ...n[qi], blanks: cur };
      return n;
    });

  const submit = () => {
    setChecked(true);
    // 提交即按正确率记录实际得分（百分制），计入今日听读得分；仅记一次
    if (!rewardedRef.current && totalUnits > 0) {
      rewardedRef.current = true;
      p.recordReadingScore(material.id, pct);
    }
  };

  return (
    <div className="card mt-4 animate-fadeup">
      <div className="flex items-center justify-between">
        <span className="section-title mb-0">理解小测</span>
        <button onClick={onClose} className="text-xs text-slate-400">
          收起
        </button>
      </div>
      <div className="mt-3 space-y-4">
        {material.questions.map((q, qi) => (
          <div key={q.id}>
            <div className="text-sm font-medium text-slate-700">
              {qi + 1}. {q.type === 'choice' ? q.question : (q.prompt ?? '选词填空')}
            </div>

            {/* 选择题 */}
            {q.type === 'choice' && (
              <div className="mt-2 space-y-2">
                {q.options.map((o, oi) => {
                  const picked = resp[qi]?.choice;
                  // 选中即加深底色，点下去马上有反馈；提交后才显示对错
                  let cls =
                    oi === picked
                      ? 'border-brand-500 bg-brand-100 text-brand-900'
                      : 'border-slate-200 bg-white hover:border-brand-300';
                  if (checked) {
                    if (oi === q.answer) cls = 'border-emerald-400 bg-emerald-50 text-emerald-700';
                    else if (oi === picked) cls = 'border-rose-400 bg-rose-50 text-rose-700';
                    else cls = 'border-slate-200 bg-white opacity-60';
                  }
                  return (
                    <button
                      key={oi}
                      disabled={checked}
                      onClick={() => !checked && setChoice(qi, oi)}
                      className={`block w-full rounded-xl border-2 px-3 py-2 text-left text-sm font-semibold transition active:scale-[0.99] ${cls}`}
                    >
                      <span className="mr-2 text-slate-400">{String.fromCharCode(65 + oi)}.</span>
                      {o}
                    </button>
                  );
                })}
              </div>
            )}

            {/* 选词填空：原文抠空，从候选词中选词填入 */}
            {q.type === 'cloze' && (
              <>
                <div className="mt-2 rounded-2xl bg-slate-50 px-3 py-2 text-[15px] leading-7 text-slate-800">
                  {q.sentence}
                </div>
                <div className="mt-2 space-y-2">
                  {q.blanks.map((b, bi) => {
                    const picked = resp[qi]?.blanks?.[bi];
                    return (
                      <div key={bi} className="flex flex-wrap items-center gap-2">
                        <span className="text-xs font-semibold text-slate-400">空{bi + 1}</span>
                        {b.options.map((o, oi) => {
                          // 选中即加深底色，点下去马上有反馈；提交后才显示对错
                          let cls =
                            oi === picked
                              ? 'border-brand-500 bg-brand-100 text-brand-900'
                              : 'border-slate-200 bg-white hover:border-brand-300';
                          if (checked) {
                            if (oi === b.answer) cls = 'border-emerald-400 bg-emerald-50 text-emerald-700';
                            else if (oi === picked) cls = 'border-rose-400 bg-rose-50 text-rose-700';
                            else cls = 'border-slate-200 bg-white opacity-60';
                          }
                          return (
                            <button
                              key={oi}
                              disabled={checked}
                              onClick={() => !checked && setBlank(qi, bi, oi)}
                              className={`rounded-xl border-2 px-3 py-1.5 text-sm font-semibold transition active:scale-95 ${cls}`}
                            >
                              {o}
                            </button>
                          );
                        })}
                      </div>
                    );
                  })}
                </div>
              </>
            )}
          </div>
        ))}
      </div>
      {!checked ? (
        <button onClick={submit} className="btn-primary mt-4 w-full">
          提交
        </button>
      ) : (
        <div className="mt-4 space-y-2">
          <div className="rounded-xl bg-emerald-50 p-3 text-sm font-medium text-emerald-700">
            ✅ 本次测试得分：{pct} 分（答对 {correctUnits} / {totalUnits}）
          </div>
          {recScore != null ? (
            <div className="rounded-xl bg-amber-50 p-3 text-sm font-medium text-amber-800">
              🎙 录音评分 {recScore} 分 ＋ 测试 {pct} 分 ＝ 本章总评 <b>{chapterTotal} 分</b>
            </div>
          ) : (
            <div className="rounded-xl bg-amber-50 p-3 text-sm text-amber-800">
              🎙 还没提交跟读录音。先到上面“整篇跟读”录一遍，总评会更高哦。
            </div>
          )}
        </div>
      )}
    </div>
  );
}
