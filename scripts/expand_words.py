#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扩充词库：向 src/data/words.ts 的 raw 数组追加大量单词。
- 词根/词缀家族词（act/port/spect/...）：带构词解析、词根/词缀、联想记忆，强化“词根词缀网络”。
- 各年级常用主题词（数字/颜色/动物/食物/学科/动词/形容词...）：补体量。
已存在的 id 自动跳过，不会重复。
运行：python scripts/expand_words.py
"""
import re
import os

SRC = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'words.ts')

def w(word, zh, pos, grade, img='🔤', phonetic='', root='', affix='', am='',
      derive='', assoc='', ph=None, ex=None, forms=None, tags=None):
    return dict(word=word, zh=zh, pos=pos, grade=grade, img=img, phonetic=phonetic,
                root=root, affix=affix, am=am, derive=derive, assoc=assoc,
                ph=ph or [], ex=ex or [], forms=forms, tags=tags or [])

NEW = []

# ============================== 词根 / 词缀家族（强化网络） ==============================
# act 家族
NEW += [
    w('actor', '演员', 'n.', 'c7s1', '🎭', '/ˈæktə(r)/', 'act', '-or', '表示人', 'actor = act(表演) + -or(人) → 演员。', 'actor 里 act 是“表演”，-or 是“人” → 表演的人就是演员。', [['a famous actor', '一位有名演员'], ['the actor acts well', '演员演得好']], [['The actor is famous.', '这位演员很有名。'], ['He wants to be an actor.', '他想当演员。']], tags=['词根 act']),
    w('actress', '女演员', 'n.', 'c7s1', '🎬', '/ˈæktrəs/', 'act', '-ress', '表示女性', 'actress = act + -ress(女性) → 女演员。', '', [['a young actress', '年轻女演员']], [['She is an actress.', '她是一名女演员。']], tags=['词根 act']),
    w('action', '行动；动作', 'n.', 'c7s1', '⚡', '/ˈækʃn/', 'act', '-ion', '名词后缀', 'action = act + -ion → 行动。', '', [['take action', '采取行动'], ['a kind action', '善意的行为']], [['We must take action.', '我们必须采取行动。']], tags=['词根 act']),
    w('active', '活跃的；积极的', 'adj.', 'c7s1', '🏃', '/ˈæktɪv/', 'act', '-ive', '构成形容词', 'active = act + -ive → 活跃的。', 'active 反过来想：做得多 → 活跃。', [['an active boy', '活泼的男孩'], ['active life', '积极的生活']], [['He is active in class.', '他课上很活跃。']], tags=['词根 act']),
    w('activity', '活动', 'n.', 'c7s1', '🎲', '/ækˈtɪvəti/', 'act', '-ity', '名词后缀', 'activity = act + -ivity → 活动。', '', [['after-school activity', '课外活动']], [['We have many activities.', '我们有很多活动。']], tags=['词根 act']),
    w('actually', '实际上；其实', 'adv.', 'c8s1', '💡', '/ˈæktʃuəli/', 'act', '-ly', '副词后缀', 'actually = actual + -ly → 实际上。', '', [['actually true', '其实是真的']], [['He is actually kind.', '他其实很善良。']], tags=['词根 act']),
    w('react', '反应；回应', 'v.', 'c8s1', '🔁', '/riˈækt/', 'act', 're-', '表示“回”', 'react = re-(回) + act(行动) → 反应回来 = 反应。', '', [['react quickly', '反应快']], [['He reacted fast.', '他反应很快。']], tags=['词根 act', '前缀 re']),
    w('exact', '精确的；准确的', 'adj.', 'c8s1', '🎯', '/ɪɡˈzækt/', 'act', 'ex-', '表示“出”', 'exact = ex-(出) + act(做) → 做出来的 = 精确的。', '', [['exact answer', '准确答案']], [['Give the exact number.', '给出准确数字。']], tags=['词根 act']),
    w('interact', '互动；交流', 'v.', 'c8s2', '🤝', '/ˌɪntərˈækt/', 'act', 'inter-', '表示“之间”', 'interact = inter-(之间) + act → 互相行动 = 互动。', '', [['interact with friends', '和朋友互动']], [['We interact in class.', '我们在课上互动。']], tags=['词根 act', '前缀 inter']),
    w('transaction', '交易；事务', 'n.', 'h1s1', '💱', '/trænˈzækʃn/', 'act', 'trans-', '表示“交换”', 'transaction = trans-(交换) + act + -ion → 交易。', '', [['a big transaction', '一笔大交易']], [['The transaction is done.', '交易完成了。']], tags=['词根 act', '前缀 trans']),
]
# port 家族
NEW += [
    w('import', '进口；输入', 'v./n.', 'c8s1', '📥', '/ˈɪmpɔːt/', 'port', 'im-', '表示“入”', 'import = im-(入) + port(运) → 运入 = 进口。', '', [['import goods', '进口货物']], [['We import cars.', '我们进口汽车。']], tags=['词根 port']),
    w('important', '重要的', 'adj.', 'g4s1', '⭐', '/ɪmˈpɔːtnt/', 'port', '-ant', '构成形容词', 'important = im-(入) + port + -ant → 值得运进来的 = 重要的。', 'important：重要的事都要“运”进来办。', [['an important day', '重要的一天'], ['very important', '非常重要']], [['This is important.', '这很重要。'], ['Health is important.', '健康很重要。']], tags=['词根 port']),
    w('passport', '护照', 'n.', 'c8s2', '🛂', '/ˈpɑːspɔːt/', 'port', '', '', 'passport = pass(过) + port(港) → 过关口的证件 = 护照。', '', [['my passport', '我的护照']], [['Show your passport.', '出示你的护照。']], tags=['词根 port']),
    w('transport', '运输；交通', 'v./n.', 'c8s1', '🚚', '/trænsˈpɔːt/', 'port', 'trans-', '表示“转”', 'transport = trans-(转) + port(运) → 转运 = 运输。', '', [['public transport', '公共交通']], [['We transport goods.', '我们运输货物。']], tags=['词根 port', '前缀 trans']),
    w('report', '报告；报道', 'n./v.', 'c7s1', '📰', '/rɪˈpɔːt/', 'port', 're-', '表示“回”', 'report = re-(回) + port(送) → 送回(上级) = 报告。', '', [['a school report', '学校报告'], ['report news', '报道新闻']], [['He reports the news.', '他报道新闻。'], ['Write a report.', '写一份报告。']], tags=['词根 port', '前缀 re']),
    w('support', '支持；支撑', 'v./n.', 'c7s2', '🤲', '/səˈpɔːt/', 'port', 'sup-', '表示“下”', 'support = sup-(下) + port(托) → 从下托住 = 支持。', '', [['support a friend', '支持朋友'], ['family support', '家庭支持']], [['We support you.', '我们支持你。'], ['They support the team.', '他们支持球队。']], tags=['词根 port']),
    w('portable', '便携的；可携带的', 'adj.', 'h1s2', '💼', '/ˈpɔːtəbl/', 'port', '-able', '表示“可…的”', 'portable = port + -able(可) → 可携带的。', '', [['a portable phone', '便携电话']], [['This computer is portable.', '这台电脑便携。']], tags=['词根 port']),
]
# spect 家族
NEW += [
    w('spectator', '观众', 'n.', 'c9s1', '👏', '/spekˈteɪtə(r)/', 'spect', '-ator', '表示人', 'spectator = spect(看) + -ator(人) → 观看的人 = 观众。', '', [['a spectator', '一名观众']], [['The spectators cheered.', '观众欢呼。']], tags=['词根 spect']),
    w('prospect', '前景；希望', 'n.', 'h2s1', '🔭', '/ˈprɒspekt/', 'spect', 'pro-', '表示“前”', 'prospect = pro-(前) + spect(看) → 向前看 = 前景。', '', [['good prospect', '好前景']], [['The prospect is good.', '前景不错。']], tags=['词根 spect', '前缀 pro']),
    w('suspect', '怀疑；猜想', 'v.', 'h2s1', '🤔', '/səˈspekt/', 'spect', 'sub-', '表示“下”', 'suspect = sub-(下) + spect(看) → 私下看 = 怀疑。', '', [['suspect a lie', '怀疑谎言']], [['I suspect he is late.', '我怀疑他迟到了。']], tags=['词根 spect', '前缀 sub']),
    w('spectacle', '景象；壮观', 'n.', 'h2s2', '🎆', '/ˈspektəkl/', 'spect', '-acle', '表示物', 'spectacle = spect + -acle → 看到的景象。', '', [['a grand spectacle', '壮观景象']], [['The show is a spectacle.', '演出很壮观。']], tags=['词根 spect']),
    w('perspective', '视角；观点', 'n.', 'h3s1', '📐', '/pəˈspektɪv/', 'spect', 'per-', '表示“透过”', 'perspective = per-(透过) + spect + -ive → 透看 = 视角。', '', [['from my perspective', '以我的视角']], [['We see it in perspective.', '我们客观看它。']], tags=['词根 spect', '前缀 per']),
    w('retrospect', '回顾；回想', 'n.', 'h3s2', '⏪', '/ˈretrəspekt/', 'spect', 'retro-', '表示“向后”', 'retrospect = retro-(后) + spect(看) → 向后看 = 回顾。', '', [['in retrospect', '回想起来']], [['In retrospect, it was right.', '回想起来那是对的。']], tags=['词根 spect', '前缀 retro']),
]
# scrib / script 家族
NEW += [
    w('script', '剧本；脚本', 'n.', 'c9s1', '📜', '/skrɪpt/', 'scrib', '', '', 'script = scrib(写) 的名词形 → 写好的本子 = 剧本。', '', [['a movie script', '电影剧本']], [['He wrote the script.', '他写了剧本。']], tags=['词根 scrib']),
    w('prescription', '处方；药方', 'n.', 'h2s1', '💊', '/prɪˈskrɪpʃn/', 'scrib', 'pre-', '表示“前”', 'prescription = pre-(前) + script(写) + -ion → 事先写好的 = 处方。', '', [['a prescription', '一张处方']], [['The doctor gave a prescription.', '医生开了处方。']], tags=['词根 scrib', '前缀 pre']),
    w('subscriber', '订阅者', 'n.', 'h2s2', '📰', '/səbˈskraɪbə(r)/', 'scrib', '-er', '表示人', 'subscriber = sub-(下) + scrib + -er(人) → 在名下写的人 = 订阅者。', '', [['a subscriber', '一名订阅者']], [['I am a subscriber.', '我是订阅者。']], tags=['词根 scrib']),
    w('transcript', '转录；文字稿', 'n.', 'h3s1', '📝', '/ˈtrænskrɪpt/', 'scrib', 'trans-', '表示“转”', 'transcript = trans-(转) + script → 转写下来的稿 = 文字稿。', '', [['a transcript', '一份文字稿']], [['We read the transcript.', '我们读文字稿。']], tags=['词根 scrib', '前缀 trans']),
]
# struct 家族
NEW += [
    w('structure', '结构；构造', 'n.', 'c8s2', '🏗️', '/ˈstrʌktʃə(r)/', 'struct', '-ure', '名词后缀', 'structure = struct(建) + -ure → 建成的东西 = 结构。', '', [['sentence structure', '句子结构']], [['The structure is clear.', '结构清晰。']], tags=['词根 struct']),
    w('construct', '建造；构建', 'v.', 'c9s1', '🔨', '/kənˈstrʌkt/', 'struct', 'con-', '表示“共同”', 'construct = con-(共同) + struct(建) → 搭建 = 建造。', '', [['construct a bridge', '建桥']], [['We construct a model.', '我们搭建模型。']], tags=['词根 struct', '前缀 con']),
    w('instruct', '指导；指示', 'v.', 'c9s1', '🧑‍🏫', '/ɪnˈstrʌkt/', 'struct', 'in-', '表示“内”', 'instruct = in-(内) + struct(建) → 把知识建入 = 指导。', '', [['instruct students', '指导学生']], [['He instructs us.', '他指导我们。']], tags=['词根 struct', '前缀 in']),
    w('instructor', '教练；讲师', 'n.', 'h1s1', '🎓', '/ɪnˈstrʌktə(r)/', 'struct', '-or', '表示人', 'instructor = instruct + -or(人) → 指导的人。', '', [['a driving instructor', '驾校教练']], [['The instructor is kind.', '教练很和蔼。']], tags=['词根 struct']),
    w('destroy', '破坏；摧毁', 'v.', 'c9s2', '💥', '/dɪˈstrɔɪ/', 'struct', 'de-', '表示“去掉”', 'destroy = de-(去掉) + stroy(struct 变体) → 拆掉建好的 = 破坏。', '', [['destroy the wall', '拆墙']], [['The storm destroyed houses.', '风暴摧毁了房屋。']], tags=['词根 struct', '前缀 de']),
    w('obstruct', '阻碍；阻挡', 'v.', 'h3s2', '🚧', '/əbˈstrʌkt/', 'struct', 'ob-', '表示“反”', 'obstruct = ob-(反) + struct → 挡住建造 = 阻碍。', '', [['obstruct the road', '挡路']], [['Do not obstruct.', '别挡路。']], tags=['词根 struct', '前缀 ob']),
]
# form 家族
NEW += [
    w('reform', '改革；改良', 'v./n.', 'c9s2', '🔧', '/rɪˈfɔːm/', 'form', 're-', '表示“再”', 'reform = re-(再) + form(形) → 重新成形 = 改革。', '', [['reform the plan', '改革计划']], [['We reform the school.', '我们改革学校。']], tags=['词根 form', '前缀 re']),
    w('transform', '使改变；转变', 'v.', 'c9s2', '🦋', '/trænsˈfɔːm/', 'form', 'trans-', '表示“转”', 'transform = trans-(转) + form → 变形 = 转变。', '', [['transform a idea', '转变想法']], [['Caterpillars transform.', '毛毛虫会蜕变。']], tags=['词根 form', '前缀 trans']),
    w('inform', '通知；告知', 'v.', 'c8s2', '📣', '/ɪnˈfɔːm/', 'form', 'in-', '表示“入”', 'inform = in-(入) + form → 把消息送入 = 通知。', '', [['inform me', '通知我']], [['Please inform us.', '请通知我们。']], tags=['词根 form', '前缀 in']),
    w('information', '信息；资料', 'n.', 'c7s2', 'ℹ️', '/ˌɪnfəˈmeɪʃn/', 'form', '-ation', '名词后缀', 'information = inform + -ation → 信息。', '', [['useful information', '有用信息']], [['We need information.', '我们需要信息。']], tags=['词根 form']),
    w('uniform', '制服；统一的', 'n./adj.', 'c8s1', '🥼', '/ˈjuːnɪfɔːm/', 'form', 'uni-', '表示“一”', 'uniform = uni-(一) + form → 同一形 = 制服/统一。', '', [['school uniform', '校服']], [['We wear uniform.', '我们穿制服。']], tags=['词根 form', '前缀 uni']),
    w('perform', '表演；执行', 'v.', 'c8s2', '🎤', '/pəˈfɔːm/', 'form', 'per-', '表示“通过”', 'perform = per-(通过) + form → 完成形式 = 表演/执行。', '', [['perform a song', '表演歌曲']], [['They perform on stage.', '他们在台上表演。']], tags=['词根 form', '前缀 per']),
    w('performance', '表演；表现', 'n.', 'c9s1', '🎭', '/pəˈfɔːməns/', 'form', '-ance', '名词后缀', 'performance = perform + -ance → 表演。', '', [['a good performance', '好表现']], [['The performance is great.', '表演很棒。']], tags=['词根 form']),
    w('conform', '遵守；符合', 'v.', 'h3s2', '✅', '/kənˈfɔːm/', 'form', 'con-', '表示“共同”', 'conform = con-(共同) + form → 同形 = 符合。', '', [['conform to rules', '遵守规则']], [['We conform to rules.', '我们遵守规则。']], tags=['词根 form', '前缀 con']),
    w('formula', '公式；配方', 'n.', 'h2s1', '🧪', '/ˈfɔːmjələ/', 'form', '', '', 'formula = form(形) + -ula → 固定的形式 = 公式。', '', [['a math formula', '数学公式']], [['We use the formula.', '我们用公式。']], tags=['词根 form']),
    w('formal', '正式的', 'adj.', 'h1s2', '🤵', '/ˈfɔːml/', 'form', '-al', '构成形容词', 'formal = form + -al → 形式的 = 正式的。', '', [['formal clothes', '正装']], [['This is a formal letter.', '这是正式信函。']], tags=['词根 form']),
]
# vent 家族
NEW += [
    w('invent', '发明；创造', 'v.', 'c8s2', '💡', '/ɪnˈvent/', 'vent', 'in-', '表示“入”', 'invent = in-(入) + vent(来) → 新东西来到 = 发明。', '', [['invent a machine', '发明机器']], [['He invented the light.', '他发明了电灯。']], tags=['词根 vent', '前缀 in']),
    w('invention', '发明（物）', 'n.', 'c9s1', '🔬', '/ɪnˈvenʃn/', 'vent', '-ion', '名词后缀', 'invention = invent + -ion → 发明(物)。', '', [['a great invention', '伟大发明']], [['The invention helps us.', '这项发明帮了我们。']], tags=['词根 vent']),
    w('event', '事件；活动', 'n.', 'c7s2', '📅', '/ɪˈvent/', 'vent', 'e-', '表示“出”', 'event = e-(出) + vent(来) → 出来的事 = 事件。', '', [['a big event', '大事件'], ['sports event', '体育活动']], [['The event is fun.', '活动很有趣。']], tags=['词根 vent']),
    w('prevent', '防止；预防', 'v.', 'c8s1', '🛡️', '/prɪˈvent/', 'vent', 'pre-', '表示“前”', 'prevent = pre-(前) + vent(来) → 在前挡住来 = 防止。', '', [['prevent accidents', '防止事故']], [['We prevent fire.', '我们防火。']], tags=['词根 vent', '前缀 pre']),
    w('adventure', '冒险；奇遇', 'n.', 'c8s2', '🗺️', '/ədˈventʃə(r)/', 'vent', 'ad-', '表示“朝”', 'adventure = ad-(朝) + vent + -ure → 走向未知 = 冒险。', '', [['a great adventure', '大冒险']], [['We love adventure.', '我们爱冒险。']], tags=['词根 vent', '前缀 ad']),
    w('convention', '大会；惯例', 'n.', 'h2s2', '🏛️', '/kənˈvenʃn/', 'vent', 'con-', '表示“共同”', 'convention = con-(共同) + vent + -ion → 大家来 = 会议。', '', [['a big convention', '大会']], [['The convention is held.', '大会召开了。']], tags=['词根 vent', '前缀 con']),
]
# press 家族
NEW += [
    w('pressure', '压力', 'n.', 'c8s2', '😐', '/ˈpreʃə(r)/', 'press', '-ure', '名词后缀', 'pressure = press + -ure → 压出来的 = 压力。', '', [['under pressure', '在压力下']], [['He feels pressure.', '他感到压力。']], tags=['词根 press']),
    w('express', '表达；表示', 'v.', 'c7s2', '💬', '/ɪkˈspres/', 'press', 'ex-', '表示“出”', 'express = ex-(出) + press(压) → 压出心声 = 表达。', '', [['express ideas', '表达想法']], [['He expressed his love.', '他表达了爱。']], tags=['词根 press', '前缀 ex']),
    w('expression', '表达；表情', 'n.', 'c9s1', '😊', '/ɪkˈspreʃn/', 'press', '-ion', '名词后缀', 'expression = express + -ion → 表达/表情。', '', [['a happy expression', '开心的表情']], [['Her expression changed.', '她的表情变了。']], tags=['词根 press']),
    w('impress', '给…留下印象', 'v.', 'c9s2', '🌟', '/ɪmˈpres/', 'press', 'im-', '表示“入”', 'impress = im-(入) + press → 压入脑海 = 留下印象。', '', [['impress the teacher', '给老师留印象']], [['He impressed us.', '他给我们留下印象。']], tags=['词根 press', '前缀 im']),
    w('impression', '印象', 'n.', 'c9s2', '👁️', '/ɪmˈpreʃn/', 'press', '-ion', '名词后缀', 'impression = impress + -ion → 印象。', '', [['a good impression', '好印象']], [['First impression matters.', '第一印象重要。']], tags=['词根 press']),
    w('suppress', '镇压；抑制', 'v.', 'h3s1', '🤫', '/səˈpres/', 'press', 'sub-', '表示“下”', 'suppress = sub-(下) + press → 压下 = 抑制。', '', [['suppress a laugh', '忍住笑']], [['He suppressed anger.', '他抑制怒气。']], tags=['词根 press', '前缀 sub']),
    w('compress', '压缩', 'v.', 'h2s2', '🗜️', '/kəmˈpres/', 'press', 'com-', '表示“共同”', 'compress = com-(共同) + press → 压在一起 = 压缩。', '', [['compress a file', '压缩文件']], [['We compress the air.', '我们压缩空气。']], tags=['词根 press', '前缀 com']),
    w('depress', '使沮丧；使萧条', 'v.', 'h3s1', '🌧️', '/dɪˈpres/', 'press', 'de-', '表示“下”', 'depress = de-(下) + press → 压下去 = 使沮丧。', '', [['depress the mood', '让心情低落']], [['Rain depresses me.', '下雨让我沮丧。']], tags=['词根 press', '前缀 de']),
]
# tract 家族
NEW += [
    w('contract', '合同；收缩', 'n./v.', 'h1s1', '📄', '/ˈkɒntrækt/', 'tract', 'con-', '表示“共同”', 'contract = con-(共同) + tract(拉) → 拉到一起 = 合同/收缩。', '', [['sign a contract', '签合同']], [['They signed a contract.', '他们签了合同。']], tags=['词根 tract', '前缀 con']),
    w('extract', '提取；摘录', 'v.', 'h2s1', '🧫', '/ɪkˈstrækt/', 'tract', 'ex-', '表示“出”', 'extract = ex-(出) + tract(拉) → 拉出 = 提取。', '', [['extract juice', '榨汁']], [['We extract oil.', '我们提取油。']], tags=['词根 tract', '前缀 ex']),
    w('subtract', '减去；扣除', 'v.', 'c7s2', '➖', '/səbˈtrækt/', 'tract', 'sub-', '表示“下”', 'subtract = sub-(下) + tract(拉) → 拉下 = 减去。', 'subtract 想成“往下拉走一些” = 减去。', [['subtract two', '减去二']], [['Subtract 2 from 5.', '5 减 2。']], tags=['词根 tract', '前缀 sub']),
    w('tractor', '拖拉机', 'n.', 'c8s1', '🚜', '/ˈtræktə(r)/', 'tract', '-or', '表示物', 'tractor = tract(拉) + -or(物) → 拉的车 = 拖拉机。', '', [['a red tractor', '红色拖拉机']], [['The tractor is big.', '拖拉机很大。']], tags=['词根 tract']),
    w('traction', '牵引；吸引力', 'n.', 'h3s2', '🪢', '/ˈtrækʃn/', 'tract', '-ion', '名词后缀', 'traction = tract + -ion → 牵引力。', '', [['lose traction', '失去抓地力']], [['The wheels need traction.', '轮子需要抓地力。']], tags=['词根 tract']),
]
# cept / cap 家族
NEW += [
    w('accept', '接受；同意', 'v.', 'c7s1', '✅', '/əkˈsept/', 'cept', 'ac-', '表示“朝”', 'accept = ac-(朝) + cept(取) → 取过来 = 接受。', '', [['accept a gift', '收礼物']], [['She accepted my help.', '她接受了我的帮助。']], tags=['词根 cept', '前缀 ac']),
    w('except', '除…之外', 'prep.', 'c8s1', '🚫', '/ɪkˈsept/', 'cept', 'ex-', '表示“出”', 'except = ex-(出) + cept(取) → 取出 = 除…外。', '', [['all except Tom', '除汤姆外全部']], [['Everyone came except him.', '除了他都来了。']], tags=['词根 cept', '前缀 ex']),
    w('concept', '概念；观念', 'n.', 'c9s2', '💭', '/ˈkɒnsept/', 'cept', 'con-', '表示“共同”', 'concept = con-(共同) + cept(取) → 取到一起 = 概念。', '', [['a new concept', '新概念']], [['This concept is clear.', '这个概念很清楚。']], tags=['词根 cept', '前缀 con']),
    w('reception', '接待；接收', 'n.', 'h1s1', '🛎️', '/rɪˈsepʃn/', 'cept', 're-', '表示“回”', 'reception = re-(回) + cept + -ion → 接收。', '', [['a warm reception', '热情接待']], [['The reception is good.', '接待很好。']], tags=['词根 cept', '前缀 re']),
    w('capture', '捕获；占领', 'v.', 'h2s1', '📸', '/ˈkæptʃə(r)/', 'cap', '-ure', '表示物', 'capture = cap(取) + -ure → 抓住 = 捕获。', '', [['capture a moment', '捕捉瞬间']], [['We captured the view.', '我们拍下风景。']], tags=['词根 cap']),
    w('escape', '逃跑；逃脱', 'v.', 'c8s2', '🏃', '/ɪˈskeɪp/', 'cap', 'ex-', '表示“出”', 'escape = ex-(出) + cap(罩) → 脱出罩子 = 逃跑。', '', [['escape danger', '逃离危险']], [['The bird escaped.', '鸟逃走了。']], tags=['词根 cap', '前缀 ex']),
    w('participate', '参加；参与', 'v.', 'h1s2', '🙋', '/pɑːˈtɪsɪpeɪt/', 'cip', 'part-', '表示“部分”', 'participate = part(部分) + cip(取) + -ate → 取一部分 = 参加。', '', [['participate in a game', '参加游戏']], [['We participate actively.', '我们积极参与。']], tags=['词根 cip']),
    w('capacity', '容量；能力', 'n.', 'h2s2', '🧺', '/kəˈpæsəti/', 'cap', '-ity', '名词后缀', 'capacity = cap(容) + -acity → 容量。', '', [['full capacity', '满容量']], [['The hall is at capacity.', '大厅满员。']], tags=['词根 cap']),
    w('anticipate', '预期；期待', 'v.', 'h3s1', '⏳', '/ænˈtɪsɪpeɪt/', 'cip', 'anti-', '表示“前”', 'anticipate = anti-(前) + cip(取) + -ate → 提前取 = 预期。', '', [['anticipate a result', '预期结果']], [['We anticipate good news.', '我们期待好消息。']], tags=['词根 cip', '前缀 anti']),
]
# mit / miss 家族
NEW += [
    w('permit', '允许；许可', 'v.', 'c8s2', '🉑', '/pəˈmɪt/', 'mit', 'per-', '表示“通过”', 'permit = per-(通过) + mit(送) → 放过去 = 允许。', '', [['permit smoking', '允许吸烟']], [['They permit it.', '他们允许。']], tags=['词根 mit', '前缀 per']),
    w('submit', '提交；屈服', 'v.', 'c9s2', '📨', '/səbˈmɪt/', 'mit', 'sub-', '表示“下”', 'submit = sub-(下) + mit(送) → 送上去 = 提交。', '', [['submit homework', '交作业']], [['We submit the form.', '我们提交表格。']], tags=['词根 mit', '前缀 sub']),
    w('transmit', '传送；传播', 'v.', 'h2s1', '📡', '/trænsˈmɪt/', 'mit', 'trans-', '表示“转”', 'transmit = trans-(转) + mit(送) → 转送 = 传送。', '', [['transmit a signal', '传送信号']], [['We transmit data.', '我们传送数据。']], tags=['词根 mit', '前缀 trans']),
    w('dismiss', '解散；解雇', 'v.', 'h1s2', '🚪', '/dɪsˈmɪs/', 'miss', 'dis-', '表示“分开”', 'dismiss = dis-(分开) + miss(送) → 送走 = 解散。', '', [['dismiss class', '下课']], [['The teacher dismissed us.', '老师让我们下课。']], tags=['词根 mit', '前缀 dis']),
    w('promise', '承诺；诺言', 'n./v.', 'c7s2', '🤝', '/ˈprɒmɪs/', 'miss', 'pro-', '表示“前”', 'promise = pro-(前) + miss(送) → 说出去的话 = 承诺。', '', [['keep a promise', '信守诺言']], [['He promised to help.', '他答应帮忙。']], tags=['词根 mit', '前缀 pro']),
    w('missile', '导弹；投射物', 'n.', 'h3s2', '🚀', '/ˈmɪsaɪl/', 'miss', '-ile', '表示物', 'missile = miss(送) + -ile → 发射物 = 导弹。', '', [['a missile', '一枚导弹']], [['The missile flew.', '导弹飞了。']], tags=['词根 mit']),
    w('admission', '准入；入场费', 'n.', 'h2s2', '🎟️', '/ədˈmɪʃn/', 'mit', 'ad-', '表示“朝”', 'admission = ad-(朝) + mit + -ion → 准许进入。', '', [['free admission', '免费入场']], [['Admission is free.', '免费入场。']], tags=['词根 mit', '前缀 ad']),
]
# vis / vid 家族
NEW += [
    w('visible', '可见的', 'adj.', 'c9s1', '👁️', '/ˈvɪzəbl/', 'vis', '-ible', '表示“可”', 'visible = vis(看) + -ible(可) → 可见的。', '', [['a visible star', '可见的星']], [['The star is visible.', '星星可见。']], tags=['词根 vis']),
    w('vision', '视力；视野', 'n.', 'c9s2', '👓', '/ˈvɪʒn/', 'vis', '', '', 'vision = vis(看) → 看的能力 = 视力/视野。', '', [['good vision', '好视力']], [['My vision is good.', '我视力好。']], tags=['词根 vis']),
    w('visit', '参观；拜访', 'v.', 'c7s1', '🚶', '/ˈvɪzɪt/', 'vis', '', '', 'visit = vis(看) + -it → 去看 = 拜访。', '', [['visit a friend', '拜访朋友'], ['visit Beijing', '游览北京']], [['We visit grandma.', '我们去看奶奶。'], ['They visited a museum.', '他们参观了博物馆。']], tags=['词根 vis']),
    w('visitor', '访客；游客', 'n.', 'c8s1', '🧳', '/ˈvɪzɪtə(r)/', 'vis', '-or', '表示人', 'visitor = visit + -or(人) → 访客。', '', [['a visitor', '一位访客']], [['We welcome visitors.', '我们欢迎访客。']], tags=['词根 vis']),
    w('video', '视频；录像', 'n.', 'c8s2', '📹', '/ˈvɪdiəʊ/', 'vid', '', '', 'video = vid(看) + -eo → 能看的 = 视频。', '', [['watch a video', '看视频']], [['We watch videos.', '我们看视频。']], tags=['词根 vid']),
    w('provide', '提供；供应', 'v.', 'c8s1', '🛒', '/prəˈvaɪd/', 'vid', 'pro-', '表示“前”', 'provide = pro-(前) + vid(看) + -e → 向前准备 = 提供。', '', [['provide food', '提供食物']], [['They provide help.', '他们提供帮助。']], tags=['词根 vid', '前缀 pro']),
    w('divide', '分；划分；除', 'v.', 'c8s2', '➗', '/dɪˈvaɪd/', 'vid', 'di-', '表示“分开”', 'divide = di-(分开) + vid(看) → 分开看 = 划分。', '', [['divide the cake', '分蛋糕']], [['Divide 10 by 2.', '10 除以 2。']], tags=['词根 vid', '前缀 di']),
    w('individual', '个人的；个体', 'adj./n.', 'h1s2', '🧍', '/ˌɪndɪˈvɪdʒuəl/', 'vid', 'in-', '表示“不”', 'individual = in-(不) + divid(分) + -ual → 不可再分 = 个人。', '', [['an individual', '一个个体']], [['Each individual counts.', '每个个体都重要。']], tags=['词根 vid', '前缀 in']),
    w('television', '电视', 'n.', 'c7s2', '📺', '/ˈtelɪvɪʒn/', 'vis', 'tele-', '表示“远”', 'television = tele-(远) + vis(看) + -ion → 远距离看 = 电视。', '', [['watch television', '看电视']], [['We watch television.', '我们看电视。']], tags=['词根 vis', '前缀 tele']),
]
# phon 家族
NEW += [
    w('phone', '电话；打电话', 'n./v.', 'c7s1', '📱', '/fəʊn/', 'phon', '', '', 'phone = phon(声) → 传声的工具 = 电话。', '', [['answer the phone', '接电话'], ['call by phone', '打电话']], [['She answered the phone.', '她接了电话。'], ['I phoned my mom.', '我给妈妈打电话。']], tags=['词根 phon']),
    w('telephone', '电话', 'n.', 'c7s2', '☎️', '/ˈtelɪfəʊn/', 'phon', 'tele-', '表示“远”', 'telephone = tele-(远) + phon(声) + -e → 远距离传声 = 电话。', '', [['a telephone', '一部电话']], [['He used a telephone.', '他用了电话。']], tags=['词根 phon', '前缀 tele']),
    w('microphone', '麦克风；话筒', 'n.', 'h1s1', '🎙️', '/ˈmaɪkrəfəʊn/', 'phon', 'micro-', '表示“小”', 'microphone = micro-(小) + phon(声) + -e → 放大微小声音 = 麦克风。', '', [['a microphone', '一支麦克风']], [['He spoke into the microphone.', '他对着麦克风说话。']], tags=['词根 phon', '前缀 micro']),
    w('headphone', '耳机', 'n.', 'h1s2', '🎧', '/ˈhedfəʊn/', 'phon', '', '', 'headphone = head(头) + phone(电话/声) → 头上的听声设备 = 耳机。', '', [['wear headphones', '戴耳机']], [['I wear headphones.', '我戴耳机。']], tags=['词根 phon']),
    w('phonetic', '语音的', 'adj.', 'h2s1', '🔤', '/fəˈnetɪk/', 'phon', '-ic', '构成形容词', 'phonetic = phon + -ic → 语音的。', '', [['phonetic symbol', '音标']], [['We learn phonetic symbols.', '我们学音标。']], tags=['词根 phon']),
    w('symphony', '交响乐', 'n.', 'h3s1', '🎻', '/ˈsɪmfəni/', 'phon', 'sym-', '表示“共同”', 'symphony = sym-(共同) + phon(声) + -y → 众声和鸣 = 交响乐。', '', [['a symphony', '一首交响乐']], [['We heard a symphony.', '我们听了一首交响乐。']], tags=['词根 phon', '前缀 sym']),
]
# bio / geo / tele 家族
NEW += [
    w('biology', '生物（学）', 'n.', 'c9s1', '🧬', '/baɪˈɒlədʒi/', 'bio', '-logy', '表示“学”', 'biology = bio(生命) + -logy(学) → 生物学。', '', [['study biology', '学生物']], [['Biology is fun.', '生物很有趣。']], tags=['词根 bio']),
    w('biography', '传记', 'n.', 'h2s2', '📖', '/baɪˈɒɡrəfi/', 'bio', 'graph', '表示“写”', 'biography = bio(生命) + graph(写) + -y → 写一生 = 传记。', '', [['a biography', '一本传记']], [['He read a biography.', '他读了一本传记。']], tags=['词根 bio', '词根 graph']),
    w('antibiotic', '抗生素', 'n.', 'h3s1', '💊', '/ˌæntibaɪˈɒtɪk/', 'bio', 'anti-', '表示“抗”', 'antibiotic = anti-(抗) + bio(生命) + -tic → 抗菌的 = 抗生素。', '', [['take antibiotics', '吃抗生素']], [['The antibiotic works.', '抗生素起效了。']], tags=['词根 bio', '前缀 anti']),
    w('geography', '地理（学）', 'n.', 'c8s1', '🗺️', '/dʒiˈɒɡrəfi/', 'geo', '-graphy', '表示“学”', 'geography = geo(地) + graphy(学) → 地理。', '', [['learn geography', '学地理']], [['Geography is useful.', '地理有用。']], tags=['词根 geo']),
    w('geology', '地质（学）', 'n.', 'h3s2', '⛰️', '/dʒiˈɒlədʒi/', 'geo', '-logy', '表示“学”', 'geology = geo(地) + -logy → 地质学。', '', [['study geology', '学地质']], [['Geology studies rocks.', '地质学研究岩石。']], tags=['词根 geo']),
    w('geometry', '几何（学）', 'n.', 'c9s2', '📐', '/dʒiˈɒmətri/', 'geo', '-metry', '表示“测量”', 'geometry = geo(地/量) + metry(测量) → 几何(测量)。', '', [['learn geometry', '学几何']], [['Geometry is hard.', '几何很难。']], tags=['词根 geo']),
    w('telescope', '望远镜', 'n.', 'c9s1', '🔭', '/ˈtelɪskəʊp/', 'tele', '-scope', '表示“看”', 'telescope = tele-(远) + scope(看) → 看远处 = 望远镜。', '', [['a telescope', '一台望远镜']], [['We look through a telescope.', '我们用望远镜看。']], tags=['前缀 tele']),
    w('telegraph', '电报', 'n.', 'h3s2', '📡', '/ˈtelɪɡrɑːf/', 'tele', '-graph', '表示“写”', 'telegraph = tele-(远) + graph(写) → 远距离写 = 电报。', '', [['send a telegraph', '发电报']], [['They sent a telegraph.', '他们发了电报。']], tags=['前缀 tele']),
    w('telecommunication', '电信', 'n.', 'h3s1', '📶', '/ˌtelikəˌmjuːnɪˈkeɪʃn/', 'tele', 'com-', '表示“共同”', 'telecommunication = tele-(远) + communication → 电信。', '', [['telecommunication', '电信']], [['We use telecommunication.', '我们用电信。']], tags=['前缀 tele']),
]
# inter / trans / pre / re / un 家族
NEW += [
    w('international', '国际的', 'adj.', 'c8s2', '🌍', '/ˌɪntəˈnæʃnəl/', 'inter', '-al', '构成形容词', 'international = inter-(之间) + nation + -al → 国家间的 = 国际的。', '', [['international day', '国际日']], [['This is an international school.', '这是国际学校。']], tags=['前缀 inter']),
    w('interview', '面试；采访', 'n./v.', 'c9s2', '🎙️', '/ˈɪntəvjuː/', 'inter', 'view', '表示“看”', 'interview = inter-(之间) + view(看) → 互相看 = 面试/采访。', '', [['a job interview', '工作面试']], [['We had an interview.', '我们进行了面试。']], tags=['前缀 inter']),
    w('internet', '互联网', 'n.', 'c7s2', '🌐', '/ˈɪntənet/', 'inter', 'net', '表示“网”', 'internet = inter-(之间) + net(网) → 互联的网。', '', [['surf the internet', '上网']], [['We use the internet.', '我们用互联网。']], tags=['前缀 inter']),
    w('interrupt', '打断；中断', 'v.', 'c9s2', '✋', '/ˌɪntəˈrʌpt/', 'rupt', 'inter-', '表示“之间”', 'interrupt = inter-(之间) + rupt(断) → 从中打断。', '', [['do not interrupt', '别打断']], [['Sorry to interrupt.', '抱歉打断。']], tags=['词根 rupt', '前缀 inter']),
    w('interpret', '口译；解释', 'v.', 'h2s1', '🗣️', '/ɪnˈtɜːprɪt/', 'pret', 'inter-', '表示“之间”', 'interpret = inter-(之间) + pret(说) → 在中间说 = 口译。', '', [['interpret for us', '为我们翻译']], [['He interprets the text.', '他解释文本。']], tags=['前缀 inter']),
    w('interfere', '干涉；打扰', 'v.', 'h3s1', '🚫', '/ˌɪntəˈfɪə(r)/', 'fer', 'inter-', '表示“之间”', 'interfere = inter-(之间) + fer(打) → 插手中间 = 干涉。', '', [['do not interfere', '别干涉']], [['Do not interfere.', '别插手。']], tags=['前缀 inter']),
    w('translate', '翻译', 'v.', 'c8s2', '🌐', '/trænsˈleɪt/', 'trans', '-late', '表示“带”', 'translate = trans-(转) + late(带) → 转带(语言) = 翻译。', '', [['translate a book', '翻译书']], [['We translate English.', '我们翻译英语。']], tags=['前缀 trans']),
    w('translation', '翻译；译文', 'n.', 'c9s1', '📝', '/trænsˈleɪʃn/', 'trans', '-ion', '名词后缀', 'translation = translate + -ion → 翻译。', '', [['a good translation', '好译文']], [['The translation is clear.', '译文清楚。']], tags=['前缀 trans']),
    w('transfer', '转移；调任', 'v.', 'h1s1', '🔄', '/trænsˈfɜː(r)/', 'trans', '-fer', '表示“运”', 'transfer = trans-(转) + fer(运) → 转运 = 转移。', '', [['transfer money', '转账']], [['We transfer to a new school.', '我们转到新学校。']], tags=['前缀 trans']),
    w('transparent', '透明的', 'adj.', 'h2s2', '🔍', '/trænsˈpærənt/', 'trans', '-parent', '表示“显现”', 'transparent = trans-(穿过) + parent(显现) → 透出 = 透明。', '', [['a transparent glass', '透明玻璃']], [['The glass is transparent.', '玻璃是透明的。']], tags=['前缀 trans']),
    w('prepare', '准备', 'v.', 'c7s2', '📝', '/prɪˈpeə(r)/', 'pre', '-pare', '表示“安排”', 'prepare = pre-(前) + pare(安排) → 提前安排 = 准备。', '', [['prepare lunch', '准备午饭']], [['We prepare for the exam.', '我们备考。']], tags=['前缀 pre']),
    w('predict', '预测', 'v.', 'c9s2', '🔮', '/prɪˈdɪkt/', 'dict', 'pre-', '表示“前”', 'predict = pre-(前) + dict(说) → 先说 = 预测。', '', [['predict the weather', '预测天气']], [['We predict rain.', '我们预测有雨。']], tags=['词根 dict', '前缀 pre']),
    w('present', '礼物；呈现；目前的', 'n./v./adj.', 'c8s1', '🎁', '/ˈpreznt/', 'pre', '-sent', '表示“在”', 'present = pre-(前) + sent(在) → 在面前的 = 礼物/呈现。', '', [['a birthday present', '生日礼物'], ['at present', '目前']], [['He gave a present.', '他送了礼物。']], tags=['前缀 pre']),
    w('pretend', '假装', 'v.', 'c7s2', '🎭', '/prɪˈtend/', 'pre', 'tend', '表示“伸”', 'pretend = pre-(前) + tend(伸) → 往前伸(装) = 假装。', '', [['pretend to sleep', '假装睡觉']], [['He pretends to be ill.', '他装病。']], tags=['前缀 pre']),
    w('prefix', '前缀', 'n.', 'h2s1', '🔠', '/ˈpriːfɪks/', 'pre', '-fix', '表示“固定”', 'prefix = pre-(前) + fix(固定) → 固定在前的 = 前缀。', '', [['a prefix', '一个前缀']], [['“un-” is a prefix.', '“un-”是前缀。']], tags=['前缀 pre']),
    w('prehistoric', '史前的', 'adj.', 'h3s2', '🦕', '/ˌpriːhɪˈstɒrɪk/', 'pre', '-historic', '表示“历史”', 'prehistoric = pre-(前) + historic → 史前的。', '', [['prehistoric animals', '史前动物']], [['Dinosaurs are prehistoric.', '恐龙是史前的。']], tags=['前缀 pre']),
    w('return', '返回；归还', 'v.', 'c7s1', '↩️', '/rɪˈtɜːn/', 're', '-turn', '表示“转”', 'return = re-(回) + turn(转) → 转回 = 返回。', '', [['return home', '回家']], [['We return the book.', '我们归还书。']], tags=['前缀 re']),
    w('review', '复习；评论', 'v./n.', 'c8s1', '📝', '/rɪˈvjuː/', 're', 'view', '表示“看”', 'review = re-(再) + view(看) → 再看 = 复习。', '', [['review lessons', '复习功课']], [['We review before exams.', '考前我们复习。']], tags=['前缀 re']),
    w('rewrite', '重写', 'v.', 'c8s2', '✍️', '/ˌriːˈraɪt/', 're', 'write', '表示“写”', 'rewrite = re-(再) + write → 重写。', '', [['rewrite the essay', '重写作文']], [['He rewrote the letter.', '他重写了信。']], tags=['前缀 re']),
    w('recall', '回忆；召回', 'v.', 'h1s2', '🧠', '/rɪˈkɔːl/', 're', 'call', '表示“叫”', 'recall = re-(再) + call(叫) → 再叫出 = 回忆。', '', [['recall a name', '想起名字']], [['I recall the day.', '我回忆那天。']], tags=['前缀 re']),
    w('receive', '收到；接待', 'v.', 'c7s2', '📬', '/rɪˈsiːv/', 'cept', 're-', '表示“回”', 'receive = re-(回) + ceiv(取) → 取回 = 收到。', '', [['receive a letter', '收到信']], [['We received a gift.', '我们收到礼物。']], tags=['词根 cept', '前缀 re']),
    w('reduce', '减少；降低', 'v.', 'c8s2', '📉', '/rɪˈdjuːs/', 're', '-duce', '表示“引”', 'reduce = re-(回) + duce(引) → 引回 = 减少。', '', [['reduce cost', '降低成本']], [['We reduce waste.', '我们减少浪费。']], tags=['前缀 re']),
    w('repeat', '重复；重说', 'v.', 'c7s1', '🔁', '/rɪˈpiːt/', 're', '-peat', '表示“说”', 'repeat = re-(再) + peat(说) → 再说 = 重复。', '', [['repeat after me', '跟我读']], [['Please repeat.', '请重复。']], tags=['前缀 re']),
    w('recover', '恢复；找回', 'v.', 'c9s1', '💪', '/rɪˈkʌvə(r)/', 're', 'cover', '表示“盖”', 'recover = re-(再) + cover(盖) → 重新盖好 = 恢复。', '', [['recover from illness', '病愈']], [['He recovered fast.', '他恢复得快。']], tags=['前缀 re']),
    w('unhappy', '不高兴的', 'adj.', 'c7s2', '😞', '/ʌnˈhæpi/', 'un', 'happy', '表示“不”', 'unhappy = un-(不) + happy → 不高兴的。', '', [['an unhappy face', '不快的脸']], [['She is unhappy.', '她不高兴。']], tags=['前缀 un']),
    w('unable', '不能的', 'adj.', 'c8s1', '🚫', '/ʌnˈeɪbl/', 'un', 'able', '表示“不”', 'unable = un-(不) + able(能) → 不能的。', '', [['unable to swim', '不会游泳']], [['He is unable to come.', '他不能来。']], tags=['前缀 un']),
    w('unusual', '不寻常的', 'adj.', 'c8s2', '🌟', '/ʌnˈjuːʒuəl/', 'un', 'usual', '表示“不”', 'unusual = un-(不) + usual(平常) → 不寻常的。', '', [['an unusual day', '不寻常的一天']], [['This is unusual.', '这不寻常。']], tags=['前缀 un']),
    w('unfair', '不公平的', 'adj.', 'c8s2', '⚖️', '/ʌnˈfeə(r)/', 'un', 'fair', '表示“不”', 'unfair = un-(不) + fair(公平) → 不公平的。', '', [['an unfair rule', '不公平的规则']], [['That is unfair.', '那不公平。']], tags=['前缀 un']),
    w('unreal', '不真实的', 'adj.', 'h1s1', '👻', '/ʌnˈrɪəl/', 'un', 'real', '表示“不”', 'unreal = un-(不) + real(真实) → 不真实的。', '', [['an unreal dream', '不真实的梦']], [['The scene is unreal.', '场景不真实。']], tags=['前缀 un']),
    w('unlock', '开锁；解锁', 'v.', 'h1s2', '🔓', '/ʌnˈlɒk/', 'un', 'lock', '表示“反”', 'unlock = un-(反) + lock(锁) → 开锁。', '', [['unlock the door', '开门锁']], [['He unlocked the phone.', '他解锁了手机。']], tags=['前缀 un']),
    w('unkind', '不友善的', 'adj.', 'c8s1', '😠', '/ʌnˈkaɪnd/', 'un', 'kind', '表示“不”', 'unkind = un-(不) + kind(友善) → 不友善的。', '', [['an unkind word', '不友善的话']], [['Do not be unkind.', '别不友善。']], tags=['前缀 un']),
    w('unsafe', '不安全的', 'adj.', 'c8s2', '⚠️', '/ʌnˈseɪf/', 'un', 'safe', '表示“不”', 'unsafe = un-(不) + safe(安全) → 不安全的。', '', [['an unsafe road', '不安全的路']], [['This is unsafe.', '这不安全。']], tags=['前缀 un']),
]
# 后缀家族（-ness/-ment/-tion/-ful/-less/-able/-ous/-ive/-al/-ly）
NEW += [
    w('happiness', '幸福；快乐', 'n.', 'c7s2', '😊', '/ˈhæpinəs/', 'happy', '-ness', '名词后缀', 'happiness = happy + -ness(名词) → 幸福。', '', [['find happiness', '找到幸福']], [['Happiness is key.', '幸福是关键。']], tags=['后缀 -ness']),
    w('illness', '疾病', 'n.', 'c8s1', '🤒', '/ˈɪlnəs/', 'ill', '-ness', '名词后缀', 'illness = ill + -ness → 疾病。', '', [['a serious illness', '重病']], [['He recovered from illness.', '他病愈了。']], tags=['后缀 -ness']),
    w('kindness', '善良；好意', 'n.', 'c8s2', '💗', '/ˈkaɪndnəs/', 'kind', '-ness', '名词后缀', 'kindness = kind + -ness → 善良。', '', [['show kindness', '表现善意']], [['Her kindness moved me.', '她的善良打动了我。']], tags=['后缀 -ness']),
    w('development', '发展；开发', 'n.', 'c9s1', '📈', '/dɪˈveləpmənt/', 'develop', '-ment', '名词后缀', 'development = develop + -ment → 发展。', '', [['economic development', '经济发展']], [['The development is fast.', '发展很快。']], tags=['后缀 -ment']),
    w('movement', '运动；移动', 'n.', 'c9s2', '🚶', '/ˈmuːvmənt/', 'move', '-ment', '名词后缀', 'movement = move + -ment → 运动。', '', [['a dance movement', '舞蹈动作']], [['The movement is slow.', '移动缓慢。']], tags=['后缀 -ment']),
    w('government', '政府', 'n.', 'c9s2', '🏛️', '/ˈɡʌvənmənt/', 'govern', '-ment', '名词后缀', 'government = govern + -ment → 政府。', '', [['the government', '政府']], [['The government helps.', '政府提供帮助。']], tags=['后缀 -ment']),
    w('agreement', '协议；一致', 'n.', 'h1s1', '🤝', '/əˈɡriːmənt/', 'agree', '-ment', '名词后缀', 'agreement = agree + -ment → 协议。', '', [['sign an agreement', '签协议']], [['We reached an agreement.', '我们达成一致。']], tags=['后缀 -ment']),
    w('education', '教育', 'n.', 'c8s2', '🎓', '/ˌedʒuˈkeɪʃn/', 'educate', '-tion', '名词后缀', 'education = educate + -tion → 教育。', '', [['good education', '好教育']], [['Education is important.', '教育很重要。']], tags=['后缀 -tion']),
    w('invitation', '邀请；请柬', 'n.', 'c9s1', '✉️', '/ˌɪnvɪˈteɪʃn/', 'invite', '-tion', '名词后缀', 'invitation = invite + -tion → 邀请。', '', [['an invitation', '一份邀请']], [['We got an invitation.', '我们收到邀请。']], tags=['后缀 -tion']),
    w('attention', '注意；关注', 'n.', 'c8s1', '👀', '/əˈtenʃn/', 'attend', '-tion', '名词后缀', 'attention = attend + -tion → 注意。', '', [['pay attention', '注意']], [['Pay attention in class.', '课上要注意。']], tags=['后缀 -tion']),
    w('information', '信息', 'n.', 'c7s2', 'ℹ️', '/ˌɪnfəˈmeɪʃn/', 'inform', '-ation', '名词后缀', 'information = inform + -ation → 信息。', '', [['useful information', '有用信息']], [['We need information.', '我们需要信息。']], tags=['后缀 -tion']),
    w('careful', '小心的；仔细的', 'adj.', 'c7s1', '🧐', '/ˈkeəfl/', 'care', '-ful', '表示“充满”', 'careful = care + -ful(充满) → 小心的。', '', [['be careful', '小心']], [['Be careful on the road.', '路上小心。']], tags=['后缀 -ful']),
    w('helpful', '有帮助的', 'adj.', 'c7s2', '🤝', '/ˈhelpfl/', 'help', '-ful', '表示“充满”', 'helpful = help + -ful → 有帮助的。', '', [['a helpful friend', '有帮助的朋友']], [['You are helpful.', '你很有帮助。']], tags=['后缀 -ful']),
    w('beautiful', '美丽的', 'adj.', 'c7s1', '🌸', '/ˈbjuːtɪfl/', 'beauty', '-ful', '表示“充满”', 'beautiful = beauty + -ful → 美丽的。', '', [['a beautiful flower', '美丽的花']], [['The park is beautiful.', '公园很美。']], tags=['后缀 -ful']),
    w('wonderful', '精彩的；极好的', 'adj.', 'c7s2', '✨', '/ˈwʌndəfl/', 'wonder', '-ful', '表示“充满”', 'wonderful = wonder + -ful → 精彩的。', '', [['a wonderful day', '美好的一天']], [['The show is wonderful.', '演出精彩。']], tags=['后缀 -ful']),
    w('careless', '粗心的', 'adj.', 'c8s1', '😶', '/ˈkeələs/', 'care', '-less', '表示“无”', 'careless = care + -less(无) → 粗心的。', '', [['a careless mistake', '粗心的错']], [['He is careless.', '他很粗心。']], tags=['后缀 -less']),
    w('homeless', '无家可归的', 'adj.', 'c9s2', '🏚️', '/ˈhəʊmləs/', 'home', '-less', '表示“无”', 'homeless = home + -less → 无家的。', '', [['a homeless cat', '流浪猫']], [['We help homeless people.', '我们帮无家者。']], tags=['后缀 -less']),
    w('useless', '无用的', 'adj.', 'c9s1', '🗑️', '/ˈjuːsləs/', 'use', '-less', '表示“无”', 'useless = use + -less → 无用的。', '', [['a useless tool', '无用的工具']], [['This is useless.', '这没用。']], tags=['后缀 -less']),
    w('comfortable', '舒适的', 'adj.', 'c8s1', '🛋️', '/ˈkʌmftəbl/', 'comfort', '-able', '表示“可”', 'comfortable = comfort + -able → 舒适的。', '', [['a comfortable bed', '舒服的床']], [['The chair is comfortable.', '椅子很舒服。']], tags=['后缀 -able']),
    w('suitable', '合适的', 'adj.', 'c9s2', '✅', '/ˈsuːtəbl/', 'suit', '-able', '表示“可”', 'suitable = suit + -able → 合适的。', '', [['a suitable gift', '合适的礼物']], [['This is suitable.', '这合适。']], tags=['后缀 -able']),
    w('readable', '可读的', 'adj.', 'h1s1', '📖', '/ˈriːdəbl/', 'read', '-able', '表示“可”', 'readable = read + -able → 可读的。', '', [['a readable book', '好读的书']], [['The text is readable.', '文本好读。']], tags=['后缀 -able']),
    w('dangerous', '危险的', 'adj.', 'c7s2', '⚠️', '/ˈdeɪndʒərəs/', 'danger', '-ous', '构成形容词', 'dangerous = danger + -ous → 危险的。', '', [['a dangerous road', '危险的路']], [['Be careful, it is dangerous.', '小心，危险。']], tags=['后缀 -ous']),
    w('famous', '著名的', 'adj.', 'c8s1', '🌟', '/ˈfeɪməs/', 'fame', '-ous', '构成形容词', 'famous = fame(名声) + -ous → 著名的。', '', [['a famous actor', '著名演员']], [['He is famous.', '他很有名。']], tags=['后缀 -ous']),
    w('poisonous', '有毒的', 'adj.', 'h2s1', '☠️', '/ˈpɔɪzənəs/', 'poison', '-ous', '构成形容词', 'poisonous = poison + -ous → 有毒的。', '', [['a poisonous snake', '毒蛇']], [['The mushroom is poisonous.', '蘑菇有毒。']], tags=['后缀 -ous']),
    w('creative', '有创造力的', 'adj.', 'c9s2', '🎨', '/kriˈeɪtɪv/', 'create', '-ive', '构成形容词', 'creative = create + -ive → 有创造力的。', '', [['a creative idea', '有创意的想法']], [['She is creative.', '她有创造力。']], tags=['后缀 -ive']),
    w('productive', '多产的；高效的', 'adj.', 'h2s2', '🌾', '/prəˈdʌktɪv/', 'product', '-ive', '构成形容词', 'productive = product + -ive → 多产的。', '', [['a productive day', '高效的一天']], [['We had a productive meeting.', '会议高效。']], tags=['后缀 -ive']),
    w('national', '国家的；民族的', 'adj.', 'c8s2', '🇨🇳', '/ˈnæʃnəl/', 'nation', '-al', '构成形容词', 'national = nation + -al → 国家的。', '', [['national flag', '国旗']], [['We love our national flag.', '我们爱国旗。']], tags=['后缀 -al']),
    w('natural', '自然的；天然的', 'adj.', 'c8s1', '🌿', '/ˈnætʃrəl/', 'nature', '-al', '构成形容词', 'natural = nature + -al → 自然的。', '', [['natural beauty', '自然美']], [['This is natural.', '这很自然。']], tags=['后缀 -al']),
    w('personal', '个人的', 'adj.', 'c9s1', '🧍', '/ˈpɜːsənl/', 'person', '-al', '构成形容词', 'personal = person + -al → 个人的。', '', [['personal space', '个人空间']], [['This is my personal view.', '这是我个人看法。']], tags=['后缀 -al']),
    w('quickly', '快速地', 'adv.', 'c7s1', '💨', '/ˈkwɪkli/', 'quick', '-ly', '副词后缀', 'quickly = quick + -ly → 快速地。', '', [['run quickly', '快跑']], [['He runs quickly.', '他跑得快。']], tags=['后缀 -ly']),
    w('slowly', '缓慢地', 'adv.', 'c7s1', '🐢', '/ˈsləʊli/', 'slow', '-ly', '副词后缀', 'slowly = slow + -ly → 缓慢地。', '', [['walk slowly', '慢走']], [['She walks slowly.', '她走得慢。']], tags=['后缀 -ly']),
    w('happily', '快乐地', 'adv.', 'c8s1', '😄', '/ˈhæpɪli/', 'happy', '-ly', '副词后缀', 'happily = happy + -ly → 快乐地。', '', [['live happily', '快乐生活']], [['They lived happily.', '他们快乐生活。']], tags=['后缀 -ly']),
    w('badly', '糟糕地；严重地', 'adv.', 'c8s2', '💢', '/ˈbædli/', 'bad', '-ly', '副词后缀', 'badly = bad + -ly → 糟糕地。', '', [['hurt badly', '伤得重']], [['He played badly.', '他打得差。']], tags=['后缀 -ly']),
]

# ============================== 各年级常用主题词（补体量） ==============================
# 小学三上
NEW += [
    w('one', '一', 'num.', 'g3s1', '1️⃣', '', root='', tags=['数字']),
    w('two', '二', 'num.', 'g3s1', '2️⃣', '', tags=['数字']),
    w('three', '三', 'num.', 'g3s1', '3️⃣', '', tags=['数字']),
    w('four', '四', 'num.', 'g3s1', '4️⃣', '', tags=['数字']),
    w('five', '五', 'num.', 'g3s1', '5️⃣', '', tags=['数字']),
    w('head', '头', 'n.', 'g3s1', '🤕', '', tags=['身体']),
    w('hand', '手', 'n.', 'g3s1', '✋', '', tags=['身体']),
    w('leg', '腿', 'n.', 'g3s1', '🦵', '', tags=['身体']),
    w('arm', '手臂', 'n.', 'g3s1', '💪', '', tags=['身体']),
    w('foot', '脚', 'n.', 'g3s1', '🦶', '', tags=['身体']),
    w('happy', '高兴的', 'adj.', 'g3s1', '😊', '', tags=['情绪']),
    w('sad', '伤心的', 'adj.', 'g3s1', '😢', '', tags=['情绪']),
    w('big', '大的', 'adj.', 'g3s1', '🐘', '', tags=['外貌'], forms={'comparative': 'bigger', 'superlative': 'biggest'}),
    w('small', '小的', 'adj.', 'g3s1', '🐭', '', tags=['外貌'], forms={'comparative': 'smaller', 'superlative': 'smallest'}),
    w('open', '打开', 'v.', 'g3s1', '🔓', '', tags=['动作']),
    w('close', '关上', 'v.', 'g3s1', '🔒', '', tags=['动作']),
    w('run', '跑', 'v.', 'g3s1', '🏃', '', tags=['动作'], forms={'past': 'ran', 'pastParticiple': 'run'}),
    w('jump', '跳', 'v.', 'g3s1', '🦘', '', tags=['动作']),
    w('eat', '吃', 'v.', 'g3s1', '🍎', '', tags=['动作'], forms={'past': 'ate', 'pastParticiple': 'eaten'}),
    w('drink', '喝', 'v.', 'g3s1', '🥤', '', tags=['动作'], forms={'past': 'drank', 'pastParticiple': 'drunk'}),
    w('sleep', '睡觉', 'v.', 'g3s1', '😴', '', tags=['动作'], forms={'past': 'slept', 'pastParticiple': 'slept'}),
]
# 小学三下
NEW += [
    w('six', '六', 'num.', 'g3s2', '6️⃣', '', tags=['数字']),
    w('seven', '七', 'num.', 'g3s2', '7️⃣', '', tags=['数字']),
    w('eight', '八', 'num.', 'g3s2', '8️⃣', '', tags=['数字']),
    w('nine', '九', 'num.', 'g3s2', '9️⃣', '', tags=['数字']),
    w('ten', '十', 'num.', 'g3s2', '🔟', '', tags=['数字']),
    w('rice', '米饭', 'n.', 'g3s2', '🍚', '', tags=['食物']),
    w('egg', '蛋', 'n.', 'g3s2', '🥚', '', tags=['食物']),
    w('milk', '牛奶', 'n.', 'g3s2', '🥛', '', tags=['食物']),
    w('bread', '面包', 'n.', 'g3s2', '🍞', '', tags=['食物']),
    w('meat', '肉', 'n.', 'g3s2', '🍖', '', tags=['食物']),
    w('fish', '鱼', 'n.', 'g3s2', '🐟', '', tags=['食物']),
    w('old', '老的；旧的', 'adj.', 'g3s2', '👴', '', tags=['外貌'], forms={'comparative': 'older', 'superlative': 'oldest'}),
    w('young', '年轻的', 'adj.', 'g3s2', '👶', '', tags=['外貌'], forms={'comparative': 'younger', 'superlative': 'youngest'}),
    w('long', '长的', 'adj.', 'g3s2', '📏', '', tags=['外貌'], forms={'comparative': 'longer', 'superlative': 'longest'}),
    w('warm', '温暖的', 'adj.', 'g3s2', '🔥', '', tags=['天气'], forms={'comparative': 'warmer', 'superlative': 'warmest'}),
    w('cold', '冷的', 'adj.', 'g3s2', '❄️', '', tags=['天气'], forms={'comparative': 'colder', 'superlative': 'coldest'}),
    w('play', '玩；演奏', 'v.', 'g3s2', '⚽', '', tags=['动作']),
    w('sing', '唱歌', 'v.', 'g3s2', '🎤', '', tags=['动作'], forms={'past': 'sang', 'pastParticiple': 'sung'}),
    w('dance', '跳舞', 'v.', 'g3s2', '💃', '', tags=['动作']),
    w('read', '读', 'v.', 'g3s2', '📖', '', tags=['动作'], forms={'past': 'read（/red/）'}),
    w('write', '写', 'v.', 'g3s2', '✍️', '', tags=['动作'], forms={'past': 'wrote', 'pastParticiple': 'written'}),
]
# 小学四上
NEW += [
    w('window', '窗户', 'n.', 'g4s1', '🪟', '', tags=['物品']),
    w('door', '门', 'n.', 'g4s1', '🚪', '', tags=['物品']),
    w('desk', '书桌', 'n.', 'g4s1', '🗄️', '', tags=['物品']),
    w('chair', '椅子', 'n.', 'g4s1', '🪑', '', tags=['物品']),
    w('phone', '电话', 'n.', 'g4s1', '📱', '', tags=['物品']),
    w('computer', '电脑', 'n.', 'g4s1', '💻', '', tags=['物品']),
    w('English', '英语', 'n./adj.', 'g4s1', '🔤', '', tags=['学科']),
    w('math', '数学', 'n.', 'g4s1', '➗', '', tags=['学科']),
    w('music', '音乐', 'n.', 'g4s1', '🎵', '', tags=['学科']),
    w('art', '美术', 'n.', 'g4s1', '🎨', '', tags=['学科']),
    w('PE', '体育', 'n.', 'g4s1', '🏀', '', tags=['学科']),
    w('science', '科学', 'n.', 'g4s1', '🔬', '', tags=['学科']),
    w('strong', '强壮的', 'adj.', 'g4s1', '💪', '', tags=['外貌'], forms={'comparative': 'stronger', 'superlative': 'strongest'}),
    w('weak', '虚弱的', 'adj.', 'g4s1', '🥀', '', tags=['外貌'], forms={'comparative': 'weaker', 'superlative': 'weakest'}),
    w('clean', '干净的', 'adj.', 'g4s1', '🧼', '', tags=['状态'], forms={'comparative': 'cleaner', 'superlative': 'cleanest'}),
    w('dirty', '脏的', 'adj.', 'g4s1', '🪥', '', tags=['状态'], forms={'comparative': 'dirtier', 'superlative': 'dirtiest'}),
    w('walk', '走路', 'v.', 'g4s1', '🚶', '', tags=['动作']),
    w('swim', '游泳', 'v.', 'g4s1', '🏊', '', tags=['动作'], forms={'past': 'swam', 'pastParticiple': 'swum'}),
    w('ride', '骑', 'v.', 'g4s1', '🚲', '', tags=['动作'], forms={'past': 'rode', 'pastParticiple': 'ridden'}),
    w('fly', '飞', 'v.', 'g4s1', '✈️', '', tags=['动作'], forms={'past': 'flew', 'pastParticiple': 'flown'}),
    w('draw', '画', 'v.', 'g4s1', '🖍️', '', tags=['动作'], forms={'past': 'drew', 'pastParticiple': 'drawn'}),
]
# 小学四下
NEW += [
    w('Monday', '星期一', 'n.', 'g4s2', '1️⃣', '', tags=['时间']),
    w('Tuesday', '星期二', 'n.', 'g4s2', '2️⃣', '', tags=['时间']),
    w('Thursday', '星期四', 'n.', 'g4s2', '4️⃣', '', tags=['时间']),
    w('Friday', '星期五', 'n.', 'g4s2', '5️⃣', '', tags=['时间']),
    w('Saturday', '星期六', 'n.', 'g4s2', '6️⃣', '', tags=['时间']),
    w('Sunday', '星期日', 'n.', 'g4s2', '7️⃣', '', tags=['时间']),
    w('spring', '春天', 'n.', 'g4s2', '🌸', '', tags=['季节']),
    w('summer', '夏天', 'n.', 'g4s2', '☀️', '', tags=['季节']),
    w('autumn', '秋天', 'n.', 'g4s2', '🍂', '', tags=['季节']),
    w('winter', '冬天', 'n.', 'g4s2', '⛄', '', tags=['季节']),
    w('hot', '热的', 'adj.', 'g4s2', '🔥', '', tags=['天气'], forms={'comparative': 'hotter', 'superlative': 'hottest'}),
    w('cool', '凉爽的', 'adj.', 'g4s2', '🍃', '', tags=['天气'], forms={'comparative': 'cooler', 'superlative': 'coolest'}),
    w('bus', '公共汽车', 'n.', 'g4s2', '🚌', '', tags=['交通']),
    w('car', '汽车', 'n.', 'g4s2', '🚗', '', tags=['交通']),
    w('train', '火车', 'n.', 'g4s2', '🚆', '', tags=['交通']),
    w('bike', '自行车', 'n.', 'g4s2', '🚲', '', tags=['交通']),
    w('help', '帮助', 'v./n.', 'g4s2', '🤝', '', tags=['动作']),
    w('learn', '学习', 'v.', 'g4s2', '📚', '', tags=['动作'], forms={'past': 'learnt/learned', 'pastParticiple': 'learnt/learned'}),
    w('study', '学习；研究', 'v.', 'g4s2', '📖', '', tags=['动作'], forms={'past': 'studied', 'pastParticiple': 'studied'}),
    w('think', '想；认为', 'v.', 'g4s2', '🤔', '', tags=['思维'], forms={'past': 'thought', 'pastParticiple': 'thought'}),
    w('know', '知道', 'v.', 'g4s2', '💡', '', tags=['思维'], forms={'past': 'knew', 'pastParticiple': 'known'}),
]
# 小学五上
NEW += [
    w('cow', '奶牛', 'n.', 'g5s1', '🐄', '', tags=['动物']),
    w('horse', '马', 'n.', 'g5s1', '🐴', '', tags=['动物']),
    w('sheep', '绵羊', 'n.', 'g5s1', '🐑', '', tags=['动物']),
    w('pig', '猪', 'n.', 'g5s1', '🐷', '', tags=['动物']),
    w('hen', '母鸡', 'n.', 'g5s1', '🐔', '', tags=['动物']),
    w('rabbit', '兔子', 'n.', 'g5s1', '🐰', '', tags=['动物']),
    w('tree', '树', 'n.', 'g5s1', '🌳', '', tags=['自然']),
    w('flower', '花', 'n.', 'g5s1', '🌼', '', tags=['自然']),
    w('grass', '草', 'n.', 'g5s1', '🌱', '', tags=['自然']),
    w('river', '河', 'n.', 'g5s1', '🏞️', '', tags=['自然']),
    w('mountain', '山', 'n.', 'g5s1', '⛰️', '', tags=['自然']),
    w('lake', '湖', 'n.', 'g5s1', '🏞️', '', tags=['自然']),
    w('shirt', '衬衫', 'n.', 'g5s1', '👕', '', tags=['衣物']),
    w('coat', '外套', 'n.', 'g5s1', '🧥', '', tags=['衣物']),
    w('shoe', '鞋', 'n.', 'g5s1', '👟', '', tags=['衣物']),
    w('hat', '帽子', 'n.', 'g5s1', '🎩', '', tags=['衣物']),
    w('buy', '买', 'v.', 'g5s1', '🛒', '', tags=['动作'], forms={'past': 'bought', 'pastParticiple': 'bought'}),
    w('sell', '卖', 'v.', 'g5s1', '💰', '', tags=['动作'], forms={'past': 'sold', 'pastParticiple': 'sold'}),
    w('give', '给', 'v.', 'g5s1', '🎁', '', tags=['动作'], forms={'past': 'gave', 'pastParticiple': 'given'}),
    w('take', '拿；带', 'v.', 'g5s1', '✋', '', tags=['动作'], forms={'past': 'took', 'pastParticiple': 'taken'}),
    w('make', '制作；使', 'v.', 'g5s1', '🔧', '', tags=['动作'], forms={'past': 'made', 'pastParticiple': 'made'}),
]
# 小学五下
NEW += [
    w('January', '一月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('February', '二月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('March', '三月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('April', '四月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('May', '五月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('June', '六月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('July', '七月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('August', '八月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('September', '九月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('October', '十月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('November', '十一月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('December', '十二月', 'n.', 'g5s2', '🗓️', '', tags=['时间']),
    w('weather', '天气', 'n.', 'g5s2', '🌤️', '', tags=['天气']),
    w('wind', '风', 'n.', 'g5s2', '🌬️', '', tags=['天气']),
    w('rain', '雨；下雨', 'n./v.', 'g5s2', '🌧️', '', tags=['天气']),
    w('snow', '雪；下雪', 'n./v.', 'g5s2', '❄️', '', tags=['天气']),
    w('cloud', '云', 'n.', 'g5s2', '☁️', '', tags=['天气']),
    w('meet', '遇见；见面', 'v.', 'g5s2', '🤝', '', tags=['动作'], forms={'past': 'met', 'pastParticiple': 'met'}),
    w('say', '说', 'v.', 'g5s2', '🗣️', '', tags=['动作'], forms={'past': 'said', 'pastParticiple': 'said'}),
    w('come', '来', 'v.', 'g5s2', '👉', '', tags=['动作'], forms={'past': 'came', 'pastParticiple': 'come'}),
    w('go', '去', 'v.', 'g5s2', '🚶', '', tags=['动作'], forms={'past': 'went', 'pastParticiple': 'gone'}),
    w('do', '做', 'v.', 'g5s2', '✅', '', tags=['动作'], forms={'past': 'did', 'pastParticiple': 'done'}),
]
# 小学六上
NEW += [
    w('map', '地图', 'n.', 'g6s1', '🗺️', '', tags=['物品']),
    w('camera', '相机', 'n.', 'g6s1', '📷', '', tags=['物品']),
    w('gift', '礼物', 'n.', 'g6s1', '🎁', '', tags=['物品']),
    w('key', '钥匙', 'n.', 'g6s1', '🔑', '', tags=['物品']),
    w('clock', '钟', 'n.', 'g6s1', '🕰️', '', tags=['物品']),
    w('money', '钱', 'n.', 'g6s1', '💵', '', tags=['物品']),
    w('high', '高的', 'adj.', 'g6s1', '🗼', '', tags=['外貌'], forms={'comparative': 'higher', 'superlative': 'highest'}),
    w('low', '低的', 'adj.', 'g6s1', '🔻', '', tags=['外貌'], forms={'comparative': 'lower', 'superlative': 'lowest'}),
    w('fast', '快的', 'adj./adv.', 'g6s1', '⚡', '', tags=['外貌'], forms={'comparative': 'faster', 'superlative': 'fastest'}),
    w('slow', '慢的', 'adj.', 'g6s1', '🐢', '', tags=['外貌'], forms={'comparative': 'slower', 'superlative': 'slowest'}),
    w('easy', '容易的', 'adj.', 'g6s1', '😌', '', tags=['状态'], forms={'comparative': 'easier', 'superlative': 'easiest'}),
    w('hard', '难的；硬的', 'adj.', 'g6s1', '🪨', '', tags=['状态'], forms={'comparative': 'harder', 'superlative': 'hardest'}),
    w('loud', '大声的', 'adj.', 'g6s1', '📢', '', tags=['状态'], forms={'comparative': 'louder', 'superlative': 'loudest'}),
    w('quiet', '安静的', 'adj.', 'g6s1', '🤫', '', tags=['状态'], forms={'comparative': 'quieter', 'superlative': 'quietest'}),
    w('love', '爱；喜爱', 'v./n.', 'g6s1', '❤️', '', tags=['情绪']),
    w('like', '喜欢', 'v.', 'g6s1', '👍', '', tags=['情绪']),
    w('hate', '讨厌', 'v.', 'g6s1', '👎', '', tags=['情绪']),
    w('want', '想要', 'v.', 'g6s1', '🙏', '', tags=['思维']),
    w('need', '需要', 'v./n.', 'g6s1', '🆘', '', tags=['思维']),
    w('find', '找到', 'v.', 'g6s1', '🔎', '', tags=['动作'], forms={'past': 'found', 'pastParticiple': 'found'}),
]
# 小学六下
NEW += [
    w('build', '建造', 'v.', 'g6s2', '🏗️', '', tags=['动作'], forms={'past': 'built', 'pastParticiple': 'built'}),
    w('break', '打破', 'v.', 'g6s2', '💔', '', tags=['动作'], forms={'past': 'broke', 'pastParticiple': 'broken'}),
    w('bring', '带来', 'v.', 'g6s2', '🎒', '', tags=['动作'], forms={'past': 'brought', 'pastParticiple': 'brought'}),
    w('catch', '抓住；接住', 'v.', 'g6s2', '🤾', '', tags=['动作'], forms={'past': 'caught', 'pastParticiple': 'caught'}),
    w('cut', '切；剪', 'v.', 'g6s2', '✂️', '', tags=['动作'], forms={'past': 'cut', 'pastParticiple': 'cut'}),
    w('feel', '感觉', 'v.', 'g6s2', '🤗', '', tags=['思维'], forms={'past': 'felt', 'pastParticiple': 'felt'}),
    w('get', '得到；变得', 'v.', 'g6s2', '🎯', '', tags=['动作'], forms={'past': 'got', 'pastParticiple': 'got/gotten'}),
    w('grow', '生长；种植', 'v.', 'g6s2', '🌱', '', tags=['动作'], forms={'past': 'grew', 'pastParticiple': 'grown'}),
    w('keep', '保持', 'v.', 'g6s2', '🔒', '', tags=['动作'], forms={'past': 'kept', 'pastParticiple': 'kept'}),
    w('leave', '离开；留下', 'v.', 'g6s2', '🚪', '', tags=['动作'], forms={'past': 'left', 'pastParticiple': 'left'}),
    w('lose', '丢失', 'v.', 'g6s2', '😞', '', tags=['动作'], forms={'past': 'lost', 'pastParticiple': 'lost'}),
    w('put', '放', 'v.', 'g6s2', '📥', '', tags=['动作'], forms={'past': 'put', 'pastParticiple': 'put'}),
    w('send', '发送', 'v.', 'g6s2', '📤', '', tags=['动作'], forms={'past': 'sent', 'pastParticiple': 'sent'}),
    w('sit', '坐', 'v.', 'g6s2', '🪑', '', tags=['动作'], forms={'past': 'sat', 'pastParticiple': 'sat'}),
    w('stand', '站', 'v.', 'g6s2', '🧍', '', tags=['动作'], forms={'past': 'stood', 'pastParticiple': 'stood'}),
    w('tell', '告诉', 'v.', 'g6s2', '🗨️', '', tags=['动作'], forms={'past': 'told', 'pastParticiple': 'told'}),
    w('teach', '教', 'v.', 'g6s2', '👩‍🏫', '', tags=['动作'], forms={'past': 'taught', 'pastParticiple': 'taught'}),
    w('understand', '理解', 'v.', 'g6s2', '💡', '', tags=['思维'], forms={'past': 'understood', 'pastParticiple': 'understood'}),
    w('wear', '穿；戴', 'v.', 'g6s2', '👚', '', tags=['动作'], forms={'past': 'wore', 'pastParticiple': 'worn'}),
    w('win', '赢', 'v.', 'g6s2', '🏆', '', tags=['动作'], forms={'past': 'won', 'pastParticiple': 'won'}),
]
# 初中七上
NEW += [
    w('beautiful', '美丽的', 'adj.', 'c7s1', '🌸', '', tags=['外貌']),
    w('clever', '聪明的', 'adj.', 'c7s1', '🧠', '', tags=['外貌']),
    w('friendly', '友好的', 'adj.', 'c7s1', '🤝', '', tags=['外貌']),
    w('busy', '忙碌的', 'adj.', 'c7s1', '🏃', '', tags=['状态']),
    w('free', '空闲的；免费的', 'adj.', 'c7s1', '🆓', '', tags=['状态']),
    w('early', '早的', 'adj./adv.', 'c7s1', '🌅', '', tags=['时间'], forms={'comparative': 'earlier', 'superlative': 'earliest'}),
    w('late', '晚的', 'adj./adv.', 'c7s1', '🌆', '', tags=['时间'], forms={'comparative': 'later', 'superlative': 'latest'}),
    w('heavy', '重的', 'adj.', 'c7s1', '🏋️', '', tags=['外貌'], forms={'comparative': 'heavier', 'superlative': 'heaviest'}),
    w('light', '轻的；灯', 'adj./n.', 'c7s1', '💡', '', tags=['外貌']),
    w('fresh', '新鲜的', 'adj.', 'c7s1', '🍃', '', tags=['状态']),
    w('sweet', '甜的', 'adj.', 'c7s1', '🍬', '', tags=['味道']),
    w('healthy', '健康的', 'adj.', 'c7s1', '🥗', '', tags=['状态']),
    w('remember', '记得', 'v.', 'c7s1', '🧠', '', tags=['思维']),
    w('forget', '忘记', 'v.', 'c7s1', '🤭', '', tags=['思维'], forms={'past': 'forgot', 'pastParticiple': 'forgotten'}),
    w('listen', '听', 'v.', 'c7s1', '👂', '', tags=['动作']),
    w('speak', '说；讲', 'v.', 'c7s1', '🗣️', '', tags=['动作'], forms={'past': 'spoke', 'pastParticiple': 'spoken'}),
    w('talk', '谈话', 'v.', 'c7s1', '💬', '', tags=['动作']),
    w('ask', '问', 'v.', 'c7s1', '❓', '', tags=['动作']),
    w('answer', '回答', 'v./n.', 'c7s1', '✅', '', tags=['动作']),
    w('work', '工作', 'v./n.', 'c7s1', '💼', '', tags=['动作']),
]
# 初中七下
NEW += [
    w('polite', '有礼貌的', 'adj.', 'c7s2', '🎩', '', tags=['品质']),
    w('rude', '粗鲁的', 'adj.', 'c7s2', '😤', '', tags=['品质']),
    w('brave', '勇敢的', 'adj.', 'c7s2', '🦁', '', tags=['品质']),
    w('honest', '诚实的', 'adj.', 'c7s2', '🤝', '', tags=['品质']),
    w('lazy', '懒惰的', 'adj.', 'c7s2', '🛌', '', tags=['品质']),
    w('proud', '骄傲的；自豪的', 'adj.', 'c7s2', '🦚', '', tags=['情绪']),
    w('angry', '生气的', 'adj.', 'c7s2', '😡', '', tags=['情绪'], forms={'comparative': 'angrier', 'superlative': 'angriest'}),
    w('afraid', '害怕的', 'adj.', 'c7s2', '😨', '', tags=['情绪']),
    w('tired', '疲倦的', 'adj.', 'c7s2', '😴', '', tags=['状态']),
    w('excited', '兴奋的', 'adj.', 'c7s2', '🤩', '', tags=['情绪']),
    w('bored', '无聊的', 'adj.', 'c7s2', '🥱', '', tags=['状态']),
    w('interesting', '有趣的', 'adj.', 'c7s2', '🤔', '', tags=['状态']),
    w('boring', '无聊的', 'adj.', 'c7s2', '😑', '', tags=['状态']),
    w('difficult', '困难的', 'adj.', 'c7s2', '🧩', '', tags=['状态']),
    w('finish', '完成', 'v.', 'c7s2', '🏁', '', tags=['动作']),
    w('start', '开始', 'v.', 'c7s2', '🚀', '', tags=['动作']),
    w('stop', '停止', 'v.', 'c7s2', '⏹️', '', tags=['动作']),
    w('try', '尝试', 'v.', 'c7s2', '🔁', '', tags=['动作'], forms={'past': 'tried', 'pastParticiple': 'tried'}),
    w('use', '使用', 'v.', 'c7s2', '🔧', '', tags=['动作']),
    w('enjoy', '享受；喜欢', 'v.', 'c7s2', '😊', '', tags=['情绪']),
]
# 初中八上
NEW += [
    w('serious', '严肃的；严重的', 'adj.', 'c8s1', '😐', '', tags=['品质']),
    w('patient', '耐心的', 'adj.', 'c8s1', '⏳', '', tags=['品质']),
    w('quiet', '安静的', 'adj.', 'c8s1', '🤫', '', tags=['状态']),
    w('noisy', '吵闹的', 'adj.', 'c8s1', '📢', '', tags=['状态']),
    w('clean', '干净的', 'adj.', 'c8s1', '🧼', '', tags=['状态']),
    w('crowded', '拥挤的', 'adj.', 'c8s1', '🚶', '', tags=['状态']),
    w('convenient', '方便的', 'adj.', 'c8s1', '✅', '', tags=['状态']),
    w('expensive', '昂贵的', 'adj.', 'c8s1', '💎', '', tags=['状态']),
    w('cheap', '便宜的', 'adj.', 'c8s1', '🏷️', '', tags=['状态']),
    w('delicious', '美味的', 'adj.', 'c8s1', '😋', '', tags=['味道']),
    w('terrible', '糟糕的', 'adj.', 'c8s1', '💢', '', tags=['状态']),
    w('wonderful', '精彩的', 'adj.', 'c8s1', '✨', '', tags=['状态']),
    w('improve', '改善；提高', 'v.', 'c8s1', '📈', '', tags=['动作']),
    w('practise', '练习', 'v.', 'c8s1', '🏋️', '', tags=['动作']),
    w('solve', '解决', 'v.', 'c8s1', '🧩', '', tags=['动作']),
    w('choose', '选择', 'v.', 'c8s1', '🔘', '', tags=['动作'], forms={'past': 'chose', 'pastParticiple': 'chosen'}),
    w('decide', '决定', 'v.', 'c8s1', '⚖️', '', tags=['思维']),
    w('believe', '相信', 'v.', 'c8s1', '🙏', '', tags=['思维']),
    w('discover', '发现', 'v.', 'c8s1', '🔭', '', tags=['动作']),
    w('explore', '探索', 'v.', 'c8s1', '🧭', '', tags=['动作']),
]
# 初中八下
NEW += [
    w('continue', '继续', 'v.', 'c8s2', '➡️', '', tags=['动作']),
    w('explain', '解释', 'v.', 'c8s2', '💡', '', tags=['思维']),
    w('suggest', '建议', 'v.', 'c8s2', '💭', '', tags=['思维']),
    w('offer', '提供；主动', 'v.', 'c8s2', '🤲', '', tags=['动作']),
    w('refuse', '拒绝', 'v.', 'c8s2', '🚫', '', tags=['动作']),
    w('allow', '允许', 'v.', 'c8s2', '🉑', '', tags=['动作']),
    w('require', '需要；要求', 'v.', 'c8s2', '📋', '', tags=['思维']),
    w('encourage', '鼓励', 'v.', 'c8s2', '🌟', '', tags=['动作']),
    w('protect', '保护', 'v.', 'c8s2', '🛡️', '', tags=['动作']),
    w('pollute', '污染', 'v.', 'c8s2', '🏭', '', tags=['动作']),
    w('celebrate', '庆祝', 'v.', 'c8s2', '🎉', '', tags=['动作']),
    w('communicate', '交流', 'v.', 'c8s2', '💬', '', tags=['动作']),
    w('compete', '竞争；比赛', 'v.', 'c8s2', '🏆', '', tags=['动作']),
    w('connect', '连接', 'v.', 'c8s2', '🔗', '', tags=['动作']),
    w('consider', '考虑', 'v.', 'c8s2', '🤔', '', tags=['思维']),
    w('control', '控制', 'v./n.', 'c8s2', '🎛️', '', tags=['动作']),
    w('create', '创造', 'v.', 'c8s2', '🎨', '', tags=['动作']),
    w('describe', '描述', 'v.', 'c8s2', '🖊️', '', tags=['思维']),
    w('develop', '发展；开发', 'v.', 'c8s2', '📈', '', tags=['动作']),
    w('discuss', '讨论', 'v.', 'c8s2', '🗣️', '', tags=['思维']),
]
# 初中九上
NEW += [
    w('achieve', '实现；达到', 'v.', 'c9s1', '🏆', '', tags=['动作']),
    w('advise', '建议', 'v.', 'c9s1', '💡', '', tags=['思维']),
    w('afford', '负担得起', 'v.', 'c9s1', '💰', '', tags=['动作']),
    w('attract', '吸引', 'v.', 'c9s1', '🧲', '', tags=['动作']),
    w('avoid', '避免', 'v.', 'c9s1', '🚫', '', tags=['动作']),
    w('behave', '表现', 'v.', 'c9s1', '🙇', '', tags=['动作']),
    w('celebrate', '庆祝', 'v.', 'c9s1', '🎉', '', tags=['动作']),
    w('compare', '比较', 'v.', 'c9s1', '⚖️', '', tags=['思维']),
    w('complete', '完成；完整的', 'v./adj.', 'c9s1', '✅', '', tags=['动作']),
    w('confuse', '使困惑', 'v.', 'c9s1', '😵', '', tags=['思维']),
    w('count', '数；重要', 'v.', 'c9s1', '🔢', '', tags=['动作']),
    w('cover', '覆盖；封面', 'v./n.', 'c9s1', '📔', '', tags=['动作']),
    w('cure', '治愈', 'v.', 'c9s1', '💊', '', tags=['动作']),
    w('demand', '要求；需求', 'v./n.', 'c9s1', '📣', '', tags=['思维']),
    w('depend', '依靠', 'v.', 'c9s1', '🔗', '', tags=['思维']),
    w('design', '设计', 'v./n.', 'c9s1', '📐', '', tags=['动作']),
    w('destroy', '破坏', 'v.', 'c9s1', '💥', '', tags=['动作']),
    w('direct', '指导；直接的', 'v./adj.', 'c9s1', '➡️', '', tags=['动作']),
    w('disturb', '打扰', 'v.', 'c9s1', '🔔', '', tags=['动作']),
    w('double', '加倍', 'v./adj.', 'c9s1', '✌️', '', tags=['动作']),
]
# 初中九下
NEW += [
    w('earn', '赚得', 'v.', 'c9s2', '💰', '', tags=['动作']),
    w('educate', '教育', 'v.', 'c9s2', '🎓', '', tags=['动作']),
    w('elect', '选举', 'v.', 'c9s2', '🗳️', '', tags=['动作']),
    w('encourage', '鼓励', 'v.', 'c9s2', '🌟', '', tags=['动作']),
    w('enter', '进入', 'v.', 'c9s2', '🚪', '', tags=['动作']),
    w('establish', '建立', 'v.', 'c9s2', '🏛️', '', tags=['动作']),
    w('examine', '检查', 'v.', 'c9s2', '🔍', '', tags=['动作']),
    w('exist', '存在', 'v.', 'c9s2', '🌌', '', tags=['状态']),
    w('expand', '扩大', 'v.', 'c9s2', '🔆', '', tags=['动作']),
    w('expect', '期待', 'v.', 'c9s2', '⏳', '', tags=['思维']),
    w('express', '表达', 'v.', 'c9s2', '💬', '', tags=['思维']),
    w('fail', '失败', 'v.', 'c9s2', '❌', '', tags=['状态']),
    w('fear', '害怕；恐惧', 'v./n.', 'c9s2', '😨', '', tags=['情绪']),
    w('feed', '喂养', 'v.', 'c9s2', '🍼', '', tags=['动作'], forms={'past': 'fed', 'pastParticiple': 'fed'}),
    w('fight', '打架；战斗', 'v.', 'c9s2', '🥊', '', tags=['动作'], forms={'past': 'fought', 'pastParticiple': 'fought'}),
    w('follow', '跟随；遵循', 'v.', 'c9s2', '👣', '', tags=['动作']),
    w('fool', '愚弄；傻瓜', 'v./n.', 'c9s2', '🤡', '', tags=['动作']),
    w('forbid', '禁止', 'v.', 'c9s2', '🚫', '', tags=['动作'], forms={'past': 'forbade', 'pastParticiple': 'forbidden'}),
    w('forgive', '原谅', 'v.', 'c9s2', '🕊️', '', tags=['动作'], forms={'past': 'forgave', 'pastParticiple': 'forgiven'}),
    w('freeze', '结冰', 'v.', 'c9s2', '🧊', '', tags=['自然'], forms={'past': 'froze', 'pastParticiple': 'frozen'}),
]
# 高中一上
NEW += [
    w('absorb', '吸收', 'v.', 'h1s1', '🧽', '', tags=['动作']),
    w('accumulate', '积累', 'v.', 'h1s1', '📚', '', tags=['动作']),
    w('accuse', '控告', 'v.', 'h1s1', '⚖️', '', tags=['动作']),
    w('adapt', '适应；改编', 'v.', 'h1s1', '🔄', '', tags=['动作']),
    w('adjust', '调整', 'v.', 'h1s1', '🎛️', '', tags=['动作']),
    w('admire', '钦佩；欣赏', 'v.', 'h1s1', '🌟', '', tags=['情绪']),
    w('admit', '承认；准入', 'v.', 'h1s1', '🚪', '', tags=['思维']),
    w('adopt', '采纳；收养', 'v.', 'h1s1', '🤝', '', tags=['动作']),
    w('advance', '推进；前进', 'v./n.', 'h1s1', '➡️', '', tags=['动作']),
    w('advertise', '做广告', 'v.', 'h1s1', '📺', '', tags=['动作']),
    w('advise', '建议', 'v.', 'h1s1', '💡', '', tags=['思维']),
    w('affect', '影响', 'v.', 'h1s1', '🌊', '', tags=['动作']),
    w('afford', '负担得起', 'v.', 'h1s1', '💰', '', tags=['动作']),
    w('agree', '同意', 'v.', 'h1s1', '🤝', '', tags=['思维']),
    w('aim', '瞄准；目标', 'v./n.', 'h1s1', '🎯', '', tags=['思维']),
    w('alarm', '警报；使惊恐', 'n./v.', 'h1s1', '🚨', '', tags=['物品']),
    w('amaze', '使惊奇', 'v.', 'h1s1', '😲', '', tags=['情绪']),
    w('analyze', '分析', 'v.', 'h1s1', '🔬', '', tags=['思维']),
    w('announce', '宣布', 'v.', 'h1s1', '📢', '', tags=['动作']),
    w('annoy', '使恼怒', 'v.', 'h1s1', '😤', '', tags=['情绪']),
]
# 高中一下
NEW += [
    w('apparent', '明显的', 'adj.', 'h1s2', '🔍', '', tags=['状态']),
    w('appeal', '呼吁；吸引', 'v./n.', 'h1s2', '📣', '', tags=['动作']),
    w('appear', '出现；似乎', 'v.', 'h1s2', '👀', '', tags=['状态']),
    w('applaud', '鼓掌；称赞', 'v.', 'h1s2', '👏', '', tags=['动作']),
    w('apply', '申请；应用', 'v.', 'h1s2', '📝', '', tags=['动作']),
    w('appoint', '任命；约定', 'v.', 'h1s2', '📅', '', tags=['动作']),
    w('appreciate', '欣赏；感激', 'v.', 'h1s2', '🌟', '', tags=['情绪']),
    w('approach', '接近；方法', 'v./n.', 'h1s2', '🚶', '', tags=['动作']),
    w('approve', '批准；赞成', 'v.', 'h1s2', '✅', '', tags=['思维']),
    w('argue', '争论；主张', 'v.', 'h1s2', '🗣️', '', tags=['思维']),
    w('arise', '出现；升起', 'v.', 'h1s2', '🌅', '', tags=['状态'], forms={'past': 'arose', 'pastParticiple': 'arisen'}),
    w('arrange', '安排', 'v.', 'h1s2', '🗂️', '', tags=['动作']),
    w('arrest', '逮捕', 'v.', 'h1s2', '🚔', '', tags=['动作']),
    w('arrive', '到达', 'v.', 'h1s2', '🛬', '', tags=['动作']),
    w('assess', '评估', 'v.', 'h1s2', '📊', '', tags=['思维']),
    w('assist', '协助', 'v.', 'h1s2', '🤝', '', tags=['动作']),
    w('assume', '假定；承担', 'v.', 'h1s2', '🤔', '', tags=['思维']),
    w('assure', '保证', 'v.', 'h1s2', '✅', '', tags=['动作']),
    w('attach', '附上；系', 'v.', 'h1s2', '📎', '', tags=['动作']),
    w('attack', '攻击', 'v./n.', 'h1s2', '⚔️', '', tags=['动作']),
]
# 高中二上
NEW += [
    w('attempt', '尝试；企图', 'v./n.', 'h2s1', '🔁', '', tags=['动作']),
    w('attend', '出席；照料', 'v.', 'h2s1', '🎓', '', tags=['动作']),
    w('attract', '吸引', 'v.', 'h2s1', '🧲', '', tags=['动作']),
    w('author', '作者', 'n.', 'h2s1', '✍️', '', tags=['身份']),
    w('automatic', '自动的', 'adj.', 'h2s1', '🤖', '', tags=['状态']),
    w('available', '可获得的', 'adj.', 'h2s1', '✅', '', tags=['状态']),
    w('average', '平均的；平均数', 'adj./n.', 'h2s1', '📊', '', tags=['状态']),
    w('avoid', '避免', 'v.', 'h2s1', '🚫', '', tags=['动作']),
    w('awkward', '尴尬的；笨拙的', 'adj.', 'h2s1', '😅', '', tags=['状态']),
    w('balance', '平衡', 'n./v.', 'h2s1', '⚖️', '', tags=['状态']),
    w('ban', '禁止', 'v./n.', 'h2s1', '🚫', '', tags=['动作'], forms={'past': 'banned', 'pastParticiple': 'banned'}),
    w('bare', '赤裸的；空的', 'adj.', 'h2s1', '🍂', '', tags=['状态']),
    w('barrier', '障碍', 'n.', 'h2s1', '🧱', '', tags=['物品']),
    w('base', '基础；以…为基础', 'n./v.', 'h2s1', '🏗️', '', tags=['物品']),
    w('beam', '光束；微笑', 'n./v.', 'h2s1', '🌟', '', tags=['自然']),
    w('bear', '忍受；熊', 'v./n.', 'h2s1', '🐻', '', tags=['动作'], forms={'past': 'bore', 'pastParticiple': 'born'}),
    w('beat', '打败；跳动', 'v.', 'h2s1', '💓', '', tags=['动作'], forms={'past': 'beat', 'pastParticiple': 'beaten'}),
    w('behave', '表现', 'v.', 'h2s1', '🙇', '', tags=['动作']),
    w('belong', '属于', 'v.', 'h2s1', '🔗', '', tags=['状态']),
    w('bend', '弯曲', 'v.', 'h2s1', '➰', '', tags=['动作'], forms={'past': 'bent', 'pastParticiple': 'bent'}),
]
# 高中二下
NEW += [
    w('benefit', '益处；受益', 'n./v.', 'h2s2', '🎁', '', tags=['物品']),
    w('betray', '背叛', 'v.', 'h2s2', '🗡️', '', tags=['动作']),
    w('blame', '责备', 'v./n.', 'h2s2', '😠', '', tags=['动作']),
    w('blank', '空白的', 'adj./n.', 'h2s2', '⬜', '', tags=['状态']),
    w('bleed', '流血', 'v.', 'h2s2', '🩸', '', tags=['动作'], forms={'past': 'bled', 'pastParticiple': 'bled'}),
    w('blend', '混合', 'v./n.', 'h2s2', '🍹', '', tags=['动作']),
    w('bloom', '开花；繁荣', 'v./n.', 'h2s2', '🌸', '', tags=['自然']),
    w('boast', '吹嘘', 'v.', 'h2s2', '💬', '', tags=['动作']),
    w('boost', '提升；推动', 'v.', 'h2s2', '🚀', '', tags=['动作']),
    w('border', '边界', 'n.', 'h2s2', '🔲', '', tags=['地点']),
    w('bother', '打扰；麻烦', 'v.', 'h2s2', '🔔', '', tags=['动作']),
    w('bounce', '弹跳', 'v.', 'h2s2', '🏀', '', tags=['动作']),
    w('branch', '树枝；分支', 'n.', 'h2s2', '🌿', '', tags=['自然']),
    w('breed', '饲养；繁殖', 'v.', 'h2s2', '🐣', '', tags=['动作'], forms={'past': 'bred', 'pastParticiple': 'bred'}),
    w('breeze', '微风', 'n.', 'h2s2', '🍃', '', tags=['自然']),
    w('brief', '简短的', 'adj.', 'h2s2', '📝', '', tags=['状态']),
    w('bright', '明亮的；聪明的', 'adj.', 'h2s2', '💡', '', tags=['状态']),
    w('broad', '宽阔的', 'adj.', 'h2s2', '↔️', '', tags=['外貌']),
    w('brush', '刷；刷子', 'v./n.', 'h2s2', '🪥', '', tags=['物品']),
    w('burst', '爆发', 'v./n.', 'h2s2', '💥', '', tags=['动作'], forms={'past': 'burst', 'pastParticiple': 'burst'}),
]
# 高中三上
NEW += [
    w('calculate', '计算', 'v.', 'h3s1', '🧮', '', tags=['动作']),
    w('campaign', '运动；战役', 'n.', 'h3s1', '📣', '', tags=['物品']),
    w('cancel', '取消', 'v.', 'h3s1', '❌', '', tags=['动作'], forms={'past': 'cancelled', 'pastParticiple': 'cancelled'}),
    w('capture', '捕获', 'v.', 'h3s1', '📸', '', tags=['动作']),
    w('career', '事业；职业', 'n.', 'h3s1', '💼', '', tags=['身份']),
    w('casual', '随意的', 'adj.', 'h3s1', '👕', '', tags=['状态']),
    w('ceremony', '仪式', 'n.', 'h3s1', '🎖️', '', tags=['物品']),
    w('challenge', '挑战', 'n./v.', 'h3s1', '🏔️', '', tags=['物品']),
    w('channel', '频道；通道', 'n.', 'h3s1', '📡', '', tags=['物品']),
    w('chapter', '章；回', 'n.', 'h3s1', '📖', '', tags=['物品']),
    w('character', '性格；角色', 'n.', 'h3s1', '🎭', '', tags=['物品']),
    w('charge', '收费；负责', 'v./n.', 'h3s1', '🔋', '', tags=['动作']),
    w('cheat', '欺骗', 'v./n.', 'h3s1', '🃏', '', tags=['动作']),
    w('chemical', '化学的；化学品', 'adj./n.', 'h3s1', '🧪', '', tags=['状态']),
    w('circuit', '电路；环形', 'n.', 'h3s1', '🔌', '', tags=['物品']),
    w('circulate', '循环；流通', 'v.', 'h3s1', '🔄', '', tags=['动作']),
    w('cite', '引用', 'v.', 'h3s1', '📎', '', tags=['动作']),
    w('civil', '公民的；民用的', 'adj.', 'h3s1', '🏛️', '', tags=['状态']),
    w('clarify', '澄清', 'v.', 'h3s1', '💡', '', tags=['思维']),
    w('classify', '分类', 'v.', 'h3s1', '🗂️', '', tags=['思维']),
]
# 高中三下
NEW += [
    w('climate', '气候', 'n.', 'h3s2', '🌦️', '', tags=['自然']),
    w('cling', '依附；紧贴', 'v.', 'h3s2', '🤗', '', tags=['动作'], forms={'past': 'clung', 'pastParticiple': 'clung'}),
    w('collapse', '倒塌；崩溃', 'v./n.', 'h3s2', '🏚️', '', tags=['动作']),
    w('colleague', '同事', 'n.', 'h3s2', '🧑‍💼', '', tags=['身份']),
    w('column', '柱；专栏', 'n.', 'h3s2', '📰', '', tags=['物品']),
    w('combine', '结合', 'v.', 'h3s2', '🔗', '', tags=['动作']),
    w('command', '命令；掌握', 'v./n.', 'h3s2', '🎖️', '', tags=['动作']),
    w('comment', '评论', 'n./v.', 'h3s2', '💬', '', tags=['思维']),
    w('commit', '承诺；犯（错）', 'v.', 'h3s2', '📝', '', tags=['动作']),
    w('commodity', '商品', 'n.', 'h3s2', '📦', '', tags=['物品']),
    w('comparison', '比较', 'n.', 'h3s2', '⚖️', '', tags=['物品']),
    w('compete', '竞争', 'v.', 'h3s2', '🏆', '', tags=['动作']),
    w('complain', '抱怨', 'v.', 'h3s2', '😣', '', tags=['情绪']),
    w('complete', '完成；完整的', 'v./adj.', 'h3s2', '✅', '', tags=['动作']),
    w('complex', '复杂的', 'adj.', 'h3s2', '🧩', '', tags=['状态']),
    w('component', '成分；部件', 'n.', 'h3s2', '⚙️', '', tags=['物品']),
    w('comprehensive', '全面的', 'adj.', 'h3s2', '📚', '', tags=['状态']),
    w('comprise', '包含；由…组成', 'v.', 'h3s2', '📦', '', tags=['动作']),
    w('conceal', '隐藏', 'v.', 'h3s2', '🫥', '', tags=['动作']),
    w('conclude', '总结；断定', 'v.', 'h3s2', '🔚', '', tags=['思维']),
]

def ts_str(s: str) -> str:
    # 转义单引号
    return s.replace('\\', '\\\\').replace("'", "\\'")

def emit(d: dict) -> str:
    parts = []
    parts.append(f"id: '{ts_str(d['word'].lower())}'")
    parts.append(f"word: '{ts_str(d['word'])}'")
    parts.append(f"meaning: '{ts_str(d['zh'])}'")
    parts.append(f"pos: '{ts_str(d['pos'])}'")
    parts.append(f"phonetic: '{ts_str(d['phonetic'])}'")
    parts.append(f"image: '{ts_str(d['img'])}'")
    if d['root']:
        parts.append(f"root: '{ts_str(d['root'])}'")
    if d['affix']:
        parts.append(f"affix: '{ts_str(d['affix'])}'")
    if d['am']:
        parts.append(f"affixMeaning: '{ts_str(d['am'])}'")
    if d['derive']:
        parts.append(f"derive: '{ts_str(d['derive'])}'")
    if d['assoc']:
        parts.append(f"association: '{ts_str(d['assoc'])}'")
    if d['forms']:
        fm = []
        if d['forms'].get('comparative'):
            fm.append(f"comparative: '{ts_str(d['forms']['comparative'])}'")
        if d['forms'].get('superlative'):
            fm.append(f"superlative: '{ts_str(d['forms']['superlative'])}'")
        if d['forms'].get('past'):
            fm.append(f"past: '{ts_str(d['forms']['past'])}'")
        if d['forms'].get('pastParticiple'):
            fm.append(f"pastParticiple: '{ts_str(d['forms']['pastParticiple'])}'")
        parts.append('forms: { ' + ', '.join(fm) + ' }')
    # phrases
    ph = ', '.join(f"{{ en: '{ts_str(p[0])}', zh: '{ts_str(p[1])}' }}" for p in d['ph'])
    parts.append(f"phrases: [{ph}]")
    # examples
    ex = ', '.join(f"{{ en: '{ts_str(e[0])}', zh: '{ts_str(e[1])}' }}" for e in d['ex'])
    parts.append(f"examples: [{ex}]")
    parts.append(f"grade: '{ts_str(d['grade'])}'")
    if d['tags']:
        tg = ', '.join(f"'{ts_str(t)}'" for t in d['tags'])
        parts.append(f"tags: [{tg}]")
    return '{ ' + ', '.join(parts) + ' }'

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        content = f.read()
    # 已有 id
    existing = set(re.findall(r"id:\s*'([^']+)'", content))
    # 去重 NEW（按 word.lower()）
    seen = set()
    entries = []
    skipped = 0
    for d in NEW:
        wid = d['word'].lower()
        if wid in existing or wid in seen:
            skipped += 1
            continue
        seen.add(wid)
        entries.append('  ' + emit(d) + ',')
    if not entries:
        print('没有需要追加的新词。')
        return
    # 在 raw 数组结尾的 ]; 之前插入
    if '\n];' not in content and '\n];\n' not in content:
        raise SystemExit('未找到 raw 数组结尾的 ];')
    head, sep, tail = content.partition('\n];')
    # head 以最后一个条目行结束（含末尾逗号+换行）；entries 每行已带前导缩进与末尾逗号
    new_content = head + '\n'.join(entries) + sep + tail
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'已追加 {len(entries)} 个单词，跳过重复 {skipped} 个。')

if __name__ == '__main__':
    main()
