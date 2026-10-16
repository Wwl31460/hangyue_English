# 为 words.ts / families.ts 中缺失音标的词条批量生成并写入 IPA 音标。
# 音标由 eng_to_ipa（纯 Python 规则音标库）生成，覆盖绝大多数常见词。
# 用法：由托管 python 运行（venv 已装 eng_to_ipa）。
import re

from eng_to_ipa import convert

WORD_RE = re.compile(r'word: "([^"]*)",')
ID_RE = re.compile(r'id:')


def process(path: str) -> int:
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    out = []
    changed = 0
    for line in lines:
        if 'id:' in line and 'word:' in line and 'phonetic:' not in line:
            m = WORD_RE.search(line)
            if m:
                w = m.group(1)
                ipa = convert(w)
                if ipa and ipa.strip() and ipa.strip().lower() != w.strip().lower():
                    ipa_s = ipa.strip()
                    if not ipa_s.startswith('/'):
                        ipa_s = '/' + ipa_s + '/'
                    # 在 word 字段后插入 phonetic
                    line = line[: m.end()] + f' phonetic: "{ipa_s}",' + line[m.end():]
                    changed += 1
        out.append(line)
    with open(path, encoding='utf-8') as f:
        pass
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    return changed


if __name__ == '__main__':
    for p in ('src/data/words.ts', 'src/data/families.ts'):
        n = process(p)
        print(f'{p}: 写入音标 {n} 条')
