/* 夢想方舟：船上的人物與動物設定
 *
 * 改這個檔就能換人、換台詞、換造型。
 * 也可以在網址最後加上 #edit，直接在頁面上點船員或業師換造型，再按「複製設定」把結果貼回這裡。
 *
 * 造型選項（look）
 *   body    人物外型：male-a、male-b、male-c、male-d、male-e、female-a、female-b、female-c、female-d、female-e
 *   hat     帽子：sailor 水手帽、captain 船長帽、cap 鴨舌帽、beret 貝雷帽、none 不戴
 *   shirt   上衣：stripe 藍白條紋、white 白襯衫、navy 深藍、charcoal 深灰外套、original 人物原本的衣服
 *   pants   褲子：navy 深藍、charcoal 深灰、original 人物原本的褲子
 *   glasses 眼鏡：true 或 false
 *
 * 船員的 deck 是平常活動的甲板：TOP 上甲板、A 訓練甲板、B 應用甲板、C 實戰甲板
 * 業師的 cabin 是平常待的艙房：training、skills、mentors、vp-studio、theater、cowork、industry、boarding、contact
 */
window.ARK_ROSTER = {
  guide: {
    name: '大副（姓名待填）', role: '巡艙導覽', line: '跟我來，從艦橋開始逛！',
    look: {body: 'male-c', hat: 'captain', shirt: 'white', pants: 'navy', glasses: false}
  },
  staff: [
    {type: 'crew', name: '產策成員 1（姓名待填）', role: '職稱待填', line: '歡迎登上夢想方舟！（台詞待填）', deck: 'TOP',
     look: {body: 'female-a', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: false}},
    {type: 'crew', name: '產策成員 2（姓名待填）', role: '職稱待填', line: '想上什麼課，問我就對了。（台詞待填）', deck: 'TOP',
     look: {body: 'male-b', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: false}},
    {type: 'crew', name: '產策成員 3（姓名待填）', role: '職稱待填', line: '訓練甲板今天也很熱鬧。（台詞待填）', deck: 'A',
     look: {body: 'female-d', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: true}},
    {type: 'crew', name: '產策成員 4（姓名待填）', role: '職稱待填', line: '攝影棚排好時段了。（台詞待填）', deck: 'B',
     look: {body: 'male-e', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: false}},
    {type: 'crew', name: '產策成員 5（姓名待填）', role: '職稱待填', line: '報名的事可以來通訊艙找我。（台詞待填）', deck: 'C',
     look: {body: 'female-c', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: false}},
    {type: 'crew', name: '產策成員 6（姓名待填）', role: '職稱待填', line: '業界專案都在實戰甲板。（台詞待填）', deck: 'C',
     look: {body: 'male-a', hat: 'sailor', shirt: 'stripe', pants: 'navy', glasses: false}},

    {type: 'mentor', name: '業師 1（姓名待填）', role: '專長待填', line: '作品先做出來，我們再一起修。（台詞待填）', cabin: 'mentors',
     look: {body: 'male-d', hat: 'none', shirt: 'charcoal', pants: 'charcoal', glasses: true}},
    {type: 'mentor', name: '業師 2（姓名待填）', role: '專長待填', line: '引擎打開，我示範一次。（台詞待填）', cabin: 'training',
     look: {body: 'female-b', hat: 'beret', shirt: 'charcoal', pants: 'charcoal', glasses: false}},
    {type: 'mentor', name: '業師 3（姓名待填）', role: '專長待填', line: '燈光打對，畫面就活了。（台詞待填）', cabin: 'skills',
     look: {body: 'male-a', hat: 'cap', shirt: 'charcoal', pants: 'original', glasses: true}},
    {type: 'mentor', name: '業師 4（姓名待填）', role: '專長待填', line: '上棚之前先對好鏡頭。（台詞待填）', cabin: 'vp-studio',
     look: {body: 'female-e', hat: 'none', shirt: 'charcoal', pants: 'charcoal', glasses: true}}
  ]
};

/* 網站訪客可以選的動物，每一種代表一項技能（技能來自 CG ARK 官方頁面）。
 * animal 可選：beaver 海狸、bunny 兔子、giraffe 長頸鹿、fox 狐狸、parrot 鸚鵡、elephant 大象、monkey 猴子 */
window.ARK_SKILLS = [
  {id: 'modeling',  skill: '3D 建模',  animal: 'beaver',   name: '海狸',   why: '天生愛動手蓋東西', line: '一起來蓋模型！'},
  {id: 'animation', skill: '動畫',     animal: 'bunny',    name: '兔子',   why: '一刻都靜不下來',   line: '動起來才好玩！'},
  {id: 'lighting',  skill: '燈光',     animal: 'giraffe',  name: '長頸鹿', why: '離燈最近',         line: '這顆燈再高一點。'},
  {id: 'vfx',       skill: '視覺特效', animal: 'fox',      name: '狐狸',   why: '最會變魔術',       line: '看我變出一團火！'},
  {id: 'concept',   skill: '概念設計', animal: 'parrot',   name: '鸚鵡',   why: '滿腦子鮮豔的點子', line: '我畫給你看！'},
  {id: 'vp',        skill: '虛擬製作', animal: 'elephant', name: '大象',   why: '撐得起整座攝影棚', line: 'LED 牆開起來！'},
  {id: 'game',      skill: '遊戲開發', animal: 'monkey',   name: '猴子',   why: '最愛玩也最會玩',   line: '再玩一場就好！'}
];

/* 其他一起搭船的動物（成對出現） */
window.ARK_EXTRA_ANIMALS = [
  {animal: 'cow', name: '乳牛', line: '哞～'},
  {animal: 'panda', name: '熊貓', line: '船上有竹子嗎？'},
  {animal: 'penguin', name: '企鵝', line: '甲板好滑！'}
];
