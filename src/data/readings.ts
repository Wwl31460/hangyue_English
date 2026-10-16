import { Reading } from '../types';
import { textbookReadings } from './readings_textbook';

// 听读材料 = 人教版教材课文：小学三年级 ~ 高中三年级，全部册次、全部单元（共 135 篇）。
// 由 scripts/gen_textbook_readings.py 读取 grades.ts 的 unitTitles 生成，
// 每篇含 sentences（英文 + 中文对照，用于逐句听读）、questions（理解小测）。
//
// 音频由浏览器 SpeechSynthesis 实时合成（audio 留空）。
// 说明：句子为该单元主题/词汇的「代表性练习摘录」，非教材逐字原文。
export const readings: Reading[] = textbookReadings;
