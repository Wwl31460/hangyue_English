#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""高中 6 册真实人教版单元合并式生成器。

步骤：
  1) 删掉 words.ts 中旧的「词族假单元」h* 条目（含 France2 等编号副本）；
  2) 追加 pep_high.py 的 611 条真实单元词（若 id 已在小学/初中库则跳过，避免跨年级重复）；
  3) 回收旧 h* 段里「真实但未被新集覆盖」的词（按原 grade+unit 放回，unit 号对应真实单元标题），
     编号副本（id 以数字结尾）丢弃，避免产生新的重复 id。
"""
import re, sys
sys.path.insert(0, 'scripts')
from pep_high import HIGH

PATH = 'src/data/words.ts'
lines = open(PATH, encoding='utf-8').read().split('\n')

entry_re = re.compile(r"^\s*\{\s*id:\s*'([^']+)'.*?grade:\s*'([^']+)'.*?\},\s*$")
HS = set(HIGH.keys())

# 1) 收集并删除旧 h* 条目
old_h = {}          # id -> 原始行
keep = []
for ln in lines:
    m = entry_re.match(ln)
    if m and m.group(2) in HS:
        old_h[m.group(1)] = ln
        continue
    keep.append(ln)

# 当前剩余 id（小学/初中）
cur_ids = set()
for ln in keep:
    m = entry_re.match(ln)
    if m:
        cur_ids.add(m.group(1))

# 2) 生成新条目
def build_new(gid, t):
    id, word, meaning, pos, ph, img, unit, tags, root, affix, am, derive, assoc = t
    tags_s = '[' + ', '.join(f"'{x}'" for x in tags) + ']'
    fam = ''
    if root: fam += f", root: '{root}'"
    if affix: fam += f", affix: '{affix}'"
    if am: fam += f", affixMeaning: '{am}'"
    if derive: fam += f", derive: '{derive}'"
    assoc_s = f", association: '{assoc}'" if assoc else ''
    return (f"  {{ id: '{id}', word: '{word}', meaning: '{meaning}', pos: '{pos}', "
            f"phonetic: '{ph}', image: '{img}', grade: '{gid}', unit: {unit}, tags: {tags_s}{fam}{assoc_s} }},")

new_block = []
pep_ids = set()
added_from_pep = 0
skipped_pep = 0
for gid, spec in HIGH.items():
    for t in spec['NEW']:
        pep_ids.add(t[0])
        if t[0] in cur_ids:
            skipped_pep += 1
            continue
        new_block.append(build_new(gid, t))
        added_from_pep += 1

# 3) 回收旧 h* 中未被新集覆盖的真实词（跳过编号副本）
recovered = 0
for wid, ln in old_h.items():
    if wid in pep_ids or wid in cur_ids:
        continue
    if re.search(r"\d$", wid):   # 编号副本，丢弃
        continue
    new_block.append(ln.rstrip())
    recovered += 1

# 插入到 raw 数组的结束 `];` 之前
marker = "  // ===================== 高中（人教版 必修/选必）真实单元 ====================="
out = []
inserted = False
for ln in keep:
    if not inserted and ln.strip() == '];':
        out.append(marker)
        out.extend(new_block)
        inserted = True
    out.append(ln)
if not inserted:   # 兜底：直接追加
    out.extend(new_block)

open(PATH, 'w', encoding='utf-8').write('\n'.join(out))
print(f'旧 h* 条目: {len(old_h)}（已删）')
print(f'新增真实单元词: {added_from_pep}（跳过已在小学/初中: {skipped_pep}）')
print(f'回收旧段真实词: {recovered}')
print(f'本脚本共写入: {len(new_block)} 行')
