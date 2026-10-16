#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并式重建初中 6 册：把 pep_junior.JUNIOR 应用到 src/data/words.ts。
- UNIT_FIX：修正已有词族词的 unit（按真实单元）
- NEW：在段末追加真实核心四会词（带音标），保留已有词的音标/联想
"""
import re, sys
sys.path.insert(0, 'scripts')
from pep_junior import JUNIOR

PATH = 'src/data/words.ts'
lines = open(PATH, encoding='utf-8').read().split('\n')

marker_re = re.compile(r'^\s*//\s*=+\s*(.+?)\s*\((\w+)\)')
marker_idx = {}
for i, ln in enumerate(lines):
    m = marker_re.match(ln)
    if m:
        marker_idx[m.group(2)] = i

def build_new(gid, t):
    id, word, meaning, pos, ph, img, unit, tags, root, affix, am, derive, assoc = t
    tags_s = '[' + ', '.join(f"'{x}'" for x in tags) + ']'
    fam = ''
    if root: fam += f", root: '{root}'"
    if affix: fam += f", affix: '{affix}'"
    if am: fam += f", affixMeaning: '{am}'"
    if derive: fam += f", derive: '{derive}'"
    assoc_s = f", association: '{assoc}'" if assoc else ''
    return f"  {{ id: '{id}', word: '{word}', meaning: '{meaning}', pos: '{pos}', phonetic: '{ph}', image: '{img}', grade: '{gid}', unit: {unit}, tags: {tags_s}{fam}{assoc_s} }},"

for gid, spec in JUNIOR.items():
    assert gid in marker_idx, f"找不到段标记: {gid}"
    start = marker_idx[gid]
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if marker_re.match(lines[j]):
            end = j
            break
    section = lines[start:end]

    # UNIT_FIX
    for wid, u in spec.get('UNIT_FIX', {}).items():
        for k in range(len(section)):
            if re.search(r"id:\s*'" + re.escape(wid) + r"'", section[k]):
                section[k] = re.sub(r"unit:\s*\d+", f"unit: {u}", section[k])
                break

    # NEW：段末追加
    new_lines = [build_new(gid, t) for t in spec.get('NEW', [])]
    section = section + new_lines

    lines[start:end] = section

open(PATH, 'w', encoding='utf-8').write('\n'.join(lines))
print('已重建', len(JUNIOR), '个初中段：', ', '.join(JUNIOR.keys()))
