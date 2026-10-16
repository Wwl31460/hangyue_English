# -*- coding: utf-8 -*-
"""词库总审计：数量/重复/覆盖率/单元标题对齐（兼容单双引号）。"""
import re
from collections import Counter, defaultdict

src = open('src/data/words.ts', encoding='utf-8').read()
lines = src.split('\n')
entry_re = re.compile(r"^\s*\{\s*id:\s*[\"']([^\"']+)[\"']")
grade_re = re.compile(r"grade:\s*[\"']([^\"']+)[\"']")
unit_re = re.compile(r"unit:\s*(\d+)")
word_re = re.compile(r"word:\s*[\"']([^\"']+)[\"']")
ent_full = re.compile(r"^\s*\{\s*id:\s*[\"']([^\"']+)[\"'].*?\},\s*$")

ids, per, phr, exa, units = [], defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(set)
for ln in lines:
    if not entry_re.match(ln):
        continue
    sid = entry_re.match(ln).group(1)
    ids.append(sid)
    g = grade_re.search(ln).group(1)
    per[g] += 1
    units[g].add(int(unit_re.search(ln).group(1)))
    if 'phrases: [' in ln and 'phrases: []' not in ln:
        phr[g] += 1
    if 'examples: [' in ln and 'examples: []' not in ln:
        exa[g] += 1

order = ['g3s1', 'g3s2', 'g4s1', 'g4s2', 'g5s1', 'g5s2', 'g6s1', 'g6s2',
         'c7s1', 'c7s2', 'c8s1', 'c8s2', 'c9s1', 'c9s2',
         'h1s1', 'h1s2', 'h2s1', 'h2s2', 'h3s1', 'h3s2']
print('总词条:', len(ids), '| 唯一 id:', len(set(ids)))
print('重复 id:', [k for k, v in Counter(ids).items() if v > 1])
print()
print('%-6s %5s %6s %6s %s' % ('grade', '词数', '有短语', '有例句', '单元编号'))
for g in order:
    print('%-6s %5d %6d %6d %s' % (g, per[g], phr[g], exa[g], sorted(units[g])))
print()
print('合计:', sum(per.values()), '有短语:', sum(phr.values()), '有例句:', sum(exa.values()))

def has(ln, field):
    return re.search(r'(?<![A-Za-z])%s:' % field, ln) is not None


cov = Counter()
for ln in lines:
    if not entry_re.match(ln):
        continue
    for f in ('root', 'affix', 'derive', 'association', 'synonyms', 'antonyms', 'forms'):
        if has(ln, f):
            cov[f] += 1

print()
print('字段覆盖率：')
n = len(ids)
for f in ('association', 'root', 'affix', 'derive', 'synonyms', 'antonyms', 'forms'):
    print('  %-12s %5d  (%2.0f%%)' % (f, cov[f], 100.0 * cov[f] / n))

# 词根词缀网络（families.ts）
fam = open('src/data/families.ts', encoding='utf-8').read()
seg_root = fam.split('export const rootFamily')[1].split('export const affixMeaning')[0]
seg_affix = fam.split('export const affixFamily')[1].split('export const wordAffixes')[0]
n_root = len(re.findall(r'^  "[^"]+": \[', seg_root, re.M))
n_affix = len(re.findall(r'^  "[^"]+": \[', seg_affix, re.M))
n_ext = len(re.findall(r"grade: ''", fam))
print()
print('词根家族 %d 组 | 词缀家族 %d 组 | 拓展词 %d 个' % (n_root, n_affix, n_ext))

# 单元标题对齐
title_src = open('src/data/grades.ts', encoding='utf-8').read()
print()
print('unitTitles 覆盖检查：')
for g in order:
    m = re.search(re.escape(g) + r":\s*\{(.*?)\n  \},", title_src, re.S)
    if not m:
        print('  %s 无标题定义' % g)
        continue
    keys = set(int(x) for x in re.findall(r'(\d+):', m.group(1)))
    lack = units[g] - keys
    if lack:
        print('  %s 词表单元 %s 缺标题' % (g, sorted(lack)))
print('（无输出 = 全部对齐）')
