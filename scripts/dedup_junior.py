#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初中重建后去重：pep_junior.py 的 NEW 重新添加了小学段已存在的词，造成跨年级重复 id。

保留规则（兼顾数据质量与年级归属）：
  1) 对每个重复 id，统计各副本的「词根/词缀丰富度」= 含 root/affix/affixMeaning/derive/association 的字段数；
  2) 优先保留丰富度最高的副本（小学段之前已补过词族数据的副本通常更完整）；
  3) 丰富度并列时，保留年级序最靠前（最早学习）的副本；
  4) 删除其余副本。
"""
import re
from collections import defaultdict

PATH = 'src/data/words.ts'
lines = open(PATH, encoding='utf-8').read().split('\n')

# 年级学习顺序（越大越晚）
GRADE_ORDER = ['g3s1','g3s2','g4s1','g4s2','g5s1','g5s2','g6s1','g6s2',
               'c7s1','c7s2','c8s1','c8s2','c9s1','c9s2',
               'h1s1','h1s2','h2s1','h2s2','h3s1','h3s2']
GO = {g: i for i, g in enumerate(GRADE_ORDER)}

ENRICH = ['root:', 'affix:', 'affixMeaning:', 'derive:', 'association:']
entry_re = re.compile(r"^\s*\{\s*id:\s*'([^']+)'.*?grade:\s*'([^']+)'.*?\},\s*$")

entries = []  # (idx, id, grade, richness)
for i, ln in enumerate(lines):
    m = entry_re.match(ln)
    if m:
        rich = sum(1 for f in ENRICH if f in ln)
        entries.append((i, m.group(1), m.group(2), rich))

by_id = defaultdict(list)
for e in entries:
    by_id[e[1]].append(e)

delete = set()
kept_earliest = 0
for wid, lst in by_id.items():
    if len(lst) <= 1:
        continue
    # 按 (丰富度降序, 年级序升序) 选最优
    best = sorted(lst, key=lambda e: (-e[3], GO.get(e[2], 99)))[0]
    kept_earliest += 1
    for e in lst:
        if e[0] != best[0]:
            delete.add(e[0])

for i in sorted(delete, reverse=True):
    lines[i] = None
lines = [ln for ln in lines if ln is not None]
open(PATH, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'删除重复条目: {len(delete)} 行；涉及重复 id 组: {kept_earliest}')
