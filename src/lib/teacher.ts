// 老师后台的数据接口
//
// 这四件事都必须在服务端校验老师口令，前端不保存口令本身：
//   hy_teacher_students        所有学生 + 学习摘要（学了几个词、几天、最近哪天）
//   hy_teacher_student_detail  某个学生的完整进度（用来展示每日明细）
//   hy_teacher_set_scope       设置这个学生能看哪些年级
//   hy_teacher_clear_progress  清除这个学生的学习数据
//
// 为什么不能直接读数据库：四张表都锁了 RLS 且不给任何授权，只能走这几个函数。
import { callRpc } from './rpc';

export interface StudentRow {
  username: string;
  displayName: string;
  role: string;
  createdAt: string;
  scope: string[] | null; // null = 全部内容开放
  learned: number; // 已学单词数
  mistakes: number; // 错词本里还有几个
  readings: number; // 完成的听读篇数
  words: number; // 历史累计学过的词次
  minutes: number; // 累计学习分钟
  days: number; // 有学习记录的天数
  lastDay: string | null; // 最近一次学习的日期 YYYY-MM-DD
  todayWords: number; // 今天学了多少词
  linked: boolean; // 云端是否已有进度记录
}

export interface StudentDetail {
  username: string;
  displayName: string;
  scope: string[] | null;
  progress: any; // 原始 ProgressData（可能是空对象）
}

// 所有函数都返回 { ok, ... }，失败把服务端给的中文原因抛出去
function unwrap(r: any, fallback: string): any {
  if (!r?.ok) throw new Error(r?.error || fallback);
  return r;
}

export async function fetchStudents(pin: string): Promise<StudentRow[]> {
  const r = unwrap(await callRpc('hy_teacher_students', { p_pin: pin }), '读取学生列表失败');
  return Array.isArray(r.students) ? (r.students as StudentRow[]) : [];
}

export async function fetchStudentDetail(pin: string, username: string): Promise<StudentDetail> {
  const r = unwrap(
    await callRpc('hy_teacher_student_detail', { p_pin: pin, p_username: username }),
    '读取学习明细失败',
  );
  return r.student as StudentDetail;
}

// scope 传 null 表示恢复全部开放
export async function setStudentScope(
  pin: string,
  username: string,
  scope: string[] | null,
): Promise<void> {
  unwrap(
    await callRpc('hy_teacher_set_scope', { p_pin: pin, p_username: username, p_scope: scope }),
    '设置内容范围失败',
  );
}

export async function clearStudentProgress(pin: string, username: string): Promise<void> {
  unwrap(
    await callRpc('hy_teacher_clear_progress', { p_pin: pin, p_username: username }),
    '清除学习数据失败',
  );
}
