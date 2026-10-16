import { useCallback, useEffect, useState } from 'react';
import { HashRouter, Routes, Route, useLocation } from 'react-router-dom';
import { ProgressProvider, useProgress } from './lib/progress';
import { AuthProvider } from './lib/auth';
import { warmupAudio, setSpeechErrorNotifier } from './lib/tts';
import {
  APP_VERSION,
  fetchLatestVersion,
  isNewer,
  setManualCheckHandler,
  type RemoteVersion,
} from './lib/update';
import BackBar from './components/BackBar';
import UpdateDialog from './components/UpdateDialog';
import Home from './pages/Home';
import Vocabulary from './pages/Vocabulary';
import WordList from './pages/WordList';
import WordStudy from './pages/WordStudy';
import Quiz from './pages/Quiz';
import Review from './pages/Review';
import Test from './pages/Test';
import Mistakes from './pages/Mistakes';
import Hard from './pages/Hard';
import Listen from './pages/Listen';
import ReadingTrain from './pages/ReadingTrain';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Teacher from './pages/Teacher';

// 学习计时：仅在页面可见时累计分钟，写入今日进度
function StudyTimer() {
  const p = useProgress();
  useEffect(() => {
    const t = setInterval(() => {
      if (document.visibilityState === 'visible') p.addMinutes(1);
    }, 60000);
    return () => clearInterval(t);
  }, [p]);
  return null;
}

function Shell() {
  const { pathname } = useLocation();
  const [toast, setToast] = useState('');
  const [update, setUpdate] = useState<RemoteVersion | null>(null);

  // 进应用就把音频上下文建好，第一次朗读不会被初始化拖慢
  useEffect(() => {
    warmupAudio();
    // 朗读彻底失败时（连不上语音服务 + 本机无离线语音）弹一条提示，避免"点了没反应"
    setSpeechErrorNotifier((m) => setToast(m));
    return () => setSpeechErrorNotifier(null);
  }, []);

  // 检查更新。manual=true 时把结果说出来（已是最新 / 检查失败）；
  // 自动检查只在真有新版时才弹窗，其它情况一声不吭。
  const runCheck = useCallback(async (manual: boolean) => {
    if (manual) setToast('正在检查更新…');
    const remote = await fetchLatestVersion();
    if (!remote) {
      setToast(manual ? '检查失败：暂时连不上更新服务器。请检查网络后重试。' : '');
      return;
    }
    if (isNewer(remote)) {
      setToast('');
      setUpdate(remote);
    } else {
      setToast(manual ? `已是最新版本（${APP_VERSION}）` : '');
    }
  }, []);

  // 启动 2 秒后静默查一次，不跟首屏抢时间
  useEffect(() => {
    const t = setTimeout(() => void runCheck(false), 2000);
    return () => clearTimeout(t);
  }, [runCheck]);

  // 「我的 → 检查更新」按钮走这里
  useEffect(() => {
    setManualCheckHandler(() => void runCheck(true));
    return () => setManualCheckHandler(null);
  }, [runCheck]);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(''), 4000);
    return () => clearTimeout(t);
  }, [toast]);

  return (
    <div
      className="flex min-h-screen flex-col bg-[#f4f7fb]"
      // Android 15 起强制边到边显示，内容会顶到状态栏/手势条下方，这里按安全区留白
      style={{
        paddingTop: 'env(safe-area-inset-top, 0px)',
        paddingBottom: 'env(safe-area-inset-bottom, 0px)',
      }}
    >
      {update && <UpdateDialog remote={update} onClose={() => setUpdate(null)} />}
      {toast && (
        <div
          className="fixed inset-x-0 z-50 flex justify-center px-4"
          style={{ bottom: 'calc(1.5rem + env(safe-area-inset-bottom, 0px))' }}
        >
          <div className="rounded-xl bg-slate-900/90 px-4 py-2 text-center text-xs leading-relaxed text-white shadow-lg">
            {toast}
          </div>
        </div>
      )}
      <div className="mx-auto flex w-full max-w-md flex-1 flex-col md:max-w-2xl xl:max-w-3xl">
        {/* 顶部固定返回栏：首页本身就是根，不需要「返回首页/上一页/背单词」 */}
        {pathname !== '/' && <BackBar />}
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/vocab" element={<Vocabulary />} />
            <Route path="/vocab/grade/:gid" element={<WordList />} />
            <Route path="/vocab/grade/:gid/unit/:uid" element={<WordList />} />
            <Route path="/vocab/study/:id" element={<WordStudy />} />
            <Route path="/vocab/quiz" element={<Quiz />} />
            <Route path="/vocab/test" element={<Test />} />
            <Route path="/vocab/test/grade/:gid" element={<Test />} />
            <Route path="/vocab/test/grade/:gid/unit/:uid" element={<Test />} />
            <Route path="/vocab/review" element={<Review />} />
            <Route path="/vocab/mistakes" element={<Mistakes />} />
            <Route path="/vocab/hard" element={<Hard />} />
            <Route path="/listen" element={<Listen />} />
            <Route path="/listen/train/:id" element={<ReadingTrain />} />
            <Route path="/me" element={<Profile />} />
            <Route path="/login" element={<Login />} />
            <Route path="/teacher" element={<Teacher />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <ProgressProvider>
        <HashRouter>
          <StudyTimer />
          <Shell />
        </HashRouter>
      </ProgressProvider>
    </AuthProvider>
  );
}
