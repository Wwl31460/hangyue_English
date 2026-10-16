// UpdateDialog.tsx —— 「发现新版本」弹窗
// 由 App 根部统一渲染：启动时自动检查到新版、或用户在「我的」页手动检查到新版，都会弹这个。
import { useState } from 'react';
import {
  APP_VERSION,
  SITE_URL,
  assetForThisPlatform,
  openInBrowser,
  startUpdate,
  type RemoteVersion,
} from '../lib/update';

interface Props {
  remote: RemoteVersion;
  onClose: () => void;
}

type Phase = 'idle' | 'downloading' | 'installing' | 'failed';

export default function UpdateDialog({ remote, onClose }: Props) {
  const [phase, setPhase] = useState<Phase>('idle');
  const [percent, setPercent] = useState(-1);
  const [err, setErr] = useState('');

  const asset = assetForThisPlatform(remote);
  const notes = (remote.notes || '').split('\n').map((s) => s.trim()).filter(Boolean);

  const doUpdate = async () => {
    if (!asset) {
      setErr(`这个版本暂时没有提供当前设备的在线更新包，请打开下载页手动下载：${SITE_URL}`);
      setPhase('failed');
      return;
    }
    setErr('');
    setPhase('downloading');
    try {
      await startUpdate(asset, (p) => {
        setPercent(p.percent);
        setPhase(p.phase === 'installing' ? 'installing' : 'downloading');
      });
      // 安装界面已经拉起，剩下的交给系统
      setPhase('installing');
    } catch (e: any) {
      setErr(e?.message || '更新失败，请稍后重试');
      setPhase('failed');
    }
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-end justify-center bg-slate-900/40 px-4 pb-6 sm:items-center sm:pb-0">
      <div className="w-full max-w-sm rounded-3xl bg-white p-5 shadow-xl animate-fadeup">
        <div className="flex items-center gap-2">
          <span className="grid h-9 w-9 place-items-center rounded-2xl bg-gradient-to-br from-brand-600 to-brand-800 text-lg">
            🚀
          </span>
          <div>
            <h2 className="text-base font-extrabold text-brand-900">发现新版本 {remote.version}</h2>
            <p className="text-xs text-slate-500">
              当前 {APP_VERSION}
              {remote.publishedAt ? ` · ${remote.publishedAt} 发布` : ''}
            </p>
          </div>
        </div>

        {notes.length > 0 && (
          <ul className="mt-4 space-y-1.5 rounded-2xl bg-slate-50 px-3.5 py-3">
            {notes.map((n, i) => (
              <li key={i} className="flex gap-2 text-xs leading-5 text-slate-600">
                <span className="text-brand-500">·</span>
                <span className="flex-1">{n}</span>
              </li>
            ))}
          </ul>
        )}

        {phase === 'downloading' && (
          <div className="mt-4">
            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className={`h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-800 transition-all ${
                  percent < 0 ? 'w-1/3 animate-pulse' : ''
                }`}
                style={percent >= 0 ? { width: `${percent}%` } : undefined}
              />
            </div>
            <p className="mt-1.5 text-center text-[11px] text-slate-400">
              {percent >= 0 ? `正在下载安装包 ${percent}%` : '正在下载安装包…'}
            </p>
          </div>
        )}

        {phase === 'installing' && (
          <p className="mt-4 rounded-xl bg-emerald-50 px-3 py-2 text-center text-xs leading-5 text-emerald-700">
            下载完成，已拉起系统安装界面。
            <br />
            按提示点「安装」即可，装好后数据都在。
          </p>
        )}

        {phase === 'failed' && (
          <p className="mt-4 rounded-xl bg-rose-50 px-3 py-2 text-xs leading-5 text-rose-600">{err}</p>
        )}

        <div className="mt-5 flex gap-2">
          {phase === 'failed' && asset ? (
            <button
              onClick={() => openInBrowser(asset.url)}
              className="flex-1 rounded-xl bg-slate-100 py-2.5 text-sm font-medium text-slate-600"
            >
              用浏览器下载
            </button>
          ) : (
            phase !== 'installing' && (
              <button
                onClick={onClose}
                disabled={phase === 'downloading'}
                className="flex-1 rounded-xl bg-slate-100 py-2.5 text-sm font-medium text-slate-600 disabled:opacity-50"
              >
                稍后再说
              </button>
            )
          )}

          {phase === 'idle' && (
            <button onClick={doUpdate} className="btn-primary flex-1 !py-2.5 text-sm">
              立即更新
            </button>
          )}
          {phase === 'installing' && (
            <button onClick={onClose} className="btn-primary flex-1 !py-2.5 text-sm">
              知道了
            </button>
          )}
          {phase === 'failed' && (
            <button onClick={doUpdate} className="btn-primary flex-1 !py-2.5 text-sm">
              重试
            </button>
          )}
        </div>

        <p className="mt-3 text-center text-[10px] text-slate-300">
          更新不会影响本机已有的学习数据
        </p>
      </div>
    </div>
  );
}
