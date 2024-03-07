liuqin = [
    ["妻财亥水", "妻财子水", "兄弟丑土", "官鬼寅木", "官鬼卯木", "兄弟辰土", "父母巳火", "父母午火", "兄弟未土",
     "子孙申金", "子孙酉金", "兄弟戌土"],
    ["兄弟亥水", "兄弟子水", "官鬼丑土", "子孙寅木", "子孙卯木", "官鬼辰土", "妻财巳火", "妻财午火", "官鬼未土",
     "父母申金", "父母酉金", "官鬼戌土"],
    ["官鬼亥水", "官鬼子水", "子孙丑土", "父母寅木", "父母卯木", "子孙辰土", "兄弟巳火", "兄弟午火", "子孙未土",
     "妻财申金", "妻财酉金", "子孙戌土"],
    ["父母亥水", "父母子水", "妻财丑土", "兄弟寅木", "兄弟卯木", "妻财辰土", "子孙巳火", "子孙午火", "妻财未土",
     "官鬼申金", "官鬼酉金", "妻财戌土"],
    ["子孙亥水", "子孙子水", "父母丑土", "妻财寅木", "妻财卯木", "父母辰土", "官鬼巳火", "官鬼午火", "父母未土",
     "兄弟申金", "兄弟酉金", "父母戌土"]]
guashu = [
    [0, 11, 9, 7, 5, 3, 1], [1, 11, 9, 7, 10, 12, 2], [2, 11, 9, 7, 9, 7, 5], [3, 11, 9, 7, 4, 6, 8],
    [4, 4, 6, 8, 4, 6, 8], [5, 3, 1, 11, 4, 6, 8], [6, 6, 8, 10, 4, 6, 8], [7, 6, 8, 10, 5, 3, 1],
    [8, 11, 9, 7, 5, 3, 1], [9, 11, 9, 7, 4, 6, 8], [10, 11, 9, 7, 7, 5, 3], [11, 11, 9, 7, 10, 12, 2],
    [12, 10, 12, 2, 10, 12, 2], [13, 1, 11, 9, 10, 12, 2], [14, 8, 10, 12, 10, 12, 2], [15, 8, 10, 12, 5, 3, 1],
    [16, 1, 11, 9, 7, 5, 3], [17, 1, 11, 9, 2, 4, 6], [18, 1, 11, 9, 5, 3, 1], [19, 1, 11, 9, 12, 2, 4],
    [20, 8, 10, 12, 12, 2, 4], [21, 11, 9, 7, 12, 2, 4], [22, 10, 12, 2, 12, 2, 4], [23, 10, 12, 2, 7, 5, 3],
    [24, 4, 6, 8, 10, 12, 2], [25, 4, 6, 8, 5, 3, 1], [26, 4, 6, 8, 12, 2, 4], [27, 4, 6, 8, 5, 3, 1],
    [28, 11, 9, 7, 5, 3, 1], [29, 6, 8, 10, 5, 3, 1], [30, 3, 1, 11, 5, 3, 1], [31, 3, 1, 11, 10, 12, 2],
    [32, 3, 1, 11, 9, 7, 5], [33, 3, 1, 11, 12, 2, 4], [34, 3, 1, 11, 5, 3, 1], [35, 3, 1, 11, 2, 4, 6],
    [36, 6, 8, 10, 2, 4, 6], [37, 11, 9, 7, 2, 4, 6], [38, 4, 6, 8, 2, 4, 6], [39, 4, 6, 8, 9, 7, 5],
    [40, 10, 12, 2, 4, 6, 8], [41, 10, 12, 2, 5, 3, 1], [42, 10, 12, 2, 2, 4, 6], [43, 10, 12, 2, 5, 3, 1],
    [44, 11, 9, 7, 5, 3, 1], [45, 8, 10, 12, 5, 3, 1], [46, 1, 11, 9, 5, 3, 1], [47, 1, 11, 9, 4, 6, 8],
    [48, 6, 8, 10, 12, 2, 4], [49, 6, 8, 10, 9, 7, 5], [50, 6, 8, 10, 10, 12, 2], [51, 6, 8, 10, 7, 5, 3],
    [52, 3, 1, 11, 7, 5, 3], [53, 4, 6, 8, 7, 5, 3], [54, 11, 9, 7, 7, 5, 3], [55, 11, 9, 7, 12, 2, 4],
    [56, 8, 10, 12, 2, 4, 6], [57, 8, 10, 12, 7, 5, 3], [58, 8, 10, 12, 4, 6, 8], [59, 8, 10, 12, 9, 7, 5],
    [60, 1, 11, 9, 9, 7, 5], [61, 10, 12, 2, 9, 7, 5], [62, 11, 9, 7, 9, 7, 5],
    [63, 11, 9, 7, 2, 4, 6]]  # guashu,六爻在1，初爻在6.爻位对应的地支为：gua[g][7-yaowei]
sanhe_sanhui = {
    "<申酉戌>": [9, 10, 11], "<亥子丑>": [12, 1, 2], "<寅卯辰>": [3, 4, 5], "<巳午未>": [6, 7, 8],
    "<申子辰>": [9, 1, 5], "<亥卯未>": [12, 4, 8], "<寅午戌>": [3, 7, 11], "<巳酉丑>": [6, 10, 2]
}
select_shiyong = {"官鬼": ["考", "职", "丈夫", "男朋友"],
                  "妻财": ["妻子", "女朋友", "钱", "财", "赚", "失物", "收益", "涨", "价"],
                  "子孙": ["儿", "孙", "孩子", "养", "孕"], "兄弟": ["朋友", "兄", "弟", "姐", "妹"],
                  "父母": ["学业", "医院", "布", "成绩", "衣服", "爷", "父", "母", "舅", "姑", "姥"],
                  "世": ["身体", "自"], "应": ["这个", "对方", "此"]}
keyword = {
    "独发": "<独发>【！信息动爻】",
    '官鬼独发': '官鬼发动主忧虑，变爻来补充说明。',
    "父母独发": "父母独发克子孙，孩子健康出问题。子孙躲藏欲逃避。疾病在何处？初爻白虎脚见血。",
    '初爻一般': '临初爻，为心事、邻居、小口、事件开始。',
    '二爻一般': '临宅爻，为家宅、店铺，临父母发动主搬迁，临用神主在家。',
    '三爻一般': '临三爻，为心事、邻居、小口、事件开始。',
    '四爻一般': '临四爻，为心事、邻居、小口、事件开始。',
    '五爻一般': '临五爻，为尊、高傲。',
    '六爻一般': '临六爻，为国外外地、退位退缩闲置、事件结束。按身体断为头脑。',
    "暗动": "暗动生克。(！)何处有疾？有何疾？忌神爻位，日辰及返卦。世用返卦卦宫知疾病。何原因？何地点？忌神六亲六神知原因。",

    "日冲": "日冲为散，愈动。浮动，不稳定之象。临子孙为不高兴，临玄武为郁闷。",
    "月破": "【应期】用神月破，实破年月凶。忌神月破，当月不凶出月凶。",
    "伏吟": "伏吟主原地踏步，没有进展；多次XX没有成功。逢合主久。【测数字】重复数",
    "反吟": "反吟痛苦呻吟，主做事反复不成；情况时好时坏。【测数字】相反数、互补数",
    "水空": "水空则流，土动来克为堵塞，临勾陈为堵塞，临玄武为厕，临初爻为下水道，子孙为管道。",
    "三爻水空": "有肾结石，临勾陈为块状堵塞，临玄武为私密，临三爻为肾，辰土为水库。",
    "木动占": "<木动克土>木主痛痒，土为皮肤，外卦为表。二爻木为肠，三爻土为胃，六爻为头。初爻为地基，木化土主动土。\n土临白虎为皮肤，临青龙主痛，临朱雀为红，临玄武为溃烂。",
    "土动占": "<土动克水>土为鼻子，'寅'合'亥'为水的病地，返卦为艮，艮为鼻子。六爻为脸面，主鼻炎。若逢水空为水流堵塞。",
    "腾蛇": "性格行为古怪，孤僻。临元神为不安，被冲克更是。",
    "白虎": "性格暴躁，着急", "白虎水爻": "白虎水爻为血。",
    "白虎土爻": "白虎土爻为皮肤。临世用更是！",
    "白虎子孙": "白虎子孙为路，临三四爻为门前道路。为孩子有病，为丧夫。",
    "青龙": "青龙主家务日常",
    "朱雀": "朱雀主口舌，发炎发烧。",
    "勾陈": "勾陈主懒惰，迟钝。用神临勾陈，不动之象。",
    "勾陈六爻": "勾陈六爻，没有精神不想动。临用神为用。",

    "玄武": "玄武主郁闷压抑，心情不好，日月克尤甚。",
    "世用初爻空亡": "用神初爻空亡，腿脚无力。", "世用相冲": "世用相冲，无缘之象，发生争论口角。临兑宫为口舌。"

}  # 断语dict，引导用户思路

# shengke[yognshen_dizhi][ric or yuel -1],
shengke_cell = [['扶', '克', '不克', '不克', '克', '不克*', '不克', '克', '生', '生', '克', '扶'],  # 亥水 is yongshen
                ['扶', '克', '不克', '不克', '克', '不克', '不克*', '克', '生', '生', '克', '扶'],
                ['不克', '扶', '克', '克', '扶', '生', '生', '不克*', '不克', '不克', '扶', '不克'],
                ['生', '不克', '扶', '扶', '不克', '不克', '不克', '不克', '克', '克', '不克', '生'],
                ['生', '不克', '扶', '扶', '不克', '不克', '不克', '不克', '克', '克', '不克', '生'],
                ['不克', '扶', '克', '克', '扶', '生', '生', '扶', '不克', '不克', '不克*', '不克'],
                ['克', '不克', '生', '生', '不克', '扶', '扶', '不克', '不克', '不克', '不克', '克'],
                ['克', '不克', '生', '生', '不克', '扶', '扶', '不克', '不克', '不克', '不克', '克'],
                ['不克', '不克*', '克', '克', '扶', '生', '生', '扶', '不克', '不克', '扶', '不克'],
                ['不克', '生', '不克*', '不克', '生', '克', '克', '生', '扶', '扶', '生', '不克'],
                ['不克', '生', '不克', '不克*', '生', '克', '克', '生', '扶', '扶', '生', '不克'],
                ['不克', '扶', '克', '克', '不克*', '生', '生', '扶', '不克', '不克', '扶', '不克']]

animals = ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"]
wuxing = {
    "世用": ['水', '火', '木', '金', '土'],
    "元神": ['金', '木', '水', '土', '火'],
    "忌神": ['土', '水', '金', '火', '木'],
    "仇神": ['火', '金', '土', '木', '水']
}
gua_dict = {
    "1": "<乾宫>\n乾为骨、头、肺，为大肠，为老男人。",
    "2": "<震宫>\n震宫为闹市，为肝，肝藏魂藏血。",
    "3": "<坎宫>\n坎为耳，为水为尿，为精为血，为肾，为膀胱；为江河湖海。",
    "4": "<巽宫>\n巽为女人，为森林植物花草，巽为眼睛，为肠(下坎变地，辰变巳，返卦为巽)，为大腿为癌症。",
    "5": "<艮宫>\n艮为鼻子(五爻为五官，为胸为肺为呼吸系统，寅返卦)，为乳房，为脖子肩膀。",
    "6": "<坤宫>\n坤为地，脾胃，为老妇人。",
    "7": "<离宫>\n离为火、光、激光，离为眼睛(午返卦)，为血液，为中暑，为小肠。",
    "8": "<兑宫>\n兑为口腔、肺；为损坏、口语说话、声、进食；为20来岁少女、咳嗽、痰多。"
}  # 切片print(gua_dict["1"][5:])
gua_infor = [
    ['<五爻克宅>', '<五爻生宅>', '<宅爻克五>', '<宅爻克五>', '<五宅比和>', '<五爻克宅>', '<宅爻生五>', '<宅爻克五>',
     '<五爻克宅>',
     '<宅爻克五>', '<宅爻生五>', '<五爻生宅>', '<五宅比和>', '<五爻克宅>', '<五爻生宅>', '<五爻克宅>', '<五宅比和>',
     '<宅爻克五>',
     '<宅爻克五>', '<五宅比和>', '<宅爻生五>', '<宅爻生五>', '<宅爻克五>', '<宅爻克五>', '<宅爻克五>', '<宅爻生五>',
     '<五爻生宅>',
     '<宅爻生五>', '<五爻克宅>', '<宅爻克五>', '<五爻生宅>', '<五宅比和>', '<五爻克宅>', '<宅爻克五>', '<五爻生宅>',
     '<五爻生宅>',
     '<宅爻克五>', '<五爻克宅>', '<宅爻生五>', '<五宅比和>', '<五爻克宅>', '<五爻生宅>', '<五爻生宅>', '<五爻生宅>',
     '<五爻克宅>',
     '<五爻克宅>', '<宅爻克五>', '<宅爻生五>', '<五宅比和>', '<宅爻生五>', '<五爻克宅>', '<五宅比和>', '<宅爻克五>',
     '<五爻生宅>',
     '<宅爻生五>', '<宅爻生五>', '<五爻克宅>', '<宅爻生五>', '<宅爻克五>', '<宅爻克五>', '<宅爻生五>', '<五爻克宅>',
     '<宅爻克五>',
     '<五爻克宅>'],
    ['<世应比和>', '<应爻生世>', '<世爻克应>', '<世爻克应>', '<世应比和>', '<世爻克应>', '<应爻生世>', '<应爻生世>',
     '<世应比和>',
     '<应爻生世>', '<世爻生应>', '<应爻生世>', '<世应比和>', '<世爻克应>', '<应爻克世>', '<世应比和>', '<世爻克应>',
     '<世爻克应>',
     '<世爻克应>', '<世应比和>', '<世爻生应>', '<应爻生世>', '<应爻克世>', '<世爻克应>', '<应爻克世>', '<应爻克世>',
     '<应爻生世>',
     '<应爻克世>', '<应爻克世>', '<应爻克世>', '<世爻克应>', '<世爻克应>', '<应爻克世>', '<世爻克应>', '<应爻生世>',
     '<应爻克世>',
     '<应爻克世>', '<世爻克应>', '<应爻生世>', '<世爻克应>', '<世爻克应>', '<应爻克世>', '<应爻生世>', '<世爻生应>',
     '<应爻克世>',
     '<世爻克应>', '<世爻生应>', '<应爻生世>', '<应爻克世>', '<世爻生应>', '<应爻克世>', '<世应比和>', '<应爻克世>',
     '<世爻生应>',
     '<应爻生世>', '<应爻克世>', '<世应比和>', '<应爻生世>', '<世爻克应>', '<应爻生世>', '<应爻生世>', '<世爻克应>',
     '<世爻生应>',
     '<世应比和>'],
    ['<八卦纯阳>', '', '<八卦纯阳>', '', '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阳>', '', '<八卦纯阳>', '',
     '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阳>', '', '<八卦纯阳>', '', '<八卦纯阴>', '', '<八卦纯阴>', '',
     '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阳>', '', '<八卦纯阳>', '', '<八卦纯阳>', '', '<八卦纯阳>', '',
     '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阳>', '', '<八卦纯阳>', '',
     '<八卦纯阴>', '', '<八卦纯阴>', '', '<八卦纯阳>', '', '<八卦纯阳>', '', '<八卦纯阴>', '', '<八卦纯阴>', '',
     '<八卦纯阳>', '', '<八卦纯阳>', ''],
    ['', '', '', '', '', '', '', '<世应同宫>', '', '<世五同宫>', '', '<应二同宫>', '', '<世应同宫>', '', '', '', '', '',
     '<世五同宫>', '', '', '', '', '', '', '', '<世五同宫>', '', '', '', '<应初同宫>', '', '<应三同宫>', '',
     '<世应同宫>', '', '', '', '<世四同宫>', '', '<应二同宫>', '', '', '', '', '', '', '', '<世六同宫>', '',
     '<应二同宫>', '', '<世应同宫>', '', '<世应同宫>', '', '', '', '<世应同宫>', '', '', '', '']

]

# 世用五行，元神五行，忌神五行，仇神五行
number = [3, 4, 6, 7, 9, 10, 1, 12]

zhi = ["亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"]
yaowei = ["初", "二", "三", "四", "五", "六"]
word = ""
yongshen = ""


# 返回相冲地支数
def xiang_chong(dizhi):
    temp_dizhi = dizhi - 6 if dizhi > 6 else dizhi + 6
    return temp_dizhi


# 返回六合地支数
def liu_he(dizhi):
    temp_dizhi = 15 - dizhi if dizhi > 2 else 3 - dizhi
    return temp_dizhi  #


# 判断用神（str）是否空亡
def if_empty(empty, text, yongshen_name=None, text_list=None):
    """
    有“子”字，换成“子水”。否则和子孙混杂。
    yongshen非空：用神空亡？else用神化空亡？
    yongshen空：语句有空亡？
    """
    empty = ["子水" if e == "子" else e for e in list(empty)]

    if yongshen_name:
        if any((yongshen_name + e) in text for e in empty):
            return True
        else:
            if any(yongshen_name in line and any(e in line for e in empty) for line in text_list):
                return True

    else:
        if any(e in text for e in empty):
            return True

    return False


# 找忌神的五行，可能有点鸡肋？
def find_decrease(search):
    for index, value in enumerate(wuxing['忌神']):
        if search in value:
            return wuxing['世用'][index]
    return None


def zhugua(g, f, yuel, ric, a: list):
    text = ""
    for li in gua_infor:
        text += f"{li[g]}"  # 根据主卦的注释文字

    dizhi_lis = guashu[g][1:].copy()
    dizhi_lis.append(yuel)
    dizhi_lis.append(ric)
    for idx, fadong in enumerate(a):
        if fadong:
            bianyao = guashu[f][1 if idx == 0 else 7 - idx]
            dizhi_lis.append(bianyao)
    for key, value in sanhe_sanhui.items():
        if all(num in dizhi_lis for num in value):
            text += key  # 根据主卦、变卦、日月的三合三会

    print(text)


# 六神定位系统，直接找到六神所临的那一行
def search_animals(h1, h2, ric, yuel, l, l_total, empty, yongshen):
    # 遍历给定dict的key和value，返回word
    def search_dict_keys_values(dict, string_to_search, wd=""):
        for key in dict:
            if key in string_to_search:
                wd += dict[key] + "\n"
        wd = wd[:-1]
        return wd

    def search_turtle(string):
        turtle_dict = {
            "水": "[玄武水爻]，为厕、为下水道。",
            "子孙": "[玄武子孙]，玄武为偷盗、诈骗。",
            "兄弟": "[玄武兄弟]，厕所，同事偷偷。兄弟为同事，玄武为暗中、偷偷。",
        }
        wd = search_dict_keys_values(turtle_dict, string)

        if wd:
            print(wd)

    def search_tiger(string, ric, l_total):
        if h2 == 1:
            print("[白虎五爻]，主路上发生的事件，人在路途上，胸腔呼吸系统有病。")
        if "水" in string and ("丑土×" in l_total or ric == 8):
            print("【依据】丑土发动克白虎水爻，入墓元神，供血不好。", end="")
            print(keyword["白虎水爻"])
        if "土" in string and "世" in string:
            print(keyword["白虎土爻"])
        if "子孙" in string:
            print(keyword["白虎子孙"])

    def search_snake(string):
        snake_dict = {
            "金": "[腾蛇金爻]为虫象，淋巴，铁丝。蛊为虫象。若是酉金，返卦为兑，兑为口腔。",
            "土": "入墓在腾蛇，主不悦、牢狱之灾。螣蛇为神秘、害怕，入墓主被管教、被控制、受拘束。",
            "子孙": "[腾蛇子孙]，为艺术、技巧、手工工艺。丑寅返卦艮，是手工。辰巳，是电脑、直播自媒体。",
            "官鬼": "[腾蛇官鬼]，心神不宁，有忧虑或有大病。因何烦恼？两现、变爻为补充说明。金临用元神，日辰冲合丑土为用。",
            "空亡": "[腾蛇空亡]主心中不安。",
        }
        wd = search_dict_keys_values(snake_dict, string)

        if if_empty(empty, string):
            wd += snake_dict["空亡"]

        if wd:
            print(wd)

    def search_gouchen(string):
        gouchen_dict = {
            "世": "[勾陈]主阻塞，懒惰迟钝，建筑。用神临勾陈，不动之象。",
            "土": "入墓在勾陈，主牢狱之灾。",
            "子孙": "[勾陈子孙]，为公安；(在家)为迟钝的孩子。",
            "妻财": "[勾陈妻财]，为房产贷款，房屋毁坏。",
            "官鬼": "[勾陈官鬼]，为政府官员，管家家政。",
        }

        if h2 == 4:
            print(keyword['勾陈六爻'])

        word = search_dict_keys_values(gouchen_dict, string)
        if word:
            print(word)

    def search_zhuque(string):
        zhuque_dict = {
            "应": "[朱雀应爻]，不宜发动来克，犯小人，有人说坏话。",
            "金": "[朱雀金爻]，金临朱雀为声、说话，何人有声何六亲，何处有声寻爻位。",
            "辰土": "[朱雀辰土]，电脑设备。邻爻在旁边。",
            "官鬼": "[朱雀官鬼]，为口舌纷争。不宜月破，发动来克。在何爻何处有纷争。",
        }
        word = search_dict_keys_values(zhuque_dict, string)
        if word:
            print(word)

        '''找某个爻位，克的是什么五行***'''

    def search_dragon(string, guagong, yuel, empty, guaText):
        dragon_dict = {"木": "[青龙木爻]为书柜、衣柜。青龙为装饰。",
                       "官鬼": "[青龙官鬼]，政府官员，辐射忧虑问题。官鬼可断为男人，青龙为色，为饮食。",
                       "父母": "[青龙父母]，书刊杂志之象，父母的饮食，喜悦之文书结婚证。"}
        word = search_dict_keys_values(dragon_dict, string)
        if "子孙" in l[2] and h2 == 6:
            word += "[二爻子孙]二爻为胎爻，子孙为生殖器。"
        if word:
            print(word)

    search_turtle(l[(7 - h2) % 6])
    search_tiger(l[6 if h2 == 6 else 6 - h2], ric, l_total)
    search_snake(l[5 - h2 if h2 < 5 else (11 - h2) % 6])
    search_gouchen(l[4 - h2 if h2 < 4 else (10 - h2) % 6])
    search_zhuque(l[3 - h2 if h2 < 3 else (9 - h2) % 6])
    search_dragon(l[1 if h2 == 1 else (8 - h2) % 6], h1, yuel, empty, l_total)


def search_hide(g, h1):
    fucang = False
    word = ""
    for k in range(1, 5):
        num1 = number[2 * k - 2]
        num2 = number[2 * k - 1]

        if num1 not in guashu[g][1:7] and num2 not in guashu[g][1:7]:

            for i in range(1, 7):
                if num1 == guashu[g - g % 8][i]:
                    word += f"{liuqin[h1][num1]}伏藏在{yaowei[6 - i]}爻，"
                    fucang = True
                elif num2 == guashu[g - g % 8][i]:
                    word += f"{liuqin[h1][num2 % 12]}伏藏在{yaowei[6 - i]}爻，"
                    fucang = True
            if "妻财" in word:
                word += "妻财为饮食，食欲不旺！"
    if fucang:
        print(word[:-1] + "。")


# 给定世用的五行，能找元神是木、忌神、仇神的五行。用这个五行，在l_total搜。但是有点麻烦。
def yongshen_my_analy(yongshen, h1, l, yuel, ric):
    global yongshen_dizhi
    string = ""
    if yongshen:
        for i, value in enumerate(liuqin[h1]):
            if yongshen in value:
                yongshen_dizhi = i
                break
        try:
            word = shengke_cell[yongshen_dizhi][yuel - 1]
            word1 = shengke_cell[yongshen_dizhi][ric - 1]
        except UnboundLocalError:
            word = word1 = "未知"
            print("yongshen_dizhi未被赋值！")

        string += f"以{yongshen}为用神。用神月{word}日{word1}(！)，出现在"
        for i, elem in enumerate(l):
            if yongshen in elem:
                string += yaowei[i - 1] + "、"

        string = f"{string[:-1]}爻。"
    print(string)


def self_choose(gua_num,  wuxing, SixMode,):
    '''世爻的地支、世爻的爻位'''
    self_posit, _ = search_self_(gua_num=gua_num)
    self_dizhi = guashu[gua_num][7 - self_posit]

    string = animals[(self_posit + SixMode - 2) % 6]
    # 爻位 + h2六神模式 - 2 = 六神
    print("【反馈】")
    word = f"世爻{liuqin[wuxing][self_dizhi % 12]}在{yaowei[self_posit - 1]}爻临{string},{keyword[string]}"

    print(word)


def search_self_(gua_num: int):
    idx_to_selfposit = [6, 1, 2, 3, 4, 5, 4, 3]
    self_posit = idx_to_selfposit[gua_num % 8]
    other_posit = self_posit - 3 if self_posit > 3 else self_posit + 3
    return self_posit, other_posit


# 　标记和初步分析卦象
def check_analy(a, l, l_total, g, f, Guawx, h2, ric, yuel, empty, r_list, yearz):
    """
    功能：对每个地支逐行分析
    原理：for循环遍历guashu
    """
    anal_text = ''
    self_posit, other_posit = search_self_(gua_num=g)

    def role_add(text, dizhi):
        """
        功能：传递文本，加入role
        原理：根据卦宫，每个key对应某个地支value[h1]
        """

        muku = {
            "官鬼墓库": [8, -1, 5, 2, 11], "妻财墓库": [5, 11, 2, -1, 8], "子孙墓库": [2, 8, -1, 11, 5],
            "父母墓库": [11, 2, 8, 5, -1]  # ,"兄弟墓库": [-1, 5, 11, 8, 2]
        }
        for key, value in muku.items():
            if value[Guawx] == dizhi:
                text += f"<{key}>"

        taidi = [4, 10, 7, 1, 4]
        if taidi[Guawx % 5] == dizhi:
            text += "<子孙胎地>"
        return text

    kongwang = zhi.index(empty[0])
    wuxing_map = [[2, 5, 8, 11], [9, 10], [1, 12], [3, 4], [6, 7]]
    muku_map = []
    # shengke_map = []    # 生表，还可加入生克表
    dufa_bool = False
    if a[1] + a[2] + a[3] + a[4] + a[5] + a[0] == 1:
        dufa_bool = True

    print(gua_dict[f"{g // 8 + 1}"])  # 待处理，六冲游魂六合等说明

    '''先记录哈希表，有没有影响全局的地支出现'''
    for r in range(1, 7):
        temp_dizhi = guashu[g][r]  # 每次循环，temp_dizhi储存临时地支
        yao_wei = 7 - r

        """
        功能：土爻发动，由于判断入动墓
        原理：添加muku_map 和 shengke_map
        """
        if a[yao_wei % 6] or temp_dizhi == xiang_chong(ric):

            if temp_dizhi in wuxing_map[0]:
                muku_map.append((temp_dizhi + 1) // 3)
            # for i, value in enumerate(wuxing_map):
            #     if temp_dizhi in value:
            #         for item in wuxing_map[(i + 1) % 5]:
            #             shengke_map.append(item)

    for r in range(1, 7):

        temp_dizhi = guashu[g][r]  # temp_dizhi临时储存地支
        yao = liuqin[Guawx][temp_dizhi % 12]
        yao_wei = 7 - r  # 1-6 --> 初爻到六爻
        role = ","
        character = ""

        bianyao_dizhi = None
        if a[yao_wei % 6] == 1:

            bianyao_dizhi = guashu[f][r]
            bianyao = liuqin[Guawx][bianyao_dizhi % 12]
            # 变爻是不是土；是不是入墓
            if bianyao_dizhi in wuxing_map[0]:
                if temp_dizhi in wuxing_map[(bianyao_dizhi + 1) // 3]:  # 不是土爻发动，是否化墓
                    character += "<化墓>"
            if dufa_bool:
                character += "<独发>"

            if xiang_chong(ric) in [temp_dizhi, bianyao_dizhi]:
                character += "<日冲>"
            if ric % 12 + 1 in [temp_dizhi, bianyao_dizhi]:
                role += "<明日>"
            if yuel % 12 + 1 in [temp_dizhi, bianyao_dizhi]:
                role += "<次月>"
            if yearz and yearz % 12 + 1 == [temp_dizhi, bianyao_dizhi]:
                role += "<明年>"
            if bianyao_dizhi == xiang_chong(yuel):
                character += "<化月破>"
            if bianyao_dizhi in [kongwang, kongwang + 1]:
                character += "<化空亡>"
            # 到此为止
            role = role_add(role, bianyao_dizhi)

        '''入动墓、入日月墓，化墓上文提及'''
        for i in muku_map:
            if temp_dizhi in wuxing_map[i]:
                character += "<入墓>"
        for item in [[yuel, "<入月墓>"], [ric, "<入日墓>"]]:
            if item[0] in wuxing_map[0]:
                if temp_dizhi in wuxing_map[(item[0] + 1) // 3]:
                    character += item[1]

        '''动爻变爻是否临日辰月建、日月合、日月冲'''
        if ric in [temp_dizhi, bianyao_dizhi]:
            character += "<日辰>"
        if yuel in [temp_dizhi, bianyao_dizhi]:
            character += "<月建>"
        if temp_dizhi == liu_he(ric):
            if "父母" in liuqin[Guawx][ric % 12] + yao:  # 日合标签，找出六亲
                character += "<父母临日合>"
            else:
                character += "<日合>"
        if temp_dizhi == liu_he(yuel):
            character += "<月合>"
        if temp_dizhi == xiang_chong(ric):
            if a[yao_wei % 6] == 0:
                character += "<暗动>"
        if temp_dizhi == xiang_chong(yuel):
            character += "<月破>"
        if temp_dizhi in [kongwang, kongwang + 1]:
            character += "<空亡>"

        '''应爻是什么'''
        if yao_wei == other_posit:
            if "官鬼" in yao:
                role += '<官鬼临应>'

        role = role_add(role, temp_dizhi)
        '''打印character；如果role，word增加了文字，就打印；'''
        character = character if role == "," else character + role

        anal_text += character + "\n"

    return anal_text


# 分析卦象的主要系统
def analysis(l, l_total, g, f, h1, h2, ric, yuel, yearz, empty, r_list):
    # 根据余数
    idx_to_selfposit = [6, 1, 2, 3, 4, 5, 4, 3]
    self_posit = idx_to_selfposit[g % 8]
    other_posit = self_posit - 3 if self_posit > 3 else self_posit + 3
    a = [1 if r in [0, 3] else 0 for r in r_list]

    self_choose(g, f, h1, h2, self_posit, a[self_posit % 6])
    # return check_analy(a, l, l_total, g, f, h1, h2, ric, yuel, empty, r_list, yearz)

    """tiger = 6 if h2 == 6 else 6 - h2
    snake = 5 - h2 if h2 < 5 else 11 - h2
    gouchen = 4 - h2 if h2 < 4 else 10 - h2
    zhuque = 3 - h2 if h2 < 3 else 9 - h2
    dragon = 1 if h2 == 1 else 8 - h2"""
