# -*- coding: utf-8 -*-
"""手工整理的**复合词家族**（共享同一个「词尾」）。

为什么必须手工写一张：
    自动扫描要求「前半截自己也是一个词」，但 football / basketball / baseball / volleyball
    里的 basket、base、volley 这些构件**在词库里根本不存在**（它们不是课本词条），
    于是扫描永远连不上这几个明明应该串记的词 —— 用户点名的例子恰好被这条规则卡住。
    同理 review / preview / interview / viewer 里的 view 也不是独立词条。

所以这里直接给出「共享词尾 → 成员」清单，并带上中文释义与 emoji；
成员若不在课本词表里，会作为拓展词进入词库（可点、可学、有例句）。

COMPOUNDS = { 共享词尾: (词尾含义, [(词, 中文, emoji), ...]) }
"""

COMPOUNDS = {
    'ball': ('球', [
        ('basketball', '篮球', '🏀'), ('baseball', '棒球', '⚾'),
        ('volleyball', '排球', '🏐'), ('football', '足球', '⚽'),
        ('handball', '手球', '🤾'),
    ]),
    'book': ('书', [
        ('textbook', '课本', '📖'), ('notebook', '笔记本', '📓'),
        ('storybook', '故事书', '📕'), ('workbook', '练习册', '📒'),
    ]),
    'room': ('房间', [
        ('classroom', '教室', '🏫'), ('bedroom', '卧室', '🛏️'),
        ('bathroom', '浴室', '🛁'), ('restroom', '洗手间', '🚻'),
    ]),
    'day': ('天；日子', [
        ('birthday', '生日', '🎂'), ('today', '今天', '📅'),
        ('weekday', '工作日', '📆'), ('weekend', '周末', '🎉'),
        ('holiday', '假日', '🏖️'),
    ]),
    'view': ('看；视野', [
        ('review', '复习；评论', '📝'), ('preview', '预习；预览', '👀'),
        ('interview', '面试；采访', '🎤'), ('viewer', '观看者', '👁️'),
    ]),
    'work': ('工作', [
        ('homework', '家庭作业', '📚'), ('housework', '家务', '🧹'),
        ('teamwork', '团队合作', '🤝'), ('schoolwork', '功课', '✏️'),
    ]),
    'ground': ('地面', [
        ('playground', '操场', '🛝'), ('background', '背景', '🖼️'),
        ('underground', '地下的；地铁', '🚇'),
    ]),
    'light': ('光', [
        ('sunlight', '阳光', '☀️'), ('daylight', '日光', '🌅'),
        ('highlight', '亮点', '✨'), ('flashlight', '手电筒', '🔦'),
    ]),
    'water': ('水', [
        ('waterfall', '瀑布', '🌊'), ('watermelon', '西瓜', '🍉'),
        ('underwater', '水下的', '🤿'),
    ]),
    'town': ('城镇', [
        ('hometown', '家乡', '🏠'), ('downtown', '市中心', '🏙️'),
    ]),
    'side': ('边；侧', [
        ('inside', '在里面', '⬅️'), ('outside', '在外面', '➡️'),
        ('beside', '在旁边', '↔️'), ('roadside', '路边', '🛣️'),
    ]),
    'thing': ('事物', [
        ('something', '某事物', '💭'), ('everything', '一切', '🌐'),
        ('nothing', '没有东西', '🚫'), ('anything', '任何东西', '❔'),
    ]),
    'body': ('身体；人', [
        ('everybody', '每个人', '👥'), ('somebody', '某人', '🧍'),
        ('nobody', '没有人', '🫥'), ('anybody', '任何人', '🤷'),
    ]),
    'one': ('一个', [
        ('everyone', '每个人', '👥'), ('someone', '某人', '🧍'),
        ('anyone', '任何人', '🤷'),
    ]),
    'where': ('哪里', [
        ('everywhere', '到处', '🌍'), ('somewhere', '某处', '📍'),
        ('anywhere', '任何地方', '🗺️'), ('nowhere', '无处', '⛔'),
    ]),
    'ever': ('任何时候', [
        ('however', '然而', '🔀'), ('whenever', '无论何时', '⏰'),
        ('whatever', '无论什么', '🤷'), ('forever', '永远', '♾️'),
    ]),
    'load': ('负荷', [
        ('download', '下载', '⬇️'), ('upload', '上传', '⬆️'),
        ('overload', '超载', '💥'),
    ]),
    'line': ('线', [
        ('online', '在线的', '💻'), ('offline', '离线的', '📴'),
        ('underline', '在…下划线', '➖'), ('airline', '航空公司', '✈️'),
    ]),
    'net': ('网', [
        ('internet', '互联网', '🌐'), ('network', '网络', '🕸️'),
    ]),
    'ware': ('物品', [
        ('software', '软件', '💾'), ('hardware', '硬件', '🔧'),
    ]),
    'board': ('板', [
        ('blackboard', '黑板', '📋'), ('keyboard', '键盘', '⌨️'),
        ('skateboard', '滑板', '🛹'),
    ]),
    'ache': ('疼痛', [
        ('headache', '头痛', '🤕'), ('toothache', '牙痛', '🦷'),
        ('stomachache', '胃痛', '🤢'),
    ]),
    'tooth': ('牙', [
        ('toothbrush', '牙刷', '🪥'), ('toothpaste', '牙膏', '🦷'),
    ]),
    'shop': ('店', [
        ('workshop', '车间；研讨会', '🔧'), ('bookshop', '书店', '📚'),
    ]),
    'bag': ('包', [
        ('schoolbag', '书包', '🎒'), ('handbag', '手提包', '👜'),
    ]),
    'house': ('房子', [
        ('greenhouse', '温室', '🌱'), ('lighthouse', '灯塔', '🗼'),
    ]),
    'mate': ('伙伴', [
        ('classmate', '同班同学', '🧑‍🎓'), ('roommate', '室友', '🛏️'),
        ('teammate', '队友', '🤝'),
    ]),
    'case': ('箱；情形', [
        ('suitcase', '手提箱', '🧳'), ('bookcase', '书柜', '📚'),
    ]),
    'brush': ('刷子', [
        ('toothbrush', '牙刷', '🪥'), ('hairbrush', '发梳', '💇'),
    ]),
    'flower': ('花', [
        ('sunflower', '向日葵', '🌻'),
    ]),
    'time': ('时间', [
        ('bedtime', '就寝时间', '🛏️'), ('lifetime', '一生', '⌛'),
    ]),
    'modern': ('现代', [
        ('postmodern', '后现代的', '🎭'),
    ]),
}


def merge_into(families, corpus=None):
    """把手工复合词家族合并进 families 字典。

    成员排在自动扫描结果之前（人工整理过的质量更高）；
    families 里已有的同一 key 会保留原成员并去重。
    """
    n = 0
    for tail, (gloss, members) in COMPOUNDS.items():
        ents = [(w, m, i) for w, m, i in members]
        if corpus and tail in corpus:
            gloss = corpus[tail]['meaning']
            self_ent = (tail, gloss, corpus[tail].get('image', '🔤'))
        else:
            gloss = gloss
            self_ent = (tail, gloss, '🔤')
        if tail in families:
            _g, old = families[tail]
            manual = {x.lower() for x, _, _ in ents}
            families[tail] = (_g, [old[0]] + ents +
                              [e for e in old[1:] if e[0].lower() not in manual])
        else:
            families[tail] = (gloss, [self_ent] + ents)
        n += 1
    return families, n
