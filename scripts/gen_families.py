# -*- coding: utf-8 -*-
"""词根词缀网络生成器。

产出 src/data/families.ts：
  - rootMeaning / rootFamily：词根 -> 含义 + 常见同根词（顺序 = 展示优先级）
  - affixMeaning / affixFamily：词缀 -> 含义 + 常见同缀词
  - wordAffixes：每个词条命中的词缀（可同时命中前缀与后缀，如 reporter = re- + -er）
  - familyWords：词根词缀拓展词（只用于网络扩展，不进入单元词表）

同时向上游提供三个函数供 rebuild_all 使用：
  detect_root / detect_affixes / make_association
"""
import json
import re
import sys

sys.path.insert(0, 'scripts')

from data_roots import ROOTS
from data_wordroots import WORDBASES
from data_affixes import AFFIXES, NOT_DERIVED, KNOWN_STEMS
from gen_phrases import gen_phrases


# 由后缀推断词性：给「没有 pos 字段」的拓展词生成例句时用
_POS_SUFFIXES = [
    ('ly', 'adv'),
    ('ness', 'n'), ('ment', 'n'), ('tion', 'n'), ('sion', 'n'), ('ity', 'n'),
    ('ship', 'n'), ('hood', 'n'), ('dom', 'n'), ('ist', 'n'), ('ism', 'n'),
    ('ance', 'n'), ('ence', 'n'), ('age', 'n'), ('er', 'n'), ('or', 'n'),
    ('ful', 'adj'), ('less', 'adj'), ('able', 'adj'), ('ible', 'adj'), ('ous', 'adj'),
    ('ive', 'adj'), ('al', 'adj'), ('ish', 'adj'), ('ic', 'adj'),
    ('proof', 'adj'), ('like', 'adj'), ('some', 'adj'), ('ward', 'adv'), ('wise', 'adv'),
    ('ize', 'v'), ('ise', 'v'), ('ify', 'v'), ('en', 'v'),
    ('y', 'adj'),
]


def infer_pos(word, meaning=''):
    """靠后缀推断词性；后缀猜不出时再用中文释义兜底（…地→副词，…的→形容词）。

    拓展词家族数据里没有 pos 字段，而缺了词性，例句生成器只能产出
    "Helpful is very important." 这种废话 —— 所以这里必须先补一步。
    """
    w = word.lower()
    for suf, pos in _POS_SUFFIXES:
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return pos
    if meaning.endswith('地'):
        return 'adv'
    if '的' in meaning:
        return 'adj'
    if meaning.startswith('使'):        # 使细化 / 使升级… 都是动词
        return 'v'
    return 'n'

# 词根 = 拉丁/希腊词根 + 英语本族单词词根（help → helpful / helpless 这类）
# 同名 key 以 data_roots.py 为准；先填 ROOTS 也保证了精选家族在匹配时优先命中。
# 注意：本族词根只通过「家族名单」精确匹配，不参与 detect_root 的子串猜测，
# 否则会闹出 early = ear + -ly 这类笑话。
# 按「越短越基础」排序后插入：这样 beautiful 会归到 beauty 家族（而不是自己再开一族），
# 学习者看到的是最完整、最基础的那一组同根词。
ALL_ROOTS = dict(ROOTS)
for _wb in sorted(WORDBASES, key=lambda k: (len(k), k)):
    if _wb not in ALL_ROOTS:
        ALL_ROOTS[_wb] = WORDBASES[_wb]

# 词根自动识别时容易踩到的“巧合包含”（如 sport 含 port、greatest 含 test）
NOT_ROOT = {
    'sport', 'sports', 'greatest', 'latest', 'fastest', 'hottest', 'shortest', 'longest',
    'newest', 'oldest', 'youngest', 'biggest', 'smallest', 'tallest', 'highest', 'lowest',
    'easiest', 'heaviest', 'happiest', 'seventeen', 'seventy', 'seventh', 'attempt',
    'temple', 'tempt', 'compass', 'accident', 'accidental', 'incident', 'resident',
    'president', 'confident', 'student', 'prudent',
    # 子串巧合
    'britain', 'mountain', 'electric', 'electrical', 'electricity', 'electronic',
    'electronics', 'integrate', 'passive', 'sister', 'stepsister', 'former',
    'independent', 'independence', 'overseas', 'proper', 'terrorist', 'terror',
    'terrible', 'terrify', 'terrific', 'pencil', 'restaurant', 'curtain',
    # 含该词根但语义无关（孩子记住会更糊涂）
    'apart', 'concert', 'terrace', 'medical', 'problem', 'trader',
    'performance', 'performer', 'monument', 'element', 'commentary', 'complement',
    'apartment', 'dimension', 'immense',
}

# 词缀含义的「短说明」，用于联想记忆拆词
SHORT_FALLBACK = re.compile(r'^(名词后缀，?|形容词后缀，?|动词后缀，?|副词后缀，?|后缀，?|序数词后缀，?|形容词/名词后缀，?|表示)')


def _short(meaning):
    return SHORT_FALLBACK.sub('', meaning).strip() or meaning


def load_corpus():
    """载入课本词库：小写词形 -> {meaning, image, pos}。

    除了三份主数据，**还必须并上 expand_words 的补充词** ——
    它们是 rebuild_all 真正写进 words.ts 的词，之前漏掉会让
    actor / dormitory 这类词永远无法充当词根或复合词尾，白白丢掉一大批扩展。
    """
    from data_primary import DATA as P
    from data_junior import DATA as J
    from data_high import DATA as H
    corpus = {}
    for SRC in (P, J, H):
        for g, lst in SRC.items():
            for w in lst:
                key = w['word'].lower().strip()
                if key not in corpus:
                    corpus[key] = {'meaning': w['meaning'], 'image': w.get('image', '🔤'),
                                   'pos': w.get('pos', '')}
    try:
        from expand_words import NEW as EXTRA
        for x in EXTRA:
            key = (x.get('word') or '').lower().strip()
            if key and key not in corpus:
                corpus[key] = {'meaning': x.get('zh', ''), 'image': x.get('img', '🔤'),
                               'pos': x.get('pos', '')}
    except Exception:
        pass
    return corpus


_MEMBERS = None


def family_members():
    """词 -> 命中的 (root, affix) 家族（依据家族库的成员名单）。结果缓存。"""
    global _MEMBERS
    if _MEMBERS is not None:
        return _MEMBERS
    members = {}
    for root, (_, words) in ALL_ROOTS.items():
        for w, _, _ in words:
            members.setdefault(w.lower(), {}).setdefault('roots', []).append(root)
    for affix, (_, words) in AFFIXES.items():
        for w, _, _ in words:
            members.setdefault(w.lower(), {}).setdefault('affixes', []).append(affix)
    _MEMBERS = members
    return members


def _plural(k):
    """名词复数形式。"""
    if k.endswith('y') and len(k) > 1 and k[-2] not in 'aeiou':
        return k[:-1] + 'ies'
    if k.endswith(('s', 'x', 'z', 'ch', 'sh', 'o')):
        return k + 'es'
    return k + 's'


def build_inflections(corpus):
    """由课本词表的词性反推「屈折变化形式」（复数/过去式/现在分词/比较级/最高级）。

    这些形式只是形态变化，不是词缀派生，必须排除，否则会闹出
    「earth = ear + -th」「longer = long + -er」这样的笑话。
    """
    bad = set()
    for k, v in corpus.items():
        toks = set(t for t in re.split(r'[./]', v.get('pos', '') or '') if t)
        if 'n' in toks:
            bad.add(_plural(k))
        if 'v' in toks:
            if k.endswith('e'):
                bad.add(k + 'd')
                bad.add(k[:-1] + 'ing')
            elif k.endswith('y') and len(k) > 1 and k[-2] not in 'aeiou':
                bad.add(k[:-1] + 'ied')
                bad.add(k + 'ing')
            else:
                bad.add(k + 'ed')
                bad.add(k + 'ing')
            bad.add(_plural(k))
        if 'adj' in toks:
            if k.endswith('e'):
                bad.add(k + 'r')
                bad.add(k + 'st')
            elif k.endswith('y') and len(k) > 1 and k[-2] not in 'aeiou':
                bad.add(k[:-1] + 'ier')
                bad.add(k[:-1] + 'iest')
            else:
                bad.add(k + 'er')
                bad.add(k + 'est')
    return bad


# 不规则过去分词 / 形似后缀但实为单词本身的常见词
IRREGULAR = {
    'fallen', 'broken', 'spoken', 'written', 'eaten', 'given', 'taken', 'chosen',
    'driven', 'hidden', 'ridden', 'risen', 'beaten', 'forgotten', 'frozen', 'stolen',
    'thrown', 'grown', 'known', 'shown', 'drawn', 'seen', 'done', 'gone', 'been',
}


def detect_root(word, corpus):
    """识别词根：先看家族名单，再按子串匹配（词根长度≥4，避免误判）。"""
    key = word.lower().strip()
    if ' ' in key:                      # take part in / play sports 之类短语不拆词根
        return None
    mem = family_members().get(key, {})
    if mem.get('roots'):
        return mem['roots'][0]
    if key in NOT_ROOT:
        return None
    best = None
    for root in ROOTS:
        if len(root) >= 4 and root in key and len(key) >= len(root) + 1:
            if best is None or len(root) > len(best):
                best = root
    return best


def _peel(key, corpus, depth=0):
    """在一段词形上逐层剥词缀（前缀、后缀各取最长命中），最多剥 3 层。

    例：reporter → -er(report) → re-(port)，于是 reporter = re- + port + -er。
    """
    if depth >= 3 or len(key) <= 4:
        return []
    pre = suf = None
    for affix in AFFIXES:
        if affix.endswith('-'):
            p = affix[:-1]
            if (key.startswith(p) and len(key) > len(p) + 2
                    and (key[len(p):] in corpus or key[len(p):] in KNOWN_STEMS)):
                if pre is None or len(p) > len(pre):
                    pre = p
    for affix in AFFIXES:
        if affix.startswith('-'):
            s = affix[1:]
            if (key.endswith(s) and len(key) > len(s) + 2
                    and (key[:-len(s)] in corpus or key[:-len(s)] in KNOWN_STEMS)):
                if suf is None or len(s) > len(suf):
                    suf = s
    if not pre and not suf:
        return []
    start = len(pre) if pre else 0
    end = len(key) - len(suf) if suf else len(key)
    hit = ([pre + '-'] if pre else []) + ([('-' + suf)] if suf else [])
    return hit + _peel(key[start:end], corpus, depth + 1)


def detect_affixes(word, corpus):
    """识别词缀：家族名单优先，其次前缀/后缀拼写 + 词干校验。

    家族名单是人工确认过的，优先级最高；拼写推断要同时过三关：
    不在禁用名单、不在屈折形式名单、词干能在词表或常见词干表里找到。
    """
    key = word.lower().strip()
    if ' ' in key:                      # 短语不拆词缀
        return []
    out = []
    mem = family_members().get(key, {})
    for a in mem.get('affixes', []):
        out.append(a)
    if not (key in NOT_DERIVED or key in IRREGULAR or key in _inflections()):
        for a in _peel(key, corpus):
            if a not in out:
                out.append(a)
    # 前缀排在前、后缀排在后；同组内长词缀优先（un- 优先于 u-）
    out.sort(key=lambda a: (0 if a.endswith('-') else 1, -len(a)))
    return out


def _inflections():
    """屈折形式名单：首次调用时按词表算好并缓存。"""
    global _INFLECTIONS
    if _INFLECTIONS is None:
        _INFLECTIONS = build_inflections(load_corpus())
    return _INFLECTIONS


_INFLECTIONS = None


def syllabify(word):
    """粗略按元音切音节，用于「拼读记忆」。切不出来返回 None。"""
    w = word.lower()
    groups = list(re.finditer(r'[aeiouy]+', w))
    if len(groups) < 2:
        return None
    if w.endswith('e') and len(groups) == 2 and groups[-1].end() == len(w) and groups[-1].start() == len(w) - 1:
        return None  # 结尾不发音的 e（make / like）→ 单音节
    cuts = []
    for i in range(len(groups) - 1):
        end = groups[i].end()
        nxt = groups[i + 1].start()
        cons = nxt - end
        cuts.append(nxt if cons <= 1 else end + 1)
    parts, prev = [], 0
    for c in cuts:
        parts.append(w[prev:c])
        prev = c
    parts.append(w[prev:])
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return None
    return '·'.join(parts)


def make_association(word, meaning, pos, root, affixes, corpus, root_words=None):
    """生成「联想记忆」文案：构词拆解 > 词根联想 > 音节拼读。"""
    key = word.lower().strip()
    core = meaning.replace(';', '；').split('；')[0].strip()
    # 1) 词缀拆解（前缀 / 后缀至少命中一个，且能切出词干）
    if affixes:
        pre = next((a for a in affixes if a.endswith('-')), None)
        suf = next((a for a in affixes if a.startswith('-')), None)
        left = pre[:-1] if pre else ''
        right = suf[1:] if suf else ''
        stem = key[len(left):len(key) - len(right)] if (left or right) else key
        if stem == '' and pre and suf:
            # 整词 = 前缀 + 后缀（superman / uncomfortable 之外的 superman 型）
            return '拆词记忆：%s(%s) + %s(%s) → %s。' % (
                pre, _short(AFFIXES[pre][0]), suf, _short(AFFIXES[suf][0]), core)
        if len(stem) >= 2:
            bits = []
            if pre:
                bits.append('%s(%s)' % (pre, _short(AFFIXES[pre][0])))
            bits.append('%s%s' % (stem, ('(%s)' % corpus[stem]['meaning'].split('；')[0]) if stem in corpus else ''))
            if suf:
                bits.append('%s(%s)' % (suf, _short(AFFIXES[suf][0])))
            return '拆词记忆：%s → %s。' % (' + '.join(bits), core)
    # 2) 词根联想：和同根词一起记
    if root and root in ALL_ROOTS:
        gloss = ALL_ROOTS[root][0]
        mates = [w for w, _, _ in ALL_ROOTS[root][1] if w.lower() != key][:3]
        if mates:
            return '词根记忆：%s 表示“%s”，和 %s 同根，串起来记 → %s。' % (
                root, gloss, ' / '.join(mates), core)
        return '词根记忆：%s 表示“%s”，按这个词根的含义去记 → %s。' % (root, gloss, core)
    # 3) 音节拼读
    syl = syllabify(key)
    if syl:
        return '拼读记忆：按音节读 %s，边读边拼 → %s。' % (syl, core)
    return '拼读记忆：读准 %s 的每个字母音 → %s。' % (key, core)


def build_ts(path='src/data/families.ts'):
    corpus = load_corpus()
    members = family_members()

    # ---- 拓展词池：家族里出现、但课本词表没有的词 ----
    pool = {}
    for root, (_, words) in ALL_ROOTS.items():
        for w, meaning, img in words:
            k = w.lower()
            if k in corpus or k in pool:
                continue
            pool[k] = {'word': w, 'meaning': meaning, 'image': img, 'root': root}
    for affix, (_, words) in AFFIXES.items():
        for w, meaning, img in words:
            k = w.lower()
            if k in corpus:
                continue
            if k in pool:
                pool[k].setdefault('affix', affix)
                continue
            pool[k] = {'word': w, 'meaning': meaning, 'image': img, 'affix': affix}

    # ---- 每个词条命中的词缀 ----
    word_affixes = {}
    for w in list(corpus) + list(pool):
        affs = detect_affixes(w, corpus)
        if affs:
            word_affixes[w] = [{'affix': a, 'meaning': AFFIXES[a][0]} for a in affs]

    # ---- 家族成员池：精选常见词在前，再补上课本里同根/同缀的其他词 ----
    # 这样「扩展不受课本单元限制」的池子 = 精选词 + 整个课本词表，但 UI 每组仍只展示 8 个。
    CAP = 12

    def merge(curated, extra_key, hits):
        lst, seen = [], set()
        for w in curated:
            k = w.lower()
            if k not in seen:
                lst.append(w)
                seen.add(k)
        for k in sorted(corpus):
            if k not in seen and extra_key in hits.get(k, []):
                lst.append(k)
                seen.add(k)
        for k in sorted(pool):
            if k not in seen and extra_key in hits.get(k, []):
                lst.append(k)
                seen.add(k)
        return lst[:CAP]

    root_hits, affix_hits = {}, {}
    for k in list(corpus) + list(pool):
        r = detect_root(k, corpus)
        if r:
            root_hits.setdefault(k, set()).add(r)
        for a in detect_affixes(k, corpus):
            affix_hits.setdefault(k, set()).add(a)

    def j(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ["import { Word } from '../types';", '',
             '// 本文件由 scripts/gen_families.py 生成，请勿手工编辑。',
             '// 词根词缀网络：扩展池 = 精选常见词 + 课本同根/同缀词，不受单元限制；UI 侧每组最多展示 8 个。',
             '',
             '// 词根含义：root -> 中文含义',
             'export const rootMeaning: Record<string, string> = {']
    for root, (gloss, _) in ALL_ROOTS.items():
        lines.append('  %s: %s,' % (j(root), j(gloss)))
    lines.append('};')
    lines.append('')
    lines.append('// 词根家族：root -> 常见同根词（顺序 = 展示优先级）')
    lines.append('export const rootFamily: Record<string, string[]> = {')
    for root, (_, words) in ALL_ROOTS.items():
        lst = merge([w for w, _, _ in words], root, root_hits)
        lines.append('  %s: [%s],' % (j(root), ', '.join(j(w) for w in lst)))
    lines.append('};')
    lines.append('')
    lines.append('// 词缀含义：affix -> 中文含义')
    lines.append('export const affixMeaning: Record<string, string> = {')
    for affix, (gloss, _) in AFFIXES.items():
        lines.append('  %s: %s,' % (j(affix), j(gloss)))
    lines.append('};')
    lines.append('')
    lines.append('// 词缀家族：affix -> 常见同缀词（顺序 = 展示优先级）')
    lines.append('export const affixFamily: Record<string, string[]> = {')
    for affix, (_, words) in AFFIXES.items():
        lst = merge([w for w, _, _ in words], affix, affix_hits)
        lines.append('  %s: [%s],' % (j(affix), ', '.join(j(w) for w in lst)))
    lines.append('};')
    lines.append('')
    lines.append('// 每个词条命中的词缀（可同时命中前缀与后缀，如 reporter = re- + -er）')
    lines.append('export const wordAffixes: Record<string, { affix: string; meaning: string }[]> = {')
    for w, affs in word_affixes.items():
        body = ', '.join('{ affix: %s, meaning: %s }' % (j(a['affix']), j(a['meaning'])) for a in affs)
        lines.append('  %s: [%s],' % (j(w), body))
    lines.append('};')
    lines.append('')
    lines.append('// 词根词缀拓展词：只用于网络扩展，不进入单元词表（grade 为空串）')
    lines.append('export const familyWords: Word[] = [')
    for k in sorted(pool):
        p = pool[k]
        affs = [a['affix'] for a in word_affixes.get(k, [])]
        if not p.get('affix') and affs:
            p['affix'] = affs[0]
        if not p.get('root'):
            hs = root_hits.get(k)
            if hs:
                p['root'] = sorted(hs)[0]
        assoc = make_association(p['word'], p['meaning'], '', p.get('root'), affs, corpus)
        # 拓展词原先没有短语/例句，学生不知道怎么用 —— 这里按词性补上（每条最多 2 组）
        _pos = infer_pos(p['word'], p['meaning'])
        _phr, _exa = gen_phrases(p['word'], p['meaning'], _pos)
        parts = ['id: %s' % j('x_' + re.sub(r'[^a-z0-9]', '_', k)),
                 'word: %s' % j(p['word']),
                 'meaning: %s' % j(p['meaning']),
                 'image: %s' % j(p['image']),
                 "grade: ''",
                 'tags: ["拓展"]']
        if p.get('root'):
            parts.append('root: %s' % j(p['root']))
        if p.get('affix'):
            parts.append('affix: %s' % j(p['affix']))
            parts.append('affixMeaning: %s' % j(AFFIXES[p['affix']][0]))
        # 短语、例句紧跟 tags / root / affix 之后（本模块只有 j()，故就地拼 { en, zh }）
        parts.append('phrases: [' + ', '.join(
            '{ en: %s, zh: %s }' % (j(a), j(b)) for a, b in (_phr or [])[:2]) + ']')
        parts.append('examples: [' + ', '.join(
            '{ en: %s, zh: %s }' % (j(a), j(b)) for a, b in (_exa or [])[:2]) + ']')
        parts.append('association: %s' % j(assoc))
        lines.append('  { %s },' % ', '.join(parts))
    lines.append('];')
    lines.append('')

    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    return len(pool), len(word_affixes), len(ALL_ROOTS), len(AFFIXES)


if __name__ == '__main__':
    n_pool, n_wa, n_r, n_a = build_ts()
    print('词根 %d 个，词缀 %d 个，拓展词 %d 个，命中词缀的词条 %d 个' % (n_r, n_a, n_pool, n_wa))
