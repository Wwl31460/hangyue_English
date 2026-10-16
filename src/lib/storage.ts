// 本地存储封装：所有学习数据存在浏览器 localStorage
const PREFIX = 'k12en:';

export function load<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(PREFIX + key);
    if (!raw) return fallback;
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

export function save<T>(key: string, val: T): void {
  try {
    localStorage.setItem(PREFIX + key, JSON.stringify(val));
  } catch {
    // 忽略写入失败（如隐私模式）
  }
}
