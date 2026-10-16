#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成「教材课文」听读材料：覆盖人教版 小学三年级 ~ 高中三年级 全部册次、全部单元。

单元清单直接读取 src/data/grades.ts 的 unitTitles（与背单词页共用同一套真实单元标题），
因此“有多少单元就生成多少篇”，小学/初中/高中一并导入。
输出 src/data/readings_textbook.ts，由 readings.ts 合并导入。

说明：句子为该单元主题/词汇的「代表性练习摘录」，每句附中文翻译（zh），
用于听读 + 理解语意；并非教材逐字原文。如需 100% 对照课本，可在生成的 sentences 中替换为课本原句。
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "src"))

# 各年级（按 id 前两位）词汇池（难度递增），用于生成主题相关的练习句
VOCAB = {
    "g3": ["ruler", "pencil", "crayon", "face", "nose", "duck", "bear", "cake", "milk", "ear", "arm", "pig"],
    "g4": ["classroom", "window", "door", "picture", "light", "computer", "fan", "wall", "floor", "teacher", "board", "desk"],
    "g5": ["clock", "plant", "bottle", "bike", "photo", "tree", "river", "hill", "bridge", "village", "lake", "house"],
    "g6": ["museum", "postcard", "supermarket", "cinema", "hospital", "crossing", "traffic", "puzzle", "hiking", "science", "film", "ship"],
    "c7": ["friend", "family", "subject", "music", "art", "sport", "weekend", "movie", "park", "restaurant", "club", "festival"],
    "c8": ["environment", "transport", "science", "invent", "protect", "recycle", "nature", "machine", "energy", "report", "planet", "action"],
    "c9": ["journey", "culture", "history", "society", "technology", "knowledge", "challenge", "future", "memory", "success", "value", "dream"],
    "h1": ["habit", "campus", "tradition", "generation", "adventure", "ambition", "volunteer", "creativity", "confidence", "explore", "communicate", "appreciate"],
    "h2": ["philosophy", "literature", "economy", "freedom", "wisdom", "responsibility", "civilization", "harmony", "vision", "dignity", "innovation", "heritage"],
    "h3": ["perspective", "sustainable", "phenomenon", "curiosity", "resilience", "diversity", "globalization", "achievement", "motivation", "cooperation", "evolution", "inspiration"],
}

COLORS = ["red", "blue", "green", "yellow", "brown", "white", "black", "orange"]
PLACE = {"g3": "room", "g4": "classroom", "g5": "school", "g6": "park"}

# 词汇 / 地点 / 颜色的中文释义（用于生成每句的中文翻译）
WORD_ZH = {
    # 三年级
    "ruler": "尺子", "pencil": "铅笔", "crayon": "蜡笔", "face": "脸", "nose": "鼻子", "duck": "鸭子",
    "bear": "熊", "cake": "蛋糕", "milk": "牛奶", "ear": "耳朵", "arm": "手臂", "pig": "猪",
    # 四年级
    "classroom": "教室", "window": "窗户", "door": "门", "picture": "图片", "light": "灯", "computer": "电脑",
    "fan": "风扇", "wall": "墙", "floor": "地板", "teacher": "老师", "board": "黑板", "desk": "课桌",
    # 五年级
    "clock": "钟", "plant": "植物", "bottle": "瓶子", "bike": "自行车", "photo": "照片", "tree": "树",
    "river": "河", "hill": "小山", "bridge": "桥", "village": "村庄", "lake": "湖", "house": "房子",
    # 六年级
    "museum": "博物馆", "postcard": "明信片", "supermarket": "超市", "cinema": "电影院", "hospital": "医院",
    "crossing": "十字路口", "traffic": "交通", "puzzle": "拼图", "hiking": "徒步", "science": "科学",
    "film": "电影", "ship": "轮船",
    # 七年级
    "friend": "朋友", "family": "家庭", "subject": "科目", "music": "音乐", "art": "美术", "sport": "运动",
    "weekend": "周末", "movie": "电影", "park": "公园", "restaurant": "餐馆", "club": "俱乐部", "festival": "节日",
    # 八年级
    "environment": "环境", "transport": "交通", "invent": "发明", "protect": "保护", "recycle": "回收",
    "nature": "自然", "machine": "机器", "energy": "能源", "report": "报告", "planet": "星球", "action": "行动",
    # 九年级
    "journey": "旅程", "culture": "文化", "history": "历史", "society": "社会", "technology": "科技",
    "knowledge": "知识", "challenge": "挑战", "future": "未来", "memory": "记忆", "success": "成功",
    "value": "价值", "dream": "梦想",
    # 高一
    "habit": "习惯", "campus": "校园", "tradition": "传统", "generation": "一代人", "adventure": "冒险",
    "ambition": "志向", "volunteer": "志愿者", "creativity": "创造力", "confidence": "自信",
    "explore": "探索", "communicate": "交流", "appreciate": "欣赏",
    # 高二
    "philosophy": "哲学", "literature": "文学", "economy": "经济", "freedom": "自由", "wisdom": "智慧",
    "responsibility": "责任", "civilization": "文明", "harmony": "和谐", "vision": "远见", "dignity": "尊严",
    "innovation": "创新", "heritage": "遗产",
    # 高三
    "perspective": "视角", "sustainable": "可持续的", "phenomenon": "现象", "curiosity": "好奇心",
    "resilience": "韧性", "diversity": "多样性", "globalization": "全球化", "achievement": "成就",
    "motivation": "动力", "cooperation": "合作", "evolution": "演变", "inspiration": "灵感",
    # 地点
    "room": "房间", "school": "学校", "city": "城市", "town": "小镇", "world": "世界",
    # 颜色
    "red": "红色", "blue": "蓝色", "green": "绿色", "yellow": "黄色", "brown": "棕色",
    "white": "白色", "black": "黑色", "orange": "橙色",
}


def zh(w):
    return WORD_ZH.get(w, w)


def parse_grades():
    """从 grades.ts 解析 grades 列表与 unitTitles（真实人教版单元标题）。"""
    text = open(os.path.join(SRC, "data", "grades.ts"), encoding="utf-8").read()

    grades = []
    for m in re.finditer(
        r"\{\s*id:\s*'(\w+)',\s*label:\s*'([^']+)',\s*short:\s*'([^']+)',\s*emoji:\s*'([^']*)',\s*section:\s*'([^']+)'\s*\}",
        text,
    ):
        grades.append({"id": m.group(1), "label": m.group(2), "short": m.group(3), "section": m.group(5)})

    ut_start = text.index("export const unitTitles")
    ut_block = text[ut_start:]

    units = {}
    for g in grades:
        gm = re.search(re.escape(g["id"]) + r":\s*\{([^}]*)\}", ut_block)
        if not gm:
            continue
        items = []
        # 标题可能用单引号或双引号包裹，两种都要能解析
        for um in re.finditer(r"(\d+):\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")", gm.group(1)):
            raw = um.group(2) if um.group(2) is not None else um.group(3)
            items.append((int(um.group(1)), raw.replace("\\'", "'").replace('\\"', '"')))
        items.sort()
        units[g["id"]] = items
    return grades, units


# 学段 / 年级显示名（按 id 前缀）
GRADE_NAME = {
    "g3": "三年级", "g4": "四年级", "g5": "五年级", "g6": "六年级",
    "c7": "七年级", "c8": "八年级", "c9": "九年级",
    "h1": "高一", "h2": "高二", "h3": "高三",
}


def sent_primary(w, c, place):
    """小学：具体形象句（看得到、摸得着）。"""
    return [
        ("Hello! Let us learn this unit.", "你好！我们来学习这一单元。"),
        (f"Look at the {w[0]}. It is {c}.", f"看这个{zh(w[0])}，它是{zh(c)}的。"),
        (f"I like the {w[1]} very much.", f"我非常喜欢{zh(w[1])}。"),
        (f"We can see a {w[2]} in the {place}.", f"在{zh(place)}里我们能看到{zh(w[2])}。"),
        (f"What colour is the {w[0]}? It is {c}.", f"{zh(w[0])}是什么颜色？是{zh(c)}的。"),
        (f"I have a {w[0]} in my bag.", f"我书包里有一个{zh(w[0])}。"),
        (f"The {w[1]} is very useful for us.", f"{zh(w[1])}对我们很有用。"),
        (f"Can you find the {w[2]}? It is here.", f"你能找到{zh(w[2])}吗？它在这里。"),
    ]


def sent_secondary(w):
    """中学：抽象、议论性句（贴合中学语篇风格）。"""
    return [
        ("Hello, class! Let us begin this unit.", "同学们好！我们开始学习这一单元。"),
        (f'We often meet the word "{w[0]}" in this unit.', f"在这一单元里我们经常会遇到单词“{zh(w[0])}”。"),
        (f"It is important to understand {w[1]}.", f"理解{zh(w[1])}很重要。"),
        (f"People talk about {w[2]} in everyday life.", f"人们在日常生活中会谈到{zh(w[2])}。"),
        (f"Can you use {w[0]} in a sentence?", f"你能用{zh(w[0])}造个句子吗？"),
        (f"The word {w[0]} has a clear meaning in English.", f"单词 {w[0]}（{zh(w[0])}）在英语里有明确的含义。"),
        (f"We should learn more about {w[1]}.", f"我们应该多了解{zh(w[1])}。"),
        (f"Try to remember the word {w[2]} today.", f"今天试着记住单词 {w[2]}（{zh(w[2])}）。"),
    ]


def build_questions(w, others, is_primary):
    q = []
    q.append({
        "id": "q1", "type": "choice",
        "question": "下面哪个单词是本单元的词？",
        "options": [w[0], others[0], others[1]],
        "answer": 0,
    })
    q.append({
        "id": "q2", "type": "choice",
        "question": f"“{zh(w[1])}”对应的英语单词是？",
        "options": [w[1], others[0], others[1]],
        "answer": 0,
    })
    q.append({
        "id": "q3", "type": "cloze",
        "prompt": "选词补全句子",
        "sentence": ("I like the ＿＿." if is_primary else "We often talk about ＿＿."),
        "blanks": [{"options": [w[1], others[0], others[1]], "answer": 0}],
    })
    return q


def esc(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')


def main():
    grades, units = parse_grades()

    out = []
    out.append("import { Reading } from '../types';")
    out.append("")
    out.append("// 自动生成（scripts/gen_textbook_readings.py）：人教版 小学三年级~高中 全部册次、全部单元。")
    out.append("// 单元标题取自 grades.ts 的 unitTitles（真实人教版单元）；句子为主题/词汇练习摘录（非教材逐字原文），每句附中文翻译。")
    out.append("export const textbookReadings: Reading[] = [")

    total = 0
    for g in grades:
        gid = g["id"]
        prefix = gid[:2]
        if prefix not in GRADE_NAME:
            continue
        sem = "上" if gid.endswith("1") else "下"
        grade_name = GRADE_NAME[prefix]
        section = g["section"]
        is_primary = prefix.startswith("g")
        pool = VOCAB[prefix]
        place = PLACE.get(prefix, "park")

        for k, (key, title) in enumerate(units.get(gid, [])):
            # 跳过复习单元（Revision / Recycle）
            if re.search(r"revision|recycle", title, re.I):
                continue

            unit_idx = k
            w = [pool[(unit_idx * 2 + j) % len(pool)] for j in range(4)]
            others = [x for x in pool if x not in w][:3]
            if len(others) < 2:
                others = (others + pool[:3])[:3]
            c = COLORS[unit_idx % len(COLORS)]

            if is_primary:
                pairs = sent_primary(w, c, place)
            else:
                pairs = sent_secondary(w)
            questions = build_questions(w, others, is_primary)

            rid = f"tb-{gid}-{key}"
            level = f"{grade_name}{sem}·人教版"
            out.append("  {")
            out.append(f'    id: "{rid}",')
            out.append(f'    level: "{level}",')
            out.append(f'    title: "{esc(title)}",')
            out.append(f'    topic: "{level}",')
            out.append('    duration: "0:50",')
            out.append('    audio: "",')
            out.append(f'    story: "{esc(" ".join(en for en, _ in pairs))}",')
            out.append("    sentences: [")
            for ji, (en, cn) in enumerate(pairs, start=1):
                out.append(f'      {{ id: "s{ji}", text: "{esc(en)}", zh: "{esc(cn)}" }},')
            out.append("    ],")
            out.append("    questions: [")
            for q in questions:
                if q["type"] == "choice":
                    opts = ", ".join(f'"{esc(o)}"' for o in q["options"])
                    out.append("      {")
                    out.append(f'        id: "{q["id"]}", type: "choice",')
                    out.append(f'        question: "{esc(q["question"])}",')
                    out.append(f'        options: [{opts}],')
                    out.append(f'        answer: {q["answer"]},')
                    out.append("      },")
                else:
                    bl = q["blanks"][0]
                    bopts = ", ".join(f'"{esc(o)}"' for o in bl["options"])
                    out.append("      {")
                    out.append(f'        id: "{q["id"]}", type: "cloze",')
                    out.append(f'        prompt: "{esc(q["prompt"])}",')
                    out.append(f'        sentence: "{esc(q["sentence"])}",')
                    out.append(f'        blanks: [{{ options: [{bopts}], answer: {bl["answer"]} }}],')
                    out.append("      },")
            out.append("    ],")
            out.append(
                f'    textbook: {{ grade: "{grade_name}", semester: "{sem}", unit: {key}, section: "{section}" }},'
            )
            out.append("  },")
            total += 1

    out.append("];")
    out.append("")

    target = os.path.normpath(os.path.join(SRC, "data", "readings_textbook.ts"))
    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"written: {target}  ({total} readings)")


if __name__ == "__main__":
    main()
