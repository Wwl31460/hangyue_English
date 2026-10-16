import { NavLink } from 'react-router-dom';

const items = [
  { to: '/', label: '首页', icon: '🏠' },
  { to: '/vocab', label: '背单词', icon: '📚' },
  { to: '/listen', label: '听读训练', icon: '🎧' },
  { to: '/me', label: '我的', icon: '⭐' },
];

export default function BottomNav() {
  return (
    <nav className="sticky bottom-0 z-20 grid grid-cols-4 border-t border-slate-200 bg-white/95 backdrop-blur">
      {items.map((it) => (
        <NavLink
          key={it.to}
          to={it.to}
          end={it.to === '/'}
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 py-2.5 text-xs ${
              isActive ? 'font-semibold text-brand-700' : 'text-slate-400'
            }`
          }
        >
          <span className="text-xl">{it.icon}</span>
          {it.label}
        </NavLink>
      ))}
    </nav>
  );
}
