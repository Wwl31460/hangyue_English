#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合并式重建：把 pep_primary.PEP 应用到 src/data/words.ts。
- UNIT_FIX：修正已有词的 unit（按真实单元）
- FAMILY：给已有词补 root/affix/affixMeaning/derive（先清旧再插）
- NEW：在段末（下一 marker 前）追加缺失四会词（含音标）
保留 words.ts 中已有词条的音标/联想/例句。g6s1 不在 PEP 中，保持 build_g6s1.py 的结果。
"""
import re, sys
sys.path.insert(0, 'scripts')
from pep_primary import PEP

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
    return f"  {{ id: '{id}', word: '{word}', meaning: '{meaning}', pos: '{pos}', phonetic: '{ph}', image: '{img}', grade: '{gid}', unit: {unit}, tags: {tags_s}{fam} }},"

for gid, spec in PEP.items():
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

    # FAMILY
    for wid, fam in spec.get('FAMILY', {}).items():
        for k in range(len(section)):
            if re.search(r"id:\s*'" + re.escape(wid) + r"'", section[k]):
                ln = section[k]
                ln = re.sub(r",?\s*root:\s*'[^']*'", '', ln)
                ln = re.sub(r",?\s*affix:\s*'[^']*'", '', ln)
                ln = re.sub(r",?\s*affixMeaning:\s*'[^']*'", '', ln)
                ln = re.sub(r",?\s*derive:\s*'[^']*'", '', ln)
                fam_s = ''
                if fam.get('root'): fam_s += f", root: '{fam['root']}'"
                if fam.get('affix'): fam_s += f", affix: '{fam['affix']}'"
                if fam.get('affixMeaning'): fam_s += f", affixMeaning: '{fam['affixMeaning']}'"
                if fam.get('derive'): fam_s += f", derive: '{fam['derive']}'"
                ln = ln.replace(' tags:', fam_s + ' tags:')
                section[k] = ln
                break

    # NEW：段末追加（下一 marker 之前）
    new_lines = [build_new(gid, t) for t in spec.get('NEW', [])]
    section = section + new_lines

    lines[start:end] = section

open(PATH, 'w', encoding='utf-8').write('\n'.join(lines))
print('已重建', len(PEP), '个小学段：', ', '.join(PEP.keys()))
