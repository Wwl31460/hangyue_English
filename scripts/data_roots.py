# -*- coding: utf-8 -*-
"""词根家族库：root -> (含义, [(单词, 中文, emoji), ...])。

说明
----
- 每个词根下列 5–8 个「最常见的同根词」，顺序即展示优先级（最常用在前）。
- 词不受课本单元限制：可以是小学、初中、高中任意册的词，也可以是课本之外的常见词，
  这是用户明确要求的（「词根词缀的扩展不需要局限于哪个单元或教材」）。
- 同一词根最多展示 8 个（在 UI 层 cap），所以这里只挑最常见的，不堆生僻词。
"""

ROOTS = {
    'act': ('做；驱动', [
        ('act', '行动', '🎬'), ('action', '行动', '🏃'), ('active', '积极的', '⚡'),
        ('activity', '活动', '🎯'), ('actor', '男演员', '🎭'), ('actress', '女演员', '👩‍🎤'),
        ('react', '反应', '💥'), ('exact', '精确的', '🎯'),
    ]),
    'anim': ('生命；精神', [
        ('animal', '动物', '🐾'), ('animate', '使有生气', '✨'), ('animation', '动画', '🎞️'),
        ('unanimous', '一致同意的', '🤝'),
    ]),
    'ann': ('年', [
        ('annual', '每年的', '📅'), ('anniversary', '周年纪念', '🎉'), ('annually', '每年地', '🗓️'),
    ]),
    'aqua': ('水', [
        ('aquarium', '水族馆', '🐠'), ('aquatic', '水生的', '💧'),
    ]),
    'aud': ('听', [
        ('audience', '观众', '👥'), ('audio', '音频', '🔊'), ('audible', '听得见的', '👂'),
        ('auditorium', '礼堂', '🏛️'),
    ]),
    'auto': ('自己', [
        ('automatic', '自动的', '🤖'), ('automobile', '汽车', '🚗'), ('autograph', '亲笔签名', '✍️'),
        ('autobiography', '自传', '📖'),
    ]),
    'bio': ('生命', [
        ('biology', '生物学', '🧬'), ('biography', '传记', '📘'), ('biodiversity', '生物多样性', '🌿'),
    ]),
    'cap': ('抓；拿', [
        ('capture', '捕获', '🎯'), ('captain', '队长', '🧑‍✈️'), ('capable', '有能力的', '💪'),
        ('capacity', '容量', '📦'), ('accept', '接受', '🤝'), ('receive', '收到', '📩'),
        ('concept', '概念', '💡'), ('except', '除…之外', '➖'),
    ]),
    'cede': ('走；让', [
        ('proceed', '继续进行', '➡️'), ('succeed', '成功', '🏆'), ('success', '成功', '🌟'),
        ('access', '进入；通道', '🚪'), ('process', '过程', '⚙️'), ('exceed', '超过', '📈'),
    ]),
    'centr': ('中心', [
        ('center', '中心', '🎯'), ('central', '中央的', '🏛️'), ('concentrate', '集中', '🧠'),
        ('century', '世纪', '⏳'),
    ]),
    'cert': ('确定', [
        ('certain', '确定的', '✅'), ('certainly', '当然', '👍'), ('certificate', '证书', '📜'),
    ]),
    'cid': ('切；落下', [
        ('decide', '决定', '🤔'), ('decision', '决定', '📋'), ('precise', '精确的', '🎯'),
        ('scissors', '剪刀', '✂️'),
    ]),
    'clud': ('关；闭', [
        ('include', '包括', '📥'), ('exclude', '排除', '🚫'), ('conclude', '得出结论', '📝'),
        ('conclusion', '结论', '📄'),
    ]),
    'cord': ('心', [
        ('record', '记录', '🎙️'), ('accord', '一致', '🤝'), ('according', '根据', '📌'),
        ('courage', '勇气', '🦁'),
    ]),
    'cred': ('相信', [
        ('credit', '信用；学分', '💳'), ('incredible', '难以置信的', '😲'), ('credible', '可信的', '✅'),
    ]),
    'cur': ('跑；关心', [
        ('current', '当前的', '🌀'), ('occur', '发生', '💥'), ('currency', '货币', '💰'),
        ('curious', '好奇的', '🤔'), ('accurate', '准确的', '🎯'), ('secure', '安全的', '🔒'),
        ('security', '安全', '🛡️'), ('cure', '治愈', '💊'),
    ]),
    'cycl': ('圆；环', [
        ('bicycle', '自行车', '🚲'), ('cycle', '循环', '🔄'), ('recycle', '回收', '♻️'),
        ('circle', '圆圈', '⭕'), ('circus', '马戏团', '🎪'),
    ]),
    'demo': ('人民', [
        ('democracy', '民主', '🗳️'), ('demonstrate', '证明；示范', '📢'),
    ]),
    'dent': ('牙', [
        ('dentist', '牙医', '🦷'), ('dental', '牙齿的', '🪥'),
    ]),
    'dict': ('说', [
        ('dictionary', '词典', '📕'), ('predict', '预测', '🔮'), ('dictation', '听写', '✍️'),
        ('dictate', '命令；听写', '🗣️'), ('contradict', '反驳', '🙅'), ('verdict', '裁决', '⚖️'),
    ]),
    'duc': ('引导', [
        ('introduce', '介绍', '🤝'), ('produce', '生产', '🏭'), ('product', '产品', '📦'),
        ('reduce', '减少', '📉'), ('conduct', '实施；指挥', '🎼'), ('education', '教育', '🎓'),
        ('educate', '教育', '📚'),
    ]),
    'dur': ('持久', [
        ('during', '在…期间', '⏳'), ('durable', '耐用的', '🔧'), ('endure', '忍受', '😣'),
        ('duration', '持续时间', '⏱️'),
    ]),
    'equ': ('相等', [
        ('equal', '相等的', '⚖️'), ('equality', '平等', '🤝'), ('equator', '赤道', '🌍'),
        ('adequate', '足够的', '👌'), ('equation', '方程', '➗'),
    ]),
    'fac': ('做；制造', [
        ('fact', '事实', '📌'), ('factory', '工厂', '🏭'), ('factor', '因素', '🔑'),
        ('perfect', '完美的', '💯'), ('difficult', '困难的', '⛰️'), ('effect', '影响', '🌟'),
        ('affect', '影响', '🌀'), ('efficient', '高效的', '⚡'),
    ]),
    'fer': ('带；拿', [
        ('offer', '提供', '🎁'), ('differ', '不同', '🔀'), ('refer', '提到', '📖'),
        ('prefer', '更喜欢', '❤️'), ('transfer', '转移', '🔁'), ('suffer', '遭受', '😖'),
        ('conference', '会议', '🎤'), ('different', '不同的', '🔀'),
    ]),
    'fin': ('结束；界限', [
        ('finish', '完成', '🏁'), ('final', '最后的', '🔚'), ('finally', '最后', '📌'),
        ('finance', '财政', '💰'), ('infinite', '无限的', '♾️'), ('define', '定义', '📘'),
    ]),
    'firm': ('坚固', [
        ('firm', '坚定的；公司', '🏢'), ('confirm', '确认', '✅'), ('affirm', '断言', '🗣️'),
    ]),
    'flex': ('弯曲', [
        ('flexible', '灵活的', '🤸'), ('reflect', '反射；反思', '🪞'), ('reflex', '反射', '⚡'),
    ]),
    'flu': ('流', [
        ('fluent', '流利的', '🗣️'), ('influence', '影响', '🌀'), ('fluid', '流体', '💧'),
    ]),
    'form': ('形状', [
        ('form', '形式', '📋'), ('uniform', '制服；统一的', '👔'), ('inform', '通知', '📢'),
        ('information', '信息', 'ℹ️'), ('perform', '表演', '🎭'), ('reform', '改革', '🔧'),
        ('format', '格式', '📐'), ('transform', '改变', '🦋'), ('formation', '形成', '🪨'),
        ('formal', '正式的', '🎩'), ('formula', '公式', '➗'),
    ]),
    'frag': ('破碎', [
        ('fragment', '碎片', '🧩'), ('fragile', '易碎的', '🥚'), ('fraction', '分数', '➗'),
    ]),
    'fund': ('基础', [
        ('fund', '基金', '💵'), ('fundamental', '基本的', '🏗️'), ('foundation', '基础；基金会', '🧱'),
        ('profound', '深刻的', '🕳️'),
    ]),
    'gen': ('产生', [
        ('gene', '基因', '🧬'), ('general', '总体的；将军', '⭐'), ('generate', '产生', '⚡'),
        ('generation', '一代', '👨‍👩‍👧'), ('genius', '天才', '🧠'), ('gentle', '温柔的', '🕊️'),
    ]),
    'geo': ('地球', [
        ('geography', '地理', '🗺️'), ('geology', '地质学', '🪨'), ('geometry', '几何', '📐'),
    ]),
    'grad': ('走；步', [
        ('grade', '年级；等级', '🏫'), ('gradual', '逐渐的', '📈'), ('gradually', '逐渐地', '🐢'),
        ('graduate', '毕业', '🎓'), ('progress', '进步', '🚀'), ('aggressive', '好斗的', '😠'),
    ]),
    'graph': ('写；画', [
        ('photograph', '照片', '📷'), ('graph', '图表', '📊'), ('geography', '地理', '🗺️'),
        ('paragraph', '段落', '📄'), ('program', '节目；程序', '💻'), ('graphic', '图表的', '🖼️'),
        ('autograph', '亲笔签名', '✍️'), ('telegraph', '电报', '📨'),
    ]),
    'grat': ('感谢', [
        ('grateful', '感激的', '🙏'), ('gratitude', '感激', '💐'), ('congratulate', '祝贺', '🎉'),
    ]),
    'hosp': ('客人', [
        ('hospital', '医院', '🏥'), ('hospitality', '好客', '🍵'), ('host', '主人', '🏠'),
        ('hotel', '旅馆', '🏨'),
    ]),
    'ident': ('相同', [
        ('identity', '身份', '🪪'), ('identify', '辨认', '🔍'), ('identical', '完全相同的', '👯'),
    ]),
    'ject': ('投掷', [
        ('project', '项目；工程', '📐'), ('reject', '拒绝', '🚫'), ('inject', '注射', '💉'),
        ('subject', '科目；主题', '📚'), ('object', '物体；反对', '📦'), ('adjective', '形容词', '🔤'),
        ('objective', '目标', '🎯'),
    ]),
    'junct': ('连接', [
        ('join', '加入', '🤝'), ('joint', '关节；联合的', '🦴'), ('junction', '交叉口', '🚦'),
    ]),
    'labor': ('劳动', [
        ('labor', '劳动', '🛠️'), ('laboratory', '实验室', '🧪'), ('collaborate', '合作', '🤝'),
        ('elaborate', '精心制作的', '🎨'),
    ]),
    'lect': ('选择；读', [
        ('collect', '收集', '📦'), ('elect', '选举', '🗳️'), ('select', '挑选', '✅'),
        ('lecture', '讲座', '🎓'), ('intelligence', '智力', '🧠'), ('legend', '传说', '🐉'),
    ]),
    'leg': ('法律', [
        ('legal', '合法的', '⚖️'), ('illegal', '非法的', '🚫'), ('legislation', '立法', '📜'),
        ('privilege', '特权', '👑'),
    ]),
    'liber': ('自由', [
        ('liberty', '自由', '🕊️'), ('liberal', '自由的', '🗽'), ('deliver', '递送', '📦'),
    ]),
    'loc': ('地方', [
        ('local', '当地的', '📍'), ('locate', '定位', '🗺️'), ('location', '位置', '📌'),
    ]),
    'log': ('言语；学科', [
        ('biology', '生物学', '🧬'), ('technology', '技术', '💻'), ('psychology', '心理学', '🧠'),
        ('dialogue', '对话', '💬'), ('apology', '道歉', '🙇'),
    ]),
    'manu': ('手', [
        ('manual', '手册；手工的', '📔'), ('manufacture', '制造', '🏭'), ('manuscript', '手稿', '📜'),
    ]),
    'mar': ('海', [
        ('marine', '海洋的', '🐋'), ('submarine', '潜艇', '🚢'),
    ]),
    'medi': ('中间', [
        ('media', '媒体', '📺'), ('medium', '媒介；中等的', '📻'), ('medicine', '药；医学', '💊'),
        ('immediate', '立即的', '⚡'), ('intermediate', '中级的', '📗'),
    ]),
    'memor': ('记忆', [
        ('memory', '记忆', '🧠'), ('remember', '记得', '💭'), ('memorize', '记住', '📝'),
        ('memorial', '纪念的', '🕯️'), ('commemorate', '纪念', '🎖️'), ('memorable', '难忘的', '🌟'),
    ]),
    # 注意：key 用 mens 而非 ment，避免与后缀 -ment（agreement/environment…）撞车
    'mens': ('心；想', [
        ('mental', '精神的', '🧠'), ('mention', '提及', '💬'), ('comment', '评论', '💭'),
    ]),
    'migr': ('迁移', [
        ('migrate', '迁徙', '🦅'), ('immigrant', '移民', '🛂'), ('migration', '迁移', '🧳'),
    ]),
    'min': ('小', [
        ('minimum', '最小量', '🔽'), ('minor', '较小的', '▪️'), ('minute', '分钟', '⏱️'),
        ('minister', '部长', '🏛️'),
    ]),
    'miss': ('送；放', [
        ('mission', '任务', '🎯'), ('message', '消息', '✉️'), ('missile', '导弹', '🚀'),
    ]),
    'mit': ('送；放', [
        ('submit', '提交', '📤'), ('permit', '允许', '✅'), ('admit', '承认；录取', '🎓'),
        ('commit', '犯罪；承诺', '⚖️'),
    ]),
    'mob': ('移动', [
        ('mobile', '移动的', '📱'), ('motion', '运动', '🏃'), ('motor', '发动机', '⚙️'),
        ('emotion', '情感', '❤️'), ('promote', '促进', '📈'), ('remove', '移除', '🧹'),
    ]),
    'nat': ('出生', [
        ('nature', '自然', '🌳'), ('native', '本地的', '🏡'), ('nation', '国家', '🌍'),
        ('national', '国家的', '🏛️'), ('nationality', '国籍', '🛂'), ('international', '国际的', '🌐'),
        ('natural', '自然的', '🍃'), ('innate', '天生的', '👶'),
    ]),
    'nom': ('名字', [
        ('nominate', '提名', '📝'), ('synonym', '近义词', '🟰'), ('antonym', '反义词', '↔️'),
    ]),
    'norm': ('标准', [
        ('normal', '正常的', '✅'), ('abnormal', '异常的', '❗'),
    ]),
    'nov': ('新', [
        ('novel', '小说；新奇的', '📖'), ('innovation', '创新', '💡'), ('renovate', '翻新', '🔨'),
    ]),
    'numer': ('数字', [
        ('number', '数字', '🔢'), ('numerous', '众多的', '🔢'),
    ]),
    'oper': ('工作', [
        ('operate', '操作', '⚙️'), ('operation', '手术；操作', '🏥'), ('cooperate', '合作', '🤝'),
        ('opera', '歌剧', '🎭'),
    ]),
    'opt': ('选择；看；眼/视觉', [
        ('option', '选择', '🔀'), ('adopt', '采纳；收养', '🤗'), ('optimistic', '乐观的', '😊'),
        ('optic', '视觉的', '🔤'), ('optical', '光学的', '🔤'), ('optimism', '乐观', '🔤'),
        ('optimize', '优化', '🔤'), ('optician', '眼镜商', '🔤'),
    ]),
    'ord': ('顺序', [
        ('order', '命令；顺序', '📋'), ('ordinary', '普通的', '🙂'), ('coordinate', '协调', '🧭'),
        ('disorder', '混乱', '🌪️'),
    ]),
    'par': ('准备；显现', [
        ('prepare', '准备', '🎒'), ('repair', '修理', '🔧'), ('apparent', '明显的', '👀'),
        ('separate', '分开', '✂️'), ('parade', '游行', '🎺'),
    ]),
    'part': ('部分', [
        ('part', '部分', '🧩'), ('party', '聚会；党', '🎉'), ('partner', '伙伴', '🤝'),
        ('partial', '部分的', '◐'), ('participate', '参加', '🙋'), ('particular', '特别的', '🔍'),
    ]),
    'pass': ('通过', [
        ('pass', '通过', '🚪'), ('passage', '段落；通道', '📄'), ('passenger', '乘客', '🧳'),
        ('passport', '护照', '🛂'),
    ]),
    'path': ('感情；疾病', [
        ('sympathy', '同情', '🤝'), ('path', '小路', '🛤️'), ('pathology', '病理学', '🔬'),
    ]),
    'ped': ('脚', [
        ('pedal', '踏板', '🚲'), ('pedestrian', '行人', '🚶'), ('expedition', '远征', '🏔️'),
    ]),
    'pel': ('推', [
        ('expel', '开除', '🚫'), ('impulse', '冲动', '💥'), ('pulse', '脉搏', '💓'),
    ]),
    'pend': ('悬挂；称量', [
        ('depend', '依靠', '🤝'), ('spend', '花费', '💸'), ('expensive', '昂贵的', '💎'),
        ('suspend', '暂停', '⏸️'),
    ]),
    'phon': ('声音', [
        ('phone', '电话', '📞'), ('telephone', '电话', '☎️'), ('microphone', '麦克风', '🎤'),
        ('symphony', '交响乐', '🎻'), ('phonetic', '语音的', '🔤'), ('headphones', '耳机', '🎧'),
        ('earphone', '耳塞', '🔤'),
    ]),
    'plic': ('折叠', [
        ('apply', '申请；应用', '📝'), ('reply', '回复', '↩️'), ('simple', '简单的', '🙂'),
        ('complicated', '复杂的', '🧩'), ('multiply', '乘；繁殖', '✖️'),
    ]),
    'popul': ('人民', [
        ('popular', '受欢迎的', '👍'), ('population', '人口', '👥'),
    ]),
    'port': ('搬运', [
        ('port', '港口', '⚓'), ('important', '重要的', '❗'), ('reporter', '记者', '🎤'),
        ('transport', '运输', '🚚'), ('export', '出口', '📤'), ('import', '进口', '📥'),
        ('support', '支持', '🤝'), ('airport', '机场', '✈️'),
    ]),
    'pos': ('放置', [
        ('position', '位置', '📍'), ('purpose', '目的', '🎯'), ('expose', '暴露', '🔦'),
        ('compose', '组成；创作', '🎼'), ('oppose', '反对', '✋'), ('postpone', '推迟', '⏰'),
    ]),
    'press': ('压', [
        ('press', '按压', '👇'), ('express', '表达', '💬'), ('impress', '使印象深刻', '😮'),
        ('pressure', '压力', '🌀'), ('depress', '使沮丧', '😞'),
    ]),
    'prim': ('第一', [
        ('primary', '初级的', '1️⃣'), ('prime', '首要的', '⭐'), ('principle', '原则', '📏'),
    ]),
    'priv': ('私人', [
        ('private', '私人的', '🔒'), ('privacy', '隐私', '🕵️'), ('privilege', '特权', '👑'),
    ]),
    'prob': ('证明；试验', [
        ('probable', '可能的', '❓'), ('probably', '大概', '🤔'), ('prove', '证明', '✅'),
        ('proof', '证据', '📑'), ('approve', '批准', '👍'), ('improve', '改善', '📈'),
    ]),
    'publ': ('公众', [
        ('public', '公共的', '🏛️'), ('publish', '出版', '📚'), ('republic', '共和国', '🏛️'),
    ]),
    'punct': ('点', [
        ('punctual', '准时的', '⏰'), ('punctuation', '标点', '❕'),
    ]),
    'rect': ('直', [
        ('correct', '正确的', '✅'), ('direct', '直接的；导演', '➡️'), ('director', '导演；主任', '🎬'),
        ('rectangle', '长方形', '▭'),
    ]),
    'reg': ('规则；统治', [
        ('regular', '规则的', '📏'), ('region', '地区', '🗺️'), ('register', '登记', '📝'),
        ('regulation', '规章', '📜'),
    ]),
    'rupt': ('断裂', [
        ('interrupt', '打断', '✋'), ('erupt', '爆发', '🌋'), ('eruption', '喷发', '🌋'),
        ('corrupt', '腐败的', '💸'), ('bankrupt', '破产的', '📉'),
    ]),
    'sci': ('知道', [
        ('science', '科学', '🔬'), ('scientist', '科学家', '👨‍🔬'), ('conscious', '有意识的', '🧠'),
        ('conscience', '良心', '🤍'), ('scientific', '科学的', '📘'),
    ]),
    'scrib': ('写', [
        ('describe', '描述', '📝'), ('subscribe', '订阅', '📰'), ('prescription', '处方', '💊'),
        ('script', '剧本；脚本', '🎬'), ('manuscript', '手稿', '📜'), ('inscribe', '题写', '✍️'),
    ]),
    'sect': ('切', [
        ('section', '部分；区', '🔪'), ('insect', '昆虫', '🐜'), ('intersect', '相交', '✖️'),
    ]),
    'sens': ('感觉', [
        ('sense', '感觉', '🖐️'), ('sensitive', '敏感的', '🌸'), ('sentence', '句子', '📝'),
        ('consent', '同意', '✅'),
    ]),
    'serv': ('服务；保持', [
        ('service', '服务', '🛎️'), ('servant', '仆人', '🧹'), ('observe', '观察', '👀'),
        ('deserve', '值得', '🏅'), ('preserve', '保护', '🛡️'), ('reserve', '预订', '📅'),
    ]),
    'sign': ('记号', [
        ('sign', '标志；签名', '✍️'), ('signal', '信号', '📶'), ('design', '设计', '🎨'),
        ('signature', '签名', '🖋️'), ('significant', '重要的', '❗'),
    ]),
    'sist': ('站立', [
        ('assist', '协助', '🤝'), ('insist', '坚持', '💪'), ('consist', '由…组成', '🧩'),
        ('resist', '抵抗', '🛡️'), ('persist', '坚持', '🔁'),
    ]),
    'soci': ('社会；同伴', [
        ('social', '社会的', '👥'), ('society', '社会', '🏙️'), ('associate', '联想；结交', '🔗'),
    ]),
    'sol': ('单独；太阳', [
        ('solo', '独奏', '🎤'), ('solar', '太阳的', '☀️'), ('solid', '固体的', '🧊'),
    ]),
    'solv': ('解开', [
        ('solve', '解决', '🧩'), ('solution', '解决方案', '💡'), ('dissolve', '溶解', '💧'),
        ('resolve', '决心', '🎯'),
    ]),
    'spect': ('看', [
        ('inspect', '检查', '🔍'), ('respect', '尊敬', '🙇'), ('expect', '期待', '⏳'),
        ('suspect', '怀疑', '🕵️'), ('spectator', '观众', '👀'), ('aspect', '方面', '📐'),
        ('prospect', '前景', '🔭'), ('retrospect', '回顾', '🔄'),
    ]),
    'spir': ('呼吸；精神', [
        ('spirit', '精神', '✨'), ('inspire', '激励', '💡'), ('spiritual', '精神的', '🕊️'),
    ]),
    'sta': ('站立', [
        ('stable', '稳定的', '🏛️'), ('station', '车站', '🚉'), ('statue', '雕像', '🗿'),
        ('status', '地位', '📊'), ('stay', '停留', '🏨'), ('establish', '建立', '🏗️'),
        ('constant', '不断的', '🔁'),
    ]),
    'struct': ('建造', [
        ('structure', '结构', '🏗️'), ('construct', '建造', '🔨'), ('instruct', '指导', '📢'),
        ('instrument', '仪器；乐器', '🎸'), ('construction', '建造', '🚧'), ('destruction', '破坏', '💥'),
        ('obstruct', '阻碍', '🚫'),
    ]),
    'sum': ('拿；取', [
        ('consume', '消耗', '🔋'), ('assume', '假定', '🤔'), ('resume', '恢复；简历', '▶️'),
        ('summary', '摘要', '📋'),
    ]),
    'tact': ('接触', [
        ('contact', '联系', '📞'), ('tangible', '有形的', '📦'),
    ]),
    'tain': ('握；持', [
        ('contain', '包含', '📦'), ('maintain', '维持', '🔧'), ('obtain', '获得', '🎁'),
        ('entertain', '娱乐', '🎪'), ('continue', '继续', '▶️'), ('container', '容器', '🫙'),
        ('attain', '达到', '🏁'), ('detain', '扣留', '🔒'), ('sustain', '维持；支撑', '🧱'),
    ]),
    'techn': ('技术', [
        ('technique', '技巧', '🎯'), ('technology', '技术', '💻'), ('technical', '技术的', '⚙️'),
        ('technician', '技术员', '🔧'),
    ]),
    'tele': ('远', [
        ('telephone', '电话', '☎️'), ('television', '电视', '📺'), ('telescope', '望远镜', '🔭'),
        ('telegram', '电报', '📨'),
    ]),
    'temp': ('时间', [
        ('temporary', '暂时的', '⏳'), ('contemporary', '当代的', '🕰️'), ('temperature', '温度', '🌡️'),
    ]),
    'tend': ('伸展', [
        ('extend', '延伸', '↔️'), ('attend', '参加；出席', '🙋'), ('intend', '打算', '🎯'),
        ('tension', '紧张', '😬'), ('intense', '强烈的', '🔥'), ('pretend', '假装', '🎭'),
        ('attention', '注意', '👀'),
    ]),
    'termin': ('界限', [
        ('term', '学期；术语', '📅'), ('terminal', '终点站', '🚉'), ('determine', '决定', '🎯'),
    ]),
    'terr': ('土地', [
        ('territory', '领土', '🗺️'), ('terrain', '地形', '⛰️'),
    ]),
    'test': ('证明', [
        ('test', '测试', '📝'), ('protest', '抗议', '✊'), ('contest', '竞赛', '🏆'),
    ]),
    'text': ('编织', [
        ('text', '文本', '📄'), ('textbook', '教科书', '📘'), ('textile', '纺织品', '🧵'),
        ('context', '上下文', '📖'),
    ]),
    'tract': ('拉；拖', [
        ('tractor', '拖拉机', '🚜'), ('attract', '吸引', '🧲'), ('contract', '合同；收缩', '📄'),
        ('extract', '提取', '🧪'), ('distract', '分心', '🌀'), ('abstract', '抽象的', '🎨'),
        ('subtract', '减去', '➖'),
    ]),
    'trad': ('交付', [
        ('trade', '贸易', '💱'), ('tradition', '传统', '🏮'), ('traditional', '传统的', '🎎'),
    ]),
    'tribut': ('给予', [
        ('contribute', '贡献', '🎁'), ('distribute', '分发', '📤'), ('attribute', '归因于；属性', '🏷️'),
    ]),
    'turb': ('扰乱', [
        ('disturb', '打扰', '😣'), ('turbine', '涡轮', '🌀'),
    ]),
    'uni': ('一', [
        ('unite', '联合', '🤝'), ('union', '联盟', '🏛️'), ('unique', '独特的', '💎'),
        ('uniform', '制服', '👔'), ('university', '大学', '🎓'), ('universe', '宇宙', '🌌'),
        ('unit', '单元', '🔢'),
    ]),
    'urb': ('城市', [
        ('urban', '城市的', '🏙️'), ('suburb', '郊区', '🏘️'),
    ]),
    'val': ('价值', [
        ('value', '价值', '💎'), ('valid', '有效的', '✅'), ('available', '可获得的', '📦'),
        ('evaluate', '评价', '📊'),
    ]),
    'var': ('变化', [
        ('vary', '变化', '🔄'), ('various', '各种各样的', '🌈'), ('variety', '多样性', '🎨'),
        ('variable', '变量', '📊'),
    ]),
    'vent': ('来', [
        ('invent', '发明', '💡'), ('prevent', '阻止', '🛑'), ('event', '事件', '🎪'),
        ('convention', '惯例；大会', '🏛️'), ('adventure', '冒险', '🧭'), ('invention', '发明', '💡'),
    ]),
    'vers': ('转', [
        ('conversation', '对话', '💬'), ('reverse', '倒转', '🔄'), ('universe', '宇宙', '🌌'),
        ('anniversary', '周年纪念', '🎉'), ('advertise', '做广告', '📢'), ('version', '版本', '🔢'),
        ('diverse', '多样的', '🌈'), ('adverse', '不利的', '⚠️'),
    ]),
    'vis': ('看', [
        ('visit', '参观', '🚶'), ('visible', '可见的', '👀'), ('vision', '视力；远见', '👁️'),
        ('television', '电视', '📺'), ('video', '视频', '📹'), ('provide', '提供', '🎁'),
        ('evident', '明显的', '🔍'), ('supervise', '监督', '👀'), ('visual', '视觉的', '👁️'),
        ('revise', '修订；复习', '🔄'), ('devise', '设计；想出', '💡'), ('advise', '建议', '💬'),
        ('division', '分开；除法', '➗'), ('visitor', '参观者', '🧳'), ('provision', '供应；规定', '📦'),
        ('supervisor', '监督者', '👮'), ('evidence', '证据', '📑'),
    ]),
    'vit': ('生命', [
        ('vital', '至关重要的', '❤️'), ('vitamin', '维生素', '💊'), ('survive', '幸存', '🛟'),
        ('vivid', '生动的', '🌈'),
    ]),
    'voc': ('叫；声音', [
        ('voice', '声音', '🔊'), ('vocal', '嗓音的', '🎤'), ('vocabulary', '词汇', '📚'),
        ('advocate', '提倡', '📢'),
    ]),
    'vol': ('意愿', [
        ('volunteer', '志愿者', '🙋'), ('voluntary', '自愿的', '🤲'),
    ]),
    'volv': ('滚；转', [
        ('involve', '涉及', '🔗'), ('revolve', '旋转', '🌀'), ('revolution', '革命；旋转', '⚙️'),
        ('evolve', '进化', '🦎'), ('volume', '体积；音量', '🔊'),
    ]),
    'ven': ('来', [
        ('avenue', '大道', '🛣️'), ('convenient', '方便的', '👌'),
    ]),
    'cess': ('走；让', [
        ('process', '过程', '🔤'),
        ('access', '进入', '🔤'),
        ('success', '成功', '🔤'),
        ('proceed', '继续', '🔤'),
        ('exceed', '超过', '🔤'),
        ('recess', '休息', '🔤'),
        ('ancestor', '祖先', '🔤'),
        ('necessary', '必要的', '🔤'),
        ('concession', '让步', '🔤'),
    ]),
    'cent': ('百', [
        ('century', '世纪', '🔤'),
        ('percent', '百分比', '🔤'),
        ('cent', '分', '🔤'),
        ('centennial', '百年纪念', '🔤'),
    ]),
    'claim': ('呼喊', [
        ('claim', '声称', '🔤'),
        ('proclaim', '宣布', '🔤'),
        ('exclaim', '惊呼', '🔤'),
        ('acclaim', '喝彩', '🔤'),
        ('reclaim', '收回', '🔤'),
        ('exclamation', '感叹', '🔤'),
    ]),
    'cogn': ('知道', [
        ('recognize', '认出', '🔤'),
        ('cognition', '认知', '🔤'),
        ('cognizant', '知晓的', '🔤'),
    ]),
    'corp': ('身体', [
        ('corporation', '公司', '🔤'),
        ('corporate', '公司的', '🔤'),
        ('corpse', '尸体', '🔤'),
        ('corporal', '肉体的', '🔤'),
    ]),
    'cour': ('跑', [
        ('current', '当前的', '🔤'),
        ('occur', '发生', '🔤'),
        ('currency', '货币', '🔤'),
        ('course', '课程', '🔤'),
        ('recur', '重现', '🔤'),
        ('cursor', '光标', '🔤'),
        ('excursion', '远足', '🔤'),
        ('curriculum', '课程', '🔤'),
    ]),
    'crit': ('判断', [
        ('critic', '批评家', '🔤'),
        ('critical', '关键的', '🔤'),
        ('criterion', '标准', '🔤'),
        ('criticism', '批评', '🔤'),
    ]),
    'doc': ('教', [
        ('doctor', '医生', '🔤'),
        ('document', '文件', '🔤'),
        ('doctrine', '学说', '🔤'),
        ('docile', '温顺的', '🔤'),
    ]),
    'dorm': ('睡眠', [
        ('dormitory', '宿舍', '🔤'),
        ('dormant', '休眠的', '🔤'),
        ('dorm', '宿舍', '🔤'),
    ]),
    'dox': ('观点', [
        ('orthodox', '正统的', '🔤'),
        ('paradox', '悖论', '🔤'),
        ('dogma', '教条', '🔤'),
    ]),
    'don': ('给予', [
        ('donate', '捐赠', '🔤'),
        ('pardon', '原谅', '🔤'),
        ('donor', '捐赠者', '🔤'),
        ('donation', '捐赠', '🔤'),
    ]),
    'dyn': ('力量', [
        ('dynamic', '动态的', '🔤'),
        ('dynamite', '炸药', '🔤'),
        ('dynasty', '王朝', '🔤'),
        ('energy', '能量', '🔤'),
    ]),
    'eco': ('环境', [
        ('economy', '经济', '🔤'),
        ('ecology', '生态', '🔤'),
        ('ecosystem', '生态系统', '🔤'),
        ('economic', '经济的', '🔤'),
    ]),
    'empl': ('用', [
        ('example', '例子', '🔤'),
        ('employ', '雇佣', '🔤'),
        ('employment', '就业', '🔤'),
    ]),
    'err': ('错', [
        ('error', '错误', '🔤'),
        ('erratic', '不稳定的', '🔤'),
        ('errand', '差事', '🔤'),
        ('erroneous', '错误的', '🔤'),
    ]),
    'ethn': ('种族', [
        ('ethnic', '民族的', '🔤'),
        ('ethnicity', '种族', '🔤'),
        ('ethnology', '民族学', '🔤'),
    ]),
    'fab': ('说', [
        ('famous', '著名的', '🔤'),
        ('fame', '名声', '🔤'),
        ('fable', '寓言', '🔤'),
        ('fabric', '织物', '🔤'),
        ('fabricate', '编造', '🔤'),
    ]),
    'feder': ('联盟', [
        ('federal', '联邦的', '🔤'),
        ('federation', 'federation', '🔤'),
        ('confederation', '联盟', '🔤'),
    ]),
    'fend': ('打击', [
        ('defend', '保卫', '🔤'),
        ('offense', '进攻', '🔤'),
        ('fence', '栅栏', '🔤'),
        ('defensive', '防御的', '🔤'),
    ]),
    'fid': ('信任', [
        ('confident', '自信的', '🔤'),
        ('fidelity', '忠诚', '🔤'),
        ('confide', '倾诉', '🔤'),
        ('diffident', '缺乏自信的', '🔤'),
    ]),
    'fil': ('线', [
        ('file', '文件', '🔤'),
        ('filament', '细丝', '🔤'),
        ('profile', '简介', '🔤'),
        ('filial', '子女的', '🔤'),
    ]),
    'flag': ('燃烧', [
        ('flame', '火焰', '🔤'),
        ('flammable', '易燃的', '🔤'),
        ('conflagration', '大火', '🔤'),
    ]),
    'flor': ('花', [
        ('flower', '花', '🔤'),
        ('floral', '花的', '🔤'),
        ('florist', '花商', '🔤'),
        ('flourish', '繁荣', '🔤'),
    ]),
    'forc': ('强', [
        ('force', '力量', '🔤'),
        ('fort', '堡垒', '🔤'),
        ('fortune', '运气', '🔤'),
        ('comfort', '舒适', '🔤'),
        ('effort', '努力', '🔤'),
        ('enforce', '执行', '🔤'),
    ]),
    'fus': ('倒', [
        ('fuse', '保险丝', '🔤'),
        ('confuse', '使困惑', '🔤'),
        ('diffuse', '扩散', '🔤'),
        ('infusion', '注入', '🔤'),
        ('refuse', '拒绝', '🔤'),
        ('transfusion', '输血', '🔤'),
    ]),
    'gram': ('写', [
        ('grammar', '语法', '🔤'),
        ('program', '程序', '🔤'),
        ('telegram', '电报', '🔤'),
        ('diagram', '图表', '🔤'),
        ('kilogram', '千克', '🔤'),
    ]),
    'grav': ('重', [
        ('grave', '坟墓', '🔤'),
        ('gravity', '重力', '🔤'),
        ('gravitation', '引力', '🔤'),
        ('aggravate', '加重', '🔤'),
    ]),
    'greg': ('群', [
        ('congregate', '聚集', '🔤'),
        ('segregate', '隔离', '🔤'),
        ('egregious', '极坏的', '🔤'),
    ]),
    'hab': ('有', [
        ('habit', '习惯', '🔤'),
        ('inhabit', '居住', '🔤'),
        ('exhibit', '展览', '🔤'),
        ('prohibit', '禁止', '🔤'),
    ]),
    'her': ('粘', [
        ('adhere', '坚持', '🔤'),
        ('coherent', '连贯的', '🔤'),
        ('inherent', '固有的', '🔤'),
    ]),
    'hom': ('同', [
        ('homogeneous', '同质的', '🔤'),
        ('homonym', '同形异义词', '🔤'),
        ('homicide', '杀人', '🔤'),
    ]),
    'hort': ('园', [
        ('horticulture', '园艺', '🔤'),
        ('orchard', '果园', '🔤'),
    ]),
    'hum': ('土', [
        ('human', '人类', '🔤'),
        ('humble', '谦逊的', '🔤'),
        ('humility', '谦卑', '🔤'),
    ]),
    'hydr': ('水', [
        ('hydrogen', '氢', '🔤'),
        ('hydraulic', '液压的', '🔤'),
        ('hydro', '水力的', '🔤'),
        ('dehydrate', '脱水', '🔤'),
    ]),
    'hypn': ('睡眠', [
        ('hypnosis', '催眠', '🔤'),
        ('hypnotize', '使催眠', '🔤'),
    ]),
    'ign': ('火', [
        ('ignite', '点燃', '🔤'),
        ('igneous', '火的', '🔤'),
        ('ignition', '点火', '🔤'),
    ]),
    'integr': ('完整', [
        ('integrate', '整合', '🔤'),
        ('integral', '完整的', '🔤'),
        ('integrity', '正直', '🔤'),
        ('disintegrate', '瓦解', '🔤'),
    ]),
    'it': ('走', [
        ('exit', '出口', '🔤'),
        ('initial', '最初的', '🔤'),
        ('initiate', '发起', '🔤'),
        ('itinerary', '行程', '🔤'),
    ]),
    'jur': ('法', [
        ('jury', '陪审团', '🔤'),
        ('justice', '正义', '🔤'),
        ('justify', '证明…正当', '🔤'),
        ('injury', '伤害', '🔤'),
        ('jurisdiction', '管辖权', '🔤'),
    ]),
    'lat': ('带', [
        ('relate', '关联', '🔤'),
        ('translate', '翻译', '🔤'),
        ('correlate', '相关', '🔤'),
        ('latitude', '纬度', '🔤'),
    ]),
    'lav': ('洗', [
        ('lava', '熔岩', '🔤'),
        ('lavish', '奢侈的', '🔤'),
        ('lavatory', '洗手间', '🔤'),
    ]),
    'lev': ('举', [
        ('elevate', '提升', '🔤'),
        ('lever', '杠杆', '🔤'),
        ('relieve', '缓解', '🔤'),
        ('levy', '征收', '🔤'),
    ]),
    'lingu': ('舌', [
        ('linguistic', '语言的', '🔤'),
        ('language', '语言', '🔤'),
        ('bilingual', '双语的', '🔤'),
    ]),
    'liter': ('字母', [
        ('literature', '文学', '🔤'),
        ('literal', '字面的', '🔤'),
        ('literate', '有文化的', '🔤'),
        ('illiterate', '文盲的', '🔤'),
    ]),
    'lith': ('石', [
        ('lithium', '锂', '🔤'),
        ('monolith', '独石', '🔤'),
        ('lithograph', '平版印刷', '🔤'),
    ]),
    'luc': ('光', [
        ('lucid', '清晰的', '🔤'),
        ('illuminate', '照亮', '🔤'),
        ('translucent', '半透明的', '🔤'),
    ]),
    'lud': ('玩', [
        ('illusion', '幻觉', '🔤'),
        ('delusion', '错觉', '🔤'),
        ('elude', '逃避', '🔤'),
        ('allude', '暗示', '🔤'),
    ]),
    'mag': ('大', [
        ('magnet', '磁铁', '🔤'),
        ('magnitude', '巨大', '🔤'),
        ('magnificent', '壮丽的', '🔤'),
        ('magnify', '放大', '🔤'),
    ]),
    'mal': ('坏', [
        ('malevolent', '恶意的', '🔤'),
        ('malicious', '恶毒的', '🔤'),
        ('maltreat', '虐待', '🔤'),
        ('malfunction', '故障', '🔤'),
    ]),
    'man': ('手', [
        ('manage', '管理', '🔤'),
        ('manifest', '明显的', '🔤'),
        ('manipulate', '操纵', '🔤'),
        ('manner', '方式', '🔤'),
        ('manicure', '美甲', '🔤'),
    ]),
    'matr': ('母', [
        ('material', '材料', '🔤'),
        ('matter', '物质', '🔤'),
        ('maternal', '母亲的', '🔤'),
        ('matriarch', '女家长', '🔤'),
        ('matrix', '矩阵', '🔤'),
    ]),
    'mech': ('机械', [
        ('mechanic', '机械师', '🔤'),
        ('mechanism', '机制', '🔤'),
        ('mechanical', '机械的', '🔤'),
    ]),
    'med': ('医治', [
        ('medical', '医学的', '🔤'),
        ('medicine', '药', '🔤'),
        ('remedy', '补救', '🔤'),
        ('mediate', '调解', '🔤'),
    ]),
    'mel': ('歌', [
        ('melody', '旋律', '🔤'),
        ('melodious', '悦耳的', '🔤'),
    ]),
    'merc': ('贸易', [
        ('merchant', '商人', '🔤'),
        ('commerce', '商业', '🔤'),
        ('merchandise', '商品', '🔤'),
        ('mercenary', '雇佣兵', '🔤'),
    ]),
    'merg': ('浸', [
        ('emerge', '出现', '🔤'),
        ('merge', '合并', '🔤'),
        ('submerge', '淹没', '🔤'),
        ('emergency', '紧急情况', '🔤'),
        ('immerse', '沉浸', '🔤'),
    ]),
    'metr': ('测量', [
        ('meter', '米', '🔤'),
        ('metric', '公制的', '🔤'),
        ('geometry', '几何', '🔤'),
        ('thermometer', '温度计', '🔤'),
        ('symmetry', '对称', '🔤'),
        ('diameter', '直径', '🔤'),
    ]),
    'mir': ('奇', [
        ('miracle', '奇迹', '🔤'),
        ('mirror', '镜子', '🔤'),
        ('admire', '钦佩', '🔤'),
    ]),
    'misc': ('混', [
        ('miscellaneous', '混杂的', '🔤'),
        ('miscible', '可混的', '🔤'),
    ]),
    'mon': ('警告', [
        ('monitor', '监控', '🔤'),
        ('monument', '纪念碑', '🔤'),
        ('admonish', '劝告', '🔤'),
    ]),
    'morph': ('形', [
        ('morphology', '形态学', '🔤'),
        ('metamorphosis', '变形', '🔤'),
        ('amorphous', '无定形的', '🔤'),
    ]),
    'mort': ('死', [
        ('mortal', '终有一死的', '🔤'),
        ('mortgage', '抵押', '🔤'),
        ('immortal', '不朽的', '🔤'),
        ('mortuary', '太平间', '🔤'),
    ]),
    'mot': ('动', [
        ('motion', '运动', '🔤'),
        ('motor', '发动机', '🔤'),
        ('emotion', '情感', '🔤'),
        ('promote', '促进', '🔤'),
        ('remote', '远程的', '🔤'),
        ('motive', '动机', '🔤'),
    ]),
    'mount': ('爬', [
        ('mountain', '山', '🔤'),
        ('mount', '登上', '🔤'),
        ('amount', '数量', '🔤'),
        ('surmount', '克服', '🔤'),
    ]),
    'mur': ('墙', [
        ('mural', '壁画', '🔤'),
        ('immune', '免疫的', '🔤'),
    ]),
    'mut': ('变', [
        ('mutate', '变异', '🔤'),
        ('mutual', '相互的', '🔤'),
        ('commute', '通勤', '🔤'),
        ('mutation', '突变', '🔤'),
    ]),
    'nav': ('船', [
        ('navy', '海军', '🔤'),
        ('navigation', '航行', '🔤'),
        ('naval', '海军的', '🔤'),
    ]),
    'neur': ('神经', [
        ('neural', '神经的', '🔤'),
        ('neuron', '神经元', '🔤'),
        ('neurosis', '神经症', '🔤'),
    ]),
    'nox': ('害', [
        ('innocent', '无辜的', '🔤'),
        ('noxious', '有害的', '🔤'),
        ('obnoxious', '讨厌的', '🔤'),
        ('nuisance', '讨厌的人', '🔤'),
    ]),
    'nutri': ('营养', [
        ('nutrition', '营养', '🔤'),
        ('nutritious', '有营养的', '🔤'),
        ('nutrient', '营养素', '🔤'),
    ]),
    'nym': ('名', [
        ('synonym', '近义词', '🔤'),
        ('antonym', '反义词', '🔤'),
        ('anonymous', '匿名的', '🔤'),
        ('acronym', '首字母缩略词', '🔤'),
    ]),
    'ocul': ('眼', [
        ('oculist', '眼科医生', '🔤'),
        ('ocular', '眼的', '🔤'),
        ('binoculars', '双筒望远镜', '🔤'),
    ]),
    'or': ('口', [
        ('oral', '口头的', '🔤'),
        ('orator', '演说家', '🔤'),
        ('oracle', '神谕', '🔤'),
    ]),
    'orb': ('圆', [
        ('orbit', '轨道', '🔤'),
        ('orb', '球体', '🔤'),
        ('orbital', '轨道的', '🔤'),
    ]),
    'orn': ('装饰', [
        ('ornament', '装饰', '🔤'),
        ('ornate', '华丽的', '🔤'),
        ('adorn', '装饰', '🔤'),
    ]),
    'ortho': ('正', [
        ('orthodox', '正统的', '🔤'),
        ('orthodontist', '正牙医生', '🔤'),
        ('orthography', '正字法', '🔤'),
    ]),
    'oss': ('骨', [
        ('ossify', '骨化', '🔤'),
        ('fossil', '化石', '🔤'),
        ('ossuary', '骨灰瓮', '🔤'),
    ]),
    'paci': ('和平', [
        ('pacific', '和平的', '🔤'),
        ('pacify', '使平静', '🔤'),
        ('pacifist', '和平主义者', '🔤'),
    ]),
    'patr': ('父', [
        ('patriot', '爱国者', '🔤'),
        ('patron', '赞助人', '🔤'),
        ('pattern', '图案', '🔤'),
        ('patriarch', '族长', '🔤'),
    ]),
    'pen': ('几乎', [
        ('penalty', '惩罚', '🔤'),
        ('peninsula', '半岛', '🔤'),
        ('peninsular', '半岛的', '🔤'),
    ]),
    'per': ('试', [
        ('experience', '经验', '🔤'),
        ('experiment', '实验', '🔤'),
        ('peril', '危险', '🔤'),
    ]),
    'pet': ('求', [
        ('compete', '竞争', '🔤'),
        ('repeat', '重复', '🔤'),
        ('appetite', '食欲', '🔤'),
        ('petition', '请愿', '🔤'),
        ('perpetual', '永恒的', '🔤'),
    ]),
    'phil': ('爱', [
        ('philosophy', '哲学', '🔤'),
        ('philanthropy', '慈善', '🔤'),
        ('philharmonic', '爱乐的', '🔤'),
    ]),
    'phob': ('怕', [
        ('phobia', '恐惧症', '🔤'),
        ('claustrophobia', '幽闭恐惧症', '🔤'),
        ('xenophobia', '排外', '🔤'),
    ]),
    'phys': ('自然', [
        ('physics', '物理', '🔤'),
        ('physician', '医生', '🔤'),
        ('physical', '身体的', '🔤'),
        ('physique', '体格', '🔤'),
    ]),
    'pict': ('画', [
        ('picture', '图画', '🔤'),
        ('depict', '描绘', '🔤'),
        ('pictograph', '象形文字', '🔤'),
    ]),
    'plac': ('悦', [
        ('place', '地方', '🔤'),
        ('placid', '平静的', '🔤'),
        ('placate', '安抚', '🔤'),
        ('complacent', '自满的', '🔤'),
    ]),
    'plaud': ('拍', [
        ('applaud', '鼓掌', '🔤'),
        ('plausible', '看似合理的', '🔤'),
        ('plaudit', '喝彩', '🔤'),
    ]),
    'ple': ('满', [
        ('complete', '完整的', '🔤'),
        ('plenty', '大量', '🔤'),
        ('replenish', '补充', '🔤'),
        ('implement', '实施', '🔤'),
        ('complement', '补充', '🔤'),
    ]),
    'plex': ('折', [
        ('complex', '复杂的', '🔤'),
        ('perplex', '使困惑', '🔤'),
        ('duplex', '双重的', '🔤'),
    ]),
    'plor': ('哭', [
        ('explore', '探索', '🔤'),
        ('deplore', '悲叹', '🔤'),
        ('implore', '恳求', '🔤'),
    ]),
    'pneum': ('气', [
        ('pneumonia', '肺炎', '🔤'),
        ('pneumatic', '气动的', '🔤'),
    ]),
    'pod': ('足', [
        ('podiatrist', '足病医生', '🔤'),
        ('pseudopod', '伪足', '🔤'),
        ('tripod', '三脚架', '🔤'),
        ('octopus', '章鱼', '🔤'),
    ]),
    'polic': ('城', [
        ('police', '警察', '🔤'),
        ('policy', '政策', '🔤'),
        ('politics', '政治', '🔤'),
        ('politician', '政客', '🔤'),
    ]),
    'pon': ('放', [
        ('component', '组成部分', '🔤'),
        ('postpone', '推迟', '🔤'),
        ('opponent', '对手', '🔤'),
        ('compound', '化合物', '🔤'),
    ]),
    'pot': ('喝', [
        ('pot', '锅', '🔤'),
        ('potion', '药水', '🔤'),
        ('potent', '有效的', '🔤'),
        ('potential', '潜在的', '🔤'),
    ]),
    'pract': ('做', [
        ('practice', '练习', '🔤'),
        ('practical', '实际的', '🔤'),
        ('practitioner', '从业者', '🔤'),
    ]),
    'prehend': ('抓', [
        ('comprehend', '理解', '🔤'),
        ('apprehend', '逮捕', '🔤'),
        ('comprehensive', '全面的', '🔤'),
    ]),
    'prof': ('说', [
        ('professor', '教授', '🔤'),
        ('profit', '利润', '🔤'),
        ('profound', '深刻的', '🔤'),
        ('profess', '承认', '🔤'),
        ('profile', '简介', '🔤'),
        ('profession', '职业', '🔤'),
    ]),
    'prom': ('前', [
        ('promise', '承诺', '🔤'),
        ('promote', '促进', '🔤'),
        ('prompt', '迅速的', '🔤'),
        ('promenade', '散步', '🔤'),
    ]),
    'pron': ('发音', [
        ('pronounce', '发音', '🔤'),
        ('pronunciation', '发音', '🔤'),
        ('pronoun', '代词', '🔤'),
    ]),
    'proper': ('自有', [
        ('property', '财产', '🔤'),
        ('proper', '适当的', '🔤'),
        ('proprietor', '所有者', '🔤'),
        ('appropriate', '适当的', '🔤'),
    ]),
    'pugn': ('战', [
        ('pugnacious', '好斗的', '🔤'),
        ('repugnant', '令人厌恶的', '🔤'),
        ('impugn', '指责', '🔤'),
    ]),
    'puls': ('驱', [
        ('pulse', '脉搏', '🔤'),
        ('impulse', '冲动', '🔤'),
        ('compel', '强迫', '🔤'),
        ('expel', '开除', '🔤'),
        ('repulsive', '排斥的', '🔤'),
        ('pulsate', '脉动', '🔤'),
    ]),
    'pur': ('纯', [
        ('pure', '纯的', '🔤'),
        ('purge', '净化', '🔤'),
        ('purify', '净化', '🔤'),
        ('purist', '纯粹主义者', '🔤'),
    ]),
    'put': ('想', [
        ('compute', '计算', '🔤'),
        ('dispute', '争论', '🔤'),
        ('repute', '声誉', '🔤'),
        ('deputy', '副手', '🔤'),
    ]),
    'pyr': ('火', [
        ('pyramid', '金字塔', '🔤'),
        ('pyre', '火葬柴堆', '🔤'),
    ]),
    'quali': ('质', [
        ('quality', '质量', '🔤'),
        ('qualify', '使合格', '🔤'),
        ('qualified', '合格的', '🔤'),
    ]),
    'quant': ('量', [
        ('quantity', '数量', '🔤'),
        ('quantify', '量化', '🔤'),
        ('quantitative', '数量的', '🔤'),
    ]),
    'quer': ('问', [
        ('question', '问题', '🔤'),
        ('request', '请求', '🔤'),
        ('require', '需要', '🔤'),
        ('inquire', '询问', '🔤'),
        ('conquer', '征服', '🔤'),
        ('quest', '追求', '🔤'),
        ('query', '查询', '🔤'),
    ]),
    'qui': ('静', [
        ('quiet', '安静的', '🔤'),
        ('quit', '退出', '🔤'),
        ('quite', '相当', '🔤'),
        ('quaint', '古雅的', '🔤'),
    ]),
    'quot': ('多少', [
        ('quote', '引用', '🔤'),
        ('quotient', '商', '🔤'),
        ('quota', '配额', '🔤'),
    ]),
    'radi': ('射线', [
        ('radar', '雷达', '🔤'),
        ('radio', '收音机', '🔤'),
        ('radiant', '辐射的', '🔤'),
        ('radiation', '辐射', '🔤'),
        ('radius', '半径', '🔤'),
    ]),
    'ras': ('刮', [
        ('erase', '擦除', '🔤'),
        ('razor', '剃刀', '🔤'),
        ('abrade', '磨损', '🔤'),
    ]),
    'rat': ('理', [
        ('ratio', '比率', '🔤'),
        ('rational', '理性的', '🔤'),
        ('rate', '比率', '🔤'),
        ('irritate', '激怒', '🔤'),
    ]),
    'rid': ('笑', [
        ('ridiculous', '荒谬的', '🔤'),
        ('ridicule', '嘲笑', '🔤'),
        ('deride', '嘲笑', '🔤'),
    ]),
    'rig': ('直', [
        ('rigid', '僵硬的', '🔤'),
        ('rigorous', '严格的', '🔤'),
    ]),
    'rod': ('咬', [
        ('corrode', '腐蚀', '🔤'),
        ('rodent', '啮齿动物', '🔤'),
        ('erode', '侵蚀', '🔤'),
    ]),
    'rog': ('问', [
        ('interrogate', '审问', '🔤'),
        ('arrogant', '傲慢的', '🔤'),
        ('prerogative', '特权', '🔤'),
    ]),
    'rol': ('滚', [
        ('role', '角色', '🔤'),
        ('roll', '滚动', '🔤'),
        ('control', '控制', '🔤'),
        ('patrol', '巡逻', '🔤'),
    ]),
    'rom': ('罗马', [
        ('romantic', '浪漫的', '🔤'),
        ('Rome', '罗马', '🔤'),
    ]),
    'rot': ('轮', [
        ('rotate', '旋转', '🔤'),
        ('rotor', '转子', '🔤'),
        ('rotary', '旋转的', '🔤'),
    ]),
    'rud': ('粗', [
        ('rude', '粗鲁的', '🔤'),
        ('rudiment', '基础', '🔤'),
        ('erudite', '博学的', '🔤'),
    ]),
    'sacr': ('圣', [
        ('sacred', '神圣的', '🔤'),
        ('sacrifice', '牺牲', '🔤'),
        ('sacrament', '圣礼', '🔤'),
    ]),
    'sal': ('盐/健', [
        ('salary', '薪水', '🔤'),
        ('salad', '沙拉', '🔤'),
        ('salute', '敬礼', '🔤'),
        ('saint', '圣徒', '🔤'),
        ('safe', '安全的', '🔤'),
    ]),
    'san': ('健', [
        ('sane', '神志清醒的', '🔤'),
        ('sanitary', '卫生的', '🔤'),
        ('insane', '疯狂的', '🔤'),
        ('sanitize', '消毒', '🔤'),
    ]),
    'scal': ('爬', [
        ('scale', '规模', '🔤'),
        ('ascend', '上升', '🔤'),
        ('descendant', '后代', '🔤'),
    ]),
    'sen': ('老', [
        ('senior', '年长的', '🔤'),
        ('senator', '参议员', '🔤'),
        ('senile', '衰老的', '🔤'),
        ('senate', '参议院', '🔤'),
    ]),
    'sequ': ('跟', [
        ('sequence', '顺序', '🔤'),
        ('consequence', '后果', '🔤'),
        ('subsequent', '随后的', '🔤'),
        ('execute', '执行', '🔤'),
        ('prosecute', '起诉', '🔤'),
    ]),
    'sess': ('坐', [
        ('session', '会议', '🔤'),
        ('possess', '拥有', '🔤'),
        ('assess', '评估', '🔤'),
        ('obsession', '痴迷', '🔤'),
    ]),
    'set': ('放', [
        ('set', '放', '🔤'),
        ('settle', '解决', '🔤'),
        ('setting', '设置', '🔤'),
    ]),
    'sid': ('坐', [
        ('reside', '居住', '🔤'),
        ('preside', '主持', '🔤'),
        ('beside', '在…旁', '🔤'),
        ('aside', '在旁边', '🔤'),
        ('inside', '里面', '🔤'),
    ]),
    'sin': ('曲', [
        ('sine', '正弦', '🔤'),
        ('sinuous', '蜿蜒的', '🔤'),
    ]),
    'somn': ('睡', [
        ('somnolent', '困倦的', '🔤'),
        ('insomnia', '失眠', '🔤'),
    ]),
    'son': ('声', [
        ('sonic', '声速的', '🔤'),
        ('sonar', '声呐', '🔤'),
        ('consonant', '辅音', '🔤'),
        ('dissonant', '不和谐的', '🔤'),
    ]),
    'soph': ('智', [
        ('sophisticated', '复杂的', '🔤'),
        ('philosopher', '哲学家', '🔤'),
        ('sophomore', '大二学生', '🔤'),
    ]),
    'sper': ('望', [
        ('despair', '绝望', '🔤'),
        ('prosper', '繁荣', '🔤'),
        ('prosperous', '繁荣的', '🔤'),
    ]),
    'spic': ('看', [
        ('conspicuous', '显眼的', '🔤'),
        ('suspicious', '怀疑的', '🔤'),
        ('perspective', '视角', '🔤'),
        ('retrospect', '回顾', '🔤'),
    ]),
    'sur': ('上', [
        ('surface', '表面', '🔤'),
        ('surpass', '超越', '🔤'),
        ('survive', '幸存', '🔤'),
        ('survey', '调查', '🔤'),
    ]),
    'tail': ('切', [
        ('tailor', '裁缝', '🔤'),
        ('detail', '细节', '🔤'),
        ('retail', '零售', '🔤'),
        ('curtailed', '缩短的', '🔤'),
    ]),
    'tang': ('触', [
        ('tangible', '可触摸的', '🔤'),
        ('taste', '品尝', '🔤'),
        ('tangent', '切线', '🔤'),
    ]),
    'temper': ('调', [
        ('temper', '脾气', '🔤'),
        ('temperament', '气质', '🔤'),
        ('temperance', '节制', '🔤'),
        ('tempest', '暴风雨', '🔤'),
    ]),
    'tempor': ('时', [
        ('tempo', '节奏', '🔤'),
        ('temporal', '暂时的', '🔤'),
    ]),
    'ten': ('持', [
        ('tenant', '房客', '🔤'),
        ('tenet', '信条', '🔤'),
        ('content', '内容', '🔤'),
        ('continent', '大陆', '🔤'),
        ('tenure', '任期', '🔤'),
        ('tenacious', '坚韧的', '🔤'),
    ]),
    'theo': ('神', [
        ('theology', '神学', '🔤'),
        ('atheist', '无神论者', '🔤'),
        ('theocracy', '神权政治', '🔤'),
    ]),
    'therm': ('热', [
        ('thermal', '热的', '🔤'),
        ('thermometer', '温度计', '🔤'),
        ('thermostat', '恒温器', '🔤'),
    ]),
    'thesis': ('放', [
        ('thesis', '论文', '🔤'),
        ('hypothesis', '假设', '🔤'),
        ('synthesis', '综合', '🔤'),
        ('parenthesis', '括号', '🔤'),
    ]),
    'tim': ('怕', [
        ('timid', '胆怯的', '🔤'),
        ('intimidate', '恐吓', '🔤'),
        ('timorous', '胆怯的', '🔤'),
    ]),
    'tir': ('拉', [
        ('tire', '疲劳', '🔤'),
        ('retire', '退休', '🔤'),
        ('attire', '服装', '🔤'),
    ]),
    'tors': ('扭', [
        ('torture', '折磨', '🔤'),
        ('distort', '扭曲', '🔤'),
        ('extort', '敲诈', '🔤'),
        ('torrent', '激流', '🔤'),
        ('retort', '反驳', '🔤'),
    ]),
    'treat': ('处理', [
        ('treat', '对待', '🔤'),
        ('treaty', '条约', '🔤'),
        ('retreat', '撤退', '🔤'),
        ('entreat', '恳求', '🔤'),
    ]),
    'trib': ('付', [
        ('tribe', '部落', '🔤'),
        ('tribute', '贡品', '🔤'),
    ]),
    'trud': ('推', [
        ('intrude', '侵入', '🔤'),
        ('extrude', '挤出', '🔤'),
        ('protrude', '突出', '🔤'),
        ('obtrude', '强加', '🔤'),
    ]),
    'tuit': ('护', [
        ('tuition', '学费', '🔤'),
        ('intuition', '直觉', '🔤'),
        ('tutor', '导师', '🔤'),
    ]),
    'typ': ('印', [
        ('type', '类型', '🔤'),
        ('typical', '典型的', '🔤'),
        ('typo', '排版错误', '🔤'),
        ('prototype', '原型', '🔤'),
        ('typography', '印刷术', '🔤'),
    ]),
    'und': ('波', [
        ('abundant', '丰富的', '🔤'),
        ('redundant', '冗余的', '🔤'),
        ('inundate', '淹没', '🔤'),
        ('undulate', '起伏', '🔤'),
    ]),
    'util': ('用', [
        ('utility', '实用', '🔤'),
        ('utilize', '利用', '🔤'),
        ('utilitarian', '实用的', '🔤'),
    ]),
    'vac': ('空', [
        ('vacant', '空的', '🔤'),
        ('vacuum', '真空', '🔤'),
        ('vacation', '假期', '🔤'),
        ('evacuate', '疏散', '🔤'),
    ]),
    'vad': ('去', [
        ('invade', '入侵', '🔤'),
        ('evade', '逃避', '🔤'),
        ('pervade', '弥漫', '🔤'),
    ]),
    'vag': ('游', [
        ('vague', '模糊的', '🔤'),
        ('vagabond', '流浪者', '🔤'),
        ('extravagant', '奢侈的', '🔤'),
    ]),
    'van': ('空', [
        ('vanish', '消失', '🔤'),
        ('vanity', '虚荣', '🔤'),
        ('vain', '徒劳的', '🔤'),
    ]),
    'veh': ('运', [
        ('vehicle', '车辆', '🔤'),
        ('vehement', '激烈的', '🔤'),
        ('convey', '传达', '🔤'),
    ]),
    'verb': ('词', [
        ('verb', '动词', '🔤'),
        ('verbal', '口头的', '🔤'),
        ('adverb', '副词', '🔤'),
        ('proverb', '谚语', '🔤'),
    ]),
    'vert': ('转', [
        ('convert', '转换', '🔤'),
        ('divert', '转移', '🔤'),
        ('invert', '倒置', '🔤'),
        ('avert', '避免', '🔤'),
        ('introvert', '内向者', '🔤'),
        ('extrovert', '外向者', '🔤'),
        ('vertebra', '脊椎', '🔤'),
    ]),
    'vest': ('衣', [
        ('vest', '背心', '🔤'),
        ('invest', '投资', '🔤'),
        ('vestige', '痕迹', '🔤'),
    ]),
    'vic': ('邻', [
        ('victim', '受害者', '🔤'),
        ('vicar', '牧师', '🔤'),
        ('vicarious', '间接的', '🔤'),
        ('vice', '缺点', '🔤'),
    ]),
    'vinc': ('胜', [
        ('victory', '胜利', '🔤'),
        ('convince', '说服', '🔤'),
        ('invincible', '不可战胜的', '🔤'),
        ('vanquish', '征服', '🔤'),
    ]),
    'vir': ('男', [
        ('virtue', '美德', '🔤'),
        ('virile', '有男子气概的', '🔤'),
        ('virus', '病毒', '🔤'),
        ('virulent', '致命的', '🔤'),
    ]),
    'vor': ('吃', [
        ('devour', '吞食', '🔤'),
        ('voracious', '贪婪的', '🔤'),
        ('carnivore', '肉食动物', '🔤'),
        ('herbivore', '草食动物', '🔤'),
    ]),
    'vot': ('愿', [
        ('vote', '投票', '🔤'),
        ('veto', '否决', '🔤'),
        ('devote', '奉献', '🔤'),
    ]),
    'xen': ('异', [
        ('xenophobia', '排外', '🔤'),
        ('xenon', '氙', '🔤'),
    ]),
    'zo': ('动物', [
        ('zoo', '动物园', '🔤'),
        ('zoology', '动物学', '🔤'),
        ('zodiac', '黄道带', '🔤'),
        ('zoom', '缩放', '🔤'),
    ]),
    'scope': ('看；观察', [
        ('telescope', '望远镜', '🔭'), ('microscope', '显微镜', '🔬'), ('scope', '范围；镜', '🔍'),
        ('periscope', '潜望镜', '🛥️'), ('kaleidoscope', '万花筒', '🎡'),
    ]),
    'chron': ('时间', [
        ('chronicle', '编年史', '📜'), ('chronic', '慢性的', '⏳'), ('chronology', '年表', '🗓️'),
        ('synchronize', '使同步', '🔄'),
    ]),

}
