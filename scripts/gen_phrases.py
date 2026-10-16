# -*- coding: utf-8 -*-
"""短语/例句生成器：为初中、高中主数据补齐 phrases / examples。

质量策略
--------
1. 内容词（名词/动词/形容词/副词）用「搭配模板」生成，中文侧只取词义的第一义项、
   并去掉多余的「的/地」，避免出现「不幸的的」「一个页」这类硬伤；
2. 功能词（代词/介词/连词/数词/情态动词/感叹词/冠词）、不规则动词、多词条目，
   由 phrase_overrides.OVERRIDE 人工给出，模板不参与；
3. 名词区分可数与不可数，正确使用 a/an、复数形式与中文量词；
4. 混合词性（如 n./v.）取第一个词性走对应模板。

输出：gen_phrases(word, meaning, pos) -> (phrases, examples)
"""

from phrase_overrides import OVERRIDE

# ---------- 不可数名词（不用 a/an，改 some） ----------
UNCOUNTABLE = {
    'water', 'milk', 'tea', 'coffee', 'juice', 'bread', 'rice', 'meat', 'beef', 'pork',
    'chicken', 'food', 'fruit', 'music', 'news', 'information', 'advice', 'furniture',
    'homework', 'housework', 'weather', 'money', 'time', 'air', 'fun', 'work', 'paper',
    'sugar', 'salt', 'cheese', 'butter', 'soup', 'popcorn', 'salad', 'mutton',
    'luck', 'help', 'progress', 'knowledge', 'exercise', 'traffic', 'vocabulary',
    # 学科
    'math', 'maths', 'science', 'geography', 'history', 'art', 'biology', 'chemistry',
    'physics', 'pe',
    # 抽象名词
    'importance', 'honor', 'honour', 'religion', 'insurance', 'education', 'courage',
    'patience', 'silence', 'equipment', 'luggage', 'permission', 'freedom', 'poverty',
    'wealth', 'health', 'strength', 'power', 'energy', 'electricity', 'pollution',
    'rubbish', 'garbage', 'trash', 'nature', 'environment', 'safety', 'happiness',
    'sadness', 'kindness', 'darkness', 'business', 'damage', 'transport', 'transportation',
    # 集合名词
    'wildlife', 'staff', 'police', 'baggage', 'scenery', 'machinery', 'poetry', 'livestock',
    # 材料
    'steel', 'iron', 'wood', 'plastic', 'glass', 'cotton', 'silk', 'gold', 'silver', 'coal',
    'oil', 'gas', 'sand', 'soil', 'stone', 'metal', 'clay', 'wool',
}

# ---------- 只有复数形式的名词 ----------
PLURAL_ONLY = {'clothes', 'trousers', 'shorts', 'jeans', 'glasses', 'shoes', 'socks', 'gloves'}

# ---------- 不规则复数 ----------
IRREGULAR_PLURAL = {
    'man': 'men', 'woman': 'women', 'child': 'children', 'foot': 'feet', 'tooth': 'teeth',
    'mouse': 'mice', 'goose': 'geese', 'sheep': 'sheep', 'fish': 'fish', 'deer': 'deer',
    'person': 'people', 'knife': 'knives', 'leaf': 'leaves', 'wolf': 'wolves',
    'wife': 'wives', 'life': 'lives', 'half': 'halves', 'shelf': 'shelves',
    'thief': 'thieves', 'hero': 'heroes', 'potato': 'potatoes', 'tomato': 'tomatoes',
}

# ---------- 元音字母开头却用 a 的词 ----------
A_NOT_AN = {'university', 'unit', 'useful', 'usual', 'usually', 'european', 'one', 'user', 'uniform'}

# ---------- 常用中文量词（按词义第一义项匹配） ----------
CLASSIFIER = {
    # 只
    '脚': '只', '手': '只', '眼': '只', '眼睛': '只', '耳': '只', '耳朵': '只', '胳膊': '只',
    '鸟': '只', '猫': '只', '狗': '只', '鸭子': '只', '兔子': '只', '猪': '只', '羊': '只',
    '鸡': '只', '马': '匹', '牛': '头', '大象': '头', '蚂蚁': '只', '老鼠': '只', '熊猫': '只',
    '猴子': '只', '狮子': '只', '老虎': '只', '熊': '只', '蝴蝶': '只', '蜜蜂': '只', '风筝': '只',
    # 条
    '路': '条', '河': '条', '鱼': '条', '蛇': '条', '腿': '条', '裤子': '条', '裙子': '条',
    '街道': '条', '绳子': '条', '消息': '条', '建议': '条',
    # 张
    '纸': '张', '桌子': '张', '床': '张', '票': '张', '脸': '张', '照片': '张', '卡片': '张',
    '地图': '张', '嘴': '张', '桌子': '张',
    # 座 / 栋 / 间
    '山': '座', '桥': '座', '楼': '座', '城市': '座', '房子': '栋', '房间': '间', '教室': '间',
    '公寓': '套', '房子': '栋',
    # 辆 / 台 / 部
    '车': '辆', '自行车': '辆', '公交车': '辆', '卡车': '辆', '出租车': '辆', '火车': '列',
    '电脑': '台', '电视': '台', '机器': '台', '手机': '部', '电影': '部', '相机': '台',
    # 件 / 本 / 支 / 把
    '事': '件', '事情': '件', '衣服': '件', '礼物': '件', '行李': '件', '衬衫': '件', '外套': '件',
    '毛衣': '件', '书': '本', '笔记本': '本', '字典': '本', '杂志': '本', '故事': '个',
    '笔': '支', '铅笔': '支', '钢笔': '支', '蜡笔': '支', '花': '朵', '树': '棵', '苹果': '个',
    '尺子': '把', '椅子': '把', '伞': '把', '刀': '把', '钥匙': '把', '扇子': '把',
    '勺子': '把', '叉子': '把', '香蕉': '根', '绳子': '根', '蜡烛': '根', '面包': '片',
    '蛋糕': '块', '糖': '块', '表': '块', '石头': '块', '硬币': '枚', '邮票': '枚',
    '歌': '首', '音乐': '首', '诗': '首', '比赛': '场', '戏': '场', '雨': '场',
    '问题': '个', '答案': '个', '主意': '个', '想法': '个', '计划': '个', '梦': '个',
}


def plural_of(w):
    """返回名词复数形式。"""
    lw = w.lower()
    if lw in IRREGULAR_PLURAL:
        return IRREGULAR_PLURAL[lw]
    if lw.endswith(('s', 'x', 'ch', 'sh', 'z')):
        return w + 'es'
    if lw.endswith('y') and len(lw) > 1 and lw[-2] not in 'aeiou':
        return w[:-1] + 'ies'
    if lw.endswith('fe'):
        return w[:-2] + 'ves'
    if lw.endswith('f'):
        return w[:-1] + 'ves'
    return w + 's'


def article_of(w):
    """返回不定冠词 a / an。"""
    lw = w.lower()
    if lw in A_NOT_AN:
        return 'a'
    return 'an' if lw[:1] in 'aeiou' else 'a'


def core_of(meaning, strip='的'):
    """取词义的第一义项，并去掉行尾的「的/地/得」（按词性分别处理）。"""
    s = meaning.replace(';', '；').split('；')[0].strip()
    while s and s[-1] in strip:
        s = s[:-1]
    return s or meaning


def _num_zh(n, core):
    """中文量词：优先用常用量词表，其次「一页/两页」，最后「一个/两个」。"""
    if core[:1] in '一二两双对些群':
        return core
    mw = CLASSIFIER.get(core)
    if mw:
        return ('一' if n == '一' else '两') + mw + core
    return (n + core) if len(core) == 1 else (n + '个' + core)


def _noun(word, meaning):
    core = core_of(meaning)
    lw = word.lower()
    if lw in PLURAL_ONLY:
        return (
            [('a pair of ' + word, _num_zh('一', core)), (word, core)],
            [('I need to buy a pair of ' + word + '.', '我需要买' + _num_zh('一', core) + '。'),
             ('These ' + word + ' are too small.', '这些' + core + '太小了。')],
        )
    if lw in UNCOUNTABLE:
        return (
            [('some ' + word, '一些' + core), ('a lot of ' + word, '很多' + core)],
            [('We need some ' + word + '.', '我们需要一些' + core + '。'),
             ('I like ' + word + ' very much.', '我非常喜欢' + core + '。')],
        )
    art, pl = article_of(word), plural_of(word)
    return (
        [(art + ' ' + word, _num_zh('一', core)), ('two ' + pl, _num_zh('两', core))],
        [('This is ' + art + ' ' + word + '.', '这是' + _num_zh('一', core) + '。'),
         ('I have two ' + pl + '.', '我有' + _num_zh('两', core) + '。')],
    )


def _verb(word, meaning):
    core = core_of(meaning)
    return (
        [('to ' + word, core), (word + ' every day', '每天' + core)],
        [('I want to ' + word + ' with my friends.', '我想和朋友们一起' + core + '。'),
         ('It is fun to ' + word + ' together.', '一起' + core + '很有趣。')],
    )


def _adj(word, meaning):
    core = core_of(meaning)
    return (
        [('be ' + word, '是' + core + '的'), ('very ' + word, '非常' + core + '的')],
        [('It is very ' + word + '.', '它非常' + core + '。'),
         ('I think it is ' + word + '.', '我认为它很' + core + '。')],
    )


def _adv(word, meaning):
    first = meaning.replace(';', '；').split('；')[0].strip()
    if first.endswith('地'):
        # 方式副词：优美地 / 安静地 / 迅速地 → 直接用「…地」
        core = core_of(meaning, '地')
        return (
            [('speak ' + word, core + '地说话'), ('do sth ' + word, core + '地做某事')],
            [('She speaks ' + word + '.', '她' + core + '地说话。'),
             ('He did it ' + word + '.', '他' + core + '地做这件事。')],
        )
    core = core_of(meaning)
    return (
        [('do sth ' + word, core + '地做某事')],
        [('He ' + word + ' works in the morning.', '他' + core + '在上午工作。'),
         ('They ' + word + ' play together.', '他们' + core + '一起玩。')],
    )


def _proper(word, meaning):
    core = core_of(meaning)
    return (
        [(word, meaning), ('about ' + word, '关于' + core)],
        [('We are talking about ' + word + '.', '我们在谈论' + core + '。'),
         ('I like ' + word + ' very much.', '我非常喜欢' + core + '。')],
    )


def gen_phrases(word, meaning, pos):
    """返回 (phrases, examples)，元素为 (en, zh) 元组。"""
    key = word.lower().strip()
    if key in OVERRIDE:
        ph, ex = OVERRIDE[key]
        return list(ph), list(ex)

    # 多词条目 → 按短语处理
    if ' ' in word or pos in ('phrase', 'phr.'):
        return (
            [(word, meaning)],
            [('We often use "' + word + '" in English.', '英语里常用「' + word + '」表达「' + meaning + '」。')],
        )

    # 专有名词（首字母大写：国家/语言/星期/月份等）与含点缩写
    if word[:1].isupper() or '.' in word:
        return _proper(word, meaning)

    # 混合词性取第一个
    p = (pos or '').lower().split('/')[0].strip()
    if p.startswith('n'):
        return _noun(word, meaning)
    if p.startswith('v'):
        return _verb(word, meaning)
    if p.startswith('adj'):
        return _adj(word, meaning)
    if p.startswith('adv'):
        return _adv(word, meaning)

    # 兜底
    core = core_of(meaning)
    return (
        [(word, meaning)],
        [(word.capitalize() + ' is very important.', core + '很重要。'),
         ('Do you know the word "' + word + '"?', '你知道「' + word + '」这个词吗？')],
    )
