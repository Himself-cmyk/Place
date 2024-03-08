# -*- coding: utf-8 -*-
from gettime import get_time
from constants import GUA_NUM_TO_LIST
GAN = ["癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬"]
ZHI = ["亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"]
KONG_WANG = ["戌亥", "子丑", "寅卯", "辰巳", "午未", "申酉"]

"""处理排卦输入"""


def delimiter_method(str_li, revers=False) -> list:
    # 参数revers=False，默认只分割，不反转。
    # 参数revers = T，认为特殊符号可以反转列表。

    if str_li.isdigit():
        # 如果输入2位数，静卦序号
        if len(str_li) < 3:
            return [int(str_li)]

        # 如果输入6位数，硬币数数组
        li = [int(num) for num in str_li]
        if revers:
            li = list(reversed(li))
        return li

    delimiters = ["-", ",", "，", ".", " "]  # 多个分隔符

    for delimiter in delimiters:
        try:
            li = list(map(int, str_li.split(delimiter)))

            if all(isinstance(item, int) for item in li):

                if revers and delimiter == ".":
                    li = list(reversed(li))  # 反转列表li
                    # attach_textbox.insert(tk.END,f"{li}正确反转！")
                return li
        except ValueError:
            pass
    else:
        print(f"啥也识别不到，字符串是【{str_li}】。")


def main_input(coinsNumber_list_input: str, Time_input: str):
    # 填入的字符串粗处理，转列表
    if Time_input:
        if "月" in Time_input and "日" in Time_input:
            Time_input_list = lunar_Time_contains_MouthDay(Time_input)
        else:
            Time_input_list = delimiter_method(Time_input)
        if Time_input_list:
            Time_list, empty, time_Str = time_input_process(Time_input_list)
        else:
            print(Time_input_list, '⚠ Time_input 是不是出现错误？自动切换当前时间...')
            yearg, yearz, yuel, rigan, richen, hour, empty, time_Str = get_time()
            Time_list = [rigan, yuel, richen, yearg, yearz, hour]
    else:
        yearg, yearz, yuel, rigan, richen, hour, empty, time_Str = get_time()
        Time_list = [rigan, yuel, richen, yearg, yearz, hour]

    coinsNumber_list = delimiter_method(coinsNumber_list_input, revers=True)

    return Time_list, empty, time_Str, coinsNumber_list


def time_input_process(input_list: list):
    # 传入纯数字列表input_list

    yearg = None
    yearz = None
    hour = None
    length = len(input_list)

    if length == 3:
        rigan, yuel, richen = input_list
    elif length == 4:
        rigan, yuel, richen, yearz = input_list
    elif length == 5:
        rigan, yuel, richen, yearg, yearz = input_list
    elif length == 6:
        rigan, yuel, richen, yearg, yearz, hour = input_list
    else:
        richen = 0
        print("请输入正确的时间格式！日干，月令，日辰，年干，年支")

    richen = 10 if richen == 0 else richen
    time_list = [rigan, yuel, richen, yearg, yearz, hour]

    ric_gan_gap = richen - rigan
    empty = KONG_WANG[(ric_gan_gap % 12 + 12) % 12 // 2]

    format_time = f"{ZHI[yuel % 12]}月 " + f"{GAN[rigan % 10]}{ZHI[richen % 12]}日"
    if yearz is not None and yearg is None:
        format_time = f"{ZHI[yearz % 12]}年 " + format_time
    elif all(n is not None for n in [yearg, yearz]) and hour is None:
        format_time = f"{GAN[yearg % 10]}{ZHI[yearz % 12]}年 " + format_time
    elif all(n is not None for n in [yearg, yearz, hour]):
        format_time = f"{GAN[yearg % 10]}{ZHI[yearz % 12]}年 " + format_time + f" {ZHI[hour % 12]}时"
    time_Str = format_time + f"（空亡：{empty}）"

    return time_list, empty, time_Str


"""换算"""


def guaNum_to_coinsList(li: list[int]):
    """
    【卦名排卦】实现：卦名数 转 硬币数组
    :param li: 卦序号数组
    :return: 硬币数组
    """

    def num_to_coinsList(lis):
        # li有两个参数：主卦序号，变卦序号。
        # 返回原本的硬币数列表（六爻，五爻，。。。）
        gua_num, biangua_num = lis

        # 主卦阴阳爻列表，变卦阴阳爻列表
        gua_list, biangua_list = GUA_NUM_TO_LIST[gua_num], GUA_NUM_TO_LIST[biangua_num]

        coinsList = []
        for m, n in zip(gua_list, biangua_list):
            if m == n:
                coinsList.append(m)
            else:
                coinsList.append(3 if m == 1 else 0)

        return coinsList

    if (length := len(li)) == 2:
        coinsNumber_list = num_to_coinsList(li)
    elif length == 1:
        coinsNumber_list = list(GUA_NUM_TO_LIST[li[0]])
    elif length == 6:
        coinsNumber_list = li
    else:
        coinsNumber_list = [1, 1, 1, 1, 1, 1]
        print("***输入的硬币数好像有点问题？")
    return coinsNumber_list


"""文本识别 | 人性化"""
GUA_NAME = [
    '乾', '姤', '遁', '否', '观', '剥', '晋', '大有', '震', '豫', '解', '恒', '升', '井', '大过', '随',
    '坎', '节', '屯', '既济', '革', '丰', '明夷', '师', '巽', '小畜', '家人', '益', '无妄', '噬嗑', '颐', '蛊',
    '艮', '贲', '大畜', '损', '睽', '履', '中孚', '渐', '坤', '复', '临', '泰', '大壮', '夬', '需', '比',
    '离', '旅', '鼎', '未济', '蒙', '涣', '讼', '同人', '兑', '困', '萃', '咸', '蹇', '谦', '小过', '归妹']
GUA_NAMES = [
    '乾为天', '天风姤', '天山遁', '天地否', '风地观', '山地剥', '火地晋', '火天大有', '震为雷', '雷地豫', '雷水解',
    '雷风恒', '地风升', '水风井', '泽风大过', '泽雷随', '坎为水', '水泽节', '水雷屯', '水火既济', '泽火革', '雷火丰',
    '地火明夷', '地水师', '巽为风', '风天小畜', '风火家人', '风雷益', '天雷无妄', '火雷噬嗑', '山雷颐', '山风蛊',
    '艮为山', '山火贲', '山天大畜', '山泽损', '火泽睽', '天泽履', '风泽中孚', '风山渐', '坤为地', '地雷复', '地泽临',
    '地天泰', '雷天大壮', '泽天夬', '水天需', '水地比', '离为火', '火山旅', '火风鼎', '火水未济', '山水蒙', '风水涣',
    '天水讼', '天火同人', '兑为泽', '泽水困', '泽地萃', '泽山咸', '水山蹇', '地山谦', '雷山小过', '雷泽归妹', '空白']
# HuaJia60 = [
#     "甲子", "甲寅", "甲辰", "甲午", "甲申", "甲戌",#     "乙丑", "乙卯", "乙巳", "乙未", "乙酉", "乙亥",
#     "丙子", "丙寅", "丙辰", "丙午", "丙申", "丙戌",#     "丁丑", "丁卯", "丁巳", "丁未", "丁酉", "丁亥",
#     "戊子", "戊寅", "戊辰", "戊午", "戊申", "戊戌",#     "己丑", "己卯", "己巳", "己未", "己酉", "己亥",
#     "庚子", "庚寅", "庚辰", "庚午", "庚申", "庚戌",#     "辛丑", "辛卯", "辛巳", "辛未", "辛酉", "辛亥",
#     "壬子", "壬寅", "壬辰", "壬午", "壬申", "壬戌",#     "癸丑", "癸卯", "癸巳", "癸未", "癸酉", "癸亥"
# ]
HuaJia60 = [
    "癸亥", "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌",
    "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌",
    "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌",
    "己亥", "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌",
    "辛亥", "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌",
]


def replace_text_in_file(file_path, match_string):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()

        sign = match_string[-1]
        match_string = match_string[:-1]

        if match_string in content:
            if "(" in match_string:
                line_parts = match_string.split("(")
                numbers = line_parts[1][:-1].split("/")
            else:
                line_parts = [match_string, '']
                numbers = [0, 0]

            if sign == '+':
                numbers = [int(num) + 1 for num in numbers]
            elif sign == '-':
                numbers[-1] = int(numbers[-1]) + 1

            line_parts[1] = "/".join(map(str, numbers))
            updated_content = line_parts[0] + "(" + line_parts[1] + ")"

            content = content.replace(match_string, updated_content)

            file.seek(0)
            file.write(content)
            file.truncate()


def lunar_Time_contains_MouthDay(s):
    # 识别含有”时日月年“的中文字符
    def find_character(s, target, position: int = -1):
        # 查找目标字符在字符串中的位置
        idx = s.find(target)
        return s[idx + position] if idx > 0 else None

    num1 = GAN.index(find_character(s, "日", -2))
    num2 = ZHI.index(find_character(s, "月", -1))
    num3 = ZHI.index(find_character(s, "日", -1))
    num1 = num1 if num1 != 0 else 10
    num2 = num2 if num2 != 0 else 12
    num3 = num3 if num3 != 0 else 12

    time_li = [num1, num2, num3]  # 日干/月令/日辰

    if "年" in s:
        idx = s.index("年")  # 年干/年支
        if idx >= 2:
            num4 = GAN.index(s[idx - 2])
            time_li.append(num4)
        num5 = ZHI.index(s[idx - 1])
        time_li.append(num5)
        if "时" in s:
            num6 = ZHI.index(find_character(s, "时", -1))  # 时支
            time_li.append(num6)

    return time_li


def find_2char_index(s, search_dic=None):
    # 检查是否有卦象的繁体字/模糊字。遍历字典，繁体替换为简体
    if search_dic is None:
        search_dic = GUA_NAME
    import chardet  # 【定位】多余

    def has_traditional_chinese(text):
        result = chardet.detect(text.encode('utf-8'))
        return result['language'] == 'zh-Hant'

    if has_traditional_chinese(s):
        replace_map = {"離": "离", "濟": "济", "訟": "讼", "損": "损", "師": "师", "豐": "丰", "節": "节",
                       "觀": "观", "過": "过", "隨": "随", "蠱": "蛊", "頤": "颐", "復": "复", "臨": "临", "賁": "贲",
                       "謙": "谦", "渙": "涣", "漸": "渐", "歸": "归"}
        for old_word, new_word in replace_map.items():
            s = s.replace(old_word, new_word)

    mapping_dict = {"蓄": "畜", "遯": "遁"}

    for old_word, new_word in mapping_dict.items():
        s = s.replace(old_word, new_word)

    # 遍历卦名g，在字符串s找到查找【卦名g】的【索引位置i】。(i,g)保存在列表s_idxes中。按照i排序，key=ele[0]

    # 只能找到出现一次的，出现两次以上的被忽略了。
    # s_idxes = [(s.find(g), g) for g in search_dic if s.find(g) != -1]

    # 能找到出现两次以上的：
    def find_all_occurrences(search_string, matching_name):
        s_idxes = []
        start_idx = 0

        # 死循环search字符串search_string所有的matching_name
        while True:

            # 指定了字符串s找字符g的起始索引：start_idx；找不到就退出循环
            idx = search_string.find(matching_name, start_idx)
            if idx == -1:
                break

            # 准备查找string的下一个matching_name，update起始索引start_idx
            start_idx = idx + len(matching_name)

            # 八卦名+宫的string不算进去；防止出现：乾宫/坎宫被算进去
            try:
                if search_string[start_idx] != "宫":
                    s_idxes.append((idx, matching_name))
            except IndexError:
                pass

        return s_idxes

    s_idxes = []
    for g in search_dic:
        s_idxes.extend(find_all_occurrences(s, g))

    s_idxes.sort(key=lambda x: x[0])

    return s_idxes


def identify_GuaName(s, Exact_match=False):
    # GuaName_li[idx]为元组(s_idx,GuaName)

    # 能否的bug，识别出否卦来了
    s = s.replace("能否", "").replace("是否", "")
    s = s + '助'

    refer_lst = GUA_NAME
    if Exact_match:
        refer_lst = GUA_NAMES

    GuaName_li = find_2char_index(s, search_dic=refer_lst)

    if (length := len(GuaName_li)) == 1:
        # 卦名GuaName_li[0][1]在 卦名列表guaname 中的序号
        return str(refer_lst.index(GuaName_li[0][1]))
    elif length == 2:
        return str(refer_lst.index(GuaName_li[0][1])) + " " + str(refer_lst.index(GuaName_li[1][1]))

    elif length >= 3:
        # 找到相邻差距最小的两个数
        neibor_least_num = []
        mindiff = 100
        for i in range(len(GuaName_li) - 1):
            diff = GuaName_li[i + 1][0] - GuaName_li[i][0]
            if diff <= mindiff:
                mindiff = diff
                neibor_least_num = [GuaName_li[i], GuaName_li[i + 1]]  # 此为元组
        return str(refer_lst.index(neibor_least_num[0][1])) + " " + str(refer_lst.index(neibor_least_num[1][1]))
    """
    引用方法：
    s = identify_60HuaJia(indentify_string)
    if s:
        self.input2.setText(s)
    """


def identify_60HuaJia(s: str):
    # 本来就是有日月格式的
    if "月" in s and "日" in s:

        # 识别诸如：1997年3月9日
        import re
        pattern = r"(\d{4})年(\d{1,2})月(\d{1,2})日"

        if matches := re.search(pattern, s):
            year = matches.group(1)
            month = matches.group(2)
            day = matches.group(3)
            from gettime import changed_time
            result_string = changed_time(year, month, day)

            return result_string

    string = ''
    huajia_li = find_2char_index(s, search_dic=HuaJia60)
    # 传入对应得到花甲在HuaJia60的索引 组成的列表
    if (length := len(huajia_li)) >= 4:
        time_li = ['年', '月', '日', '时']
        for i in range(4):
            string += huajia_li[i][1] + time_li[i]
    elif length == 3:
        time_li = ['年', '月', '日']
        for i in range(length):
            string += huajia_li[i][1] + time_li[i]
    return string
    """
    引用方法：
    s = identify_60HuaJia(indentify_string)
    if s:
    # 识别不出来字体，就是空字符串；识别出来就整理好了
        self.input3.setText(s)
    """
