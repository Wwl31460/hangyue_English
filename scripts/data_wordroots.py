# -*- coding: utf-8 -*-
"""本族单词词根（英语本族自由语素 + 派生后缀）。

由 scripts/auto_wordroots.py 自动扫描词表生成，**请勿手工编辑**。
例：help（帮助）本身就是词根 → helpful / helpless / helpfully …
与 data_roots.py 的拉丁/希腊词根互为补充；同名 key 以 data_roots.py 为准。
"""

WORDBASES = {
    "accept": ("接受", [
        ("accept", "接受", "✅"),
        ("acceptable", "可接受的", "✅"),
    ]),
    "accommodate": ("容纳；提供住宿", [
        ("accommodate", "容纳；提供住宿", "🛏️"),
        ("accommodation", "住宿；膳宿", "🛏️"),
    ]),
    "account": ("账户；解释", [
        ("account", "账户；解释", "📒"),
        ("accountant", "会计", "🔤"),
    ]),
    "achieve": ("实现", [
        ("achieve", "实现", "🏅"),
        ("achievement", "成就", "🏆"),
    ]),
    "active": ("活跃的", [
        ("active", "活跃的", "🏃"),
        ("activity", "活动", "🎲"),
        ("activist", "活动人士", "📣"),
        ("interactive", "互动的", "🖱️"),
    ]),
    "add": ("增加", [
        ("add", "增加", "➕"),
        ("addition", "添加；增加", "➕"),
        ("additional", "额外的", "➕"),
    ]),
    "addition": ("添加；增加", [
        ("addition", "添加；增加", "➕"),
        ("additional", "额外的", "➕"),
    ]),
    "adjust": ("调整；适应", [
        ("adjust", "调整；适应", "🔧"),
        ("adjustable", "可调节的", "🔧"),
    ]),
    "adventure": ("冒险；奇遇", [
        ("adventure", "冒险；奇遇", "🗺️"),
        ("adventurous", "爱冒险的", "🧗"),
    ]),
    "afford": ("承担得起", [
        ("afford", "承担得起", "💰"),
        ("affordable", "负担得起的", "💰"),
    ]),
    "agree": ("同意；赞成", [
        ("agree", "同意；赞成", "🤝"),
        ("agreement", "同意", "🤝"),
        ("disagree", "不同意", "❌"),
    ]),
    "aim": ("目标；旨在", [
        ("aim", "目标；旨在", "🎯"),
        ("aimless", "漫无目的的", "🧭"),
    ]),
    "announce": ("宣布", [
        ("announce", "宣布", "📢"),
        ("announcement", "公告", "📢"),
    ]),
    "apart": ("分离", [
        ("apart", "分离", "🔀"),
        ("apartment", "公寓", "🏢"),
    ]),
    "appropriate": ("合适的", [
        ("appropriate", "合适的", "✅"),
        ("appropriately", "适当地", "✅"),
    ]),
    "arrange": ("安排", [
        ("arrange", "安排", "🗂️"),
        ("arrangement", "安排；布置", "📋"),
    ]),
    "art": ("艺术；美术", [
        ("art", "艺术；美术", "🎨"),
        ("artist", "艺术家", "🎨"),
    ]),
    "assist": ("协助；帮助", [
        ("assist", "协助；帮助", "🤝"),
        ("assistant", "助手", "🔤"),
    ]),
    "attend": ("出席", [
        ("attend", "出席", "🙋"),
        ("attendant", "服务员", "🔤"),
    ]),
    "attract": ("吸引", [
        ("attract", "吸引", "🧲"),
        ("attractive", "有吸引力的", "✨"),
    ]),
    "back": ("回来；背部", [
        ("back", "回来；背部", "🔙"),
        ("backward", "向后", "⏪"),
    ]),
    "bad": ("坏的", [
        ("bad", "坏的", "👎"),
        ("badly", "糟糕地；严重地", "💢"),
    ]),
    "beautiful": ("美丽的", [
        ("beautiful", "美丽的", "🌸"),
        ("beautifully", "优美地", "🌸"),
    ]),
    "beauty": ("美；美人", [
        ("beauty", "美；美人", "🌸"),
        ("beautiful", "美丽的", "🌸"),
        ("beautifully", "优美地", "🌸"),
    ]),
    "believe": ("相信", [
        ("believe", "相信", "💯"),
        ("believable", "可信的", "🤨"),
    ]),
    "blue": ("蓝色（的）", [
        ("blue", "蓝色（的）", "🔵"),
        ("bluish", "微蓝的", "💙"),
    ]),
    "book": ("书", [
        ("book", "书", "📖"),
        ("textbook", "课本", "📖"),
        ("notebook", "笔记本", "📓"),
        ("storybook", "故事书", "📕"),
        ("workbook", "练习册", "📒"),
        ("bookish", "书呆子气的", "📚"),
    ]),
    "boy": ("男孩", [
        ("boy", "男孩", "👦"),
        ("boyish", "男孩气的", "🧒"),
    ]),
    "brave": ("勇敢的", [
        ("brave", "勇敢的", "🦁"),
        ("bravely", "勇敢地", "🦁"),
    ]),
    "bright": ("明亮的", [
        ("bright", "明亮的", "💡"),
        ("brighten", "使明亮", "💡"),
        ("brightly", "明亮地", "✨"),
        ("brightness", "明亮", "☀️"),
    ]),
    "brother": ("兄弟", [
        ("brother", "兄弟", "👦"),
        ("brotherhood", "兄弟情", "🤝"),
    ]),
    "bury": ("埋葬；掩埋", [
        ("bury", "埋葬；掩埋", "⚰️"),
        ("burial", "埋葬", "⚰️"),
    ]),
    "busy": ("忙碌的", [
        ("busy", "忙碌的", "🐝"),
        ("business", "生意", "💼"),
        ("businesslike", "务实的", "💼"),
    ]),
    "care": ("关心", [
        ("care", "关心", "💗"),
        ("careful", "小心的", "🛡️"),
        ("careless", "粗心的", "😵"),
        ("carefully", "细致地", "🔍"),
    ]),
    "careful": ("小心的", [
        ("careful", "小心的", "🛡️"),
        ("carefully", "细致地", "🔍"),
    ]),
    "case": ("情况", [
        ("case", "情况", "📦"),
        ("suitcase", "手提箱", "🧳"),
        ("bookcase", "书柜", "📚"),
        ("casual", "随意的", "👕"),
    ]),
    "celebrate": ("庆祝", [
        ("celebrate", "庆祝", "🎉"),
        ("celebration", "庆祝", "🎉"),
    ]),
    "certain": ("某种", [
        ("certain", "某种", "🔹"),
        ("certainly", "当然", "✅"),
    ]),
    "change": ("改变", [
        ("change", "改变", "🔄"),
        ("changeable", "易变的", "🔄"),
        ("exchange", "交换", "🔄"),
    ]),
    "cheer": ("欢呼；激励", [
        ("cheer", "欢呼；激励", "📣"),
        ("cheerful", "快乐的", "😄"),
    ]),
    "citizen": ("公民；市民", [
        ("citizen", "公民；市民", "🏙️"),
        ("citizenship", "公民身份", "🪪"),
    ]),
    "class": ("班级；课", [
        ("class", "班级；课", "🏫"),
        ("classify", "分类", "🗂️"),
        ("classical", "古典的", "🎼"),
    ]),
    "classic": ("经典作品", [
        ("classic", "经典作品", "📚"),
        ("classical", "古典的", "🎼"),
    ]),
    "clear": ("清楚易懂的", [
        ("clear", "清楚易懂的", "🔍"),
        ("clearly", "清楚地", "👓"),
    ]),
    "clock": ("钟", [
        ("clock", "钟", "🕐"),
        ("clockwise", "顺时针地", "🕐"),
    ]),
    "close": ("近的；关闭", [
        ("close", "近的；关闭", "🚪"),
        ("closely", "密切地", "🔍"),
        ("enclose", "附入", "🔤"),
    ]),
    "collect": ("收集", [
        ("collect", "收集", "🗂️"),
        ("collection", "收集", "📚"),
    ]),
    "color": ("颜色", [
        ("color", "颜色", "🎨"),
        ("colorful", "多彩的", "🎨"),
    ]),
    "comment": ("评论", [
        ("comment", "评论", "💬"),
        ("commentary", "评论；解说", "🎙️"),
    ]),
    "communicate": ("交流", [
        ("communicate", "交流", "💬"),
        ("communication", "交流", "💬"),
    ]),
    "compete": ("竞争", [
        ("compete", "竞争", "🏁"),
        ("competition", "比赛", "🏆"),
        ("competitive", "有竞争力的", "🏅"),
    ]),
    "complete": ("完成", [
        ("complete", "完成", "✅"),
        ("completely", "完全地", "🔵"),
        ("incomplete", "不完整的", "🧩"),
    ]),
    "confuse": ("使困惑", [
        ("confuse", "使困惑", "😵"),
        ("confusion", "困惑；混乱", "😵"),
    ]),
    "congratulate": ("祝贺", [
        ("congratulate", "祝贺", "🎉"),
        ("congratulation", "祝贺", "🎉"),
    ]),
    "consider": ("考虑", [
        ("consider", "考虑", "🤔"),
        ("consideration", "考虑", "🤔"),
    ]),
    "construct": ("建造；构建", [
        ("construct", "建造；构建", "🔨"),
        ("construction", "建设", "🏗️"),
        ("constructive", "建设性的", "🔤"),
    ]),
    "corporate": ("公司的；法人的", [
        ("corporate", "公司的；法人的", "🏢"),
        ("corporation", "公司", "🔤"),
    ]),
    "correct": ("正确的", [
        ("correct", "正确的", "✅"),
        ("correctly", "正确地", "✔️"),
        ("incorrect", "不正确的", "❌"),
    ]),
    "count": ("数；计数", [
        ("count", "数；计数", "🔢"),
        ("countless", "无数的", "♾️"),
        ("discount", "折扣", "🏷️"),
    ]),
    "courage": ("勇气", [
        ("courage", "勇气", "🦁"),
        ("courageous", "勇敢的", "🦁"),
        ("encourage", "鼓励", "📣"),
    ]),
    "create": ("创造", [
        ("create", "创造", "💡"),
        ("creative", "有创造力的", "💡"),
        ("creatively", "创造性地", "🎨"),
        ("creativity", "创造力", "🎨"),
    ]),
    "creative": ("有创造力的", [
        ("creative", "有创造力的", "💡"),
        ("creatively", "创造性地", "🎨"),
        ("creativity", "创造力", "🎨"),
    ]),
    "deep": ("深的", [
        ("deep", "深的", "🌊"),
        ("deepen", "加深", "🕳️"),
        ("deeply", "深深地", "🌊"),
    ]),
    "depend": ("依靠", [
        ("depend", "依靠", "🔗"),
        ("dependent", "依赖的", "🔤"),
        ("dependable", "可靠的", "🛡️"),
    ]),
    "detect": ("察觉；探测", [
        ("detect", "察觉；探测", "🔍"),
        ("detective", "侦探的", "🔤"),
    ]),
    "develop": ("发展", [
        ("develop", "发展", "📈"),
        ("development", "发展；开发", "📈"),
    ]),
    "direct": ("指导；直接的", [
        ("direct", "指导；直接的", "➡️"),
        ("direction", "方向", "🧭"),
        ("directly", "直接地", "➡️"),
        ("indirect", "间接的", "↔️"),
    ]),
    "discuss": ("讨论", [
        ("discuss", "讨论", "🗣️"),
        ("discussion", "讨论", "💬"),
    ]),
    "dispose": ("处理；布置", [
        ("dispose", "处理；布置", "🗑️"),
        ("disposable", "一次性的；可弃的", "🗑️"),
    ]),
    "down": ("向下", [
        ("down", "向下", "⬇️"),
        ("downward", "向下的", "⬇️"),
    ]),
    "easy": ("容易的", [
        ("easy", "容易的", "✅"),
        ("easily", "容易地", "😌"),
    ]),
    "educate": ("教育", [
        ("educate", "教育", "📚"),
        ("education", "教育", "📚"),
        ("educational", "有教育意义的", "📚"),
    ]),
    "education": ("教育", [
        ("education", "教育", "📚"),
        ("educational", "有教育意义的", "📚"),
    ]),
    "electric": ("用电的", [
        ("electric", "用电的", "⚡"),
        ("electricity", "电；电力", "⚡"),
    ]),
    "encourage": ("鼓励", [
        ("encourage", "鼓励", "📣"),
        ("encouragement", "鼓励", "🤝"),
    ]),
    "enjoy": ("享受", [
        ("enjoy", "享受", "😊"),
        ("enjoyable", "愉快的", "😄"),
    ]),
    "environment": ("环境", [
        ("environment", "环境", "🌍"),
        ("environmental", "环境的", "🌍"),
        ("environmentalist", "环保人士", "🌿"),
    ]),
    "exact": ("精确的；准确的", [
        ("exact", "精确的；准确的", "🎯"),
        ("exactly", "确切地", "✅"),
    ]),
    "examine": ("检查", [
        ("examine", "检查", "🔍"),
        ("examination", "考试", "📝"),
    ]),
    "excite": ("使激动", [
        ("excite", "使激动", "🤩"),
        ("excitement", "兴奋", "🎉"),
    ]),
    "exhibit": ("展览；展出", [
        ("exhibit", "展览；展出", "🖼️"),
        ("exhibition", "展览；博览会", "🖼️"),
    ]),
    "experiment": ("实验；尝试", [
        ("experiment", "实验；尝试", "🧪"),
        ("experimental", "实验的", "🔬"),
    ]),
    "express": ("表达", [
        ("express", "表达", "💬"),
        ("expression", "表情；表达", "😊"),
        ("expressive", "有表现力的", "🔤"),
    ]),
    "fact": ("事实", [
        ("fact", "事实", "📌"),
        ("factory", "工厂", "🏭"),
    ]),
    "fair": ("合理的", [
        ("fair", "合理的", "⚖️"),
        ("fairness", "公平", "⚖️"),
        ("unfair", "不公平的", "⚖️"),
    ]),
    "fame": ("名声", [
        ("fame", "名声", "⭐"),
        ("famous", "著名的", "⭐"),
    ]),
    "fast": ("快的", [
        ("fast", "快的", "⚡"),
        ("fasten", "系紧", "🔗"),
        ("breakfast", "早餐", "🍳"),
    ]),
    "father": ("父亲；爸爸", [
        ("father", "父亲；爸爸", "👨"),
        ("fatherhood", "父性", "👨‍👧"),
        ("grandfather", "祖父；外祖父", "👴"),
        ("stepfather", "继父", "🔤"),
    ]),
    "fear": ("害怕", [
        ("fear", "害怕", "😨"),
        ("fearless", "无畏的", "🦁"),
        ("fearsome", "可怕的", "🔤"),
    ]),
    "fire": ("火", [
        ("fire", "火", "🔥"),
        ("fireproof", "防火的", "🔥"),
    ]),
    "fit": ("适合", [
        ("fit", "适合", "✅"),
        ("fitness", "健康；适合", "💪"),
    ]),
    "fool": ("蠢人", [
        ("fool", "蠢人", "🤡"),
        ("foolish", "愚蠢的", "🔤"),
    ]),
    "forget": ("忘记", [
        ("forget", "忘记", "🤔"),
        ("forgetful", "健忘的", "🧠"),
    ]),
    "forgive": ("原谅", [
        ("forgive", "原谅", "🕊️"),
        ("forgiveness", "原谅", "🤗"),
    ]),
    "fortunate": ("幸运的", [
        ("fortunate", "幸运的", "🍀"),
        ("fortunately", "幸运地", "🍀"),
    ]),
    "found": ("找到", [
        ("found", "找到", "🔎"),
        ("foundation", "基础；基金会", "🏗️"),
    ]),
    "free": ("空闲的；免费的", [
        ("free", "空闲的；免费的", "🆓"),
        ("freedom", "自由", "🕊️"),
    ]),
    "friend": ("朋友", [
        ("friend", "朋友", "🤝"),
        ("friendly", "友好的", "🤝"),
        ("friendship", "友谊", "🤝"),
    ]),
    "general": ("总的", [
        ("general", "总的", "🔢"),
        ("generally", "通常", "📊"),
    ]),
    "good": ("好的", [
        ("good", "好的", "💯"),
        ("goodness", "善良", "😇"),
    ]),
    "great": ("伟大的；好极了", [
        ("great", "伟大的；好极了", "🌟"),
        ("greatly", "非常", "🙌"),
        ("greatness", "伟大", "🏆"),
    ]),
    "green": ("绿色（的）", [
        ("green", "绿色（的）", "🟢"),
        ("greenish", "微绿的", "🔤"),
    ]),
    "hand": ("手", [
        ("hand", "手", "✋"),
        ("handful", "一把；少数", "🤏"),
        ("handsome", "帅气的", "🔤"),
    ]),
    "happy": ("快乐的", [
        ("happy", "快乐的", "😄"),
        ("happily", "快乐地", "😄"),
        ("happiness", "幸福；快乐", "😊"),
        ("unhappy", "不高兴的", "😞"),
    ]),
    "hard": ("努力地", [
        ("hard", "努力地", "💪"),
        ("hardly", "几乎不", "🚫"),
        ("harden", "使变硬", "🪨"),
        ("hardship", "艰难", "⛰️"),
    ]),
    "harm": ("伤害", [
        ("harm", "伤害", "⚠️"),
        ("harmful", "有害的", "⚠️"),
        ("harmless", "无害的", "🕊️"),
    ]),
    "heavy": ("重的", [
        ("heavy", "重的", "🏋️"),
        ("heavily", "大量地", "🌧️"),
    ]),
    "help": ("帮助", [
        ("help", "帮助", "🆘"),
        ("helpful", "有帮助的", "🤝"),
        ("helpless", "无助的", "🥺"),
    ]),
    "high": ("高的", [
        ("high", "高的", "🗼"),
        ("highly", "高度地", "🚀"),
    ]),
    "honest": ("诚实的", [
        ("honest", "诚实的", "🤍"),
        ("honestly", "诚实地", "🤞"),
        ("dishonest", "不诚实的", "🤥"),
    ]),
    "hope": ("希望", [
        ("hope", "希望", "🌈"),
        ("hopeful", "有希望的", "😊"),
        ("hopeless", "绝望的", "😞"),
    ]),
    "ill": ("生病的", [
        ("ill", "生病的", "🤒"),
        ("illness", "疾病", "🤒"),
    ]),
    "imagine": ("想象", [
        ("imagine", "想象", "💭"),
        ("imaginary", "想象中的", "💭"),
        ("imagination", "想象力", "🎨"),
        ("imaginative", "有想象力的", "🎨"),
    ]),
    "impress": ("给…留下印象", [
        ("impress", "给…留下印象", "🌟"),
        ("impression", "印象", "👁️"),
        ("impressive", "令人印象深刻的", "👏"),
    ]),
    "improve": ("改进", [
        ("improve", "改进", "⬆️"),
        ("improvement", "改善", "📈"),
    ]),
    "inform": ("通知；告知", [
        ("inform", "通知；告知", "📣"),
        ("informal", "非正式的", "👕"),
        ("information", "信息", "ℹ️"),
    ]),
    "institute": ("机构；建立", [
        ("institute", "机构；建立", "🏛️"),
        ("institution", "机构；制度", "🏛️"),
    ]),
    "instruct": ("指导；指示", [
        ("instruct", "指导；指示", "🧑‍🏫"),
        ("instruction", "指示", "📋"),
    ]),
    "interact": ("互动；交流", [
        ("interact", "互动；交流", "🤝"),
        ("interactive", "互动的", "🖱️"),
    ]),
    "interrupt": ("打断；中断", [
        ("interrupt", "打断；中断", "✋"),
        ("interruption", "打断；中断", "⛔"),
    ]),
    "invent": ("发明", [
        ("invent", "发明", "💡"),
        ("invention", "发明", "💡"),
        ("inventive", "有创造力的", "🔤"),
    ]),
    "invite": ("邀请", [
        ("invite", "邀请", "💌"),
        ("invitation", "邀请；请柬", "✉️"),
    ]),
    "job": ("工作；职业", [
        ("job", "工作；职业", "💼"),
        ("jobless", "失业的", "📉"),
    ]),
    "joy": ("高兴", [
        ("joy", "高兴", "😄"),
        ("joyful", "快乐的", "😃"),
        ("enjoy", "享受", "😊"),
    ]),
    "just": ("只是；恰好", [
        ("just", "只是；恰好", "🙂"),
        ("justify", "证明…正当", "🔤"),
    ]),
    "kind": ("和蔼的；友善的", [
        ("kind", "和蔼的；友善的", "😊"),
        ("kindness", "仁慈", "💗"),
        ("unkind", "不友善的", "😠"),
    ]),
    "king": ("国王", [
        ("king", "国王", "👑"),
        ("kingdom", "王国", "👑"),
    ]),
    "knowledge": ("知识", [
        ("knowledge", "知识", "📚"),
        ("knowledgeable", "知识渊博的", "📚"),
    ]),
    "late": ("迟到的", [
        ("late", "迟到的", "⏰"),
        ("lately", "最近", "🕐"),
    ]),
    "lazy": ("懒惰的", [
        ("lazy", "懒惰的", "😴"),
        ("laziness", "懒惰", "🦥"),
    ]),
    "leader": ("领导", [
        ("leader", "领导", "🧑‍🏫"),
        ("leadership", "领导力", "🧭"),
    ]),
    "light": ("灯；光", [
        ("light", "灯；光", "💡"),
        ("sunlight", "阳光", "☀️"),
        ("daylight", "日光", "🌅"),
        ("highlight", "亮点", "✨"),
        ("flashlight", "手电筒", "🔦"),
        ("lightly", "轻微地", "🪶"),
    ]),
    "like": ("喜欢", [
        ("like", "喜欢", "👍"),
        ("likewise", "同样地", "🔁"),
    ]),
    "limit": ("限制；限度", [
        ("limit", "限制；限度", "🚧"),
        ("limitless", "无限的", "🌌"),
    ]),
    "live": ("居住", [
        ("live", "居住", "🏠"),
        ("lively", "生气勃勃的", "🌟"),
        ("livelihood", "生计", "🍚"),
    ]),
    "lively": ("生气勃勃的", [
        ("lively", "生气勃勃的", "🌟"),
        ("livelihood", "生计", "🍚"),
    ]),
    "lonely": ("孤独的", [
        ("lonely", "孤独的", "😔"),
        ("loneliness", "孤独", "🥺"),
    ]),
    "loud": ("响亮的", [
        ("loud", "响亮的", "📢"),
        ("loudly", "喧闹地", "📢"),
    ]),
    "main": ("主要的", [
        ("main", "主要的", "🔑"),
        ("mainly", "主要地", "🎯"),
        ("remain", "保持不变", "⏸️"),
    ]),
    "major": ("主要的；专业", [
        ("major", "主要的；专业", "⭐"),
        ("majority", "大多数", "👥"),
    ]),
    "manage": ("管理", [
        ("manage", "管理", "🧑‍💼"),
        ("management", "管理", "📊"),
    ]),
    "marry": ("结婚", [
        ("marry", "结婚", "💍"),
        ("marriage", "婚姻", "💍"),
    ]),
    "meaning": ("意义", [
        ("meaning", "意义", "💡"),
        ("meaningless", "毫无意义的", "🚫"),
        ("meaningful", "有意义的", "💡"),
    ]),
    "measure": ("测量；措施", [
        ("measure", "测量；措施", "📏"),
        ("measurement", "测量", "📏"),
    ]),
    "member": ("成员", [
        ("member", "成员", "👥"),
        ("membership", "会员资格", "🪪"),
        ("remember", "记得", "🧠"),
    ]),
    "memory": ("记忆", [
        ("memory", "记忆", "🧠"),
        ("memorial", "纪念的；纪念碑", "🕯️"),
    ]),
    "most": ("大多数的", [
        ("most", "大多数的", "🔢"),
        ("mostly", "主要地", "🔢"),
    ]),
    "mother": ("母亲；妈妈", [
        ("mother", "母亲；妈妈", "👩"),
        ("motherhood", "母性", "🤱"),
        ("grandmother", "祖母；外祖母", "👵"),
        ("stepmother", "继母", "🔤"),
    ]),
    "mountain": ("山", [
        ("mountain", "山", "⛰️"),
        ("mountainous", "多山的", "⛰️"),
    ]),
    "mouth": ("嘴", [
        ("mouth", "嘴", "👄"),
        ("mouthful", "一口", "🍚"),
    ]),
    "move": ("移动", [
        ("move", "移动", "🚶"),
        ("movement", "运动；移动", "🚶"),
        ("remove", "移走；去掉", "➖"),
    ]),
    "music": ("音乐", [
        ("music", "音乐", "🎵"),
        ("musical", "音乐的", "🎵"),
    ]),
    "national": ("国家的；民族的", [
        ("national", "国家的；民族的", "🇨🇳"),
        ("nationality", "国籍；民族", "🌍"),
        ("international", "国际的", "🌐"),
    ]),
    "near": ("在附近", [
        ("near", "在附近", "📍"),
        ("nearly", "几乎", "🫧"),
    ]),
    "neighbor": ("邻居", [
        ("neighbor", "邻居", "🏡"),
        ("neighborhood", "社区", "🏘️"),
    ]),
    "nine": ("九", [
        ("nine", "九", "9️⃣"),
        ("ninety", "九十", "9️⃣0️⃣"),
    ]),
    "notice": ("注意到；公告", [
        ("notice", "注意到；公告", "📌"),
        ("noticeable", "明显的", "👁️"),
    ]),
    "novel": ("小说", [
        ("novel", "小说", "📖"),
        ("novelist", "小说家", "✍️"),
    ]),
    "object": ("物体；反对", [
        ("object", "物体；反对", "🔹"),
        ("objective", "客观的；目标", "🎯"),
    ]),
    "office": ("办公室", [
        ("office", "办公室", "🏢"),
        ("official", "官员；官方的", "🏛️"),
    ]),
    "organize": ("组织", [
        ("organize", "组织", "🗂️"),
        ("organization", "组织", "🗂️"),
    ]),
    "origin": ("起源；出身", [
        ("origin", "起源；出身", "🌱"),
        ("original", "原始的", "🌱"),
    ]),
    "other": ("其他的", [
        ("other", "其他的", "🔀"),
        ("otherwise", "否则", "🚫"),
    ]),
    "owner": ("主人", [
        ("owner", "主人", "🙋"),
        ("ownership", "所有权", "🔑"),
    ]),
    "pain": ("痛苦", [
        ("pain", "痛苦", "💔"),
        ("painful", "令人痛苦的", "💔"),
        ("painless", "无痛的", "💊"),
    ]),
    "partner": ("搭档", [
        ("partner", "搭档", "🤝"),
        ("partnership", "合伙", "🤝"),
    ]),
    "pay": ("付费", [
        ("pay", "付费", "💳"),
        ("payment", "付款", "💳"),
    ]),
    "peace": ("和平", [
        ("peace", "和平", "🕊️"),
        ("peaceful", "和平的", "🕊️"),
    ]),
    "perfect": ("完美的", [
        ("perfect", "完美的", "💯"),
        ("perfectly", "完美地", "💯"),
        ("imperfect", "不完美的", "🩹"),
    ]),
    "perform": ("表演；执行", [
        ("perform", "表演；执行", "🎤"),
        ("performance", "表演", "🎭"),
    ]),
    "person": ("人", [
        ("person", "人", "🧑"),
        ("personal", "个人的", "🙋"),
        ("personality", "个性", "🎭"),
    ]),
    "personal": ("个人的", [
        ("personal", "个人的", "🙋"),
        ("personality", "个性", "🎭"),
    ]),
    "polite": ("有礼貌的", [
        ("polite", "有礼貌的", "🙇"),
        ("politely", "礼貌地", "🤝"),
        ("politeness", "礼貌", "🎩"),
        ("impolite", "不礼貌的", "🙅"),
    ]),
    "pollute": ("污染", [
        ("pollute", "污染", "🏭"),
        ("pollution", "污染", "🏭"),
    ]),
    "post": ("邮政", [
        ("post", "邮政", "📮"),
        ("postage", "邮资", "🔤"),
    ]),
    "power": ("权力", [
        ("power", "权力", "👑"),
        ("powerful", "强大的", "💪"),
        ("superpower", "超级大国", "🏛️"),
    ]),
    "predict": ("预测", [
        ("predict", "预测", "🔮"),
        ("prediction", "预言", "🔮"),
    ]),
    "prepare": ("准备", [
        ("prepare", "准备", "📝"),
        ("preparation", "准备", "📝"),
    ]),
    "price": ("价格", [
        ("price", "价格", "💲"),
        ("priceless", "无价的", "💎"),
    ]),
    "prime": ("首要的", [
        ("prime", "首要的", "1️⃣"),
        ("primary", "最初的", "1️⃣"),
    ]),
    "prior": ("先前的；优先的", [
        ("prior", "先前的；优先的", "⏮️"),
        ("priority", "优先；优先权", "⭐"),
    ]),
    "product": ("产品", [
        ("product", "产品", "📦"),
        ("productive", "多产的；高效的", "🌾"),
    ]),
    "progress": ("进步", [
        ("progress", "进步", "📈"),
        ("progressive", "进步的", "🔤"),
    ]),
    "protect": ("保护", [
        ("protect", "保护", "🛡️"),
        ("protection", "保护", "🛡️"),
        ("protective", "保护的", "🛡️"),
    ]),
    "pure": ("纯的；纯粹的", [
        ("pure", "纯的；纯粹的", "⚪"),
        ("purify", "净化", "🔤"),
        ("purist", "纯粹主义者", "🔤"),
    ]),
    "purpose": ("目的", [
        ("purpose", "目的", "🎯"),
        ("purposeful", "有目的的", "🎯"),
    ]),
    "quick": ("快的", [
        ("quick", "快的", "⚡"),
        ("quickly", "快速地", "💨"),
    ]),
    "quiet": ("安静的", [
        ("quiet", "安静的", "🤫"),
        ("quietly", "安静地", "🤫"),
    ]),
    "rapid": ("迅速的", [
        ("rapid", "迅速的", "⚡"),
        ("rapidly", "迅速地", "⚡"),
    ]),
    "read": ("读", [
        ("read", "读", "📖"),
        ("readable", "可读的", "📖"),
    ]),
    "ready": ("准备好的", [
        ("ready", "准备好的", "✅"),
        ("readiness", "准备就绪", "🎒"),
    ]),
    "reason": ("原因", [
        ("reason", "原因", "❓"),
        ("reasonable", "合理的", "⚖️"),
    ]),
    "reception": ("接待；接收", [
        ("reception", "接待；接收", "🛎️"),
        ("receptionist", "接待员", "🛎️"),
    ]),
    "recycle": ("回收", [
        ("recycle", "回收", "♻️"),
        ("recyclable", "可回收的", "♻️"),
    ]),
    "red": ("红色（的）", [
        ("red", "红色（的）", "🔴"),
        ("reddish", "微红的", "🔤"),
    ]),
    "relation": ("关系", [
        ("relation", "关系", "🔗"),
        ("relationship", "关系", "🔗"),
    ]),
    "relative": ("亲属", [
        ("relative", "亲属", "👪"),
        ("relativity", "相对论；相对性", "🌀"),
    ]),
    "require": ("需要", [
        ("require", "需要", "🙏"),
        ("requirement", "要求", "📋"),
    ]),
    "rest": ("休息", [
        ("rest", "休息", "😴"),
        ("restless", "不安的", "😣"),
    ]),
    "reuse": ("重新使用", [
        ("reuse", "重新使用", "♻️"),
        ("reusable", "可重复使用的", "♻️"),
    ]),
    "rich": ("富有的", [
        ("rich", "富有的", "💰"),
        ("richness", "丰富", "💰"),
        ("enrich", "丰富", "💎"),
    ]),
    "sad": ("难过的", [
        ("sad", "难过的", "😢"),
        ("sadness", "悲伤", "😢"),
    ]),
    "safe": ("安全的", [
        ("safe", "安全的", "🔒"),
        ("safely", "安全地", "🛡️"),
        ("unsafe", "不安全的", "⚠️"),
    ]),
    "second": ("第二", [
        ("second", "第二", "2️⃣"),
        ("secondly", "第二", "2️⃣"),
    ]),
    "select": ("选择；挑选", [
        ("select", "选择；挑选", "✅"),
        ("selective", "选择性的", "🔤"),
    ]),
    "self": ("自我", [
        ("self", "自我", "🙋"),
        ("selfish", "自私的", "🔤"),
        ("selfless", "无私的", "🔤"),
        ("herself", "她自己", "🙋"),
        ("yourself", "你自己", "🙋"),
    ]),
    "sense": ("感觉；意识", [
        ("sense", "感觉；意识", "💡"),
        ("sensible", "明智的", "🧠"),
        ("sensitive", "敏感的", "🌸"),
        ("nonsense", "胡说", "🤪"),
    ]),
    "serious": ("严肃的", [
        ("serious", "严肃的", "😐"),
        ("seriously", "严肃地", "🎓"),
    ]),
    "seven": ("七", [
        ("seven", "七", "7️⃣"),
        ("seventy", "七十", "7️⃣0️⃣"),
    ]),
    "sharp": ("锋利的；敏锐的", [
        ("sharp", "锋利的；敏锐的", "🔪"),
        ("sharpen", "削尖", "✏️"),
    ]),
    "ship": ("船", [
        ("ship", "船", "🚢"),
        ("shipment", "运输", "📦"),
    ]),
    "short": ("矮的；短的", [
        ("short", "矮的；短的", "📏"),
        ("shortly", "不久", "⏱️"),
    ]),
    "shy": ("害羞的", [
        ("shy", "害羞的", "😳"),
        ("shyness", "害羞", "😳"),
    ]),
    "sick": ("生病的", [
        ("sick", "生病的", "🤒"),
        ("sickness", "疾病", "🤒"),
    ]),
    "simple": ("简单的", [
        ("simple", "简单的", "🔹"),
        ("simplify", "简化", "✂️"),
    ]),
    "six": ("六", [
        ("six", "六", "6️⃣"),
        ("sixty", "六十", "6️⃣0️⃣"),
    ]),
    "skill": ("技艺", [
        ("skill", "技艺", "🛠️"),
        ("skillful", "熟练的", "🛠️"),
    ]),
    "sleep": ("睡觉", [
        ("sleep", "睡觉", "😴"),
        ("sleepless", "失眠的", "🌙"),
    ]),
    "slight": ("轻微的；细小的", [
        ("slight", "轻微的；细小的", "➖"),
        ("slightly", "稍微", "↗️"),
    ]),
    "slow": ("慢的", [
        ("slow", "慢的", "🐢"),
        ("slowly", "缓慢地", "🐢"),
    ]),
    "smooth": ("悦耳的", [
        ("smooth", "悦耳的", "🎵"),
        ("smoothly", "顺利地", "🛣️"),
    ]),
    "social": ("社会的", [
        ("social", "社会的", "👥"),
        ("socialize", "社交", "🗣️"),
        ("antisocial", "反社会的", "🚫"),
    ]),
    "soft": ("软的", [
        ("soft", "软的", "☁️"),
        ("soften", "使柔软", "☁️"),
        ("softly", "轻柔地", "☁️"),
        ("softness", "柔软", "☁️"),
    ]),
    "sound": ("听起来", [
        ("sound", "听起来", "🔊"),
        ("soundproof", "隔音的", "🔇"),
    ]),
    "special": ("特色菜；特别的", [
        ("special", "特色菜；特别的", "⭐"),
        ("specialist", "专家", "🔬"),
    ]),
    "speech": ("讲话", [
        ("speech", "讲话", "🎤"),
        ("speechless", "说不出话的", "😶"),
    ]),
    "spirit": ("精神", [
        ("spirit", "精神", "🔥"),
        ("spiritual", "精神的", "🕊️"),
    ]),
    "standard": ("标准", [
        ("standard", "标准", "📏"),
        ("standardize", "标准化", "📐"),
    ]),
    "state": ("州；国家", [
        ("state", "州；国家", "🗺️"),
        ("statement", "声明", "🗣️"),
    ]),
    "stress": ("精神压力", [
        ("stress", "精神压力", "😣"),
        ("stressful", "有压力的", "😫"),
    ]),
    "strong": ("强壮的", [
        ("strong", "强壮的", "💪"),
        ("strongly", "强烈地", "💪"),
    ]),
    "study": ("书房；学习", [
        ("study", "书房；学习", "📚"),
        ("studious", "好学的", "📖"),
    ]),
    "success": ("成功", [
        ("success", "成功", "🎉"),
        ("successful", "成功的", "🎉"),
    ]),
    "sudden": ("突然的", [
        ("sudden", "突然的", "💥"),
        ("suddenly", "突然", "💥"),
    ]),
    "suggest": ("建议", [
        ("suggest", "建议", "💡"),
        ("suggestion", "建议", "💡"),
    ]),
    "suit": ("西服", [
        ("suit", "西服", "🤵"),
        ("suitable", "合适的", "✅"),
    ]),
    "sure": ("当然；确信", [
        ("sure", "当然；确信", "✅"),
        ("surely", "当然", "👍"),
    ]),
    "sweet": ("甜的", [
        ("sweet", "甜的", "🍬"),
        ("sweetness", "甜蜜", "🍯"),
    ]),
    "talk": ("说话；交谈", [
        ("talk", "说话；交谈", "💬"),
        ("talkative", "健谈的", "💬"),
    ]),
    "tall": ("高的", [
        ("tall", "高的", "🦒"),
        ("tallish", "稍高的", "📏"),
    ]),
    "tight": ("紧的；牢固的", [
        ("tight", "紧的；牢固的", "🔒"),
        ("tighten", "拧紧", "🔧"),
    ]),
    "tired": ("疲倦的", [
        ("tired", "疲倦的", "😮‍💨"),
        ("tiredness", "疲惫", "😪"),
    ]),
    "total": ("总的", [
        ("total", "总的", "🔢"),
        ("totally", "完全地", "💯"),
    ]),
    "tour": ("旅行", [
        ("tour", "旅行", "🧳"),
        ("tourist", "游客", "📸"),
        ("tourism", "旅游业", "🧳"),
    ]),
    "translate": ("翻译", [
        ("translate", "翻译", "🌐"),
        ("translation", "翻译；译文", "📝"),
    ]),
    "transport": ("运输；交通工具", [
        ("transport", "运输；交通工具", "🚚"),
        ("transportation", "交通", "🚗"),
    ]),
    "trouble": ("麻烦", [
        ("trouble", "麻烦", "😣"),
        ("troublesome", "麻烦的", "🔤"),
    ]),
    "truth": ("真相", [
        ("truth", "真相", "📌"),
        ("truthful", "诚实的", "🤍"),
    ]),
    "typical": ("典型的", [
        ("typical", "典型的", "🔹"),
        ("typically", "通常", "📊"),
    ]),
    "understand": ("理解", [
        ("understand", "理解", "🤝"),
        ("understandable", "可以理解的", "🧩"),
        ("misunderstand", "误解", "🤷"),
    ]),
    "universe": ("宇宙", [
        ("universe", "宇宙", "🌌"),
        ("university", "大学", "🎓"),
    ]),
    "use": ("使用", [
        ("use", "使用", "🔧"),
        ("useful", "有用的", "🛠️"),
        ("useless", "无用的", "🗑️"),
        ("reuse", "重新使用", "♻️"),
    ]),
    "value": ("重视", [
        ("value", "重视", "💎"),
        ("valuable", "贵重的", "💎"),
    ]),
    "vary": ("变化；不同", [
        ("vary", "变化；不同", "🔄"),
        ("variable", "变量；多变的", "🔄"),
        ("various", "各种各样的", "🌈"),
    ]),
    "victory": ("胜利", [
        ("victory", "胜利", "🏆"),
        ("victorious", "胜利的", "🏆"),
    ]),
    "violin": ("小提琴", [
        ("violin", "小提琴", "🎻"),
        ("violinist", "小提琴手", "🎻"),
    ]),
    "visual": ("视觉的；画面的", [
        ("visual", "视觉的；画面的", "👁️"),
        ("visualize", "想象", "👁️"),
    ]),
    "warm": ("温暖的", [
        ("warm", "温暖的", "🌤️"),
        ("warmly", "热情地", "🔥"),
    ]),
    "water": ("水", [
        ("water", "水", "💧"),
        ("waterfall", "瀑布", "🌊"),
        ("watermelon", "西瓜", "🍉"),
        ("underwater", "水下的", "🤿"),
        ("waterproof", "防水的", "💧"),
    ]),
    "weak": ("虚弱的", [
        ("weak", "虚弱的", "😟"),
        ("weakness", "弱点", "🪫"),
    ]),
    "week": ("周；星期", [
        ("week", "周；星期", "📅"),
        ("weekly", "每周的", "📅"),
    ]),
    "wide": ("宽的", [
        ("wide", "宽的", "↔️"),
        ("widely", "广泛地", "🌐"),
    ]),
    "wonder": ("想知道", [
        ("wonder", "想知道", "🤔"),
        ("wonderful", "精彩的", "🌟"),
    ]),
    "worth": ("值得", [
        ("worth", "值得", "💎"),
        ("worthless", "无价值的", "🗑️"),
    ]),
    "yellow": ("黄色（的）", [
        ("yellow", "黄色（的）", "🟡"),
        ("yellowish", "微黄的", "💛"),
    ]),
    "all": ("全部的", [
        ("all", "全部的", "🔢"),
        ("overall", "总体的", "🔤"),
    ]),
    "appear": ("出现", [
        ("appear", "出现", "👀"),
        ("disappear", "消失", "👻"),
    ]),
    "appoint": ("任命；约定", [
        ("appoint", "任命；约定", "📅"),
        ("disappoint", "使失望", "😞"),
    ]),
    "author": ("作者", [
        ("author", "作者", "✍️"),
        ("coauthor", "合著者", "🔤"),
    ]),
    "away": ("离开", [
        ("away", "离开", "🚪"),
        ("takeaway", "外卖", "🥡"),
    ]),
    "bag": ("包；书包", [
        ("bag", "包；书包", "🎒"),
        ("schoolbag", "书包", "🎒"),
        ("handbag", "手提包", "👜"),
    ]),
    "ball": ("球", [
        ("ball", "球", "⚽"),
        ("basketball", "篮球", "🏀"),
        ("baseball", "棒球", "⚾"),
        ("volleyball", "排球", "🏐"),
        ("football", "足球", "⚽"),
        ("handball", "手球", "🤾"),
    ]),
    "biography": ("传记", [
        ("biography", "传记", "📖"),
        ("autobiography", "自传", "📖"),
    ]),
    "biology": ("生物学", [
        ("biology", "生物学", "🧬"),
        ("microbiology", "微生物学", "🔤"),
    ]),
    "bleed": ("流血", [
        ("bleed", "流血", "🩸"),
        ("nosebleed", "鼻出血", "🩸"),
    ]),
    "board": ("板", [
        ("board", "板", "🪧"),
        ("blackboard", "黑板", "📋"),
        ("keyboard", "键盘", "⌨️"),
        ("skateboard", "滑板", "🛹"),
    ]),
    "body": ("身体", [
        ("body", "身体", "🧍"),
        ("everybody", "每个人", "👥"),
        ("somebody", "某人", "🧍"),
        ("nobody", "没有人", "🫥"),
        ("anybody", "任何人", "🤷"),
        ("antibody", "抗体", "🔤"),
    ]),
    "build": ("身材；建造", [
        ("build", "身材；建造", "🏗️"),
        ("rebuild", "重建", "🏗️"),
    ]),
    "cake": ("蛋糕", [
        ("cake", "蛋糕", "🎂"),
        ("mooncake", "月饼", "🥮"),
    ]),
    "call": ("打电话；呼叫", [
        ("call", "打电话；呼叫", "📞"),
        ("recall", "回忆起", "🔙"),
    ]),
    "card": ("卡片", [
        ("card", "卡片", "🃏"),
        ("postcard", "明信片", "📮"),
    ]),
    "circle": ("圆圈", [
        ("circle", "圆圈", "⭕"),
        ("semicircle", "半圆", "🔤"),
    ]),
    "coat": ("外套", [
        ("coat", "外套", "🧥"),
        ("overcoat", "大衣", "🔤"),
    ]),
    "come": ("来", [
        ("come", "来", "🚶"),
        ("become", "变成", "🔄"),
        ("overcome", "克服", "💪"),
        ("outcome", "结果", "🏁"),
    ]),
    "comfortable": ("舒适的", [
        ("comfortable", "舒适的", "🛋️"),
        ("uncomfortable", "不舒服的", "😣"),
    ]),
    "common": ("常见的", [
        ("common", "常见的", "🔹"),
        ("uncommon", "不常见的", "❓"),
    ]),
    "cover": ("覆盖", [
        ("cover", "覆盖", "🛡️"),
        ("recover", "恢复；找回", "🔄"),
        ("discover", "发现", "🔍"),
        ("uncover", "揭开", "🔤"),
    ]),
    "crowded": ("拥挤的", [
        ("crowded", "拥挤的", "🚶"),
        ("uncrowded", "不拥挤的", "🟢"),
    ]),
    "date": ("日期", [
        ("date", "日期", "📅"),
        ("update", "更新", "🔄"),
    ]),
    "daughter": ("女儿", [
        ("daughter", "女儿", "👧"),
        ("granddaughter", "（外）孙女", "👧"),
        ("stepdaughter", "继女", "🔤"),
    ]),
    "door": ("门", [
        ("door", "门", "🚪"),
        ("indoor", "室内的", "🔤"),
        ("outdoor", "户外的", "🏕️"),
    ]),
    "ever": ("曾经", [
        ("ever", "曾经", "⏳"),
        ("however", "然而", "🔀"),
        ("whenever", "无论何时", "⏰"),
        ("whatever", "无论什么", "🤷"),
        ("forever", "永远", "♾️"),
    ]),
    "expensive": ("昂贵的", [
        ("expensive", "昂贵的", "💰"),
        ("inexpensive", "不贵的", "💲"),
    ]),
    "face": ("脸", [
        ("face", "脸", "😊"),
        ("preface", "前言", "🔤"),
    ]),
    "fiction": ("小说", [
        ("fiction", "小说", "📖"),
        ("nonfiction", "非虚构", "🔤"),
    ]),
    "file": ("文件；档案", [
        ("file", "文件；档案", "📁"),
        ("profile", "简介", "🔤"),
    ]),
    "fine": ("健康的；好的", [
        ("fine", "健康的；好的", "👍"),
        ("define", "定义", "📘"),
    ]),
    "fly": ("飞", [
        ("fly", "飞", "🪰"),
        ("butterfly", "蝴蝶", "🦋"),
    ]),
    "fold": ("折叠", [
        ("fold", "折叠", "📜"),
        ("unfold", "展开；显露", "📂"),
    ]),
    "force": ("力；迫使", [
        ("force", "力；迫使", "💪"),
        ("enforce", "执行", "🔤"),
    ]),
    "formal": ("正式的", [
        ("formal", "正式的", "🤵"),
        ("informal", "非正式的", "👕"),
    ]),
    "front": ("前面", [
        ("front", "前面", "⬆️"),
        ("confront", "面对；对抗", "⚔️"),
    ]),
    "glasses": ("眼镜", [
        ("glasses", "眼镜", "👓"),
        ("sunglasses", "太阳镜", "🕶️"),
    ]),
    "grade": ("成绩；年级", [
        ("grade", "成绩；年级", "🏫"),
        ("upgrade", "升级", "⬆️"),
    ]),
    "graduate": ("毕业", [
        ("graduate", "毕业", "🎓"),
        ("undergraduate", "大学生", "🔤"),
    ]),
    "ground": ("地面", [
        ("ground", "地面", "🟫"),
        ("playground", "操场", "🛝"),
        ("background", "背景", "🖼️"),
        ("underground", "地下的；地铁", "🚇"),
    ]),
    "habit": ("习惯", [
        ("habit", "习惯", "🔁"),
        ("cohabit", "同居", "🔤"),
        ("inhabit", "居住", "🔤"),
    ]),
    "half": ("一半", [
        ("half", "一半", "½"),
        ("behalf", "代表；利益", "🤝"),
    ]),
    "have": ("有；吃", [
        ("have", "有；吃", "✅"),
        ("behave", "表现", "🙇"),
    ]),
    "head": ("头", [
        ("head", "头", "🧑"),
        ("forehead", "额头", "🧑"),
        ("overhead", "在头顶上", "🔤"),
    ]),
    "hill": ("小山", [
        ("hill", "小山", "⛰️"),
        ("uphill", "上坡的", "🔤"),
    ]),
    "historic": ("有历史意义的", [
        ("historic", "有历史意义的", "🏛️"),
        ("prehistoric", "史前的", "🦕"),
    ]),
    "hold": ("拥有；举行", [
        ("hold", "拥有；举行", "🤲"),
        ("uphold", "支持", "🤝"),
    ]),
    "integrate": ("整合；使融入", [
        ("integrate", "整合；使融入", "🧩"),
        ("disintegrate", "瓦解", "🔤"),
    ]),
    "large": ("大的", [
        ("large", "大的", "🐘"),
        ("enlarge", "扩大", "🔍"),
    ]),
    "let": ("让", [
        ("let", "让", "➡️"),
        ("outlet", "出口", "🔤"),
    ]),
    "line": ("行；线", [
        ("line", "行；线", "➖"),
        ("online", "在线的", "💻"),
        ("offline", "离线的", "📴"),
        ("underline", "在…下划线", "➖"),
        ("airline", "航空公司", "✈️"),
        ("outline", "轮廓；提纲", "📐"),
        ("guideline", "指导方针", "📏"),
    ]),
    "lock": ("锁上", [
        ("lock", "锁上", "🔒"),
        ("unlock", "开锁；解锁", "🔓"),
    ]),
    "long": ("长的", [
        ("long", "长的", "➖"),
        ("belong", "属于", "🔗"),
    ]),
    "look": ("看；看起来", [
        ("look", "看；看起来", "👀"),
        ("overlook", "忽视", "🙈"),
    ]),
    "low": ("低的", [
        ("low", "低的", "🔻"),
        ("below", "在…下面", "🔽"),
    ]),
    "market": ("市场", [
        ("market", "市场", "🏪"),
        ("supermarket", "超市", "🛒"),
    ]),
    "master": ("大师", [
        ("master", "大师", "🎓"),
        ("headmaster", "校长", "👨‍🏫"),
    ]),
    "mind": ("头脑；介意", [
        ("mind", "头脑；介意", "🧠"),
        ("remind", "提醒", "🔔"),
    ]),
    "mobile": ("可移动的", [
        ("mobile", "可移动的", "📱"),
        ("automobile", "汽车", "🚗"),
    ]),
    "natural": ("自然的", [
        ("natural", "自然的", "🌿"),
        ("supernatural", "超自然的", "🔤"),
    ]),
    "night": ("夜晚", [
        ("night", "夜晚", "🌃"),
        ("tonight", "今晚", "🌙"),
        ("overnight", "一夜之间", "🌙"),
        ("midnight", "午夜", "🔤"),
    ]),
    "noon": ("正午", [
        ("noon", "正午", "🌞"),
        ("afternoon", "下午", "🌞"),
    ]),
    "one": ("一", [
        ("one", "一", "1️⃣"),
        ("everyone", "每个人", "👥"),
        ("someone", "某人", "🧍"),
        ("anyone", "任何人", "🤷"),
    ]),
    "order": ("点餐；命令", [
        ("order", "点餐；命令", "📝"),
        ("disorder", "混乱", "🌪️"),
    ]),
    "over": ("结束；在…上方", [
        ("over", "结束；在…上方", "🔚"),
        ("crossover", "跨界", "🔤"),
    ]),
    "pair": ("一双；一对", [
        ("pair", "一双；一对", "👫"),
        ("repair", "修理", "🔧"),
    ]),
    "paper": ("纸", [
        ("paper", "纸", "📄"),
        ("newspaper", "报纸", "📰"),
    ]),
    "patient": ("有耐心的", [
        ("patient", "有耐心的", "🙂"),
        ("impatient", "不耐烦的", "😤"),
    ]),
    "phone": ("电话", [
        ("phone", "电话", "📞"),
        ("headphone", "耳机", "🎧"),
        ("microphone", "麦克风；话筒", "🎙️"),
    ]),
    "pilot": ("飞行员", [
        ("pilot", "飞行员", "👨‍✈️"),
        ("copilot", "副驾驶", "🔤"),
    ]),
    "place": ("地点；地方", [
        ("place", "地点；地方", "📍"),
        ("replace", "替换", "🔤"),
    ]),
    "plain": ("平原；朴素的", [
        ("plain", "平原；朴素的", "🟫"),
        ("explain", "解释", "💡"),
        ("complain", "抱怨；投诉", "😤"),
    ]),
    "plant": ("植物", [
        ("plant", "植物", "🪴"),
        ("transplant", "移植", "🔤"),
    ]),
    "play": ("玩；打（球）", [
        ("play", "玩；打（球）", "🎮"),
        ("display", "展示", "🔤"),
    ]),
    "position": ("位置", [
        ("position", "位置", "📍"),
        ("composition", "作曲；作文", "🎹"),
    ]),
    "possible": ("可能的", [
        ("possible", "可能的", "✅"),
        ("impossible", "不可能的", "🚫"),
    ]),
    "profit": ("利润；益处", [
        ("profit", "利润；益处", "💰"),
        ("nonprofit", "非营利的", "🔤"),
    ]),
    "public": ("公开的", [
        ("public", "公开的", "📢"),
        ("republic", "共和国", "🏛️"),
    ]),
    "ring": ("戒指；环", [
        ("ring", "戒指；环", "💍"),
        ("earring", "耳环", "💎"),
    ]),
    "room": ("房间", [
        ("room", "房间", "🚪"),
        ("classroom", "教室", "🏫"),
        ("bedroom", "卧室", "🛏️"),
        ("bathroom", "浴室", "🛁"),
        ("restroom", "洗手间", "🚻"),
        ("washroom", "洗手间", "🚻"),
    ]),
    "school": ("学校", [
        ("school", "学校", "🏫"),
        ("preschool", "学前的", "🧒"),
    ]),
    "science": ("科学", [
        ("science", "科学", "🔬"),
        ("conscience", "良心；良知", "🤍"),
    ]),
    "see": ("看见", [
        ("see", "看见", "👀"),
        ("foresee", "预见", "🔮"),
    ]),
    "side": ("边；侧", [
        ("side", "边；侧", "↔️"),
        ("inside", "在里面", "⬅️"),
        ("outside", "在外面", "➡️"),
        ("beside", "在旁边", "↔️"),
        ("roadside", "路边", "🛣️"),
        ("alongside", "在…旁边", "➡️"),
        ("reside", "居住", "🔤"),
        ("preside", "主持", "🔤"),
    ]),
    "sister": ("姐妹", [
        ("sister", "姐妹", "👧"),
        ("stepsister", "继姐/妹", "👧"),
    ]),
    "solve": ("解决", [
        ("solve", "解决", "✅"),
        ("resolve", "决心", "🎯"),
        ("dissolve", "溶解", "💧"),
    ]),
    "spell": ("拼写", [
        ("spell", "拼写", "✏️"),
        ("misspell", "拼错", "🔤"),
    ]),
    "stand": ("忍受；站", [
        ("stand", "忍受；站", "🚶"),
        ("understand", "理解", "🤝"),
    ]),
    "star": ("星星；明星", [
        ("star", "星星；明星", "⭐"),
        ("superstar", "超级明星", "🌟"),
    ]),
    "stop": ("停；车站", [
        ("stop", "停；车站", "🛑"),
        ("nonstop", "不停的", "🔁"),
    ]),
    "store": ("商店", [
        ("store", "商店", "🏬"),
        ("bookstore", "书店", "📚"),
    ]),
    "storm": ("暴风雨", [
        ("storm", "暴风雨", "🌩️"),
        ("rainstorm", "暴风雨", "🌧️"),
    ]),
    "strict": ("严格的", [
        ("strict", "严格的", "📏"),
        ("restrict", "限制；约束", "🚧"),
    ]),
    "summer": ("夏天", [
        ("summer", "夏天", "☀️"),
        ("midsummer", "仲夏", "☀️"),
    ]),
    "take": ("拿；带；拍", [
        ("take", "拿；带；拍", "📸"),
        ("mistake", "错误", "❌"),
    ]),
    "term": ("学期", [
        ("term", "学期", "📚"),
        ("midterm", "期中", "🔤"),
    ]),
    "thing": ("东西；事情", [
        ("thing", "东西；事情", "📦"),
        ("something", "某事物", "💭"),
        ("everything", "一切", "🌐"),
        ("nothing", "没有东西", "🚫"),
        ("anything", "任何东西", "❔"),
    ]),
    "trust": ("信任", [
        ("trust", "信任", "🤝"),
        ("entrust", "委托；托付", "🤝"),
    ]),
    "turn": ("转向", [
        ("turn", "转向", "↩️"),
        ("return", "回来；归还", "🔙"),
    ]),
    "visible": ("可见的", [
        ("visible", "可见的", "👁️"),
        ("invisible", "看不见的", "👻"),
    ]),
    "walk": ("走路", [
        ("walk", "走路", "🚶"),
        ("spacewalk", "太空行走", "🚶"),
    ]),
    "war": ("战争", [
        ("war", "战争", "⚔️"),
        ("antiwar", "反战的", "🔤"),
        ("postwar", "战后的", "🕊️"),
    ]),
    "wear": ("穿；戴", [
        ("wear", "穿；戴", "👕"),
        ("underwear", "内衣", "🩲"),
    ]),
    "weight": ("重量", [
        ("weight", "重量", "⚖️"),
        ("overweight", "超重的", "⚖️"),
    ]),
    "where": ("在哪里", [
        ("where", "在哪里", "📍"),
        ("everywhere", "到处", "🌍"),
        ("somewhere", "某处", "📍"),
        ("anywhere", "任何地方", "🗺️"),
        ("nowhere", "无处", "⛔"),
    ]),
    "word": ("单词；话语", [
        ("word", "单词；话语", "🔤"),
        ("crossword", "填字游戏", "🔤"),
    ]),
    "work": ("工作", [
        ("work", "工作", "🔨"),
        ("homework", "家庭作业", "📚"),
        ("housework", "家务", "🧹"),
        ("teamwork", "团队合作", "🤝"),
        ("schoolwork", "功课", "✏️"),
        ("overwork", "过度工作", "😫"),
    ]),
    "worker": ("工作者", [
        ("worker", "工作者", "💼"),
        ("coworker", "同事", "🔤"),
    ]),
    "write": ("写", [
        ("write", "写", "✍️"),
        ("rewrite", "重写", "✍️"),
    ]),
    "day": ("天；日子", [
        ("day", "天；日子", "🔤"),
        ("birthday", "生日", "🎂"),
        ("today", "今天", "📅"),
        ("weekday", "工作日", "📆"),
        ("weekend", "周末", "🎉"),
        ("holiday", "假日", "🏖️"),
    ]),
    "view": ("看；视野", [
        ("view", "看；视野", "🔤"),
        ("review", "复习；评论", "📝"),
        ("preview", "预习；预览", "👀"),
        ("interview", "面试；采访", "🎤"),
        ("viewer", "观看者", "👁️"),
    ]),
    "town": ("镇；城镇", [
        ("town", "镇；城镇", "🏘️"),
        ("hometown", "家乡", "🏠"),
        ("downtown", "市中心", "🏙️"),
    ]),
    "load": ("负荷", [
        ("load", "负荷", "🔤"),
        ("download", "下载", "⬇️"),
        ("upload", "上传", "⬆️"),
        ("overload", "超载", "💥"),
    ]),
    "net": ("网", [
        ("net", "网", "🔤"),
        ("internet", "互联网", "🌐"),
        ("network", "网络", "🕸️"),
    ]),
    "ware": ("物品", [
        ("ware", "物品", "🔤"),
        ("software", "软件", "💾"),
        ("hardware", "硬件", "🔧"),
    ]),
    "ache": ("疼痛", [
        ("ache", "疼痛", "🔤"),
        ("headache", "头痛", "🤕"),
        ("toothache", "牙痛", "🦷"),
        ("stomachache", "胃痛", "🤢"),
    ]),
    "tooth": ("牙齿", [
        ("tooth", "牙齿", "🦷"),
        ("toothbrush", "牙刷", "🪥"),
        ("toothpaste", "牙膏", "🦷"),
    ]),
    "shop": ("店", [
        ("shop", "店", "🔤"),
        ("workshop", "车间；研讨会", "🔧"),
        ("bookshop", "书店", "📚"),
    ]),
    "house": ("房子", [
        ("house", "房子", "🏠"),
        ("greenhouse", "温室", "🌱"),
        ("lighthouse", "灯塔", "🗼"),
    ]),
    "mate": ("伙伴", [
        ("mate", "伙伴", "🔤"),
        ("classmate", "同班同学", "🧑‍🎓"),
        ("roommate", "室友", "🛏️"),
        ("teammate", "队友", "🤝"),
    ]),
    "brush": ("刷；刷子", [
        ("brush", "刷；刷子", "🪥"),
        ("toothbrush", "牙刷", "🪥"),
        ("hairbrush", "发梳", "💇"),
    ]),
    "flower": ("花", [
        ("flower", "花", "🌸"),
        ("sunflower", "向日葵", "🌻"),
    ]),
    "time": ("时间", [
        ("time", "时间", "⏰"),
        ("bedtime", "就寝时间", "🛏️"),
        ("lifetime", "一生", "⌛"),
    ]),
    "modern": ("现代", [
        ("modern", "现代", "🔤"),
        ("postmodern", "后现代的", "🎭"),
    ]),
}
