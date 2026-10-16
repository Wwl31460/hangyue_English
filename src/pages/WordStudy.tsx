import { ReactNode, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { wordById, wordByText, words } from '../data/words';
import { rootFamily, rootMeaning, affixFamily, wordAffixes } from '../data/families';
import { Word } from '../types';
import { useProgress } from '../lib/progress';
import { speak, prefetchSpeech } from '../lib/tts';

// 每个词根 / 词缀最多扩展 8 个词：太多记不住
const MAX_PER_GROUP = 8;

// 「困难」按钮选中后的样式：明显变色，让学生一眼看出已经标上了
const HARD_ON =
  'rounded-2xl bg-gradient-to-br from-rose-500 to-rose-600 font-semibold text-white shadow-soft active:scale-[0.98] transition';

// 把「家族词形清单」解析成可点词条；解析不到的直接跳过。
// 拓展词来自 families.ts（不受课本单元限制），课本词优先展示。
function resolveFamily(texts: string[], selfKey: string): Word[] {
  const out: Word[] = [];
  for (const t of texts) {
    if (t.toLowerCase() === selfKey) continue; // 不含自己
    const w = wordByText[t.toLowerCase()];
    if (w) out.push(w);
    if (out.length >= MAX_PER_GROUP) break;
  }
  return out;
}

// 单词详解页：词 + 音标 + 词性 + 释义 + 形象图；
// 词根网络 / 词缀网络（reporter 会同时命中 re- 与 -er），每组最多 8 个；
// 近义词 / 反义词（有才显示）；词组、例句单排并附中文。点网络任意词可跳转。
export default function WordStudy() {
  const { id } = useParams();
  const nav = useNavigate();
  const p = useProgress();
  const w = wordById[id ?? ''];
  if (!w) return <div className="p-6 text-slate-500">未找到单词。</div>;

  // 打开即记为“已学”，后续测试只从已学词中抽取
  useEffect(() => {
    p.addLearned(w.id);
  }, [w.id, p]);

  // 本词重点朗读项（词 + 前几个词组/例句）：提前合成好，点「朗读」几乎立刻出声
  const speakItems = useMemo(
    () => [
      w.word,
      ...(w.phrases ?? []).slice(0, 2).map((x) => x.en),
      ...(w.examples ?? []).slice(0, 1).map((x) => x.en),
    ],
    [w],
  );

  // “下一个”要跳的词：既能给按钮用，也顺手预热它的读音
  const nextWord = useMemo(() => {
    if (!w.grade) return null;
    const list = words.filter((x) => x.grade === w.grade && x.unit === w.unit);
    const idx = list.findIndex((x) => x.id === w.id);
    return idx >= 0 && idx < list.length - 1 ? list[idx + 1] : null;
  }, [w.id, w.grade, w.unit]);

  useEffect(() => {
    prefetchSpeech([...speakItems, nextWord?.word ?? ''], {}, 5);
  }, [speakItems, nextWord, p.settings.voiceName]);

  const key = w.word.toLowerCase();
  const hard = p.isHard(w.id);

  // 词根网络：同词根的其他词（不受单元限制，优先展示最常见词）
  const rootWords = w.root ? resolveFamily(rootFamily[w.root] ?? [], key) : [];

  // 词缀网络：该词命中的全部词缀（前缀 + 后缀），逐个展开同缀词。
  // reporter 会同时命中 re- 与 -er，两个家族分别展示。
  const ownAffixes = wordAffixes[key] ?? (w.affix ? [{ affix: w.affix, meaning: w.affixMeaning ?? '' }] : []);
  const affixGroups = ownAffixes
    .map((a) => ({
      affix: a.affix,
      meaning: a.meaning,
      list: resolveFamily(affixFamily[a.affix] ?? [], key),
    }))
    .filter((g) => g.list.length > 0);
  // 前缀排在前面，后缀排在后面
  const prefixGroups = affixGroups.filter((g) => g.affix.endsWith('-'));
  const suffixGroups = affixGroups.filter((g) => g.affix.startsWith('-'));

  // 近义词 / 反义词：有才给，没有就不显示
  const syn = (w.synonyms ?? []).filter((x) => wordByText[x.toLowerCase()]);
  const ant = (w.antonyms ?? []).filter((x) => wordByText[x.toLowerCase()]);

  // “下一个”：跳到本章本节下一个词；末词回单元列表；拓展词（无单元）返回上一页
  const goNext = () => {
    if (nextWord) nav(`/vocab/study/${nextWord.id}`);
    else if (w.grade) nav(`/vocab/grade/${w.grade}/unit/${w.unit}`);
    else nav(-1);
  };

  const goWord = (fid: string) => nav(`/vocab/study/${fid}`);
  const goText = (text: string) => {
    const t = wordByText[text.toLowerCase()];
    if (t) nav(`/vocab/study/${t.id}`);
  };

  return (
    <div className="page pb-6 pt-5">
      {/* 单词卡：形象图 + 词 + 音标 + 词性 + 释义 */}
      <div className="card mt-3 animate-fadeup">
        <div className="flex items-center gap-4">
          <span className="grid h-20 w-20 shrink-0 place-items-center rounded-3xl bg-brand-50 text-6xl">
            {w.image ?? '🔤'}
          </span>
          <div className="min-w-0">
            <div className="truncate text-3xl font-extrabold text-brand-900">{w.word}</div>
            {w.phonetic && <div className="text-sm text-slate-500">{w.phonetic}</div>}
            <div className="mt-1 flex flex-wrap items-center gap-2">
              {w.pos && (
                <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600">
                  {w.pos}
                </span>
              )}
              <span className="text-base font-medium text-rose-500">{w.meaning}</span>
            </div>
          </div>
        </div>

        {/* 顶部操作：朗读 / 困难 / 下一个 一行 */}
        <div className="mt-4 grid grid-cols-3 gap-2">
          <button
            onClick={() => speak(w.word)}
            className="btn-primary flex items-center justify-center !py-3 text-sm"
          >
            🔊 朗读
          </button>
          <button
            onClick={() => (hard ? p.removeHard(w.id) : p.addHard(w.id))}
            aria-pressed={hard}
            className={`flex items-center justify-center !py-3 text-sm ${hard ? HARD_ON : 'btn-ghost'}`}
          >
            {hard ? '✅ 困难' : '😣 困难'}
          </button>
          <button onClick={goNext} className="btn-primary flex items-center justify-center !py-3 text-sm">
            下一个 →
          </button>
        </div>
        {hard && (
          <p className="mt-2 text-center text-xs text-rose-500">
            已加入困难单词本，可到「我的 → 困难单词」复习；再点一次可取消。
          </p>
        )}
      </div>

      {/* 联想记忆：拆词 / 词根 / 拼读，每个词的必背助记法 */}
      {w.association && (
        <Section title="💡 联想记忆">
          <div className="rounded-2xl bg-gradient-to-br from-amber-50 to-orange-50 p-4 text-[15px] leading-relaxed text-amber-900 shadow-sm">
            {w.association}
          </div>
        </Section>
      )}

      {/* 构词解析 */}
      {w.derive && (
        <Section title="构词解析">
          <div className="rounded-2xl bg-gradient-to-br from-brand-600 to-brand-800 p-4 text-white shadow-sm">
            <p className="text-[15px] leading-relaxed">{w.derive}</p>
          </div>
        </Section>
      )}

      {/* 近义词 / 反义词：有才给，没有就不给 */}
      {(syn.length > 0 || ant.length > 0) && (
        <Section title="🔁 近义词 / 反义词">
          {syn.length > 0 && (
            <div className="mb-3">
              <div className="mb-2 text-xs font-semibold text-emerald-700">近义词 · 意思差不多</div>
              <div className="flex flex-wrap gap-2">
                {syn.map((s) => (
                  <WordPill key={s} text={s} word={wordByText[s.toLowerCase()]} onTap={() => goText(s)} />
                ))}
              </div>
            </div>
          )}
          {ant.length > 0 && (
            <div>
              <div className="mb-2 text-xs font-semibold text-rose-600">反义词 · 意思相反</div>
              <div className="flex flex-wrap gap-2">
                {ant.map((s) => (
                  <WordPill key={s} text={s} word={wordByText[s.toLowerCase()]} onTap={() => goText(s)} />
                ))}
              </div>
            </div>
          )}
        </Section>
      )}

      {/* 词组：单排、大字，不截断 */}
      {(w.phrases?.length ?? 0) > 0 && (
        <Section title="词组">
          <div className="flex flex-col gap-2">
            {(w.phrases ?? []).map((ph, i) => (
              <div key={i} className="flex items-center justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2.5">
                <span className="min-w-0">
                  <span className="block text-[15px] font-semibold text-slate-800">{ph.en}</span>
                  <span className="mt-0.5 block text-[13px] text-slate-500">{ph.zh}</span>
                </span>
                <button onClick={() => speak(ph.en, { rate: 0.9 })} className="shrink-0 text-lg text-brand-600">
                  🔊
                </button>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* 例句：单排、大字，不截断 */}
      {(w.examples?.length ?? 0) > 0 && (
        <Section title="例句">
          <div className="flex flex-col gap-2">
            {(w.examples ?? []).map((ex, i) => (
              <div key={i} className="flex items-start justify-between gap-3 rounded-xl bg-slate-50 px-3 py-2.5">
                <span className="min-w-0">
                  <span className="block text-[15px] font-semibold leading-snug text-slate-800">{ex.en}</span>
                  <span className="mt-0.5 block text-[13px] leading-snug text-slate-500">{ex.zh}</span>
                </span>
                <button onClick={() => speak(ex.en, { rate: 0.9 })} className="shrink-0 self-center text-lg text-brand-600">
                  🔊
                </button>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* 词根 / 词缀扩展：先把单词记住，再成串扩展记忆 */}
      {(rootWords.length > 0 || prefixGroups.length > 0 || suffixGroups.length > 0) && (
        <Section title="🧩 词根词缀扩展">
          {rootWords.length > 0 && (
            <div className="mb-4">
              <div className="mb-2 text-xs font-semibold text-brand-700">
                词根扩展：{w.root}（{rootMeaning[w.root!] ?? ''}）
              </div>
              <div className="grid grid-cols-2 gap-2">
                {rootWords.map((fw) => (
                  <NetCell key={fw.id} fw={fw} onTap={() => goWord(fw.id)} />
                ))}
              </div>
            </div>
          )}
          {prefixGroups.map((g) => (
            <div key={g.affix} className="mb-4">
              <div className="mb-2 text-xs font-semibold text-brand-700">前缀扩展：{g.affix}（{g.meaning}）</div>
              <div className="grid grid-cols-2 gap-2">
                {g.list.map((fw) => (
                  <NetCell key={fw.id} fw={fw} onTap={() => goWord(fw.id)} />
                ))}
              </div>
            </div>
          ))}
          {suffixGroups.map((g) => (
            <div key={g.affix}>
              <div className="mb-2 text-xs font-semibold text-brand-700">后缀扩展：{g.affix}（{g.meaning}）</div>
              <div className="grid grid-cols-2 gap-2">
                {g.list.map((fw) => (
                  <NetCell key={fw.id} fw={fw} onTap={() => goWord(fw.id)} />
                ))}
              </div>
            </div>
          ))}
        </Section>
      )}

      {/* 词形变化：比较级 / 最高级 / 过去式 / 过去分词 */}
      {w.forms && (w.forms.comparative || w.forms.superlative || w.forms.past || w.forms.pastParticiple) && (
        <Section title="词形变化">
          <div className="grid grid-cols-2 gap-2">
            {w.forms.comparative && <FormRow label="比较级" value={w.forms.comparative} />}
            {w.forms.superlative && <FormRow label="最高级" value={w.forms.superlative} />}
            {w.forms.past && <FormRow label="过去式" value={w.forms.past} />}
            {w.forms.pastParticiple && <FormRow label="过去分词" value={w.forms.pastParticiple} />}
          </div>
        </Section>
      )}

    </div>
  );
}

// 双排格子：只保留「单词 + 中文 + 发音」，纵向排列且允许折行，
// 这样在半宽的格子里长单词（uncomfortable / misunderstood）也能完整显示，不会被截断。
function NetCell({ fw, onTap }: { fw: Word; onTap: () => void }) {
  return (
    <div className="relative rounded-xl border border-slate-200 bg-white px-2.5 py-2 pr-8 transition hover:border-brand-300 hover:bg-brand-50">
      <button onClick={onTap} className="block w-full text-left active:scale-[0.99]">
        <span className="block break-words text-[13px] font-bold leading-tight text-brand-900">
          {fw.word}
        </span>
        <span className="mt-0.5 block break-words text-[11px] leading-snug text-slate-500">
          {fw.meaning}
        </span>
      </button>
      <button
        onClick={() => speak(fw.word, { rate: 0.9 })}
        className="absolute bottom-1.5 right-1.5 text-sm text-brand-600"
        aria-label={`朗读 ${fw.word}`}
      >
        🔊
      </button>
    </div>
  );
}

// 近义 / 反义词的小圆角标签
function WordPill({ text, word, onTap }: { text: string; word?: Word; onTap: () => void }) {
  return (
    <button
      onClick={onTap}
      className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-left transition hover:border-brand-300 hover:bg-brand-50 active:scale-[0.98]"
    >
      <span className="text-sm font-semibold text-brand-900">{text}</span>
      {word?.meaning && <span className="text-xs text-slate-500">{word.meaning}</span>}
    </button>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="card mt-4 animate-fadeup">
      <div className="section-title">{title}</div>
      {children}
    </div>
  );
}

// 词形变化的一行：标签 + 形式
function FormRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-2 rounded-xl bg-slate-50 px-3 py-2">
      <span className="shrink-0 text-xs font-medium text-slate-500">{label}</span>
      <span className="truncate text-sm font-semibold text-brand-900">{value}</span>
    </div>
  );
}
