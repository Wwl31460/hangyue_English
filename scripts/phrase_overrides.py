# -*- coding: utf-8 -*-
"""功能词 / 多词条目的短语与例句人工覆盖表。

键 = word 小写；值 = (phrases, examples)，均为 (en, zh) 元组列表。
模板生成器遇到这些词时直接采用本表，避免自动模板产生不自然的句子。
"""

OVERRIDE = {
    # ---------------- 冠词 ----------------
    'the': (
        [('the book', '这本书'), ('the best', '最好的')],
        [('The book on the desk is mine.', '桌上那本书是我的。'),
         ('She is the tallest in our class.', '她是我们班最高的。')],
    ),
    # ---------------- 连词 ----------------
    'although': (
        [('although it is hard', '虽然很难')],
        [('Although it was late, he kept working.', '虽然很晚了，他还在工作。'),
         ('Although he is young, he is brave.', '虽然他很小，但他很勇敢。')],
    ),
    'because': (
        [('because of', '因为'), ('because it is raining', '因为在下雨')],
        [('I stay at home because it is raining.', '我待在家，因为下雨了。'),
         ('He was late because he missed the bus.', '他迟到了，因为他错过了公交。')],
    ),
    'but': (
        [('not ... but ...', '不是…而是…'), ('but also', '而且')],
        [('I like tea but not coffee.', '我喜欢茶但不喜欢咖啡。'),
         ('It is small but useful.', '它虽小但很有用。')],
    ),
    'nor': (
        [('neither ... nor ...', '既不…也不…')],
        [("He can't sing, nor can he dance.", '他不会唱歌，也不会跳舞。'),
         ('She neither smiled nor spoke.', '她既没笑也没说话。')],
    ),
    'once': (
        [('once a week', '每周一次'), ('at once', '立刻')],
        [("Once you start, don't give up.", '一旦你开始了，就别放弃。'),
         ('Once upon a time, there was a king.', '从前有一个国王。')],
    ),
    'or': (
        [('or so', '大约'), ('either ... or ...', '或者…或者…')],
        [('Tea or coffee?', '茶还是咖啡？'),
         ("Hurry up, or we'll be late.", '快点，否则我们会迟到。')],
    ),
    'unless': (
        [('unless you try', '除非你尝试')],
        [("You can't pass unless you work hard.", '除非你努力，否则无法通过。'),
         ("We'll go out unless it rains.", '除非下雨，否则我们就出去。')],
    ),
    'whenever': (
        [('whenever you like', '无论何时，只要你愿意')],
        [('Come to see me whenever you are free.', '你有空随时来看我。'),
         ('Whenever I see her, she smiles.', '我每次见到她，她都微笑。')],
    ),
    'whether': (
        [('whether or not', '是否'), ('whether to go', '是否去')],
        [("I don't know whether he will come.", '我不知道他是否会来。'),
         ('It depends on whether it is fine.', '这取决于天气是否好。')],
    ),
    'while': (
        [('while doing sth', '在做某事时'), ('for a while', '一会儿')],
        [('He read a book while I cooked.', '我做饭时他在看书。'),
         ('Please wait for a while.', '请等一会儿。')],
    ),
    # ---------------- 感叹词 ----------------
    'hello': (
        [('say hello to sb', '向某人问好'), ('hello everyone', '大家好')],
        [('Hello! Nice to meet you.', '你好！很高兴见到你。'),
         ('She said hello to me with a smile.', '她微笑着向我问好。')],
    ),
    'hey': (
        [('hey, look at that', '嘿，看那个')],
        [('Hey! What are you doing?', '嘿！你在干什么？'),
         ('Hey, come here please.', '嘿，请过来。')],
    ),
    'please': (
        [('please help me', '请帮帮我')],
        [('Please open the window.', '请打开窗户。'),
         ('Come in, please.', '请进。')],
    ),
    'thanks': (
        [('thanks to', '多亏'), ('thanks a lot', '非常感谢')],
        [('Thanks for your help.', '谢谢你的帮助。'),
         ('Thanks a lot for the gift.', '非常感谢这份礼物。')],
    ),
    # ---------------- 情态动词 ----------------
    'may': (
        [('may be', '也许是'), ('May I ...?', '我可以…吗？')],
        [('May I come in?', '我可以进来吗？'),
         ('It may rain tomorrow.', '明天可能会下雨。')],
    ),
    'might': (
        [('might be', '可能是')],
        [('He might be at home now.', '他现在可能在家。'),
         ('I might go with you.', '我可能会和你一起去。')],
    ),
    'must': (
        [('must be', '一定是'), ('must do sth', '必须做某事')],
        [('You must finish it today.', '你今天必须完成它。'),
         ('He must be very tired.', '他一定很累。')],
    ),
    'shall': (
        [('Shall we ...?', '我们…好吗？')],
        [('Shall we go now?', '我们现在走好吗？'),
         ('I shall be there at six.', '我六点会在那里。')],
    ),
    'should': (
        [('should do sth', '应该做某事'), ('should not', '不应该')],
        [('You should see a doctor.', '你应该去看医生。'),
         ('We should protect the earth.', '我们应该保护地球。')],
    ),
    'would': (
        [('would like to', '想要'), ('would rather', '宁愿')],
        [('I would like to have a cup of tea.', '我想喝杯茶。'),
         ('She said she would help us.', '她说她会帮我们。')],
    ),
    # ---------------- 连字符名词 ----------------
    't-shirt': (
        [('a cotton T-shirt', '一件棉T恤'), ('wear a T-shirt', '穿T恤')],
        [('He is wearing a white T-shirt.', '他穿着一件白T恤。'),
         ('This T-shirt is too big for me.', '这件T恤对我来说太大了。')],
    ),
    'e-mail': (
        [('send an e-mail', '发电子邮件'), ('by e-mail', '通过电子邮件')],
        [('I will send you an e-mail.', '我会给你发一封电子邮件。'),
         ('She reads her e-mail every morning.', '她每天早上看电子邮件。')],
    ),
    'ice-cream': (
        [('an ice cream', '一份冰淇淋'), ('have ice cream', '吃冰淇淋')],
        [('The ice cream is very sweet.', '这冰淇淋很甜。'),
         ('Children love ice cream.', '孩子们喜欢冰淇淋。')],
    ),
    'kung fu': (
        [('Chinese kung fu', '中国功夫'), ('learn kung fu', '学功夫')],
        [('He is good at Chinese kung fu.', '他擅长中国功夫。'),
         ('Many people learn kung fu in China.', '在中国很多人学功夫。')],
    ),
    'ping-pong': (
        [('play ping-pong', '打乒乓球'), ('a ping-pong ball', '乒乓球')],
        [('We play ping-pong after school.', '我们放学后打乒乓球。'),
         ('Ping-pong is very popular in China.', '乒乓球在中国很受欢迎。')],
    ),
    # ---------------- 数词 ----------------
    'billion': (
        [('billions of', '数十亿的')],
        [('There are billions of stars in space.', '太空中有数十亿颗星星。'),
         ('The company is worth two billion yuan.', '这家公司价值二十亿元。')],
    ),
    'eighteen': (
        [('eighteen years old', '十八岁')],
        [('My brother is eighteen years old.', '我哥哥十八岁。'),
         ('There are eighteen students here.', '这里有十八名学生。')],
    ),
    'eighth': (
        [('the eighth day', '第八天')],
        [('August is the eighth month of the year.', '八月是一年中的第八个月。'),
         ('He came eighth in the race.', '他在比赛中得了第八名。')],
    ),
    'eighty': (
        [('eighty years old', '八十岁')],
        [('My grandpa is eighty years old.', '我爷爷八十岁。'),
         ('There are eighty books on the shelf.', '书架上有八十本书。')],
    ),
    'eleven': (
        [('eleven years old', '十一岁')],
        [('She is eleven years old.', '她十一岁。'),
         ('The bus leaves at eleven.', '公交车十一点出发。')],
    ),
    'fifteen': (
        [('fifteen minutes', '十五分钟')],
        [('It takes fifteen minutes to get there.', '到那里需要十五分钟。'),
         ('He is fifteen years old.', '他十五岁。')],
    ),
    'fifth': (
        [('the fifth floor', '第五层')],
        [('She lives on the fifth floor.', '她住在五楼。'),
         ('Today is the fifth of May.', '今天是五月五日。')],
    ),
    'fifty': (
        [('fifty yuan', '五十元')],
        [('The book costs fifty yuan.', '这本书五十元。'),
         ('My father is fifty years old.', '我爸爸五十岁。')],
    ),
    'first': (
        [('at first', '起初'), ('first of all', '首先')],
        [('This is my first visit to Beijing.', '这是我第一次来北京。'),
         ('At first I was a little nervous.', '起初我有点紧张。')],
    ),
    'hundred': (
        [('two hundred', '两百'), ('hundreds of', '数百的')],
        [('There are two hundred students in our school.', '我们学校有两百名学生。'),
         ('Hundreds of people came to the show.', '数百人来看演出。')],
    ),
    'ninety': (
        [('ninety yuan', '九十元')],
        [('My grandma is ninety years old.', '我奶奶九十岁。'),
         ('The room is ninety square meters.', '这个房间九十平方米。')],
    ),
    'ninth': (
        [('the ninth day', '第九天')],
        [('September is the ninth month of the year.', '九月是一年中的第九个月。'),
         ('She is the ninth in line.', '她排在第九个。')],
    ),
    'second': (
        [('the second one', '第二个'), ('in a second', '马上')],
        [('This is my second time here.', '这是我第二次来这里。'),
         ('Please wait a second.', '请等一秒。')],
    ),
    'seventy': (
        [('seventy years old', '七十岁')],
        [('My grandpa is seventy years old.', '我爷爷七十岁。'),
         ('There are seventy people in the hall.', '大厅里有七十个人。')],
    ),
    'sixty': (
        [('sixty minutes', '六十分钟')],
        [('An hour has sixty minutes.', '一小时有六十分钟。'),
         ('He is sixty years old.', '他六十岁。')],
    ),
    'third': (
        [('the third floor', '第三层')],
        [('She lives on the third floor.', '她住在三楼。'),
         ('He is the third one to come.', '他是第三个来的。')],
    ),
    'thirteen': (
        [('thirteen years old', '十三岁')],
        [('My sister is thirteen years old.', '我妹妹十三岁。'),
         ('There are thirteen apples in the basket.', '篮子里有十三个苹果。')],
    ),
    'thirty': (
        [('thirty minutes', '三十分钟')],
        [('It takes thirty minutes by bus.', '坐公交需要三十分钟。'),
         ('He is thirty years old.', '他三十岁。')],
    ),
    'thousand': (
        [('two thousand', '两千'), ('thousands of', '数千的')],
        [('There are two thousand words in this book.', '这本书里有两千个词。'),
         ('Thousands of birds fly south in autumn.', '秋天成千上万的鸟向南飞。')],
    ),
    'twelfth': (
        [('the twelfth month', '第十二个月')],
        [('December is the twelfth month of the year.', '十二月是一年中的第十二个月。'),
         ('Today is the twelfth of June.', '今天是六月十二日。')],
    ),
    'twelve': (
        [('twelve months', '十二个月')],
        [('A year has twelve months.', '一年有十二个月。'),
         ('She is twelve years old.', '她十二岁。')],
    ),
    'twentieth': (
        [('the twentieth century', '二十世纪')],
        [('This is the twentieth lesson.', '这是第二十课。'),
         ('He was born in the twentieth century.', '他出生在二十世纪。')],
    ),
    'twenty': (
        [('twenty yuan', '二十元')],
        [('There are twenty students in the class.', '班上有二十名学生。'),
         ('He is twenty years old.', '他二十岁。')],
    ),
    # ---------------- 短语 ----------------
    'world war ii': (
        [('during World War II', '二战期间')],
        [('World War II ended in 1945.', '二战于1945年结束。'),
         ('Many people died in World War II.', '许多人在二战中丧生。')],
    ),
    'after all': (
        [('after all', '毕竟；终究')],
        [("Don't blame him; after all, he is a child.", '别怪他，毕竟他还是个孩子。'),
         ('After all, we are good friends.', '毕竟我们是好朋友。')],
    ),
    'at the same time': (
        [('at the same time', '同时')],
        [('They spoke at the same time.', '他们同时说话。'),
         ('He works and studies at the same time.', '他边工作边学习。')],
    ),
    'be harmful to': (
        [('be harmful to health', '对健康有害')],
        [('Smoking is harmful to your health.', '吸烟对你的健康有害。'),
         ('Too much sugar is harmful to children.', '太多糖对孩子有害。')],
    ),
    'by the time': (
        [("by the time I got there", '等我到那里时')],
        [('By the time he arrived, we had left.', '他到时我们已经走了。'),
         ('By the time you come back, I will have finished.', '等你回来时我就完成了。')],
    ),
    'costume party': (
        [('go to a costume party', '参加化装舞会')],
        [('We had a costume party last night.', '昨晚我们办了化装舞会。'),
         ('She wore a beautiful dress to the costume party.', '她穿着漂亮的裙子去化装舞会。')],
    ),
    "go out of one's way": (
        [("go out of one's way to help", '特地帮忙')],
        [('He went out of his way to help me.', '他特地来帮我。'),
         ('She always goes out of her way to be kind.', '她总是特意对人友善。')],
    ),
    'in line with': (
        [('in line with the rules', '与规则一致')],
        [('Stand in line with the others.', '和其他人排成一排。'),
         ('His idea is in line with ours.', '他的想法与我们的相符。')],
    ),
    'in person': (
        [('in person', '亲自')],
        [('I will tell him in person.', '我会亲自告诉他。'),
         ('She came to say sorry in person.', '她亲自来道歉。')],
    ),
    'in that case': (
        [('in that case', '既然那样')],
        [('In that case, we should leave early.', '既然那样，我们应该早点走。'),
         ('In that case, I agree with you.', '既然那样，我同意你的看法。')],
    ),
    'look back at': (
        [('look back at the past', '回首过去')],
        [('When I look back at my school days, I smile.', '回首学生时代我会微笑。'),
         ('He looked back at the old photos.', '他回头看着那些老照片。')],
    ),
    'make a mess': (
        [('make a mess of the room', '把房间弄得一团糟')],
        [('The children made a mess in the kitchen.', '孩子们把厨房弄得一团糟。'),
         ("Don't make a mess here.", '别在这里弄得一团糟。')],
    ),
    'make an effort': (
        [('make an effort to do sth', '努力做某事')],
        [('You should make an effort to study.', '你应该努力学习。'),
         ('She made an effort to smile.', '她努力笑了笑。')],
    ),
    'prime minister': (
        [('the Prime Minister', '首相')],
        [('The Prime Minister gave a speech.', '首相发表了讲话。'),
         ('He became prime minister last year.', '他去年成为首相。')],
    ),
    'separate from': (
        [('separate from', '与…分开')],
        [('The child was separated from his mother.', '那孩子和他的母亲走散了。'),
         ('Please separate the white from the yellow.', '请把白色的和黄色的分开。')],
    ),
    'show up': (
        [('show up on time', '准时出现')],
        [("He didn't show up at the party.", '他没有出现在聚会上。'),
         ('Please show up before eight.', '请在八点前到场。')],
    ),
    'take off': (
        [('take off your coat', '脱下外套'), ('the plane takes off', '飞机起飞')],
        [('Please take off your shoes.', '请脱下你的鞋子。'),
         ('The plane took off at nine.', '飞机九点起飞。')],
    ),
    'take part in': (
        [('take part in an activity', '参加活动')],
        [('Many students took part in the game.', '许多学生参加了比赛。'),
         ('Will you take part in the sports meeting?', '你会参加运动会吗？')],
    ),
    'upside down': (
        [('turn upside down', '倒置')],
        [('He held the map upside down.', '他把地图拿倒了。'),
         ('The boat turned upside down.', '船翻了。')],
    ),
    # ---------------- 介词 ----------------
    'above': (
        [('above the clouds', '在云层上方')],
        [('The plane flew above the clouds.', '飞机在云层上方飞行。'),
         ('The picture is above the desk.', '那幅画在桌子的上方。')],
    ),
    'across': (
        [('across the street', '横过街道'), ('across from', '在…对面')],
        [('He walked across the street.', '他穿过街道。'),
         ('The bank is across from the park.', '银行在公园对面。')],
    ),
    'after': (
        [('after school', '放学后'), ('after all', '毕竟')],
        [('We play football after school.', '我们放学后踢足球。'),
         ('He came back after three days.', '他三天后回来了。')],
    ),
    'against': (
        [('against the wall', '靠着墙'), ('be against', '反对')],
        [('He stood against the wall.', '他靠着墙站着。'),
         ('I am against this plan.', '我反对这个计划。')],
    ),
    'along': (
        [('along the river', '沿着河')],
        [('We walked along the river.', '我们沿着河走。'),
         ('Trees grow along the road.', '树沿着路边生长。')],
    ),
    'alongside': (
        [('alongside the river', '在河边')],
        [('He worked alongside his father.', '他和他父亲并肩工作。'),
         ('The boat moved alongside the ship.', '小船靠在大船旁边。')],
    ),
    'among': (
        [('among the trees', '在树丛中'), ('among us', '在我们中间')],
        [('She is the tallest among us.', '她是我们当中最高的。'),
         ('He hid among the trees.', '他躲在树丛中。')],
    ),
    'as': (
        [('as ... as', '和…一样'), ('as usual', '像平常一样')],
        [('He is as tall as his father.', '他和他父亲一样高。'),
         ('As usual, she was late.', '像平常一样，她迟到了。')],
    ),
    'below': (
        [('below zero', '零度以下')],
        [('The temperature is below zero.', '温度在零度以下。'),
         ('Write your name below the line.', '把名字写在线的下方。')],
    ),
    'beyond': (
        [('beyond the river', '在河的那边')],
        [('The village is beyond the hills.', '村庄在山的那边。'),
         ('It is beyond my ability.', '这超出了我的能力。')],
    ),
    'despite': (
        [('despite the rain', '尽管下雨')],
        [('Despite the rain, we went out.', '尽管下雨，我们还是出去了。'),
         ('He came despite being ill.', '尽管生病了，他还是来了。')],
    ),
    'during': (
        [('during the holiday', '在假期期间')],
        [('We visited many places during the holiday.', '假期里我们参观了很多地方。'),
         ('Please be quiet during the class.', '上课期间请安静。')],
    ),
    'from': (
        [('from ... to ...', '从…到…'), ('come from', '来自')],
        [('I come from China.', '我来自中国。'),
         ('The shop is open from nine to six.', '商店从九点开到六点。')],
    ),
    'in': (
        [('in front of', '在…前面'), ('in the morning', '在早上')],
        [('There is a cat in the box.', '盒子里有一只猫。'),
         ('I get up early in the morning.', '我早上起得早。')],
    ),
    'near': (
        [('near the school', '在学校附近')],
        [('My home is near the school.', '我家在学校附近。'),
         ("Don't stand near the fire.", '别站在火边。')],
    ),
    'on': (
        [('on the desk', '在桌上'), ('on time', '准时')],
        [('The book is on the desk.', '书在桌子上。'),
         ('Please come on time.', '请准时来。')],
    ),
    'onto': (
        [('onto the stage', '上舞台')],
        [('He climbed onto the roof.', '他爬上了屋顶。'),
         ('The cat jumped onto the table.', '猫跳上了桌子。')],
    ),
    'than': (
        [('more than', '多于'), ('less than', '少于')],
        [('He is taller than me.', '他比我高。'),
         ('There are more than fifty people.', '有五十多个人。')],
    ),
    'through': (
        [('through the forest', '穿过森林')],
        [('We walked through the forest.', '我们穿过森林。'),
         ('He got the news through a friend.', '他通过一个朋友得到了消息。')],
    ),
    'till': (
        [('till the end', '直到最后')],
        [('Wait till I come back.', '等到我回来。'),
         ('He worked till midnight.', '他工作到午夜。')],
    ),
    'under': (
        [('under the tree', '在树下'), ('under control', '在控制之中')],
        [('The cat is under the tree.', '猫在树下。'),
         ("Don't stand under the tree in a storm.", '暴风雨中别站在树下。')],
    ),
    'via': (
        [('via e-mail', '通过电子邮件')],
        [('I sent it via e-mail.', '我通过电子邮件发的。'),
         ('We flew to London via Paris.', '我们经巴黎飞往伦敦。')],
    ),
    'with': (
        [('with the help of', '在…的帮助下'), ('play with sb', '和某人玩')],
        [('I go to school with my sister.', '我和妹妹一起上学。'),
         ('With his help, I finished the work.', '在他的帮助下，我完成了工作。')],
    ),
    'without': (
        [('without water', '没有水')],
        [("We can't live without water.", '没有水我们无法生存。'),
         ('He left without saying goodbye.', '他不辞而别。')],
    ),
    # ---------------- 代词 ----------------
    'anybody': (
        [('anybody else', '其他任何人')],
        [('Is anybody here?', '有人在吗？'),
         ('Anybody can join us.', '任何人都可以加入我们。')],
    ),
    'anyone': (
        [('anyone else', '其他任何人')],
        [('Is anyone at home?', '有人在家吗？'),
         ('Anyone can do this job.', '任何人都能做这份工作。')],
    ),
    'both': (
        [('both of us', '我们两个都'), ('both ... and ...', '既…又…')],
        [('Both of us like music.', '我们俩都喜欢音乐。'),
         ('She can both sing and dance.', '她既会唱歌又会跳舞。')],
    ),
    'everybody': (
        [('everybody here', '这里的每个人')],
        [('Everybody likes her.', '大家都喜欢她。'),
         ('Everybody is ready now.', '现在大家都准备好了。')],
    ),
    'everyone': (
        [('everyone else', '其他每个人')],
        [('Everyone is here.', '大家都到了。'),
         ('Everyone wants to be happy.', '每个人都想快乐。')],
    ),
    'her': (
        [('her book', '她的书')],
        [('This is her pen.', '这是她的钢笔。'),
         ('I gave her a gift.', '我给了她一份礼物。')],
    ),
    'herself': (
        [('by herself', '她独自')],
        [('She made the cake herself.', '她自己做了蛋糕。'),
         ('She lives by herself.', '她独自生活。')],
    ),
    'himself': (
        [('by himself', '他自己')],
        [('He cleaned the room himself.', '他自己打扫了房间。'),
         ('He often talks to himself.', '他常常自言自语。')],
    ),
    'his': (
        [('his bag', '他的包')],
        [('This is his bike.', '这是他的自行车。'),
         ('His words made me happy.', '他的话让我很高兴。')],
    ),
    'itself': (
        [('by itself', '它自己')],
        [('The door opened by itself.', '门自己开了。'),
         ('The cat is cleaning itself.', '猫在舔自己。')],
    ),
    'mine': (
        [('a friend of mine', '我的一个朋友')],
        [('This book is mine.', '这本书是我的。'),
         ('He is a friend of mine.', '他是我的一个朋友。')],
    ),
    'myself': (
        [('by myself', '我自己')],
        [('I did my homework by myself.', '我自己做的作业。'),
         ('I hurt myself.', '我伤到了自己。')],
    ),
    'neither': (
        [('neither of us', '我们两个都不')],
        [('Neither of them came.', '他们俩都没来。'),
         ('Neither answer is right.', '两个答案都不对。')],
    ),
    'nobody': (
        [('nobody else', '没有别人')],
        [('Nobody was at home.', '没人在家。'),
         ('Nobody knows the answer.', '没人知道答案。')],
    ),
    'nothing': (
        [('nothing else', '没有别的')],
        [('There is nothing in the box.', '盒子里什么都没有。'),
         ('He said nothing and left.', '他什么也没说就走了。')],
    ),
    'our': (
        [('our school', '我们的学校')],
        [('Our teachers are very kind.', '我们的老师很和善。'),
         ('This is our classroom.', '这是我们的教室。')],
    ),
    'ours': (
        [('a friend of ours', '我们的一个朋友')],
        [('The house is ours.', '这房子是我们的。'),
         ('This classroom is ours.', '这间教室是我们的。')],
    ),
    'ourselves': (
        [('by ourselves', '我们自己')],
        [('We finished the work by ourselves.', '我们自己完成了工作。'),
         ('We should believe in ourselves.', '我们应该相信自己。')],
    ),
    'plenty': (
        [('plenty of', '大量的')],
        [('There is plenty of water here.', '这里有很多水。'),
         ('We have plenty of time.', '我们有充足的时间。')],
    ),
    'someone': (
        [('someone else', '别人')],
        [('Someone is knocking at the door.', '有人在敲门。'),
         ('I need someone to help me.', '我需要有人帮我。')],
    ),
    'something': (
        [('something to eat', '吃的东西')],
        [('I want something to drink.', '我想要点喝的。'),
         ('There is something wrong with it.', '它出毛病了。')],
    ),
    'that': (
        [('that one', '那个')],
        [('That is my school.', '那是我的学校。'),
         ('I know that he is right.', '我知道他是对的。')],
    ),
    'their': (
        [('their parents', '他们的父母')],
        [('Their home is near the park.', '他们家离公园很近。'),
         ('The students love their teacher.', '学生们爱他们的老师。')],
    ),
    'them': (
        [('help them', '帮助他们')],
        [('I like them very much.', '我非常喜欢他们。'),
         ('Please give them to me.', '请把它们给我。')],
    ),
    'themselves': (
        [('by themselves', '他们自己')],
        [('The children made it themselves.', '孩子们自己做成的。'),
         ('They enjoyed themselves at the party.', '他们在聚会上玩得很开心。')],
    ),
    'these': (
        [('these days', '这些天')],
        [('These are my books.', '这些是我的书。'),
         ('These days I am very busy.', '这些天我很忙。')],
    ),
    'they': (
        [('they are', '他们是')],
        [('They are my classmates.', '他们是我的同学。'),
         ('They play football every week.', '他们每周踢足球。')],
    ),
    'this': (
        [('this morning', '今天早上')],
        [('This is my pen.', '这是我的钢笔。'),
         ('What is this?', '这是什么？')],
    ),
    'those': (
        [('those days', '那些日子')],
        [('Those are my friends.', '那些是我的朋友。'),
         ('I still remember those days.', '我仍然记得那些日子。')],
    ),
    'us': (
        [('help us', '帮助我们')],
        [('Please come with us.', '请和我们一起来。'),
         ('Let us go home.', '我们回家吧。')],
    ),
    'we': (
        [('we are', '我们是')],
        [('We are good friends.', '我们是好朋友。'),
         ('We go to school together.', '我们一起去上学。')],
    ),
    'what': (
        [('what about', '…怎么样'), ('what time', '几点')],
        [('What is your name?', '你叫什么名字？'),
         ('What about going out?', '出去怎么样？')],
    ),
    'whatever': (
        [('whatever you want', '无论你想要什么')],
        [('Whatever you do, do it well.', '无论你做什么，都要做好。'),
         ('You can eat whatever you like.', '你想吃什么都可以。')],
    ),
    'who': (
        [('who else', '还有谁')],
        [('Who is that girl?', '那个女孩是谁？'),
         ('Who wants to try?', '谁想试一试？')],
    ),
    'whom': (
        [('by whom', '由谁')],
        [('Whom did you meet yesterday?', '你昨天遇见了谁？'),
         ('The man whom I met is kind.', '我遇到的那个人很和善。')],
    ),
    'whose': (
        [('whose book', '谁的书')],
        [('Whose bag is this?', '这是谁的包？'),
         ("I don't know whose it is.", '我不知道这是谁的。')],
    ),
    'your': (
        [('your name', '你的名字')],
        [('What is your name?', '你叫什么名字？'),
         ('Is this your book?', '这是你的书吗？')],
    ),
    'yours': (
        [('a friend of yours', '你的一个朋友')],
        [('Is this pen yours?', '这支钢笔是你的吗？'),
         ('He is a friend of yours.', '他是你的一个朋友。')],
    ),
    'yourself': (
        [('by yourself', '你自己')],
        [('You should do it yourself.', '你应该自己做。'),
         ('Take good care of yourself.', '你要照顾好自己。')],
    ),
    # ---------------- 动词短语 ----------------
    'clean up': (
        [('clean up the room', '打扫房间')],
        [("Let's clean up the classroom.", '我们把教室打扫干净吧。'),
         ('He cleaned up the kitchen after dinner.', '晚饭后他打扫了厨房。')],
    ),
    # ---------------- 高频不规则 / 系动词（模板易出错，人工给定） ----------------
    'be': (
        [('be happy', '开心'), ('be from', '来自')],
        [('I want to be a teacher.', '我想成为一名老师。'),
         ("Don't be late.", '别迟到。')],
    ),
    'become': (
        [('become a doctor', '成为医生')],
        [('He wants to become a doctor.', '他想成为一名医生。'),
         ('The weather becomes cold in winter.', '冬天天气变冷。')],
    ),
    'seem': (
        [('seem happy', '看起来开心')],
        [('He seems very tired today.', '他今天看起来很累。'),
         ('It seems that she is right.', '看起来她是对的。')],
    ),
    'appear': (
        [('appear on TV', '上电视')],
        [('He appeared at the door.', '他出现在门口。'),
         ('A smile appeared on her face.', '她脸上露出了笑容。')],
    ),
    'belong': (
        [('belong to', '属于')],
        [('This book belongs to me.', '这本书属于我。'),
         ('Which team do you belong to?', '你属于哪一队？')],
    ),
    'include': (
        [('include sth', '包括某物')],
        [('The price includes breakfast.', '价格包含早餐。'),
         ('Everyone was included in the list.', '每个人都在名单中。')],
    ),
    'contain': (
        [('contain water', '含有水')],
        [('This box contains many books.', '这个盒子装有很多书。'),
         ('The drink contains too much sugar.', '这种饮料含糖太多。')],
    ),
    'cost': (
        [('cost a lot', '花费很多')],
        [('The ticket costs ten yuan.', '票价十元。'),
         ('How much does it cost?', '这要多少钱？')],
    ),
    'weigh': (
        [('weigh 50 kilos', '重五十公斤')],
        [('How much do you weigh?', '你多重？'),
         ('The box weighs ten kilos.', '这个箱子重十公斤。')],
    ),
    'matter': (
        [("What's the matter?", '怎么了？')],
        [("What's the matter with you?", '你怎么了？'),
         ("It doesn't matter.", '没关系。')],
    ),
    'exist': (
        [('exist in the world', '存在于世界上')],
        [('Water exists everywhere.', '水到处都存在。'),
         ('Dinosaurs no longer exist.', '恐龙已经不存在了。')],
    ),
    'consist': (
        [('consist of', '由…组成')],
        [('The team consists of six players.', '这个队由六名队员组成。'),
         ('Water consists of hydrogen and oxygen.', '水由氢和氧组成。')],
    ),
    'depend': (
        [('depend on', '依靠；取决于')],
        [('Children depend on their parents.', '孩子依靠父母。'),
         ('It depends on the weather.', '这取决于天气。')],
    ),
    'prove': (
        [('prove to be true', '证明是真的')],
        [('He proved that he was right.', '他证明了自己是对的。'),
         ('The plan proved useful.', '这个计划证明很有用。')],
    ),
    'remain': (
        [('remain silent', '保持沉默')],
        [('He remained calm in danger.', '危险中他保持冷静。'),
         ('Only a few trees remain.', '只剩下几棵树了。')],
    ),
    'taste': (
        [('taste good', '尝起来不错')],
        [('The soup tastes delicious.', '这汤尝起来很美味。'),
         ('Would you like to taste it?', '你想尝尝吗？')],
    ),
    'smell': (
        [('smell nice', '闻起来很香')],
        [('The flowers smell sweet.', '花闻起来很香。'),
         ('Can you smell the smoke?', '你能闻到烟味吗？')],
    ),
    'sound': (
        [('sound great', '听起来很棒')],
        [('Your idea sounds great.', '你的主意听起来很棒。'),
         ('That sounds like fun.', '那听起来很有趣。')],
    ),
    'feel': (
        [('feel happy', '感到开心')],
        [('I feel much better now.', '我现在感觉好多了。'),
         ('How do you feel today?', '你今天感觉怎么样？')],
    ),
    'look': (
        [('look at', '看'), ('look like', '看起来像')],
        [('Look at the blackboard, please.', '请看黑板。'),
         ('She looks like her mother.', '她长得像她妈妈。')],
    ),
    'rise': (
        [('rise early', '早起'), ('the sun rises', '太阳升起')],
        [('The sun rises in the east.', '太阳从东方升起。'),
         ('Prices are rising quickly.', '物价上涨很快。')],
    ),
    'raise': (
        [('raise your hand', '举手'), ('raise money', '筹钱')],
        [('Raise your hand if you know.', '知道的话请举手。'),
         ('They raised money for the poor.', '他们为穷人筹款。')],
    ),
    'lie': (
        [('lie down', '躺下'), ('lie to sb', '对某人撒谎')],
        [('He lay on the bed.', '他躺在床上。'),
         ("Don't lie to me.", '别对我撒谎。')],
    ),
    'hold': (
        [('hold on', '等一下'), ('hold a meeting', '开会')],
        [('Please hold on a moment.', '请稍等一会儿。'),
         ('He held the baby in his arms.', '他把婴儿抱在怀里。')],
    ),
    'hurt': (
        [('hurt oneself', '伤到自己')],
        [('My leg hurts a lot.', '我的腿很疼。'),
         ('Be careful not to hurt others.', '小心别伤到别人。')],
    ),
    'beat': (
        [('beat sb', '打败某人')],
        [('Our team beat theirs.', '我们队打败了他们队。'),
         ('His heart beats fast.', '他的心跳得很快。')],
    ),
    'win': (
        [('win the game', '赢得比赛')],
        [('Our class won the game.', '我们班赢得了比赛。'),
         ('He wants to win the first prize.', '他想赢得一等奖。')],
    ),
    'lose': (
        [('lose the game', '输掉比赛'), ("lose one's way", '迷路')],
        [("Don't lose your key.", '别丢了钥匙。'),
         ('We lost the game yesterday.', '我们昨天输了比赛。')],
    ),
    'lead': (
        [('lead to', '导致'), ('lead a team', '带领团队')],
        [('This road leads to the park.', '这条路通向公园。'),
         ('He leads his team well.', '他把团队带得很好。')],
    ),
    'mean': (
        [('mean to do sth', '打算做某事')],
        [('What does this word mean?', '这个词什么意思？'),
         ("I didn't mean to hurt you.", '我不是故意要伤害你。')],
    ),
    'mind': (
        [('mind doing sth', '介意做某事')],
        [('Would you mind opening the window?', '你介意开窗吗？'),
         ('Never mind.', '没关系。')],
    ),
    'happen': (
        [('happen to sb', '发生在某人身上')],
        [('What happened to you?', '你发生了什么事？'),
         ('It happened last night.', '这是昨晚发生的。')],
    ),
    'arrive': (
        [('arrive at the station', '到达车站')],
        [('We arrived at the station early.', '我们很早就到了车站。'),
         ('When will you arrive in Beijing?', '你什么时候到北京？')],
    ),
    'agree': (
        [('agree with sb', '同意某人')],
        [('I agree with you.', '我同意你的看法。'),
         ('They agreed to help us.', '他们同意帮我们。')],
    ),
    'die': (
        [('die of illness', '死于疾病')],
        [('The old tree died last year.', '那棵老树去年死了。'),
         ('Many animals die of hunger.', '许多动物死于饥饿。')],
    ),
    'stay': (
        [('stay at home', '待在家')],
        [('I stayed at home all day.', '我一整天都待在家。'),
         ('Please stay here and wait.', '请待在这里等。')],
    ),
    'keep': (
        [('keep doing sth', '一直做某事')],
        [('He keeps running every morning.', '他每天早上都跑步。'),
         ('Keep quiet in the library.', '在图书馆保持安静。')],
    ),
    'grow': (
        [('grow up', '长大'), ('grow vegetables', '种菜')],
        [('He grew up in the countryside.', '他在乡下长大。'),
         ('The trees grow very fast.', '这些树长得很快。')],
    ),
    'turn': (
        [('turn on', '打开'), ('turn off', '关掉')],
        [('Please turn on the light.', '请打开灯。'),
         ('Turn left at the corner.', '在拐角处左转。')],
    ),
    'get': (
        [('get up', '起床'), ('get along with', '与…相处')],
        [('I get up at six.', '我六点起床。'),
         ('How can I get to the station?', '我怎么去车站？')],
    ),
    'have': (
        [('have to', '不得不'), ('have fun', '玩得开心')],
        [('I have a new bike.', '我有一辆新自行车。'),
         ('We had a good time.', '我们玩得很开心。')],
    ),
    'do': (
        [('do homework', '做作业'), ("do one's best", '尽力')],
        [('What do you do on Sundays?', '你周日做什么？'),
         ('Please do your best.', '请尽力而为。')],
    ),
    'make': (
        [('make friends', '交朋友'), ('make a cake', '做蛋糕')],
        [('She made a cake for me.', '她为我做了个蛋糕。'),
         ("It's easy to make friends here.", '在这里交朋友很容易。')],
    ),
    'take': (
        [('take a bus', '乘公交'), ('take care of', '照顾')],
        [('I take a bus to school.', '我乘公交上学。'),
         ('Please take care of yourself.', '请照顾好自己。')],
    ),
    'give': (
        [('give sb sth', '给某人某物'), ('give up', '放弃')],
        [('He gave me a book.', '他给了我一本书。'),
         ("Don't give up too early.", '别太早放弃。')],
    ),
    'put': (
        [('put on', '穿上'), ('put away', '收好')],
        [('Put on your coat.', '穿上外套。'),
         ('Please put away your books.', '请把书收好。')],
    ),
    'say': (
        [('say hello to sb', '向某人问好')],
        [('What did he say?', '他说了什么？'),
         ('She said she was tired.', '她说她累了。')],
    ),
    'tell': (
        [('tell sb a story', '给某人讲故事')],
        [('Please tell me the truth.', '请告诉我真相。'),
         ('He told me a funny story.', '他给我讲了个有趣的故事。')],
    ),
    'speak': (
        [('speak English', '说英语')],
        [('Can you speak English?', '你会说英语吗？'),
         ('Please speak more slowly.', '请说慢一点。')],
    ),
    'talk': (
        [('talk with sb', '和某人交谈')],
        [('I often talk with my friends.', '我常和朋友交谈。'),
         ("Let's talk about the plan.", '我们谈谈这个计划吧。')],
    ),
    'help': (
        [('help sb do sth', '帮助某人做某事'), ('with the help of', '在…帮助下')],
        [('Can you help me?', '你能帮我吗？'),
         ('Thank you for helping me.', '谢谢你帮我。')],
    ),
    # ---------------- 副词（非方式副词，模板不适用，人工给定） ----------------
    'actually': (
        [('actually, ...', '其实'), ('not actually', '并不真的')],
        [("Actually, I don't like it.", '其实我不喜欢它。'),
         ('He is actually very kind.', '他其实很善良。')],
    ),
    'again': (
        [('once again', '再一次'), ('again and again', '反复地')],
        [('Please say it again.', '请再说一遍。'),
         ('He tried again and again.', '他反复尝试。')],
    ),
    'ahead': (
        [('go ahead', '继续；请讲'), ('ahead of', '在…前面')],
        [('Go ahead, I am listening.', '继续说，我在听。'),
         ('There is a river ahead.', '前面有一条河。')],
    ),
    'alone': (
        [('live alone', '独自生活'), ('leave sb alone', '别打扰某人')],
        [('He lives alone.', '他独自生活。'),
         ('Leave me alone, please.', '请让我一个人待着。')],
    ),
    'already': (
        [('already done', '已经做完')],
        [('I have already finished it.', '我已经完成了。'),
         ("It is already ten o'clock.", '已经十点了。')],
    ),
    'always': (
        [('always do sth', '总是做某事'), ('as always', '一如既往')],
        [('She is always late.', '她总是迟到。'),
         ('I always get up early.', '我总是早起。')],
    ),
    'anyway': (
        [('anyway', '无论如何')],
        [("Anyway, let's try again.", '无论如何，我们再试一次。'),
         ("It's late, but I'll go anyway.", '很晚了，但我还是要去。')],
    ),
    'anywhere': (
        [('anywhere else', '其他任何地方')],
        [("I can't find it anywhere.", '我到处都找不到它。'),
         ('You can sit anywhere.', '你可以坐在任何地方。')],
    ),
    'apart': (
        [('apart from', '除…之外'), ('far apart', '相隔很远')],
        [('Apart from English, he also learns French.', '除英语外，他还学法语。'),
         ('The two houses are far apart.', '这两栋房子相隔很远。')],
    ),
    'ashore': (
        [('go ashore', '上岸')],
        [('The sailors went ashore.', '水手们上岸了。'),
         ('They swam ashore safely.', '他们安全地游到了岸上。')],
    ),
    'away': (
        [('far away', '很远'), ('go away', '走开')],
        [('The school is far away from here.', '学校离这里很远。'),
         ('Please go away.', '请走开。')],
    ),
    'back': (
        [('come back', '回来'), ('look back', '回头看')],
        [('He came back at six.', '他六点回来的。'),
         ('Please give the book back to me.', '请把书还给我。')],
    ),
    'besides': (
        [('besides that', '除此之外')],
        [('Besides English, she speaks French.', '除英语外，她还会说法语。'),
         ("I don't want to go; besides, it's raining.", '我不想去；况且，还在下雨。')],
    ),
    'certainly': (
        [('certainly not', '当然不')],
        [('Certainly, I will help you.', '当然，我会帮你。'),
         ('He will certainly come.', '他肯定会来。')],
    ),
    'else': (
        [('anything else', '其他东西'), ('someone else', '别人')],
        [('Do you want anything else?', '你还想要别的吗？'),
         ('What else can I do?', '我还能做什么？')],
    ),
    'especially': (
        [('especially in winter', '尤其在冬天')],
        [('I like fruit, especially apples.', '我喜欢水果，尤其是苹果。'),
         ('It is cold here, especially at night.', '这里很冷，尤其在晚上。')],
    ),
    'ever': (
        [('have you ever ...', '你曾…吗'), ('ever since', '自从')],
        [('Have you ever been to Beijing?', '你去过北京吗？'),
         ('It is the best film I have ever seen.', '这是我看过最好的电影。')],
    ),
    'everywhere': (
        [('everywhere in the world', '世界各地')],
        [('I looked for it everywhere.', '我到处找它。'),
         ('There is water everywhere.', '到处都是水。')],
    ),
    'exactly': (
        [('exactly right', '完全正确')],
        [('That is exactly what I mean.', '那正是我的意思。'),
         ("It is exactly six o'clock.", '现在正好六点。')],
    ),
    'finally': (
        [('finally, ...', '最后')],
        [('Finally, we got there.', '最后我们到了。'),
         ('He finally passed the exam.', '他终于通过了考试。')],
    ),
    'forward': (
        [('look forward to', '盼望'), ('move forward', '向前走')],
        [('I am looking forward to your letter.', '我盼望着你的来信。'),
         ('Please move forward.', '请向前走。')],
    ),
    'furthermore': (
        [('furthermore, ...', '此外')],
        [('Furthermore, it is cheap.', '此外，它还很便宜。'),
         ('He is kind; furthermore, he is clever.', '他善良；此外，他还聪明。')],
    ),
    'hardly': (
        [('hardly ever', '几乎从不')],
        [('I hardly know him.', '我几乎不认识他。'),
         ('He hardly speaks in class.', '他在课上几乎不说话。')],
    ),
    'hard': (
        [('work hard', '努力工作'), ('hard work', '艰苦的工作')],
        [('He works very hard.', '他工作非常努力。'),
         ('It is hard to say.', '这很难说。')],
    ),
    'how': (
        [('how are you', '你好吗'), ('how about', '…怎么样')],
        [('How do you go to school?', '你怎么去上学？'),
         ('How interesting the book is!', '这本书多有趣啊！')],
    ),
    'instead': (
        [('instead of', '代替；而不是')],
        [('He stayed at home instead.', '他相反留在了家里。'),
         ("Let's walk instead of taking a bus.", '我们走路而不是坐公交吧。')],
    ),
    'just': (
        [('just now', '刚才'), ('just a minute', '等一下')],
        [('I have just finished my homework.', '我刚做完作业。'),
         ('Just a minute, please.', '请等一下。')],
    ),
    'least': (
        [('at least', '至少'), ('the least', '最少')],
        [('At least ten people came.', '至少来了十个人。'),
         ('This is the least difficult one.', '这是最不难的一个。')],
    ),
    'left': (
        [('turn left', '向左转'), ('on the left', '在左边')],
        [('Turn left at the corner.', '在拐角处左转。'),
         ('The shop is on the left.', '商店在左边。')],
    ),
    'maybe': (
        [('maybe not', '也许不')],
        [('Maybe he is at home.', '也许他在家。'),
         ('Maybe we should wait.', '也许我们应该等等。')],
    ),
    'never': (
        [('never mind', '没关系'), ('never again', '再也不')],
        [('I never go to bed late.', '我从不晚睡。'),
         ('He has never been there.', '他从没去过那里。')],
    ),
    'nowadays': (
        [('nowadays', '如今')],
        [('Nowadays people use phones a lot.', '如今人们大量使用手机。'),
         ('Nowadays life is much easier.', '如今生活方便多了。')],
    ),
    "o'clock": (
        [("at six o'clock", '在六点')],
        [("It is eight o'clock now.", '现在八点了。'),
         ("I get up at six o'clock.", '我六点起床。')],
    ),
    'off': (
        [('turn off', '关掉'), ('get off', '下车')],
        [('Please turn off the light.', '请关灯。'),
         ('Get off the bus at the next stop.', '在下一站下车。')],
    ),
    'only': (
        [('only a few', '只有几个'), ('not only ... but also', '不仅…而且')],
        [('I have only one book.', '我只有一本书。'),
         ('He not only sings but also dances.', '他不仅唱歌还跳舞。')],
    ),
    'outside': (
        [('go outside', '出去'), ('outside the door', '在门外')],
        [('It is cold outside.', '外面很冷。'),
         ('The children are playing outside.', '孩子们在外面玩。')],
    ),
    'overnight': (
        [('stay overnight', '过夜')],
        [('We stayed there overnight.', '我们在那里过夜了。'),
         ('He became famous overnight.', '他一夜成名。')],
    ),
    'overseas': (
        [('study overseas', '留学海外'), ('overseas students', '海外学生')],
        [('She wants to study overseas.', '她想出国留学。'),
         ('Many overseas students come here.', '许多海外学生来到这里。')],
    ),
    'probably': (
        [('probably not', '大概不')],
        [('He will probably come.', '他大概会来。'),
         ('It is probably going to rain.', '大概要下雨了。')],
    ),
    'rather': (
        [('would rather', '宁愿'), ('rather than', '而不是')],
        [('I would rather stay at home.', '我宁愿待在家。'),
         ('He is rather tall.', '他相当高。')],
    ),
    'recently': (
        [('recently', '最近')],
        [('I have seen him recently.', '我最近见过他。'),
         ('Recently he has been very busy.', '最近他很忙。')],
    ),
    'right': (
        [('turn right', '向右转'), ('all right', '好；行')],
        [('Turn right at the corner.', '在拐角处右转。'),
         ('You are right.', '你是对的。')],
    ),
    'secondly': (
        [('secondly, ...', '第二')],
        [('Secondly, we must save time.', '第二，我们必须节省时间。'),
         ('Firstly he is kind; secondly he is clever.', '首先他善良；其次他聪明。')],
    ),
    'seldom': (
        [('seldom do sth', '很少做某事')],
        [('He seldom goes out at night.', '他很少晚上出门。'),
         ('I seldom eat meat.', '我很少吃肉。')],
    ),
    'simply': (
        [('simply put', '简单地说')],
        [('It is simply wonderful.', '它简直太棒了。'),
         ('He simply did not answer.', '他干脆没有回答。')],
    ),
    'somewhere': (
        [('somewhere else', '别的地方')],
        [('I left my key somewhere.', '我把钥匙落在某个地方了。'),
         ("Let's go somewhere quiet.", '我们去个安静的地方吧。')],
    ),
    'suddenly': (
        [('suddenly', '突然')],
        [('Suddenly it began to rain.', '突然下起雨来。'),
         ('The lights suddenly went out.', '灯突然灭了。')],
    ),
    'thankfully': (
        [('thankfully', '幸好')],
        [('Thankfully, nobody was hurt.', '幸好没人受伤。'),
         ('Thankfully, the rain stopped.', '幸好雨停了。')],
    ),
    'then': (
        [('then and now', '那时与现在'), ('and then', '然后')],
        [('We had lunch and then went home.', '我们吃了午饭然后回家了。'),
         ('Then he came in.', '然后他进来了。')],
    ),
    'there': (
        [('over there', '在那边'), ('here and there', '到处')],
        [('There is a park near my home.', '我家附近有个公园。'),
         ('Look over there!', '看那边！')],
    ),
    'though': (
        [('though', '不过')],
        [('It is small, though it is useful.', '它虽小，不过很有用。'),
         ("He said he would come; he didn't, though.", '他说会来；不过他没来。')],
    ),
    'together': (
        [('work together', '一起工作'), ('together with', '连同')],
        [('We study together every day.', '我们每天一起学习。'),
         ("Let's go together.", '我们一起走吧。')],
    ),
    'too': (
        [('too much', '太多'), ('too ... to ...', '太…以至于不能…')],
        [('The box is too heavy.', '这个箱子太重了。'),
         ('I like music, too.', '我也喜欢音乐。')],
    ),
    'totally': (
        [('totally different', '完全不同')],
        [('I totally agree with you.', '我完全同意你。'),
         ('It is totally wrong.', '这完全错了。')],
    ),
    'truly': (
        [('truly', '真正地')],
        [('I truly believe him.', '我真心相信他。'),
         ('He is a truly good man.', '他是个真正的好人。')],
    ),
    'twice': (
        [('twice a week', '每周两次')],
        [('I go swimming twice a week.', '我每周游泳两次。'),
         ('He called me twice.', '他给我打了两次电话。')],
    ),
    'up': (
        [('get up', '起床'), ('stand up', '起立')],
        [('I get up at six.', '我六点起床。'),
         ('Stand up, please.', '请起立。')],
    ),
    'usually': (
        [('usually', '通常'), ('as usual', '像平常一样')],
        [('I usually get up at seven.', '我通常七点起床。'),
         ('She is late as usual.', '她像平常一样迟到了。')],
    ),
    'very': (
        [('very good', '非常好'), ('very much', '非常')],
        [('This book is very interesting.', '这本书很有趣。'),
         ('Thank you very much.', '非常感谢。')],
    ),
    'west': (
        [('in the west', '在西方'), ('go west', '向西走')],
        [('The sun sets in the west.', '太阳从西方落下。'),
         ('They traveled west.', '他们向西旅行。')],
    ),
    'when': (
        [('when and where', '何时何地')],
        [('When do you get up?', '你什么时候起床？'),
         ('I was reading when he came.', '他来的时候我在看书。')],
    ),
    'where': (
        [('where to go', '去哪里')],
        [('Where is my pen?', '我的钢笔在哪？'),
         ('Where do you live?', '你住在哪里？')],
    ),
    'why': (
        [('why not', '为什么不')],
        [('Why are you late?', '你为什么迟到？'),
         ("Why not go with us?", '为什么不和我们一起去？')],
    ),
    'yet': (
        [('not yet', '还没有'), ('as yet', '到目前为止')],
        [('Have you finished yet?', '你做完了吗？'),
         ('He has not come yet.', '他还没来。')],
    ),
    'aboard': (
        [('go aboard', '上船/上飞机'), ('aboard the ship', '在船上')],
        [('All the passengers went aboard.', '所有乘客都上了船。'),
         ('Welcome aboard!', '欢迎登机/上船！')],
    ),
    # ---------------- 称谓 ----------------
    'mr': (
        [('Mr Green', '格林先生')],
        [('Mr Green is our English teacher.', '格林先生是我们的英语老师。'),
         ('Good morning, Mr Li.', '早上好，李先生。')],
    ),
    'mrs': (
        [('Mrs Brown', '布朗夫人')],
        [('Mrs Brown is very kind.', '布朗夫人很和善。'),
         ('This is Mrs Wang.', '这位是王女士。')],
    ),
    'ms': (
        [('Ms Li', '李女士')],
        [('Ms Li teaches us math.', '李女士教我们数学。'),
         ('Let me introduce Ms Zhao.', '让我介绍一下赵女士。')],
    ),
    'miss': (
        [('Miss Li', '李小姐'), ('miss the bus', '错过公交车')],
        [('Miss Li is our new teacher.', '李小姐是我们的新老师。'),
         ('Hurry up, or we will miss the train.', '快点，否则我们会错过火车。')],
    ),
    'sir': (
        [('Yes, sir.', '是的，先生。')],
        [('Good morning, sir.', '早上好，先生。'),
         ('Can I help you, sir?', '先生，需要帮忙吗？')],
    ),
}
