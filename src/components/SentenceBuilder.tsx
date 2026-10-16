import { useState } from 'react';

interface Props {
  blocks: string[]; // 正确顺序的词块
  onDone?: (ok: boolean) => void;
}

function shuffle<T>(a: T[]): T[] {
  const r = [...a];
  for (let i = r.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [r[i], r[j]] = [r[j], r[i]];
  }
  return r;
}

// 组句练习：拖拽词块排序，与正确句比对
export default function SentenceBuilder({ blocks, onDone }: Props) {
  const correct = blocks.join(' ');
  const [order, setOrder] = useState<string[]>(() => shuffle([...blocks]));
  const [dragIdx, setDragIdx] = useState<number | null>(null);
  const [status, setStatus] = useState<'idle' | 'ok' | 'wrong'>('idle');

  function onDrop(i: number) {
    if (dragIdx === null) return;
    const n = [...order];
    const [moved] = n.splice(dragIdx, 1);
    n.splice(i, 0, moved);
    setOrder(n);
    setDragIdx(null);
    setStatus('idle');
  }

  function check() {
    const ok = order.join(' ') === correct;
    setStatus(ok ? 'ok' : 'wrong');
    onDone?.(ok);
  }

  function reset() {
    setOrder(shuffle([...blocks]));
    setStatus('idle');
  }

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {order.map((b, i) => (
          <div
            key={i}
            draggable
            onDragStart={() => setDragIdx(i)}
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => onDrop(i)}
            className={`cursor-grab select-none rounded-xl border px-3 py-2 text-base text-slate-800 active:cursor-grabbing ${
              status === 'ok'
                ? 'border-emerald-300 bg-emerald-50'
                : status === 'wrong'
                  ? 'border-rose-300 bg-rose-50'
                  : 'border-slate-200 bg-white'
            }`}
          >
            {b}
          </div>
        ))}
      </div>

      <div className="mt-3 flex items-center gap-2">
        <button
          onClick={check}
          className="rounded-full bg-brand-700 px-4 py-2 text-sm text-white"
        >
          检查
        </button>
        <button onClick={reset} className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
          重排
        </button>
        {status === 'ok' && <span className="text-sm font-medium text-emerald-600">✓ 正确！</span>}
        {status === 'wrong' && (
          <span className="text-sm text-rose-600">再试试：{correct}</span>
        )}
      </div>
      <p className="mt-2 text-[11px] text-slate-400">长按词块拖拽排序（移动端可长按后拖动）。</p>
    </div>
  );
}
