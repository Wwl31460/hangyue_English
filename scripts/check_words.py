import re
from collections import Counter

src = open('src/data/words.ts', encoding='utf-8').read()
ids = re.findall(r"id:\s*'([^']+)'", src)
words = re.findall(r"word:\s*'([^']+)'", src)
grades = re.findall(r"grade:\s*'([^']+)'", src)

print('total entries:', len(ids))
print('unique ids:', len(set(ids)))
print('dup ids:', [k for k, v in Counter(ids).items() if v > 1])
print('unique words:', len(set(words)))

# 余留的过去式条目检查
past_like = {'went', 'ate', 'saw', 'had'}
leftover = [i for i in ids if i in past_like]
print('leftover past-tense ids:', leftover)

print('\nper grade:')
gc = Counter(grades)
for g in ['g3s1','g3s2','g4s1','g4s2','g5s1','g5s2','g6s1','g6s2',
          'c7s1','c7s2','c8s1','c8s2','c9s1','c9s2',
          'h1s1','h1s2','h2s1','h2s2','h3s1','h3s2']:
    print(f'  {g}: {gc.get(g,0)}')

# 词根/词缀网络规模
roots = re.findall(r"root:\s*'([^']+)'", src)
affixes = re.findall(r"affix:\s*'([^']+)'", src)
print('\n带词根的词:', len(roots), '| 不同词根:', len(set(roots)))
print('带词缀的词:', len(affixes), '| 不同词缀:', len(set(affixes)))
