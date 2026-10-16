# -*- coding: utf-8 -*-
"""初中 6 册主数据：把 pep_junior.JUNIOR（真实 Go for it! 单元词）转成统一 dict 格式，
并用 gen_phrases 补齐 phrases / examples。
"""
import sys

sys.path.insert(0, 'scripts')
from pep_junior import JUNIOR
from gen_phrases import gen_phrases


def convert(spec):
    out = []
    for t in spec['NEW']:
        wid, word, meaning, pos, ph, img, unit, tags, root, affix, am, derive, assoc = t
        word = word.replace('_ord', '')          # 序数词的 word 字段带 _ord 后缀，去掉
        phr, exa = gen_phrases(word, meaning, pos)
        d = {'id': wid, 'word': word, 'meaning': meaning, 'pos': pos, 'phonetic': ph,
             'image': img, 'unit': unit, 'phrases': phr, 'examples': exa}
        if tags:
            d['tags'] = tags
        if root:
            d['root'] = root
        if affix:
            d['affix'] = affix
        if am:
            d['affixMeaning'] = am
        if derive:
            d['derive'] = derive
        if assoc:
            d['association'] = assoc
        out.append(d)
    return out


DATA = {g: convert(spec) for g, spec in JUNIOR.items()}

if __name__ == '__main__':
    for g in DATA:
        print(g, len(DATA[g]))
