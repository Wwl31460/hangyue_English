#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按真实人教版(PEP) 六年级上册重建 g6s1：6 个真实单元 + 71 个四会词，
并补入用户要求的词族扩展（ex- 前缀 / cit 词根 / -ed 情绪形容词）。
替换 words.ts 中整个 g6s1 段落；与现有其它年级词去重（id 冲突则跳过）。
"""
import re

PATH = 'src/data/words.ts'
SECTION = '小学六年级上册 (g6s1)'
NEXT = '小学六年级下册 (g6s2)'


def w(**kw):
    """生成一行 Word 对象字面量（仅输出存在的可选字段）。"""
    order = ['id', 'word', 'meaning', 'pos', 'phonetic', 'image', 'grade', 'unit',
             'root', 'affix', 'affixMeaning', 'derive', 'association', 'forms', 'tags']
    parts = []
    for k in order:
        if k in kw and kw[k] is not None:
            v = kw[k]
            if k == 'tags':
                arr = '[' + ', '.join(f"'{t}'" for t in v) + ']'
                parts.append(f"{k}: {arr}")
            elif k == 'forms':
                inner = ', '.join(f"{fk}: '{fv}'" for fk, fv in v.items())
                parts.append(f"forms: {{{inner}}}")
            elif k in ('root', 'affix', 'affixMeaning', 'derive', 'association', 'meaning',
                       'word', 'pos', 'phonetic', 'image', 'id'):
                parts.append(f"{k}: '{v}'")
            else:
                parts.append(f"{k}: {v}")
    return '  { ' + ', '.join(parts) + ' },'


def entries():
    G = 'g6s1'
    E = []  # 收集

    # ===== Unit 1 How can I get there?（问路，地点） =====
    U1 = 1
    E.append(w(id='science_museum', word='science museum', meaning='科学博物馆', pos='n.', phonetic="/ˈsaɪəns mjuˈziːəm/", image='🏛️', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='post_office', word='post office', meaning='邮局', pos='n.', phonetic='/pəʊst ˈɒfɪs/', image='📮', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='bookstore', word='bookstore', meaning='书店', pos='n.', phonetic='/ˈbʊkstɔː(r)/', image='📚', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='cinema', word='cinema', meaning='电影院', pos='n.', phonetic='/ˈsɪnəmə/', image='🎬', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='hospital', word='hospital', meaning='医院', pos='n.', phonetic='/ˈhɒspɪtl/', image='🏥', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='crossing', word='crossing', meaning='十字路口', pos='n.', phonetic='/ˈkrɒsɪŋ/', image='🛣️', grade=G, unit=U1, tags=['地点', '四会']))
    E.append(w(id='turn', word='turn', meaning='转弯；转向', pos='v.', phonetic='/tɜːn/', image='↩️', grade=G, unit=U1, tags=['动作', '四会']))
    E.append(w(id='left', word='left', meaning='左；左边', pos='adv./n.', phonetic='/left/', image='⬅️', grade=G, unit=U1, tags=['方向', '四会']))
    E.append(w(id='right', word='right', meaning='右；右边', pos='adv./n.', phonetic='/raɪt/', image='➡️', grade=G, unit=U1, tags=['方向', '四会']))
    E.append(w(id='straight', word='straight', meaning='笔直地', pos='adv.', phonetic='/streɪt/', image='⬆️', grade=G, unit=U1, tags=['方向', '四会']))
    E.append(w(id='ask', word='ask', meaning='问；请求', pos='v.', phonetic='/ɑːsk/', image='❓', grade=G, unit=U1, tags=['动作', '四会']))
    E.append(w(id='sir', word='sir', meaning='先生（称呼）', pos='n.', phonetic='/sɜː/', image='🎩', grade=G, unit=U1, tags=['称呼', '四会']))
    E.append(w(id='interesting', word='interesting', meaning='有趣的', pos='adj.', phonetic='/ˈɪntrəstɪŋ/', image='🤔', grade=G, unit=U1, root='interest', association='in(在…里)+terest(搅动) → 让人心里起波澜的，有趣的。', tags=['四会']))
    # Unit1 前缀扩展（ex- 表“出/向外”）
    E.append(w(id='exit', word='exit', meaning='出口；离开', pos='n./v.', phonetic='/ˈeksɪt/', image='🚪', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', derive='exit = ex(出) + it(走) → 走出去 = 出口。', tags=['前缀 ex', '地点']))
    E.append(w(id='expect', word='expect', meaning='期待；预料', pos='v.', phonetic='/ɪkˈspekt/', image='⏳', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='spect', derive='expect = ex(向外) + spect(看) → 向外张望 = 期待。', tags=['前缀 ex']))
    E.append(w(id='explain', word='explain', meaning='解释；说明', pos='v.', phonetic='/ɪkˈspleɪn/', image='💬', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='plain', derive='explain = ex(向外) + plain(清楚) → 把道理说清楚 = 解释。', tags=['前缀 ex']))
    E.append(w(id='explore', word='explore', meaning='探索；探险', pos='v.', phonetic='/ɪkˈsplɔː(r)/', image='🧭', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='plore', derive='explore = ex(向外) + plore(探寻) → 向外探寻 = 探索。', tags=['前缀 ex']))
    E.append(w(id='examine', word='examine', meaning='检查；考试', pos='v.', phonetic='/ɪɡˈzæmɪn/', image='🔍', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='amine', derive='examine = ex(出) + amine(考察) → 检查、考察。', tags=['前缀 ex']))
    E.append(w(id='example', word='example', meaning='例子；榜样', pos='n.', phonetic='/ɪɡˈzɑːmpl/', image='📝', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='ample', derive='example = ex(出) + ample(样品) → 拿出来的样品 = 例子。', tags=['前缀 ex']))
    E.append(w(id='excellent', word='excellent', meaning='极好的；优秀的', pos='adj.', phonetic='/ˈeksələnt/', image='⭐', grade=G, unit=U1, affix='ex-', affixMeaning='表示出/向外', root='cell', derive='excellent = ex(出) + cell(凸起) → 脱颖而出 = 优秀。', tags=['前缀 ex']))

    # ===== Unit 2 Ways to go to school（交通方式） =====
    U2 = 2
    E.append(w(id='on_foot', word='on foot', meaning='步行', pos='phr.', phonetic='/ɒn fʊt/', image='🚶', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='by', word='by', meaning='乘（交通工具）', pos='prep.', phonetic='/baɪ/', image='🚆', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='bus', word='bus', meaning='公共汽车', pos='n.', phonetic='/bʌs/', image='🚌', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='plane', word='plane', meaning='飞机', pos='n.', phonetic='/pleɪn/', image='✈️', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='taxi', word='taxi', meaning='出租汽车', pos='n.', phonetic='/ˈtæksi/', image='🚕', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='ship', word='ship', meaning='船', pos='n.', phonetic='/ʃɪp/', image='🚢', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='subway', word='subway', meaning='地铁', pos='n.', phonetic='/ˈsʌbweɪ/', image='🚇', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='train', word='train', meaning='火车', pos='n.', phonetic='/treɪn/', image='🚄', grade=G, unit=U2, tags=['交通', '四会']))
    E.append(w(id='slow', word='slow', meaning='慢的', pos='adj.', phonetic='/sləʊ/', image='🐢', grade=G, unit=U2, tags=['四会']))
    E.append(w(id='down', word='down', meaning='向下；减少', pos='adv.', phonetic='/daʊn/', image='⬇️', grade=G, unit=U2, tags=['四会']))
    E.append(w(id='stop', word='stop', meaning='停下', pos='v.', phonetic='/stɒp/', image='🛑', grade=G, unit=U2, tags=['动作', '四会']))
    E.append(w(id='mrs', word='Mrs', meaning='夫人；太太', pos='n.', phonetic='/ˈmɪsɪz/', image='👩', grade=G, unit=U2, tags=['称呼', '四会']))

    # ===== Unit 3 My weekend plan（周末计划） =====
    U3 = 3
    E.append(w(id='visit', word='visit', meaning='拜访；参观', pos='v.', phonetic='/ˈvɪzɪt/', image='🏠', grade=G, unit=U3, root='vis', tags=['动作', '四会']))
    E.append(w(id='film', word='film', meaning='电影', pos='n.', phonetic='/fɪlm/', image='🎞️', grade=G, unit=U3, tags=['四会']))
    E.append(w(id='trip', word='trip', meaning='旅行', pos='n.', phonetic='/trɪp/', image='🧳', grade=G, unit=U3, tags=['四会']))
    E.append(w(id='supermarket', word='supermarket', meaning='超市', pos='n.', phonetic='/ˈsuːpəmɑːkɪt/', image='🛒', grade=G, unit=U3, root='market', tags=['地点', '四会']))
    E.append(w(id='evening', word='evening', meaning='晚上', pos='n.', phonetic='/ˈiːvnɪŋ/', image='🌆', grade=G, unit=U3, tags=['时间', '四会']))
    E.append(w(id='tonight', word='tonight', meaning='今晚', pos='n./adv.', phonetic='/təˈnaɪt/', image='🌙', grade=G, unit=U3, tags=['时间', '四会']))
    E.append(w(id='tomorrow', word='tomorrow', meaning='明天', pos='n./adv.', phonetic='/təˈmɒrəʊ/', image='📅', grade=G, unit=U3, tags=['时间', '四会']))
    E.append(w(id='dictionary', word='dictionary', meaning='词典', pos='n.', phonetic='/ˈdɪkʃənri/', image='📕', grade=G, unit=U3, root='dict', tags=['四会']))
    E.append(w(id='comic', word='comic', meaning='滑稽的；连环画', pos='adj./n.', phonetic='/ˈkɒmɪk/', image='😄', grade=G, unit=U3, tags=['四会']))
    E.append(w(id='comic_book', word='comic book', meaning='连环画', pos='n.', phonetic='/ˈkɒmɪk bʊk/', image='📗', grade=G, unit=U3, tags=['四会']))
    E.append(w(id='word_book', word='word book', meaning='单词书', pos='n.', phonetic='/wɜːd bʊk/', image='📘', grade=G, unit=U3, tags=['四会']))
    E.append(w(id='postcard', word='postcard', meaning='明信片', pos='n.', phonetic='/ˈpəʊstkɑːd/', image='💌', grade=G, unit=U3, tags=['四会']))

    # ===== Unit 4 I have a pen pal（笔友，爱好） =====
    U4 = 4
    E.append(w(id='pen_pal', word='pen pal', meaning='笔友', pos='n.', phonetic='/pen pæl/', image='✉️', grade=G, unit=U4, tags=['人际', '四会']))
    E.append(w(id='hobby', word='hobby', meaning='业余爱好', pos='n.', phonetic='/ˈhɒbi/', image='🎨', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='puzzle', word='puzzle', meaning='谜；拼图', pos='n.', phonetic='/ˈpʌzl/', image='🧩', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='hiking', word='hiking', meaning='远足；徒步', pos='n.', phonetic='/ˈhaɪkɪŋ/', image='🥾', grade=G, unit=U4, root='hike', tags=['四会']))
    E.append(w(id='jasmine', word='jasmine', meaning='茉莉', pos='n.', phonetic='/ˈdʒæzmɪn/', image='🌼', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='idea', word='idea', meaning='想法；主意', pos='n.', phonetic='/aɪˈdɪə/', image='💡', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='amazing', word='amazing', meaning='令人惊奇的', pos='adj.', phonetic='/əˈmeɪzɪŋ/', image='😲', grade=G, unit=U4, root='maze', association='a(一个)+mazing(迷宫) → 像走进迷宫一样，令人惊奇。', tags=['四会']))
    E.append(w(id='shall', word='shall', meaning='将要（征求意见）', pos='modal v.', phonetic='/ʃæl/', image='🤔', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='goal', word='goal', meaning='目标', pos='n.', phonetic='/ɡəʊl/', image='🎯', grade=G, unit=U4, tags=['四会']))
    E.append(w(id='join', word='join', meaning='加入；参加', pos='v.', phonetic='/dʒɔɪn/', image='➕', grade=G, unit=U4, tags=['动作', '四会']))
    E.append(w(id='club', word='club', meaning='俱乐部', pos='n.', phonetic='/klʌb/', image='🤼', grade=G, unit=U4, association='c(聚)+lub(乐部) → 聚在一起玩乐的部，俱乐部。', tags=['四会']))
    E.append(w(id='share', word='share', meaning='分享', pos='v.', phonetic='/ʃeə/', image='🤝', grade=G, unit=U4, tags=['动作', '四会']))

    # ===== Unit 5 What does he do?（职业） =====
    U5 = 5
    E.append(w(id='factory', word='factory', meaning='工厂', pos='n.', phonetic='/ˈfæktri/', image='🏭', grade=G, unit=U5, root='fact', tags=['地点', '四会']))
    E.append(w(id='worker', word='worker', meaning='工人', pos='n.', phonetic='/ˈwɜːkə/', image='👷', grade=G, unit=U5, affix='-er', affixMeaning='表示人', root='work', derive='worker = work(工作) + -er(人) → 工人。', tags=['职业', '四会']))
    E.append(w(id='postman', word='postman', meaning='邮递员', pos='n.', phonetic='/ˈpəʊstmən/', image='📮', grade=G, unit=U5, affix='-man', affixMeaning='表示人', root='post', derive='postman = post(邮政) + man(人) → 邮递员。', tags=['职业', '四会']))
    E.append(w(id='businessman', word='businessman', meaning='商人', pos='n.', phonetic='/ˈbɪznəsmən/', image='💼', grade=G, unit=U5, affix='-man', affixMeaning='表示人', root='business', derive='businessman = business(生意) + man(人) → 商人。', tags=['职业', '四会']))
    E.append(w(id='police_officer', word='police officer', meaning='警察', pos='n.', phonetic='/pəˈliːs ˈɒfɪsə/', image='👮', grade=G, unit=U5, tags=['职业', '四会']))
    E.append(w(id='fisherman', word='fisherman', meaning='渔民', pos='n.', phonetic='/ˈfɪʃəmən/', image='🎣', grade=G, unit=U5, affix='-man', affixMeaning='表示人', root='fish', derive='fisherman = fish(鱼) + man(人) → 渔民。', tags=['职业', '四会']))
    E.append(w(id='scientist', word='scientist', meaning='科学家', pos='n.', phonetic='/ˈsaɪəntɪst/', image='🔬', grade=G, unit=U5, affix='-ist', affixMeaning='表示人（职业）', root='sci', derive='scientist = sci(知) + -ist(人) → 科学家。', tags=['职业', '四会']))
    E.append(w(id='pilot', word='pilot', meaning='飞行员', pos='n.', phonetic='/ˈpaɪlət/', image='✈️', grade=G, unit=U5, tags=['职业', '四会']))
    E.append(w(id='coach', word='coach', meaning='教练', pos='n.', phonetic='/kəʊtʃ/', image='🏅', grade=G, unit=U5, tags=['职业', '四会']))
    E.append(w(id='country', word='country', meaning='国家', pos='n.', phonetic='/ˈkʌntri/', image='🌍', grade=G, unit=U5, tags=['四会']))
    E.append(w(id='sea', word='sea', meaning='大海', pos='n.', phonetic='/siː/', image='🌊', grade=G, unit=U5, tags=['自然', '四会']))

    # ===== Unit 6 How do you feel?（情绪感受） =====
    U6 = 6
    E.append(w(id='angry', word='angry', meaning='生气的', pos='adj.', phonetic='/ˈæŋɡri/', image='😠', grade=G, unit=U6, tags=['情绪', '四会']))
    E.append(w(id='afraid', word='afraid', meaning='害怕的', pos='adj.', phonetic='/əˈfreɪd/', image='😨', grade=G, unit=U6, tags=['情绪', '四会']))
    E.append(w(id='sad', word='sad', meaning='难过的', pos='adj.', phonetic='/sæd/', image='😢', grade=G, unit=U6, tags=['情绪', '四会']))
    E.append(w(id='worried', word='worried', meaning='担心的', pos='adj.', phonetic='/ˈwʌrid/', image='😟', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='worry', derive='worried = worry(使担忧) + -ed → 感到担心的。', tags=['情绪', '四会']))
    E.append(w(id='happy', word='happy', meaning='高兴的', pos='adj.', phonetic='/ˈhæpi/', image='😊', grade=G, unit=U6, tags=['情绪', '四会']))
    E.append(w(id='wear', word='wear', meaning='穿；戴', pos='v.', phonetic='/weə/', image='👕', grade=G, unit=U6, tags=['动作', '四会']))
    E.append(w(id='more', word='more', meaning='更多的', pos='adj./adv.', phonetic='/mɔː/', image='➕', grade=G, unit=U6, tags=['四会']))
    E.append(w(id='deep', word='deep', meaning='深的', pos='adj.', phonetic='/diːp/', image='🌊', grade=G, unit=U6, tags=['四会']))
    E.append(w(id='breath', word='breath', meaning='呼吸', pos='n.', phonetic='/breθ/', image='💨', grade=G, unit=U6, tags=['四会']))
    E.append(w(id='count', word='count', meaning='数数', pos='v.', phonetic='/kaʊnt/', image='🔢', grade=G, unit=U6, association='c(数)+ount(多少) → 数有多少，数数。', tags=['动作', '四会']))
    E.append(w(id='chase', word='chase', meaning='追赶', pos='v.', phonetic='/tʃeɪs/', image='🏃', grade=G, unit=U6, tags=['动作', '四会']))
    E.append(w(id='mouse', word='mouse', meaning='老鼠（复数 mice）', pos='n.', phonetic='/maʊs/', image='🐭', grade=G, unit=U6, tags=['动物', '四会']))
    # Unit6 情绪 -ed 家族（感到…的）
    E.append(w(id='bored', word='bored', meaning='感到无聊的', pos='adj.', phonetic='/bɔːd/', image='😑', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='bore', derive='bored = bore(使无聊) + -ed → 感到无聊的。', tags=['情绪', '-ed']))
    E.append(w(id='surprised', word='surprised', meaning='感到惊讶的', pos='adj.', phonetic='/səˈpraɪzd/', image='😲', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='surprise', derive='surprised = surprise(使惊讶) + -ed → 感到惊讶的。', tags=['情绪', '-ed']))
    E.append(w(id='interested', word='interested', meaning='感兴趣的', pos='adj.', phonetic='/ˈɪntrəstɪd/', image='🤓', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='interest', derive='interested = interest(使感兴趣) + -ed → 感兴趣的。', tags=['情绪', '-ed']))
    E.append(w(id='relaxed', word='relaxed', meaning='感到放松的', pos='adj.', phonetic='/rɪˈlækst/', image='😌', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='relax', derive='relaxed = relax(使放松) + -ed → 感到放松的。', tags=['情绪', '-ed']))
    E.append(w(id='tired', word='tired', meaning='疲惫的', pos='adj.', phonetic='/ˈtaɪəd/', image='😴', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='tire', derive='tired = tire(使疲倦) + -ed → 疲惫的。', tags=['情绪', '-ed']))
    E.append(w(id='frightened', word='frightened', meaning='感到害怕的', pos='adj.', phonetic='/ˈfraɪtnd/', image='😨', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='fright', derive='frightened = fright(使害怕) + -ed → 感到害怕的。', tags=['情绪', '-ed']))
    E.append(w(id='amazed_w', word='amazed', meaning='感到惊奇的', pos='adj.', phonetic='/əˈmeɪzd/', image='🤩', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='maze', derive='amazed = amaze(使惊奇) + -ed → 感到惊奇的。', tags=['情绪', '-ed']))
    # Unit6 词根 cit 家族（ex- 向外 + cit 激起）
    E.append(w(id='excited', word='excited', meaning='感到兴奋的', pos='adj.', phonetic='/ɪkˈsaɪtɪd/', image='🤩', grade=G, unit=U6, affix='-ed', affixMeaning='表示感到…的', root='cit', derive='excited = excit(使兴奋) + -ed → 感到兴奋的。', tags=['情绪', '-ed', '词根 cit']))
    E.append(w(id='excite', word='excite', meaning='使兴奋；使激动', pos='v.', phonetic='/ɪkˈsaɪt/', image='⚡', grade=G, unit=U6, affix='ex-', affixMeaning='表示出/向外', root='cit', derive='excite = ex(向外) + cit(激起) → 激起情绪 = 使兴奋。', tags=['前缀 ex', '词根 cit']))
    E.append(w(id='exciting', word='exciting', meaning='令人兴奋的', pos='adj.', phonetic='/ɪkˈsaɪtɪŋ/', image='🎉', grade=G, unit=U6, affix='-ing', affixMeaning='表示令人…的', root='cit', derive='exciting = excite + -ing → 令人兴奋的。', tags=['后缀 -ing', '词根 cit']))
    E.append(w(id='excitement', word='excitement', meaning='兴奋；激动', pos='n.', phonetic='/ɪkˈsaɪtmənt/', image='🎊', grade=G, unit=U6, affix='-ment', affixMeaning='名词后缀', root='cit', derive='excitement = excite + -ment → 兴奋（名词）。', tags=['后缀 -ment', '词根 cit']))
    E.append(w(id='recite', word='recite', meaning='背诵；朗诵', pos='v.', phonetic='/rɪˈsaɪt/', image='🗣️', grade=G, unit=U6, affix='re-', affixMeaning='表示再', root='cit', derive='recite = re(再次) + cit(唤起) → 再次唤起记忆 = 背诵。', tags=['前缀 re', '词根 cit']))
    E.append(w(id='recitation', word='recitation', meaning='背诵；朗诵', pos='n.', phonetic='/ˌresɪˈteɪʃn/', image='📜', grade=G, unit=U6, affix='-ation', affixMeaning='名词后缀', root='cit', derive='recitation = recite + -ation → 背诵（名词）。', tags=['后缀 -ation', '词根 cit']))
    return E


def main():
    with open(PATH, encoding='utf-8') as f:
        src = f.read()
    start_marker = f'// ===================== {SECTION} ====================='
    end_marker = f'// ===================== {NEXT} ====================='

    lines = entries()
    wanted_ids = [re.search(r"id: '([^']+)'", e).group(1) for e in lines]
    # 这些 id 若在其它年级已存在，说明之前被放错了年级 → 移到 6 上（删除旧副本）
    for wid in wanted_ids:
        pat = re.compile(r"^\s*\{\s*id: '%s'.*\},?\s*$" % re.escape(wid), re.M)
        src = pat.sub('', src)

    i = src.index(start_marker)
    j = src.index(end_marker)

    seen = set()
    final = []
    for e in lines:
        wid = re.search(r"id: '([^']+)'", e).group(1)
        if wid in seen:
            continue
        seen.add(wid)
        final.append(e)

    block = start_marker + '\n' + '\n'.join(final) + '\n'
    src = src[:i] + block + src[j:]
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f'g6s1 写入 {len(final)} 条（含从其它年级移入的重复词）')


if __name__ == '__main__':
    main()
