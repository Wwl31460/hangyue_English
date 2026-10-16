// 年级阶段（人教版）：小学3年级起 → 高中三年级，每学期一个阶段
// 点开图标进入该阶段单词学习；每页都有返回按钮。

export type SectionKey = '小学' | '初中' | '高中';

export interface GradeStage {
  id: string;
  label: string; // 小学三年级上册
  short: string; // 3上
  emoji: string; // 阶段图标
  section: SectionKey;
}

export const grades: GradeStage[] = [
  // ===== 小学（三年级起）=====
  { id: 'g3s1', label: '小学三年级上册', short: '3上', emoji: '📘', section: '小学' },
  { id: 'g3s2', label: '小学三年级下册', short: '3下', emoji: '📗', section: '小学' },
  { id: 'g4s1', label: '小学四年级上册', short: '4上', emoji: '📙', section: '小学' },
  { id: 'g4s2', label: '小学四年级下册', short: '4下', emoji: '📕', section: '小学' },
  { id: 'g5s1', label: '小学五年级上册', short: '5上', emoji: '📔', section: '小学' },
  { id: 'g5s2', label: '小学五年级下册', short: '5下', emoji: '📓', section: '小学' },
  { id: 'g6s1', label: '小学六年级上册', short: '6上', emoji: '📒', section: '小学' },
  { id: 'g6s2', label: '小学六年级下册', short: '6下', emoji: '📚', section: '小学' },
  // ===== 初中（七年级起）=====
  { id: 'c7s1', label: '初中七年级上册', short: '7上', emoji: '🔤', section: '初中' },
  { id: 'c7s2', label: '初中七年级下册', short: '7下', emoji: '🔡', section: '初中' },
  { id: 'c8s1', label: '初中八年级上册', short: '8上', emoji: '🅰️', section: '初中' },
  { id: 'c8s2', label: '初中八年级下册', short: '8下', emoji: '🆎', section: '初中' },
  { id: 'c9s1', label: '初中九年级上册', short: '9上', emoji: '🆑', section: '初中' },
  { id: 'c9s2', label: '初中九年级下册', short: '9下', emoji: '🆔', section: '初中' },
  // ===== 高中 =====
  { id: 'h1s1', label: '高中一年级上册', short: '高一上', emoji: '🎓', section: '高中' },
  { id: 'h1s2', label: '高中一年级下册', short: '高一下', emoji: '🏫', section: '高中' },
  { id: 'h2s1', label: '高中二年级上册', short: '高二上', emoji: '📐', section: '高中' },
  { id: 'h2s2', label: '高中二年级下册', short: '高二下', emoji: '📊', section: '高中' },
  { id: 'h3s1', label: '高中三年级上册', short: '高三上', emoji: '📈', section: '高中' },
  { id: 'h3s2', label: '高中三年级下册', short: '高三下', emoji: '🏆', section: '高中' },
];

export const gradeById: Record<string, GradeStage> = Object.fromEntries(
  grades.map((g) => [g.id, g]),
);

// 各年级真实单元标题（人教版）：unit 编号 -> 标题。点单元时显示真实课题名。
export const unitTitles: Record<string, Record<number, string>> = {
  // ===== 小学（人教版 PEP）=====
  g3s1: {
    1: 'U1 Hello!', 2: 'U2 Colours', 3: 'U3 Look at me!', 4: 'U4 We love animals',
    5: 'U5 Let\'s eat', 6: 'U6 Happy birthday!', 7: 'U7 Revision',
  },
  g3s2: {
    1: 'U1 Welcome back to school!', 2: 'U2 My family', 3: 'U3 At the zoo', 4: 'U4 Where is my car?',
    5: 'U5 Do you like pears?', 6: 'U6 How many?',
  },
  g4s1: {
    1: 'U1 My classroom', 2: 'U2 My schoolbag', 3: 'U3 My friends', 4: 'U4 My home',
    5: "U5 Dinner's ready", 6: 'U6 Meet my family',
  },
  g4s2: {
    1: 'U1 My school', 2: 'U2 What time is it?', 3: 'U3 Weather', 4: 'U4 At the farm',
    5: 'U5 My clothes', 6: 'U6 Shopping',
  },
  g5s1: {
    1: "U1 What's he like?", 2: 'U2 My week', 3: 'U3 What would you like?', 4: 'U4 What can you do?',
    5: 'U5 There is a big bed', 6: 'U6 In a nature park',
  },
  g5s2: {
    1: 'U1 This is my day', 2: 'U2 My favourite season', 3: 'U3 My school calendar', 4: 'U4 When is Easter?',
    5: 'U5 Whose dog is it?', 6: 'U6 Work quietly',
  },
  g6s1: {
    1: 'U1 How can I get there?', 2: 'U2 Ways to go to school', 3: 'U3 My weekend plan', 4: 'U4 I have a pen pal',
    5: 'U5 What does he do?', 6: 'U6 How do you feel?',
  },
  g6s2: {
    1: 'U1 How tall are you?', 2: 'U2 Last weekend', 3: 'U3 Where did you go?', 4: 'U4 Then and now',
  },
  // ===== 初中（Go for it!）=====
  c7s1: {
    1: 'Starter 1 Good morning!', 2: 'Starter 2 What\'s this in English?', 3: 'Starter 3 What color is it?',
    4: 'U1 My name\'s Gina.', 5: 'U2 This is my sister.', 6: 'U3 Is this your pencil?',
    7: 'U4 Where\'s my schoolbag?', 8: 'U5 Do you have a soccer ball?', 9: 'U6 Do you like bananas?',
    10: 'U7 How much are these socks?', 11: 'U8 When is your birthday?', 12: 'U9 My favorite subject is science.',
  },
  c7s2: {
    1: 'U1 Can you play the guitar?', 2: 'U2 What time do you go to school?', 3: 'U3 How do you get to school?',
    4: 'U4 Don\'t eat in class.', 5: 'U5 Why do you like pandas?', 6: 'U6 I\'m watching TV.',
    7: 'U7 It\'s raining!', 8: 'U8 Is there a post office near here?', 9: 'U9 What does he look like?',
    10: 'U10 I\'d like some noodles.', 11: 'U11 How was your school trip?', 12: 'U12 What did you do last weekend?',
  },
  c8s1: {
    1: 'U1 Where did you go on vacation?', 2: 'U2 How often do you exercise?', 3: 'U3 I\'m more outgoing than my sister.',
    4: 'U4 What\'s the best movie theater?', 5: 'U5 Do you want to watch a game show?', 6: 'U6 I\'m going to study computer science.',
    7: 'U7 Will people have robots?', 8: 'U8 How do you make a banana milk shake?', 9: 'U9 Can you come to my party?',
    10: 'U10 If you go to the party, you\'ll have a great time!',
  },
  c8s2: {
    1: 'U1 What\'s the matter?', 2: 'U2 I\'ll help to clean up the city parks.', 3: 'U3 Could you please clean your room?',
    4: 'U4 Why don\'t you talk to your parents?', 5: 'U5 What were you doing when the rainstorm came?', 6: 'U6 An old man tried to move the mountains.',
    7: 'U7 What\'s the highest mountain in the world?', 8: 'U8 Have you read Treasure Island yet?', 9: 'U9 Have you ever been to a museum?',
    10: 'U10 I\'ve had this bike for three years.',
  },
  c9s1: {
    1: 'U1 How can we become good learners?', 2: 'U2 I think that mooncakes are delicious!', 3: 'U3 Could you please tell me where the restrooms are?',
    4: 'U4 I used to be afraid of the dark.', 5: 'U5 What are the shirts made of?', 6: 'U6 When was it invented?',
    7: 'U7 Teenagers should be allowed to choose their own clothes.',
  },
  c9s2: {
    1: 'U8 It must belong to Carla.', 2: 'U9 I like music that I can dance to.', 3: 'U10 You\'re supposed to shake hands.',
    4: 'U11 Sad movies make me cry.', 5: 'U12 Life is full of the unexpected.', 6: 'U13 We\'re trying to save the earth!',
    7: 'U14 I remember meeting all of you in Grade 7.',
  },
  // ===== 高中（人教版 必修/选必）=====
  h1s1: {
    0: 'Welcome Unit', 1: 'U1 Teenage Life', 2: 'U2 Travelling Around', 3: 'U3 Sports and Fitness',
    4: 'U4 Natural Disasters', 5: 'U5 Languages Around the World',
  },
  h1s2: {
    1: 'U1 Cultural Heritage', 2: 'U2 Wildlife Protection', 3: 'U3 The Internet', 4: 'U4 History and Traditions', 5: 'U5 Music',
  },
  h2s1: {
    1: 'U1 Festivals and Celebrations', 2: 'U2 Morals and Virtues', 3: 'U3 Diverse Cultures', 4: 'U4 Space Exploration', 5: 'U5 The Value of Money',
  },
  h2s2: {
    1: 'U1 People of Achievement', 2: 'U2 Looking into the Future', 3: 'U3 Fascinating Parks', 4: 'U4 Body Language', 5: 'U5 Working the Land',
  },
  h3s1: {
    1: 'U1 Science and Scientists', 2: 'U2 Bridging Cultures', 3: 'U3 Food and Culture', 4: 'U4 Journey Across a Vast Land', 5: 'U5 First Aid',
  },
  h3s2: {
    1: 'U1 Art', 2: 'U2 Healthy Lifestyle', 3: 'U3 Environmental Protection', 4: 'U4 Adversity and Courage', 5: 'U5 Poems',
  },
};
