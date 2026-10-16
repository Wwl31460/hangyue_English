#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 20 年级顺序重建 src/data/words.ts。

- 每个 level 的主数据文件导出 DATA = { grade: [word_dict, ...] }；
  data_primary.py / data_junior.py / data_high.py 存在即参与重建，缺失的年级保留原文件内容。
- 所有字符串用 json.dumps 转义（en 例句里的撇号不会破坏 TS）。
- 年级内顺序 = 主数据顺序；单元内按录入顺序排列。
"""
import json
import re
import sys

sys.path.insert(0, 'scripts')

from gen_families import (load_corpus, detect_root, detect_affixes,
                          make_association)
from data_relations import ANT_PAIRS, SYN_GROUPS

ORDER = ['g3s1','g3s2','g4s1','g4s2','g5s1','g5s2','g6s1','g6s2',
         'c7s1','c7s2','c8s1','c8s2','c9s1','c9s2',
         'h1s1','h1s2','h2s1','h2s2','h3s1','h3s2']

MASTER = {}
for mod in ['data_primary', 'data_junior', 'data_high']:
    try:
        m = __import__(mod)
        MASTER.update(m.DATA)
        print(f'载入 {mod}: {len(m.DATA)} 个年级')
    except Exception as e:  # 尚未提供该 level 的主数据
        print(f'（跳过 {mod}：{e}）')

# ---- 并入 expand_words.NEW 的补充词（词根词缀家族词 + 主题词，用于补足词量）----
# 主数据里已有的词形不再重复；新词挂到该册最后一个单元。
try:
    from expand_words import NEW as EXTRA
except Exception as e:
    EXTRA = []
    print(f'（跳过 expand_words：{e}）')

_have = {w['word'].lower() for g in MASTER for w in MASTER[g]}
_added = 0
try:
    from gen_phrases import gen_phrases as _genphr
except Exception:
    _genphr = None
for x in EXTRA:
    g = x['grade']
    k = x['word'].lower()
    if g not in MASTER or k in _have:
        continue
    _have.add(k)
    _added += 1
    phr = [tuple(p) for p in (x['ph'] or [])]
    exa = [tuple(p) for p in (x['ex'] or [])]
    if _genphr and (not phr or not exa):      # 缺短语/例句的用生成器补上
        p2, e2 = _genphr(x['word'], x['zh'], x['pos'])
        phr = phr or p2
        exa = exa or e2
    d = {'id': re.sub(r'[^a-z0-9]', '_', k), 'word': x['word'], 'meaning': x['zh'],
         'pos': x['pos'], 'phonetic': x['phonetic'], 'image': x['img'],
         'unit': max((w['unit'] for w in MASTER[g]), default=1),
         'phrases': phr, 'examples': exa}
    for src, dst in [('root', 'root'), ('affix', 'affix'), ('am', 'affixMeaning'),
                     ('derive', 'derive'), ('assoc', 'association'), ('forms', 'forms'),
                     ('tags', 'tags')]:
        if x.get(src):
            d[dst] = x[src]
    MASTER[g].append(d)
print(f'并入 expand_words 补充词: {_added} 个')

CORPUS = load_corpus()

# ---- 近义词 / 反义词索引（按小写词形） ----
SYN = {}
for grp in SYN_GROUPS:
    for x in grp:
        SYN.setdefault(x.lower(), [])
        for y in grp:
            if y.lower() != x.lower() and y not in SYN[x.lower()]:
                SYN[x.lower()].append(y)
ANT = {}
for a, b in ANT_PAIRS:
    ANT.setdefault(a.lower(), [])
    ANT.setdefault(b.lower(), [])
    if b not in ANT[a.lower()]:
        ANT[a.lower()].append(b)
    if a not in ANT[b.lower()]:
        ANT[b.lower()].append(a)

PATH = 'src/data/words.ts'
text = open(PATH, encoding='utf-8').read()
# 精确定位 `const raw: Word[] = [` 里数组真正的起始方括号（避免误取 Word[] 的括号）
m = re.search(r'const raw\s*:\s*Word\[\]\s*=\s*\[', text)
arr_start = m.end() - 1
close = text.rindex('];')
header = text[:arr_start + 1]
body = text[arr_start + 1:close]

# 头部补上 families 的 import（词根词缀拓展词）
if "from './families'" not in header:
    header = header.replace(
        "import { Word } from '../types';",
        "import { Word } from '../types';\nimport { familyWords } from './families';", 1)

entry_re = re.compile(r"^\s*\{\s*id:\s*[\"']([^\"']+)[\"'].*?grade:\s*[\"']([^\"']+)[\"'].*?\},\s*$")
existing = {}
for ln in body.split('\n'):
    m = entry_re.match(ln)
    if m:
        existing.setdefault(m.group(2), []).append(ln.rstrip())


def j(s):
    return json.dumps(s, ensure_ascii=False)


def jarr(pairs):
    return '[' + ', '.join('{ en: ' + j(a) + ', zh: ' + j(b) + ' }' for a, b in pairs) + ']'


def jstrlist(items):
    return '[' + ', '.join(j(x) for x in items) + ']'


def enrich(w):
    """补齐词根 / 词缀 / 联想记忆 / 近义反义（已有的不覆盖）。"""
    w = dict(w)
    key = w['word'].lower().strip()
    affixes = detect_affixes(key, CORPUS)
    if not w.get('root'):
        r = detect_root(key, CORPUS)
        if r:
            w['root'] = r
    if not w.get('affix') and affixes:
        w['affix'] = affixes[0]
        from data_affixes import AFFIXES
        w['affixMeaning'] = AFFIXES[affixes[0]][0]
    if not w.get('association'):
        w['association'] = make_association(
            w['word'], w['meaning'], w.get('pos', ''), w.get('root'), affixes, CORPUS)
    if not w.get('synonyms') and key in SYN:
        w['synonyms'] = SYN[key][:4]
    if not w.get('antonyms') and key in ANT:
        w['antonyms'] = ANT[key][:3]
    return w


def emit(g, w):
    p = [f"id: {j(w['id'])}", f"word: {j(w['word'])}", f"meaning: {j(w['meaning'])}"]
    if w.get('pos'): p.append(f"pos: {j(w['pos'])}")
    if w.get('phonetic'): p.append(f"phonetic: {j(w['phonetic'])}")
    if w.get('image'): p.append(f"image: {j(w['image'])}")
    p.append(f"grade: {j(g)}")
    p.append(f"unit: {w['unit']}")
    if w.get('root'): p.append(f"root: {j(w['root'])}")
    if w.get('affix'): p.append(f"affix: {j(w['affix'])}")
    if w.get('affixMeaning'): p.append(f"affixMeaning: {j(w['affixMeaning'])}")
    if w.get('derive'): p.append(f"derive: {j(w['derive'])}")
    if w.get('association'): p.append(f"association: {j(w['association'])}")
    if w.get('phrases'): p.append('phrases: ' + jarr(w['phrases']))
    if w.get('examples'): p.append('examples: ' + jarr(w['examples']))
    if w.get('synonyms'): p.append('synonyms: ' + jstrlist(w['synonyms']))
    if w.get('antonyms'): p.append('antonyms: ' + jstrlist(w['antonyms']))
    if w.get('forms'):
        p.append('forms: { ' + ', '.join(f"{k}: {j(v)}" for k, v in w['forms'].items()) + ' }')
    if w.get('tags'): p.append('tags: [' + ', '.join(j(t) for t in w['tags']) + ']')
    return '  { ' + ', '.join(p) + ' },'


out = [header]
used_ids = set()


def norm_key(s):
    """归一化词形：小写、连字符/下划线统一为空格，用于跨册重复识别。"""
    return re.sub(r'[-_]', ' ', s.lower()).strip()


for g in ORDER:
    out.append(f"  // ===================== {g} =====================")
    if g in MASTER:
        for w0 in MASTER[g]:
            w = w0
            # 同一词在不同课本再次出现时保留，但 id 需全局唯一 → 追加学年后缀
            if w['id'] in used_ids:
                base = w['id']
                w = dict(w)
                w['id'] = f'{base}_{g}'
                n = 2
                while w['id'] in used_ids:
                    w['id'] = f'{base}_{g}{n}'
                    n += 1
            used_ids.add(w['id'])
            out.append(emit(g, enrich(w)))
    else:
        out.extend(existing.get(g, []))

# 尾部：导出主词表 + 网络词表 + 两套索引
out.append('];')
out.append('')
out.append('export const words: Word[] = raw;')
out.append('')
out.append('// 词根词缀网络用词表 = 课本词 + 拓展词（拓展词只用于网络扩展，不进入单元列表、不参与测试）')
out.append('export const networkWords: Word[] = [...words, ...familyWords];')
out.append('')
out.append('export const wordById: Record<string, Word> = Object.fromEntries(networkWords.map((w) => [w.id, w]));')
out.append('export const wordByText: Record<string, Word> = Object.fromEntries(networkWords.map((w) => [w.word.toLowerCase(), w]));')
out.append('')

open(PATH, 'w', encoding='utf-8').write('\n'.join(out))
print('重建完成。主数据覆盖年级:', [g for g in ORDER if g in MASTER])
print('写入词条总数:', len(used_ids), '| 唯一 id:', len(set(used_ids)))
