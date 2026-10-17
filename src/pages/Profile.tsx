import { ReactNode, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useProgress } from '../lib/progress';
import { useAuth } from '../lib/auth';
import { englishVoicesSorted, speak } from '../lib/tts';
import { APP_VERSION, triggerManualCheck } from '../lib/update';

// 统计可选的时间维度
const RANGES = [
  { label: '一周', days: 7 },
  { label: '一个月', days: 30 },
  { label: '三个月', days: 90 },
  { label: '半年', days: 180 },
];

// 把 2026-10-16 转成「周五」
function weekdayOf(dateStr: string): string {
  const [y, m, d] = dateStr.split('-').map(Number);
  return '日一二三四五六'[new Date(y, m - 1, d).getDay()];
}

export default function Profile() {
  const p = useProgress();
  const { user, ready, syncState, logout } = useAuth();
  const [voices, setVoices] = useState<string[]>([]);
  const [rangeDays, setRangeDays] = useState(7);

  useEffect(() => {
    const loadVoices = () => setVoices(englishVoicesSorted().map((v) => v.name));
    loadVoices();
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

  // 选定时间维度内的每日数据
  const series = p.dailySeries(rangeDays);
  const sumWords = series.reduce((n, d) => n + d.words, 0);
  const sumReadings = series.reduce((n, d) => n + d.readings, 0);
  const sumStars = Math.round(series.reduce((n, d) => n + p.dayStars(d), 0) * 10) / 10;
  const activeDays = series.filter((d) => d.words > 0 || d.readings > 0).length;
  const maxStars = Math.max(10, ...series.map((d) => p.dayStars(d)));
  // 明细只列有记录的日子，最近的排在最前
  const active = series.filter((d) => d.words > 0 || d.readings > 0 || d.minutes > 0).reverse();

  const totalStars = p.totalStars();
  const toNextPoint = Math.max(0, Math.round((10 - (totalStars % 10)) * 10) / 10);
  const todayBest = p.daily.readingIds.reduce((m, id) => Math.max(m, p.getReadingScore(id) ?? 0), 0);

  return (
    <div className="page pb-24 pt-6">
      <h1 className="text-xl font-extrabold text-brand-900">我的</h1>

      {/* 账号：登录态 / 进度同步 */}
      <div className="card mt-4 animate-fadeup">
        <div className="section-title">账号</div>
        {ready && user ? (
          <div className="mt-2">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-bold text-brand-900">👤 {user.name}</div>
                <div className="text-xs text-slate-500">
                  {syncState === 'saved'
                    ? '进度已自动同步到云端'
                    : syncState === 'error'
                      ? '云端同步失败，本机进度正常'
                      : '正在与云端同步…'}
                </div>
              </div>
              <button
                onClick={() => logout()}
                className="rounded-full bg-rose-50 px-3 py-1.5 text-sm font-medium text-rose-600"
              >
                退出登录
              </button>
            </div>
          </div>
        ) : (
          <div className="mt-2 flex items-center justify-between">
            <div className="text-sm text-slate-500">未登录：进度只存在本机</div>
            <Link to="/login" className="btn-primary !py-1.5 !px-4 text-sm">
              登录同步
            </Link>
          </div>
        )}
        <Link
          to="/teacher"
          className="mt-3 block rounded-xl bg-slate-50 px-3 py-2 text-center text-xs text-slate-500"
        >
          老师后台（添加学生账号）
        </Link>
      </div>

      {/* 今日学习情况 */}
      <div className="card mt-4 animate-fadeup">
        <div className="flex items-center justify-between">
          <span className="section-title mb-0">今日学习</span>
          <span className="text-sm font-bold text-brand-700">{p.todayStars()} / 10 ⭐</span>
        </div>
        <div className="mt-2 h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-800 transition-all"
            style={{ width: `${Math.min(100, p.todayStars() * 10)}%` }}
          />
        </div>
        <div className="mt-3 grid grid-cols-4 gap-2">
          <MiniTile icon="📝" label="新单词" value={p.daily.words} />
          <MiniTile icon="🎧" label="听读" value={todayBest > 0 ? `${todayBest}分` : '未测'} />
          <MiniTile icon="⏱️" label="分钟" value={p.daily.minutes} />
          <MiniTile icon="⭐" label="今日星" value={p.dayStars(p.daily).toFixed(1)} />
        </div>
      </div>

      {/* 学习统计：累计 + 可选时间维度 + 每日明细 */}
      <div className="card mt-4 animate-fadeup">
        <div className="flex items-center justify-between">
          <span className="section-title mb-0">学习统计</span>
          <span className="text-xs text-slate-400">10 ⭐ = 1 积分</span>
        </div>

        {/* 累计（不管选哪个时间维度，这里都是全部历史） */}
        <div className="mt-3 grid grid-cols-3 gap-2">
          <MiniTile icon="⭐" label="累计星星" value={totalStars.toFixed(1)} />
          <MiniTile icon="🏅" label="积分" value={p.totalPoints()} />
          <MiniTile icon="🔥" label="连续学习" value={`${p.streakDays()} 天`} />
        </div>
        <p className="mt-1.5 text-center text-[11px] text-slate-400">
          再得 {toNextPoint.toFixed(1)} ⭐ 即可兑换下一个积分
        </p>

        {/* 时间维度 */}
        <div className="mt-4 flex gap-2">
          {RANGES.map((r) => (
            <button
              key={r.days}
              onClick={() => setRangeDays(r.days)}
              className={`chip flex-1 !px-0 text-center ${rangeDays === r.days ? 'chip-on' : 'chip-off'}`}
            >
              {r.label}
            </button>
          ))}
        </div>

        {/* 区间汇总 */}
        <div className="mt-3 grid grid-cols-4 gap-2">
          <MiniTile icon="📝" label="学习单词" value={sumWords} />
          <MiniTile icon="🎧" label="听读" value={sumReadings} />
          <MiniTile icon="📅" label="学习天数" value={activeDays} />
          <MiniTile icon="⭐" label="获得星星" value={sumStars.toFixed(1)} />
        </div>

        {/* 每天多少星 */}
        <div className="mt-4 flex h-24 items-end gap-px">
          {series.map((d) => {
            const s = p.dayStars(d);
            return (
              <div key={d.date} className="flex h-full flex-1 flex-col items-center justify-end">
                <div
                  className={`w-full rounded-t ${s > 0 ? 'bg-gradient-to-t from-brand-700 to-accent-400' : 'bg-slate-100'}`}
                  style={{ height: `${(s / maxStars) * 100}%`, minHeight: s > 0 ? 4 : 2 }}
                  title={`${d.date}：${s} ⭐`}
                />
              </div>
            );
          })}
        </div>
        <div className="mt-1 flex justify-between text-[10px] text-slate-400">
          <span>{series[0]?.date}</span>
          <span>今天 {p.today}</span>
        </div>

        {/* 每日明细：哪一天学了多少 */}
        <div className="mt-3 max-h-60 space-y-1.5 overflow-y-auto pr-1">
          {active.length === 0 && (
            <p className="py-2 text-center text-xs text-slate-400">这段时间还没有学习记录，去学一会儿吧～</p>
          )}
          {active.map((d) => (
            <div
              key={d.date}
              className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2 text-xs"
            >
              <span className="font-semibold text-slate-600">
                {d.date.slice(5)}
                <span className="ml-1 font-normal text-slate-400">周{weekdayOf(d.date)}</span>
              </span>
              <span className="flex items-center gap-2.5 text-slate-500">
                <span className="font-bold text-amber-500">⭐ {p.dayStars(d).toFixed(1)}</span>
                <span>📝 {d.words}</span>
                <span>🎧 {d.readings}</span>
                <span>⏱️ {d.minutes}′</span>
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 单词本：错词本 / 困难单词本 */}
      <div className="card mt-4 animate-fadeup">
        <div className="section-title">单词本</div>
        <div className="mt-2 grid grid-cols-2 gap-3">
          <Link to="/vocab/mistakes" className="rounded-2xl bg-slate-50 px-3 py-3 text-center text-sm font-medium text-slate-700">
            📕 错词本
          </Link>
          <Link to="/vocab/hard" className="rounded-2xl bg-slate-50 px-3 py-3 text-center text-sm font-medium text-slate-700">
            😣 困难单词本
          </Link>
        </div>
      </div>

      {/* 设置 */}
      <div className="card mt-4 animate-fadeup">
        <div className="section-title">设置</div>
        <label className="mt-2 flex items-center justify-between text-sm text-slate-600">
          默认语速
          <select
            value={p.settings.defaultRate}
            onChange={(e) => p.updateSettings({ defaultRate: parseFloat(e.target.value) })}
            className="rounded-lg border border-slate-200 bg-white px-2 py-1"
          >
            {[0.5, 0.75, 0.9, 1, 1.1, 1.2].map((r) => (
              <option key={r} value={r}>
                {r}x
              </option>
            ))}
          </select>
        </label>
        <div className="mt-3">
          <div className="flex items-center justify-between text-sm text-slate-600">
            <span>发音人</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => speak('Hello, I am your English teacher. Nice to meet you!', { name: p.settings.voiceName })}
                className="rounded-lg bg-slate-100 px-2 py-1 text-xs text-slate-500"
              >
                🔊 试听
              </button>
              <select
                value={p.settings.voiceName ?? ''}
                onChange={(e) => p.updateSettings({ voiceName: e.target.value || null })}
                className="rounded-lg border border-slate-200 bg-white px-2 py-1"
              >
                <option value="">英式 Sonia（Edge 真人语音 · 推荐）</option>
                <option value="en-GB-RyanNeural">英式 Ryan（Edge 男声）</option>
                <option value="en-US-AriaNeural">美式 Aria（Edge 女声）</option>
                <option value="en-US-GuyNeural">美式 Guy（Edge 男声）</option>
                {voices.length > 0 && (
                  <optgroup label="本机系统语音">
                    {voices.map((v) => (
                      <option key={v} value={v}>
                        {v}
                      </option>
                    ))}
                  </optgroup>
                )}
              </select>
            </div>
          </div>
          <p className="mt-1.5 text-[11px] leading-5 text-slate-400">
            默认使用 <b>Edge 在线真人语音</b>（英式 Sonia，语调自然），需联网；断网或失败时自动切换为系统语音。
          </p>
        </div>
        <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-4">
          <div className="text-sm text-slate-600">
            当前版本 <span className="font-bold text-slate-700">{APP_VERSION}</span>
          </div>
          <button
            onClick={triggerManualCheck}
            className="rounded-lg bg-slate-100 px-3 py-1.5 text-xs text-slate-600"
          >
            🔄 检查更新
          </button>
        </div>

        {/* 清除学习数据只有老师能做：学生在这个页面没有这个按钮，避免误点把进度清空 */}
        <p className="mt-4 rounded-xl bg-slate-50 px-3 py-2.5 text-center text-xs leading-5 text-slate-400">
          要清除学习数据，请让老师在「老师后台」处理。学生端不提供这个操作。
        </p>
      </div>
    </div>
  );
}

// 小统计块：图标 + 数值 + 标签
function MiniTile({ icon, label, value }: { icon: string; label: string; value: ReactNode }) {
  return (
    <div className="rounded-2xl bg-gradient-to-b from-slate-50 to-white px-2 py-2.5 text-center ring-1 ring-slate-100">
      <div className="text-base">{icon}</div>
      <div className="mt-0.5 text-lg font-extrabold leading-tight text-brand-700">{value}</div>
      <div className="text-[11px] text-slate-500">{label}</div>
    </div>
  );
}
