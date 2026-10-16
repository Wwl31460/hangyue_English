// 数据格式定义：单词与听读材料

// 单词
export interface Word {
  id: string;
  word: string;
  meaning: string; // 中文释义
  pos?: string; // 词性，如 n. / v. / adj. / adv.
  phonetic?: string; // 音标，可不填（留空时由 TTS 读音）
  image?: string; // 形象/滑稽 emoji 配图
  root?: string; // 词根，如 act
  affix?: string; // 词缀，如 -or / -er / -tion
  affixMeaning?: string; // 词缀含义，如 “表示人”（用于词缀网络按义分组）
  derive?: string; // 构词解析
  association?: string; // 联想记忆（仅小学/形象词使用，不强求）
  forms?: {
    // 词形变化：仅在单词自身详情页内介绍，不单独成词
    comparative?: string; // 比较级（形容词/副词）
    superlative?: string; // 最高级
    past?: string; // 过去式
    pastParticiple?: string; // 过去分词
  };
  phrases?: { en: string; zh: string }[]; // 词组（含中文），可不填
  examples?: { en: string; zh: string }[]; // 例句（含中文），可不填
  synonyms?: string[]; // 近义词（有才给，没有就不显示）
  antonyms?: string[]; // 反义词（有才给，没有就不显示）
  grade: string; // 所属年级阶段 id（见 grades.ts）
  unit?: number; // 所属单元（人教版每册分 Unit 1..N），导入官方词表时按 grade+unit 落位
  tags?: string[];
  emoji?: string; // 兼容字段（同 image）
}

// 听读等级：初级1-5 / 中级1-5 / 高级1-5
export type ListenLevel = string;

export interface Sentence {
  id: string;
  text: string;
  zh?: string; // 对应中文翻译，播放器在英文下方展示，便于理解语意
}

// 听读测试题：支持两种题型
// - choice：选择题（根据题意选答案）
// - cloze ：抠空选词填空（原文抠出若干空，从候选词中选词填入）
export type Question =
  | {
      id: string;
      type: 'choice';
      question: string;
      options: string[];
      answer: number; // 正确选项下标
    }
  | {
      id: string;
      type: 'cloze';
      sentence: string; // 含 “＿＿” 占位（一个 ＿＿ 表示一个空）
      blanks: ClozeBlank[]; // 按出现顺序对应每个 ＿＿
      prompt?: string; // 题干提示
    };

// 抠空选词：每个空的候选词与正确答案
export interface ClozeBlank {
  options: string[]; // 候选词（含正确词 + 干扰词）
  answer: number; // 正确词在 options 中的下标
}

// 一道题的计分单元数（选择题=1，抠空题=空的数量）
export function questionUnits(q: Question): number {
  return q.type === 'cloze' ? q.blanks.length : 1;
}

export interface Reading {
  id: string;
  level: ListenLevel;
  title: string;
  topic: string;
  duration: string; // 展示用时长，如 "1:10"
  audio: string; // 音频地址（原型用 TTS 实时合成，留空）
  story: string; // 约 1 分钟小故事全文（供通读）
  sentences: Sentence[]; // 分句，用于逐句听读练习
  questions: Question[];
  // 教材课文定位：有则表示“教材课文”，按 学段(小学/初中/高中) → 年级 → 学期 → Unit 组织
  textbook?: { grade: string; semester: '上' | '下'; unit: number; section?: '小学' | '初中' | '高中' };
}
