#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 g6s1 段的两类问题：
1) build_g6s1.py 把 grade 写成了未引号的变量 `grade: g6s1`（TS 无法编译），
   统一补成 `grade: 'g6s1'`。
2) 删除被 expand_words.py 误标成 g6s1、且落在 g6s2 区域、低质（空音标/空例句）
   的 17 条填充词（camera/gift/key/clock/money/high/low/fast/easy/hard/
   loud/love/like/hate/want/need/find）。
"""
PATH = 'src/data/words.ts'
src = open(PATH, encoding='utf-8').read()
lines = src.split('\n')

out = []
removed = 0
for ln in lines:
    # 删除误放且低质的 g6s1 遗留条目：带引号 g6s1 且为空例句填充词
    if "grade: 'g6s1'" in ln and 'phrases: []' in ln:
        removed += 1
        continue
    out.append(ln)

src2 = '\n'.join(out)
# 仅把 g6s1 段内的未引号 grade 补成引号（其它年级本就带引号，不受影响）
src2 = src2.replace('grade: g6s1,', "grade: 'g6s1',")

open(PATH, 'w', encoding='utf-8').write(src2)
print(f'已删除误放低质条目: {removed}')
print("已将 g6s1 段 grade 补成引号。")
