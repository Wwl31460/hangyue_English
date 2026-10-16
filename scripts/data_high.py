# -*- coding: utf-8 -*-
"""高中 6 册主数据：把 pep_high.HIGH（人教2019 必修/选必真实单元词）转成统一 dict 格式，
并用 gen_phrases 补齐 phrases / examples。
"""
import sys

sys.path.insert(0, 'scripts')
from pep_high import HIGH
from gen_phrases import gen_phrases


def convert(spec):
    out = []
    for t in spec['NEW']:
        wid, word, meaning, pos, ph, img, unit, tags, root, affix, am, derive, assoc = t
        word = word.replace('_ord', '')
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


DATA = {g: convert(spec) for g, spec in HIGH.items()}

if __name__ == '__main__':
    for g in DATA:
        print(g, len(DATA[g]))
