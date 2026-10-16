#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 words.ts 中每个单词按年级切分单元：每 8 个词为一个 Unit。
例如某年级 49 个词 -> Unit 1..7。模拟人教版“每册分若干单元”的结构，
便于后续导入官方词表时按 grade + unit 落位。
幂等：若 grade 后已带 unit: 则跳过，避免重复插入。
"""
import re

PATH = 'src/data/words.ts'

def main():
    with open(PATH, encoding='utf-8') as f:
        src = f.read()

    # 按文件顺序统计每个年级已出现的次数，计算所属单元
    counts: dict[str, int] = {}
    CHUNK = 8

    def repl(m: re.Match) -> str:
        gid = m.group(1)
        # 已存在 unit 则原样返回，保证幂等
        if m.group(0).rstrip().endswith('unit:'):
            return m.group(0)
        counts[gid] = counts.get(gid, 0) + 1
        idx = counts[gid] - 1
        unit = idx // CHUNK + 1
        return f"grade: '{gid}', unit: {unit}"

    # 仅匹配尚未带 unit 的 grade: 'xxx'
    pat = re.compile(r"grade: '([a-z0-9]+)'(?!\s*,\s*unit:)")
    new = pat.sub(repl, src)

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(new)

    print('已分配单元，各年级词数：')
    for gid, n in counts.items():
        print(f'  {gid}: {n} 词 -> Unit 1..{ (n+CHUNK-1)//CHUNK }')

if __name__ == '__main__':
    main()
