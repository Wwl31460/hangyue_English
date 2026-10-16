import { useNavigate } from 'react-router-dom';

// 每页顶部固定的返回栏：返回首页 / 返回上一页 / 回到背单词页
// 固定在顶部（sticky top-0），向下翻时始终可见，可随时点击。
export default function BackBar() {
  const nav = useNavigate();
  return (
    <nav className="sticky top-0 z-30 grid grid-cols-3 border-b border-slate-200 bg-white/95 backdrop-blur">
      <button
        onClick={() => nav('/')}
        className="flex flex-col items-center gap-0.5 py-2.5 text-xs text-slate-600"
      >
        <span className="text-xl">🏠</span>
        返回首页
      </button>
      <button
        onClick={() => nav(-1)}
        className="flex flex-col items-center gap-0.5 border-x border-slate-100 py-2.5 text-xs text-slate-600"
      >
        <span className="text-xl">↩️</span>
        返回上一页
      </button>
      <button
        onClick={() => nav('/vocab')}
        className="flex flex-col items-center gap-0.5 py-2.5 text-xs text-slate-600"
      >
        <span className="text-xl">📚</span>
        回到背单词
      </button>
    </nav>
  );
}
