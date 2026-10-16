# -*- coding: utf-8 -*-
"""自动生成「本族单词词根」家族。

data_roots.py 收的是拉丁/希腊词根（tract / port / dict…），
但英语里大量单词本身就是词根（本族自由语素），可以派生出一串词：
    help → helpful / helpless / helpfully
    care → careful / careless / carefully
    use  → useful  / useless / usable
这些是用户在中高考里最常遇到、也最好记的一批 —— 但手工列举不现实，所以自动扫。

匹配规则（严格后缀派生，不是子串包含，避免 early ← ear+ly 这类误判）：
  1. W == S + suf
  2. S 以 e 结尾且 suf 以元音开头 → W == S[:-1] + suf  （usable / lovable）
  3. S 以辅音+y 结尾         → W == S[:-1] + i + suf  （happiness / easily）
  4. CVC 短词双写末辅音       → W == S + S[-1] + suf  （sun→sunny / fun→funny）
再做传递闭包（≤3 层），让 help → helpful → helpfully 都归到 help 家族。

降噪：`家庭至少要 2 个派生词` 才成立，绝大多数偶发误配对（early ← ear）天然只有 1 个成员，会被过滤掉。
"""
import json
import sys

sys.path.insert(0, 'scripts')

from gen_families import load_corpus, build_inflections, IRREGULAR
from data_roots import ROOTS
from data_affixes import AFFIXES

# 真派生后缀。刻意排除纯屈折 -s / -ed / -ing / -er(比较级) / -est
# （-er 施事名词走既有 AFFIXES 的 '-er' 家族，不在这里重复造格子）
DERIV_SUFFIXES = [
    'ful', 'less', 'able', 'ible', 'ness', 'ly',
    'al', 'ial', 'ical', 'ual', 'ous', 'ious', 'eous',
    'ive', 'ative', 'itive',
    'ment', 'ism', 'ist',
    'tion', 'sion', 'ation', 'ition', 'ution', 'ion',
    'ity', 'ty',
    'ize', 'ise', 'ify',
    'ance', 'ence', 'ant', 'ent',
    'ary', 'ory', 'age',
    'hood', 'dom', 'ship',
    'ward', 'wards', 'wise', 'like', 'free', 'proof', 'fold', 'some', 'ish', 'en',
    'y',
]

VOWELS = 'aeiou'
CAP = 12          # 每族最多留多少个派生成员
MIN_MEMBERS = 2   # 少于这个数不建族（主要用来过滤偶发误配对）

# 拼写上像「词干 + 后缀」、但语义其实没有派生关系的偶合组合，
# 逐个看过确认为误导后在此拉黑（ learner 会照字面硬记，反而更糊涂 ）。
FALSE_DERIV = {
    ('ear', 'early'), ('one', 'onion'), ('sale', 'salary'), ('see', 'seize'),
    ('die', 'diary'), ('eve', 'event'), ('file', 'filial'), ('fine', 'finish'),
    ('fine', 'finance'), ('fall', 'fallen'), ('cure', 'curious'),
    ('men', 'mention'), ('mess', 'message'), ('tale', 'talent'),
    ('party', 'partial'), ('please', 'pleasant'), ('prime', 'primitive'),
    # 以下还会经「去 e / y→i」拼写规则从派生路径混进来，故两边都要拉黑
    ('trade', 'tradition'), ('trade', 'traditional'),
    ('grade', 'gradual'), ('grade', 'gradually'),
    ('import', 'important'), ('import', 'importance'),
    ('gravy', 'gravity'), ('state', 'station'),
    ('hospital', 'hospitality'),
}

# 复合词里「拼写偶合但并非真构词」的组合（已逐个核对确认会误导学习者）
FALSE_COMPOUND = {
    ('ice', 'office'),      # office 并非 off + ice
    ('ice', 'justice'),     # 同理：justice 与 ice 无关
    ('age', 'manage'), ('age', 'message'),
    ('cute', 'prosecute'), ('cite', 'excite'), ('cite', 'recite'),
    ('dish', 'reddish'), ('fit', 'profit'), ('fix', 'prefix'),
    ('gravy', 'gravity'), ('hospital', 'hospitality'),
    ('found', 'profound'), ('grade', 'gradually'), ('grade', 'gradual'),
    ('late', 'translate'), ('late', 'relate'),
    ('import', 'important'), ('import', 'importance'),
    ('culture', 'multiculture'), ('cause', 'because'),
    ('action', 'transaction'), ('rate', 'generate'), ('ride', 'deride'),
    ('tent', 'content'), ('parent', 'transparent'), ('pound', 'compound'),
    ('state', 'station'), ('trade', 'tradition'), ('trade', 'traditional'),
    ('tuition', 'intuition'),
}


def is_cvc(s):
    """CVC 短词：sun / big / fun —— 加元音开头的后缀时要双写末辅音。"""
    return (len(s) >= 3 and s[-1] not in VOWELS and s[-1] not in 'wxy'
            and s[-2] in VOWELS and s[-3] not in VOWELS)


def direct_derived(stem, vocab):
    """由 stem 加一层真后缀能得到的词（限 vocab 内）。"""
    out = set()
    for suf in DERIV_SUFFIXES:
        cands = [stem + suf]
        if stem.endswith('e') and suf[0] in VOWELS:
            cands.append(stem[:-1] + suf)                      # usable / lovable
        if stem.endswith('y') and len(stem) > 2 and stem[-2] not in VOWELS:
            cands.append(stem[:-1] + 'i' + suf)                # happiness / easily
        if is_cvc(stem) and suf[0] in VOWELS:
            cands.append(stem + stem[-1] + suf)                # sunny / funny
        for c in cands:
            if c != stem and c in vocab and len(c) >= len(stem) + 2:
                out.add(c)
    return out


def closure(stem, vocab, max_depth=3):
    """多层派生的传递闭包：help → helpful → helpfully。"""
    got, frontier = set(), {stem}
    for _ in range(max_depth):
        nxt = set()
        for s in frontier:
            for d in direct_derived(s, vocab):
                if d not in got:
                    got.add(d)
                    nxt.add(d)
        if not nxt:
            break
        frontier = nxt
    return got


def main(min_members=MIN_MEMBERS):
    corpus = load_corpus()
    # 参与匹配的词表 = 课本词 + 家族库里出现的词（后者会在 familyWords 里，同样可点）
    vocab = set(corpus)
    meta = {}
    for k, v in corpus.items():
        meta[k] = (v['meaning'], v.get('image', '🔤'))
    for src in (ROOTS, AFFIXES):
        for _k, (_g, words) in src.items():
            for w, meaning, img in words:
                k = w.lower()
                vocab.add(k)
                meta.setdefault(k, (meaning, img or '🔤'))

    inflections = build_inflections(corpus)

    families = {}
    for stem in sorted(corpus):                 # 词干必须是课本里的真词
        if len(stem) < 3 or ' ' in stem:
            continue
        if stem in ROOTS:                       # 已有精心整理的词根，不覆盖
            continue
        derived = closure(stem, vocab)
        derived.discard(stem)
        derived = {d for d in derived
                   if d not in inflections      # 复数/过去式/比较级等纯屈折变化
                   and d not in IRREGULAR       # fallen / spoken / written…
                   and (stem, d) not in FALSE_DERIV}
        if len(derived) < min_members:
            continue

        def rank(w):
            # 课本词优先（最常见），其次直接派生（层数≈长度差小），最后字典序
            return (0 if w in corpus else 1, len(w), w)

        members = sorted(derived, key=rank)[:CAP - 1]
        gloss = corpus[stem]['meaning']
        # 词干自己也放进家族名单：这样打开 help 时能识别到自己的家族
        # （UI 侧 resolveFamily 会自动排除「自己」）
        families[stem] = (gloss, [(stem, gloss, corpus[stem].get('image', '🔤'))] + [
            (w, meta.get(w, ('', '🔤'))[0], meta.get(w, ('', '🔤'))[1]) for w in members
        ])

    # ---------- 复合词家族：共享同一个「词尾」 ----------
    # football / basketball / baseball / volleyball 共享 ball；
    # review / preview / interview 共享 view。
    # 降噪关键：前半截必须自己也是一个真词（或已知前缀），
    # 于是 human(hu+man) / German(Ger+man) / Monday(Mon+day) 这类偶合会被自动挡掉。
    known_prefixes = {a[:-1] for a in AFFIXES if a.endswith('-')}
    known_prefixes |= {'over', 'under', 'out', 'to', 'no', 'off', 'up', 'down', 'in', 'on', 'by'}

    def rank2(w):
        return (0 if w in corpus else 1, len(w), w)

    n_compound = 0
    for tail in sorted(corpus):
        if len(tail) < 3 or ' ' in tail or tail in ROOTS:
            continue
        if ('-' + tail) in AFFIXES:   # 已经是后缀（able / less / ful…），不作复合词尾
            continue
        members = []
        for w in vocab:
            if w == tail or not w.endswith(tail):
                continue
            head = w[: -len(tail)]
            if len(head) < 2:
                continue
            ok = (head in vocab and len(head) >= 3) or head in known_prefixes
            if ok and w not in inflections and (tail, w) not in FALSE_COMPOUND:
                members.append(w)
        if len(members) < min_members:
            continue
        n_compound += 1
        members = sorted(set(members), key=rank2)[:CAP - 1]
        gloss = corpus[tail]['meaning']
        ents = [(w, meta.get(w, ('', '🔤'))[0], meta.get(w, ('', '🔤'))[1]) for w in members]
        if tail in families:
            _g, old = families[tail]
            have = {x.lower() for x, _, _ in old}
            families[tail] = (_g, old + [e for e in ents if e[0].lower() not in have])
        else:
            families[tail] = (gloss, [(tail, gloss, corpus[tail].get('image', '🔤'))] + ents)

    # ---------- 手工整理的复合词家族 ----------
    # 补自动扫描抓不到的那一批：basketball / baseball 里的 basket、base 压根不是词条，
    # review / preview 里的 view 也不是词条 —— 只能靠人工点名。
    from data_compounds import COMPOUNDS, merge_into as _merge_comp
    clash = [t for t in COMPOUNDS if t in ROOTS]
    if clash:
        print('  警告：这些复合词尾与 data_roots 同名，会被精选词根覆盖:', clash)
    families, n_manual = _merge_comp(families, corpus)

    def j(s):
        return json.dumps(s, ensure_ascii=False)

    lines = ['# -*- coding: utf-8 -*-',
             '"""本族单词词根（英语本族自由语素 + 派生后缀）。',
             '',
             '由 scripts/auto_wordroots.py 自动扫描词表生成，**请勿手工编辑**。',
             '例：help（帮助）本身就是词根 → helpful / helpless / helpfully …',
             '与 data_roots.py 的拉丁/希腊词根互为补充；同名 key 以 data_roots.py 为准。',
             '"""',
             '',
             'WORDBASES = {']
    for stem, (gloss, members) in families.items():
        lines.append('    %s: (%s, [' % (j(stem), j(gloss)))
        for w, meaning, img in members:
            lines.append('        (%s, %s, %s),' % (j(w), j(meaning), j(img)))
        lines.append('    ]),')
    lines.append('}')
    lines.append('')

    with open('scripts/data_wordroots.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print('本族单词词根家族:', len(families),
          '（自动复合词', n_compound, '个 + 手工复合词', n_manual, '个）')
    print('派生成员总数:', sum(len(v[1]) for v in families.values()))
    for probe in ['help', 'care', 'use', 'hope', 'friend', 'ball', 'view', 'work', 'day', 'foot']:
        if probe in families:
            gl, ms = families[probe]
            print('  %s(%s) → %s' % (probe, gl, ' / '.join(w for w, _, _ in ms)))
        else:
            print('  %s → （未命中）' % probe)


if __name__ == '__main__':
    import sys as _s
    main(min_members=int(_s.argv[1]) if len(_s.argv) > 1 else MIN_MEMBERS)
