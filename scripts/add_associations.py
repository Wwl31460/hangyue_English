#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给单词补 association 字段（联想记忆法：拆分 / 形象 / 画面）。

要点：
- 尽量“讲画面”：复合词按 A(义)+B(义)=合义，并配一句形象的话，让学生一眼能记；
  例如 glasses = glass(玻璃) 的复数，两块玻璃片架在鼻梁两边，不就是眼镜吗？
- 本脚本对 DATA 中的词【覆盖写】association（即便之前已有，也会替换成更形象的版本），
  方便持续打磨记忆法。
- 文本不含英文单引号，避免破坏 TS 字符串（脚本也会主动去掉单引号）。

用法：python scripts/add_associations.py
依赖：先由 gen_families / rebuild_all 生成 src/data/words.ts
"""
import re

PATH = 'src/data/words.ts'

# id -> 联想记忆文本（形象、具体、好记）
DATA = {
    # —— 用户点名的例子 ——
    'glasses': 'glass 表示玻璃，glasses 是它的复数——两块玻璃片架在鼻子两边，不就是眼镜吗？',
    'glass': 'glass 表示玻璃；玻璃做的杯子叫 a glass，复数 glasses 就是眼镜。',

    # —— 教室 / 学校 ——
    'classroom': 'class(课) + room(房间) = 上课的房间，就是教室。',
    'classmate': 'class(班) + mate(同伴) = 同班同伴，同学。',
    'school': 'school 学校，s 想“书”，是读书的地方。',
    'schoolbag': 'school(学校) + bag(包) = 上学背的包，书包。',
    'backpack': 'back(背) + pack(包) = 背在背上的包，书包。',
    'notebook': 'note(笔记) + book(书) = 记笔记的本子，笔记本。',
    'pencil_box': 'pencil(铅笔) + box(盒) = 装铅笔的盒子，铅笔盒。',
    'bookstore': 'book(书) + store(店) = 卖书的店，书店。',
    'library': 'library 图书馆，借书看书的地方。',
    'playground': 'play(玩) + ground(场地) = 玩耍的场地，操场。',
    'blackboard': 'black(黑) + board(板) = 黑色的板，黑板。',
    'window': 'wind(风) 从窗户缝吹进来；中间的 o 像方方的窗框。',
    'door': 'door 就是家里进出的那扇门，开关之间进出屋子。',
    'teacher': 'teach(教) + er(人) = 教人的人，老师。',
    'student': 'stud(学习) + ent(人) = 学习的人，学生。',

    # —— 家人 / 人 ——
    'father': 'fa(发) + ther：爸爸发工资养家。',
    'mother': 'mo(摸) + ther：妈妈常摸摸你、疼你。',
    'brother': 'bro(兄弟) + ther：兄弟。',
    'sister': 'sis(姐妹) + ter：姐妹。',
    'grandfather': 'grand(祖) + father(爸) = 爷爷或外公。',
    'grandmother': 'grand(祖) + mother(妈) = 奶奶或外婆。',
    'parents': 'parent(父/母)的复数，就是爸爸妈妈。',
    'children': 'child 的复数，孩子们。',
    'friend': 'friend 朋友，f 想“扶”——扶你一把的人就是朋友。',
    'friendship': 'friend(朋友) + ship(关系) = 朋友间的关系，友谊。',
    'worker': 'work(工作) + er(人) = 工作的人，工人。',
    'driver': 'drive(驾驶) + er(人) = 开车的人，司机。',
    'player': 'play(打/玩) + er(人) = 打球的人，运动员。',
    'singer': 'sing(唱) + er(人) = 唱歌的人，歌手。',
    'writer': 'write(写) + er(人) = 写书的人，作家。',
    'farmer': 'farm(农场) + er(人) = 种地的人，农民。',
    'actor': 'act(演) + or(人) = 演戏的人，演员。',
    'actress': 'act(演) + ress(女) = 女演员。',
    'policeman': 'police(警察) + man(人) = 男警察。',
    'policewoman': 'police(警察) + woman(女) = 女警察。',
    'fireman': 'fire(火) + man(人) = 救火的人，消防员。',
    'postman': 'post(邮) + man(人) = 送信的人，邮递员。',
    'fisherman': 'fish(鱼) + man(人) = 打鱼的人，渔夫。',
    'businessman': 'business(生意) + man(人) = 做生意的人，商人。',

    # —— 房间 / 家居 ——
    'bedroom': 'bed(床) + room(房间) = 放床的房间，卧室。',
    'bathroom': 'bath(洗澡) + room(房间) = 洗澡的房间，浴室。',
    'diningroom': 'dining(吃饭) + room(房间) = 吃饭的房间，餐厅。',
    'kitchen': 'kitchen 厨房，做饭的房间。',
    'garden': 'garden 花园，种花种草的院子。',
    'homework': 'home(家) + work(作业) = 回家做的作业，家庭作业。',
    'hometown': 'home(家) + town(镇) = 家乡。',

    # —— 运动 / 球 ——
    'football': 'foot(脚) + ball(球) = 用脚踢的球，足球。',
    'basketball': 'basket(篮) + ball(球) = 投进篮子的球，篮球。',
    'volleyball': 'volley(截击) + ball(球) = 用手截击过网的球，排球。',
    'bicycle': 'bi(两) + cycle(轮) = 两个轮子的车，自行车。',
    'motorcycle': 'motor(马达) + cycle(轮) = 有马达的两轮车，摩托车。',

    # —— 天气 / 自然 ——
    'sunny': 'sun(太阳) + y(…的) = 晴朗的。',
    'cloudy': 'cloud(云) + y(…的) = 多云的。',
    'rainy': 'rain(雨) + y(…的) = 下雨的。',
    'windy': 'wind(风) + y(…的) = 有风的。',
    'snowman': 'snow(雪) + man(人) = 雪堆的人，雪人。',
    'snowflake': 'snow(雪) + flake(片) = 雪花。',
    'raindrop': 'rain(雨) + drop(滴) = 雨滴。',
    'sunlight': 'sun(太阳) + light(光) = 太阳光。',
    'sunshine': 'sun(太阳) + shine(照耀) = 太阳照耀，阳光。',
    'moonlight': 'moon(月亮) + light(光) = 月光。',
    'earthquake': 'earth(地) + quake(震) = 地震。',
    'river': 'river 河，水哗哗地流。',
    'bridge': 'bridge 桥，跨过小河的道。',
    'mountain': 'mountain 高山，高高的。',
    'forest': 'forest 森林，很多树长在一起。',
    'village': 'village 村庄，乡下一片小房子。',
    'weather': 'weather 天气，晴雨冷暖。',
    'season': 'season 季节，春夏秋冬。',

    # —— 食物 / 水果 ——
    'watermelon': 'water(水) + melon(瓜) = 水多的瓜，西瓜。',
    'strawberry': 'straw(草) + berry(莓) = 草上的小红莓，草莓。',
    'mooncake': 'moon(月亮) + cake(饼) = 中秋的月饼。',
    'seafood': 'sea(海) + food(食物) = 海鲜。',
    'apple': 'a(一个) + pple(圆圆的) = 一个圆苹果。',
    'banana': 'ba(爸) + nana(娜娜)：爸爸给娜娜一根香蕉。',
    'orange': 'o 像圆圆的橙子，orange 就是橙子。',
    'egg': 'e 像蛋的形状，egg 就是蛋。',
    'milk': 'milk 牛奶，妈妈(m)给的奶。',

    # —— 动物 ——
    'elephant': 'e 像卷起的象鼻，ele-phant 一只胖大象。',
    'panda': 'pan 想“胖”、da 想“大”，胖胖大大的熊猫。',
    'tiger': 'tiger 老虎，ti 像“踢”——老虎一踢腿，小动物快跑。',
    'monkey': 'monkey 猴子，爱摸东摸西，连钥匙(key)都拿起来玩。',
    'bear': 'bear 熊，抱着(b)大耳朵(ear)，憨憨的。',
    'duck': 'duck 鸭子，肚(du)皮圆圆，走路左右摇。',
    'cat': 'cat 猫，爱抓(c)东西吃(at)。',

    # —— 颜色 / 自然物 ——
    'red': 'red 红色，红灯亮了要停下。',
    'green': 'green 绿色，草和树叶是绿的。',
    'blue': 'blue 蓝色，天空和海是蓝的。',
    'sun': 'sun 太阳，晒得暖暖的。',
    'water': 'water 水，wa 想“哇”流出来了。',

    # —— 通讯 / 远 ——
    'telephone': 'tele(远) + phone(声音) = 远距离传声，电话。',
    'television': 'tele(远) + vis(看) + ion = 远距离看画面，电视。',
    'computer': 'comput(计算) + er(机器) = 会算数的机器，电脑。',

    # —— 前缀 re(再) / un(不) / im-in(入) / ex(出) ——
    'unhappy': 'un(不) + happy(开心) = 不开心。',
    'review': 're(再) + view(看) = 再看一遍，复习。',
    'repeat': 're(再) + peat(说) = 再说一遍，重复。',
    'react': 're(回) + act(做) = 反应。',
    'reduce': 're(回) + duc(引) = 引回去，减少。',
    'recycle': 're(再) + cycle(循环) = 再循环，回收。',
    'report': 're(回) + port(送) = 送回消息，报告。',
    'prepare': 'pre(前) + pare(准备) = 事先准备。',
    'prefer': 'pre(前) + fer(取) = 先取这个，更喜欢。',
    'export': 'ex(出) + port(运) = 运出去，出口。',
    'import': 'im(入) + port(运) = 运进来，进口。',
    'express': 'ex(出) + press(压) = 把想法压出来，表达。',

    # —— 动作 / 状态 ——
    'science': 'sci(知) + ence(名词) = 科学知识，科学。',
    'pressure': 'press(压) + ure = 压力。',
    'action': 'act(做) + ion(名词) = 行动。',
    'active': 'act(做) + ive(…的) = 爱做事情的，活跃的。',
    'activity': 'act(做) + ivity = 活动。',
    'inventor': 'invent(发明) + or(人) = 发明家。',
    'helpful': 'help(帮助) + ful(充满) = 乐于助人的。',
    'useful': 'use(用) + ful(充满) = 有用的。',
    'careful': 'care(小心) + ful(充满) = 小心的。',
    'colorful': 'color(颜色) + ful(充满) = 色彩丰富的。',
    'powerful': 'power(力量) + ful(充满) = 有力量的。',
    'thankful': 'thank(谢) + ful(充满) = 感恩的。',
    'wonderful': 'wonder(奇妙) + ful(充满) = 充满奇妙的，精彩的。',
    'beautiful': 'beauty(美) + ful(充满) = 充满美的，美丽的。',
    'cheerful': 'cheer(欢呼) + ful(充满) = 欢乐的。',
    'careless': 'care(小心) + less(无) = 不小心的，粗心的。',
    'hopeless': 'hope(希望) + less(无) = 没希望的。',
    'homeless': 'home(家) + less(无) = 无家可归的。',
    'illness': 'ill(病) + ness(名词) = 疾病。',
    'happiness': 'happy(开心) + ness(名词) = 幸福。',
    'kindness': 'kind(善良) + ness(名词) = 善良。',
    'darkness': 'dark(暗) + ness(名词) = 黑暗。',
    'friendly': 'friend(朋友) + ly(…的) = 像朋友一样的，友好的。',
    'remember': 're(再) + member(成员) = 把成员再想起，记住。',
    'forget': 'forget 忘记，该带的又没了。',
    'understand': 'under(在…下) + stand(站) = 站在下面全看清，明白。',

    # —— 时间 / 日子 ——
    'weekend': 'week(周) + end(末) = 一周的末尾，周末。',
    'weekday': 'week(周) + day(天) = 工作日。',
    'afternoon': 'after(在…后) + noon(中午) = 中午之后，下午。',
    'midnight': 'mid(中) + night(夜) = 半夜。',
    'birthday': 'birth(出生) + day(天) = 出生那天，生日。',
    'holiday': 'holiday 假日，不用上学的日子。',
    'everyday': 'every(每) + day(天) = 每天。',

    # —— some/any/no + body/thing/where ——
    'somebody': 'some(某个) + body(人) = 某人。',
    'nobody': 'no(没有) + body(人) = 没有人。',
    'everybody': 'every(每个) + body(人) = 每个人。',
    'something': 'some(某个) + thing(东西) = 某物。',
    'nothing': 'no(没有) + thing(东西) = 什么都没有。',
    'everything': 'every(每个) + thing(东西) = 一切。',
    'anywhere': 'any(任何) + where(地方) = 任何地方。',
    'somewhere': 'some(某个) + where(地方) = 某处。',
    'everywhere': 'every(每个) + where(地方) = 到处。',
    'inside': 'in(在…里) + side(边) = 在里面。',
    'outside': 'out(在…外) + side(边) = 在外面。',
    'underline': 'under(在…下) + line(线) = 在下面画线，下划线。',

    # —— 交通 / 地点 ——
    'airport': 'air(空) + port(港) = 空港，飞机场。',
    'railway': 'rail(铁轨) + way(路) = 铁路。',
    'highway': 'high(高) + way(路) = 公路。',
    'subway': 'sub(下) + way(路) = 地下的路，地铁。',
    'supermarket': 'super(超级) + market(市场) = 超级市场，超市。',
    'restaurant': 'restaurant 餐馆，在外面吃饭的地方。',
    'hospital': 'hospital 医院，生病去看医生的地方。',
    'countryside': 'country(乡村) + side(边) = 乡间。',

    # —— 比较级 ——
    'taller': 'tall(高) + er(更) = 更高的。',
    'bigger': 'big(大) + ger(更) = 更大的。',
    'smaller': 'small(小) + er(更) = 更小的。',
    'stronger': 'strong(强壮) + er(更) = 更强壮的。',
}


def main():
    with open(PATH, encoding='utf-8') as f:
        lines = f.readlines()

    inserted = 0
    out = []
    for line in lines:
        m = re.match(r'\s*\{ id: "([A-Za-z0-9_]+)",', line)
        if m and m.group(1) in DATA:
            text = DATA[m.group(1)].replace("'", '').replace('"', '')  # 去掉引号，避免破坏 TS 字符串
            # 先去掉该行已有的 association（覆盖写，兼容单/双引号）
            newline = re.sub(r',\s*association: ["\'][^"\']*["\']', '', line)
            newline = newline.replace(
                '{ id: "%s",' % m.group(1),
                '{ id: "%s", association: "%s",' % (m.group(1), text),
                1,
            )
            out.append(newline)
            inserted += 1
        else:
            out.append(line)

    with open(PATH, 'w', encoding='utf-8') as f:
        f.writelines(out)

    print(f'已写入/覆盖联想记忆：{inserted} 个词')


if __name__ == '__main__':
    main()
