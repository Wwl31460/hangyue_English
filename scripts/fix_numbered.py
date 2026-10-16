#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理旧数据中「跨年级重复导致的编号副本」(France2/easy2/teacher2...)。

规则：
  - id 以数字结尾（如 teacher2）且存在干净 base（teacher）→ 删编号副本，保留 base；
  - 若编号副本的词根/词缀更丰富，则把编号副本改名成 base，并删除原 base；
  - base 不存在 → 把编号副本的 id 改名为 base（word 字段本就是干净词）。
"""
import re
from collections import defaultdict

PATH = 'src/data/words.ts'
lines = open(PATH, encoding='utf-8').read().split('\n')
entry_re = re.compile(r"^\s*\{\s*id:\s*'([^']+)'.*?grade:\s*'([^']+)'.*?\},\s*$")
ENRICH = ['root:', 'affix:', 'affixMeaning:', 'derive:', 'association:']

# 收集所有条目
entries = []  # (idx, id, grade, richness, line)
for i, ln in enumerate(lines):
    m = entry_re.match(ln)
    if m:
        rich = sum(1 for f in ENRICH if f in ln)
        entries.append((i, m.group(1), m.group(2), rich, ln))

by_id = defaultdict(list)
for e in entries:
    by_id[e[1]].append(e)

delete = set()
rename = {}  # idx -> new_id
for e in entries:
    i, wid, grade, rich, ln = e
    if not re.search(r'\d$', wid):
        continue
    base = re.sub(r'\d+$', '', wid)
    if base == wid:
        continue
    if base in by_id:
        # base 存在：比较丰富度
        base_e = by_id[base][0]
        if rich > base_e[3]:
            rename[i] = base          # 编号副本更丰富 → 改名成 base
            delete.add(base_e[0])     # 删除原 base
        else:
            delete.add(i)             # 删编号副本
    else:
        rename[i] = base              # 无 base → 改名

out = []
for i, ln in enumerate(lines):
    if i in delete:
        continue
    if i in rename:
        new_id = rename[i]
        ln = re.sub(r"id:\s*'" + re.escape(ln.split("id: '")[1].split("'")[0]) + r"'",
                    "id: '" + new_id + "'", ln, count=1)
    out.append(ln)

open(PATH, 'w', encoding='utf-8').write('\n'.join(out))
print(f'删除编号副本: {len(delete)}；改名编号副本: {len(rename)}')
