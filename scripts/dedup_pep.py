#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去重：build_pep.py 后，部分词因旧数据已存在而产生重复 id。
保留「应属年级」(PEP 主数据 NEW/UNIT_FIX 指定的年级) 的副本，删除其余（错年级/错单元的旧副本）。
"""
import re, sys
sys.path.insert(0, 'scripts')
from pep_primary import PEP

PATH = 'src/data/words.ts'
lines = open(PATH, encoding='utf-8').read().split('\n')

# 应属年级映射
intended = {}
for gid, spec in PEP.items():
    for t in spec.get('NEW', []):
        intended[t[0]] = gid
    for wid, u in spec.get('UNIT_FIX', {}).items():
        intended.setdefault(wid, gid)

entry_re = re.compile(r"^\s*\{\s*id:\s*'([^']+)'.*?grade:\s*'([^']+)'.*?\},\s*$")
entries = []  # (idx, id, grade)
for i, ln in enumerate(lines):
    m = entry_re.match(ln)
    if m:
        entries.append((i, m.group(1), m.group(2)))

from collections import defaultdict
by_id = defaultdict(list)
for e in entries:
    by_id[e[1]].append(e)

delete = set()
for wid, lst in by_id.items():
    if len(lst) <= 1:
        continue
    want = intended.get(wid)
    keep = [e for e in lst if e[2] == want] if want else []
    if not keep:
        keep = [lst[-1]]  # 兜底：保留最后一个
    # keep 内取最后一个（NEW 追加在后）
    keep_idx = keep[-1][0]
    for e in lst:
        if e[0] != keep_idx:
            delete.add(e[0])

for i in sorted(delete, reverse=True):
    lines[i] = None
lines = [ln for ln in lines if ln is not None]
open(PATH, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'删除重复条目: {len(delete)}；保留应属年级命中: {sum(1 for v in by_id.values() if len(v)>1)} 组')
