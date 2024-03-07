import datetime

gan = ["癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬"]
zhi = ["亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"]
kongw = ["戌亥", "子丑", "寅卯", "辰巳", "午未", "申酉"]
yaowei = ["初", "二", "三", "四", "五", "六"]

# 神煞的字典，按照此格式整理：索引0储存末尾，“亥”“癸”等等，查询时加 %；索引是卦序号g无妨
ric_god = {
    '驿马': ['巳', '寅', '亥', '申'], '桃花': ['子', '酉', '午', '卯'], '将星': ['卯', '子', '酉', '午'],
    '华盖': ['未', '辰', '丑', '戌'], '谋星': ['丑', '戌', '未', '辰']
}
h_god = {
    '*昼贵*': ['卯', '丑', '子', '亥', '亥', '丑', '子', '丑', '寅', '卯'],
    '*夜贵*': ['巳', '未', '申', '酉', '酉', '未', '申', '未', '午', '巳'],
    '飞符': ['戌', '巳', '辰', '卯', '寅', '丑', '午', '未', '申', '酉'],
    '文昌': ['卯', '巳', '午', '申', '酉', '申', '酉', '亥', '子', '寅'],
    '红艳': ['申', '午', '申', '寅', '未', '辰', '辰', '戌', '酉', '子']
}
yuel_god = {
    '天烛': ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'],
    '独火': ["午", "未", "申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳"],
    '天火': ['午', '卯', '子', '酉', '午', '卯', '子', '酉', '午', '卯', '子', '酉'],
    '霹雳': ['卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑', '寅'],
    '木狼': ['申', '寅', '申', '卯', '寅', '申', '丑', '戌', '辰', '子', '未', '戌'],
    '天河': ['丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子'],
    '退悔': ['戌', '戌', '戌', '未', '未', '未', '丑', '丑', '丑', '巳', '巳', '巳']

}
year_god = {
    '太阳': ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],
    '丧门': ["丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子"],
    '吊客': ["酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申"],
    '灾煞': ['酉', '午', '卯', '子', '酉', '午', '卯', '子', '酉', '午', '卯', '子'],
    '攀鞍': ["辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑", "寅", "卯"]
}
gua_god = {
    "卦身": ['巳', '午', '未', '申', '酉', '戌', '卯', '寅',
             '亥', '午', '丑', '寅', '酉', '辰', '卯', '申',
             '亥', '子', '未', '寅', '卯', '戌', '酉', '申',
             '巳', '子', '未', '申', '卯', '戌', '酉', '寅',
             '巳', '子', '丑', '申', '卯', '辰', '酉', '寅',
             '亥', '子', '丑', '寅', '卯', '辰', '酉', '申',
             '巳', '午', '丑', '申', '酉', '辰', '卯', '寅',
             '亥', '午', '未', '寅', '酉', '戌', '卯', '申'],
    "床帐": ['辰戌丑未', '辰戌丑未', '申酉', '亥子', '亥子', '申酉', '巳午',
             '巳午', '寅卯', '辰戌丑未', '申酉', '巳午', '亥子', '申酉', '巳午',
             '亥子', '寅卯', '寅卯', '申酉', '巳午', '巳午', '申酉', '亥子',
             '亥子', '辰戌丑未', '寅卯', '申酉', '亥子', '巳午', '申酉', '亥子',
             '巳午', '辰戌丑未', '寅卯', '申酉', '亥子', '巳午', '申酉', '亥子',
             '巳午', '寅卯', '寅卯', '申酉', '巳午', '巳午', '申酉', '亥子',
             '亥子', '辰戌丑未', '辰戌丑未', '申酉', '亥子', '亥子', '申酉', '巳午',
             '巳午', '寅卯', '辰戌丑未', '申酉', '巳午', '亥子', '申酉', '巳午', '亥子'],
    "香闺": ['申酉', '申酉', '亥子', '寅卯', '寅卯', '亥子', '辰戌丑未', '辰戌丑未', '巳午', '申酉', '亥子',
             '辰戌丑未', '寅卯', '亥子', '辰戌丑未', '寅卯', '巳午', '巳午', '亥子', '辰戌丑未', '辰戌丑未', '亥子',
             '寅卯', '寅卯', '申酉', '巳午', '亥子', '寅卯', '辰戌丑未', '亥子', '寅卯', '辰戌丑未', '申酉', '巳午',
             '亥子', '寅卯', '辰戌丑未', '亥子', '寅卯', '辰戌丑未', '巳午', '巳午', '亥子', '辰戌丑未', '辰戌丑未',
             '亥子', '寅卯', '寅卯', '申酉', '申酉', '亥子', '寅卯', '寅卯', '亥子', '辰戌丑未', '辰戌丑未', '巳午',
             '申酉', '亥子', '辰戌丑未', '寅卯', '亥子', '辰戌丑未', '寅卯']
}
merged_dict = {}

jieDATA = [
    [[12, 7, 17], [11, 8, 0], [10, 8, 21], [9, 8, 5], [8, 8, 2], [7, 7, 16], [6, 6, 6], [5, 6, 2], [4, 5, 9], [3, 6, 4],
     [2, 4, 10], [1, 6, 4]],  # 2023
    [[12, 6, 23], [11, 7, 6], [10, 8, 2], [9, 7, 11], [8, 7, 8], [7, 6, 22], [6, 5, 12], [5, 5, 8], [4, 4, 15],
     [3, 5, 10], [2, 4, 16], [1, 6, 4]],  # 2024
    [[12, 7, 5], [11, 7, 12], [10, 8, 8], [9, 7, 16], [8, 7, 13], [7, 7, 4], [6, 5, 17], [5, 5, 13], [4, 4, 20],
     [3, 5, 16], [2, 3, 22], [1, 5, 10]],  # 2025年内节气
    [[12, 7, 10], [11, 7, 17], [10, 8, 14], [9, 7, 22], [8, 7, 19], [7, 7, 9], [6, 5, 23], [5, 5, 19], [4, 5, 2],
     [3, 5, 21], [2, 4, 4], [1, 5, 16]],  # 2026年内节气
    [[12, 7, 16], [11, 7, 23], [10, 8, 20], [9, 8, 4], [8, 8, 1], [7, 7, 15], [6, 6, 5], [5, 6, 1], [4, 5, 8],
     [3, 6, 3], [2, 4, 9], [1, 5, 22]],  # 2027
    [[12, 6, 22], [11, 7, 5], [10, 8, 2], [9, 7, 10], [8, 7, 7], [7, 6, 21], [6, 5, 11], [5, 5, 7], [4, 4, 14],
     [3, 5, 9], [2, 4, 15], [1, 6, 3]],  # 2028
    [[12, 7, 4], [11, 7, 11], [10, 8, 7], [9, 7, 16], [8, 7, 13], [7, 7, 3], [6, 5, 17], [5, 5, 13], [4, 4, 19],
     [3, 5, 15], [2, 3, 21], [1, 5, 9]],  # 2029
    [[12, 7, 10], [11, 7, 17], [10, 8, 13], [9, 7, 21], [8, 7, 18], [7, 7, 8], [6, 5, 22], [5, 5, 18], [4, 5, 1],
     [3, 5, 21], [2, 4, 3], [1, 5, 15]],  # 2030
    [[12, 7, 16], [11, 7, 23], [10, 8, 19], [9, 8, 3], [8, 8, 0], [7, 7, 14], [6, 6, 4], [5, 6, 0], [4, 5, 7],
     [3, 6, 2], [2, 4, 8], [1, 5, 21]],
    [[12, 6, 21], [11, 7, 4], [10, 8, 1], [9, 7, 9], [8, 7, 6], [7, 6, 20], [6, 5, 10], [5, 5, 6], [4, 4, 13],
     [3, 5, 8], [2, 4, 14], [1, 6, 3]],
    [[12, 7, 3], [11, 7, 10], [10, 8, 7], [9, 7, 15], [8, 7, 12], [7, 7, 2], [6, 5, 16], [5, 5, 12], [4, 4, 19],
     [3, 5, 14], [2, 3, 20], [1, 5, 9]]  # 2033
]
# 【2033年12月31日，更新每年的节气】方法是在这个网站找节气表https:// jieqi.txcx.com/jieqi-2032.html，让chatgpt帮你整理：请你整理出节气的[month,day,hour]。https:// chat23.yqcloud.top/#/chat/1681893181723
gap = [[0, 1, -1, 0, 0, 1, 1, 2, 3, 3, 4, 4], [0, 1, 0, 1, 1, 2, 2, 3, 4, 4, 5, 5]]  # 1月1号转X月1号，闰年选[1]


def h_ric_calulate(Y, m, d, current_hour=12):
    start_date = datetime.datetime(2023, 3, 6)
    target_date = datetime.datetime(Y, m, d)
    days_diff = (target_date - start_date).days

    if (h := days_diff % 10) <= 0:
        h += 10
    if (ric := days_diff % 12) <= 0:
        ric += 12

    if current_hour == 23:  # 如果当前时间为 23 时
        h += 1
        ric += 1  # 则天干加一,日辰加一

    return h, ric


"""li = h_ric_calulate(2000,2,8)
print(gan[li[0]%10],zhi[li[1]%12])
li = h_ric_calulate(2023,11,12)
print(gan[li[0]%10],zhi[li[1]%12])"""


def get_time():
    # 获取当前时间
    currentTime = datetime.datetime.now()
    year = currentTime.year
    month = currentTime.month
    day = currentTime.day
    hour = currentTime.hour
    check_time = hour + day * 24 + month * 744
    yuel = 1

    # 日干支:h,ric
    h, ric = h_ric_calulate(year, month, day, hour)

    ric_h = ric - h
    empty = kongw[(ric_h % 12 + 12) % 12 // 2]

    # 计算当前时刻的地支（注意：月份、日子从上一年开始计算）
    hour = ((hour + 3) // 2) % 12

    # 计算当前月份的地支
    for i in range(12):
        t_standard = jieDATA[year - 2023][i][0] * 744 + jieDATA[year - 2023][i][1] * 24 + jieDATA[year - 2023][i][2]
        if check_time > t_standard:
            yuel = 13 - i
            break
        elif check_time == t_standard:
            yuel = 13 - i
            print("正在交节气，请勿摇卦")

        if i == 10:  # 如果循环结构运行到了第 12 轮，也就是循环了 12 个节气
            year = year - 1  # 则年份减一

    # 计算年份的干支
    yearg = (year - 3) % 10
    yearz = (year - 3) % 12
    ganStr = gan[yearg % 12]
    zhiStr2 = zhi[yearz % 12]

    # 输出结果
    time = ganStr + zhiStr2 + "年 " + zhi[yuel % 12] + "月 " + gan[h % 10] + zhi[ric % 12] + "日 " + zhi[
        hour] + "时（空亡：" + empty + "）"

    return yearg, yearz, yuel, h, ric, hour, empty, time


def changed_time(year, month, date):
    # 转换时间格式
    year = int(year)
    month = int(month)
    date = int(date)

    Monthzhi = 1

    # 计算当前月份的地支
    check_time = date * 24 + month * 744
    for i in range(12):
        t_standard = jieDATA[0][i][0] * 744 + jieDATA[0][i][1] * 24
        if check_time >= t_standard:
            Monthzhi = 13 - i
            break

        if i == 10:  # 如果循环结构运行到了第 12 轮，也就是循环了 12 个节气
            year = year - 1  # 则年份减一

    YganIdx = gan[(year + 7) % 10]
    YzhiIdx = zhi[(year - 3) % 12]
    Monthzhi = zhi[Monthzhi % 12]

    Date_li = h_ric_calulate(year, month, date)
    date = gan[Date_li[0] % 10] + zhi[Date_li[1] % 12]

    time = f"{YganIdx}{YzhiIdx}年 {Monthzhi}月 {date}日"
    return time


def input_time(richen_tiangan: int, input_Numberlist: list):
    # input_Numberlist传入了纯数字列表

    yearg = None
    yearz = None
    if len(input_Numberlist) == 2:
        yuel, richen = input_Numberlist
    elif len(input_Numberlist) == 3:
        yearz, yuel, richen = input_Numberlist
    elif len(input_Numberlist) == 4:
        yearg, yearz, yuel, richen = input_Numberlist
    else:
        richen = 0
        print("请输入正确的时间格式：yuel-ric；yearz-yuel-ric；yearg-yearz-yuel-ric")

    richen_tiangan_gap = richen - richen_tiangan
    empty = kongw[(richen_tiangan_gap % 12 + 12) % 12 // 2]

    format_time = zhi[yuel % 12] + "月 " + gan[richen_tiangan % 10] + zhi[richen % 12] + "日（空亡：" + empty + "）"
    if yearz is None and yearg is None:
        time = format_time
    elif yearz is not None and yearg is None:
        time = zhi[yearz % 12] + "年 " + format_time
    elif yearg is not None and yearz is not None:
        time = gan[yearg % 10] + zhi[yearz % 12] + "年 " + format_time

    return yearg, yearz, yuel, richen, empty, time


def append_dict(index, dict):
    """

    :param index:一般是给定的卦序号g，日辰ric及天干h，月令yuel，年yearz
    :param dict:
    :return:
    """
    for key, value in dict.items():
        if value[index] in merged_dict:
            merged_dict[value[index]].append(key)
        else:
            merged_dict[value[index]] = [key]


def search_god(g, h, ric, yuel, yearz):
    """

    :param g:卦序号
    :param h:
    :param ric:
    :param yuel:
    :param yearz:
    :return: 
    """
    global merged_dict
    # ordered_dict = {zhi[i]: merged_dict.get(zhi[i]) for i in range(len(zhi))}

    text = ''

    append_dict(ric % 4, ric_god)
    append_dict(h % 10, h_god)
    append_dict(yuel % 12, yuel_god)
    if yearz:
        append_dict(yearz % 12, year_god)

    ordered_dict = {key: merged_dict.get(key) for key in zhi if key in merged_dict}

    for key, value in ordered_dict.items():
        text += f"{key} - {','.join(value)} ;\n"  # merged_dict.items()的内容填充text

    for key, value in gua_god.items():
        text += f"{key} - {gua_god[key][g]};"

    # 恢复空字典
    merged_dict = {}

    return text


def get_ganzhi_date(year, month, day):
    start_date = datetime.datetime(2023, 7, 4)  # 起始日期
    target_date = datetime.datetime(year, month, day)
    days_diff = (target_date - start_date).days

    h = days_diff % 10  # + ((days_diff % 10) // 5)  # 日辰天干
    ric = days_diff % 12

    ganzhi_day = gan[h % 10] + zhi[ric % 12]

    return ganzhi_day


"""def get_time_old():
    # 获取当前时间
    currentTime = datetime.datetime.now()
    year = currentTime.year
    month = currentTime.month
    day = currentTime.day
    hour = currentTime.hour
    check_time = hour + day * 24 + month * 744
    yuel = 1
    h = 6
    ric = 8 - 6 * ((month + 1) % 2)  # 【每年更新1月1日的干支】

    # 计算当前时刻的地支（注意：月份、日子从上一年开始计算）
    zhiIndex = ((hour + 3) // 2) % 12

    # 计算当前月份的地支
    for i in range(12):
        t_standard = jieDATA[year - 2023][i][0] * 744 + jieDATA[year - 2023][i][1] * 24 + jieDATA[year - 2023][i][2]
        if check_time > t_standard:
            yuel = 13 - i
            break
        elif check_time == t_standard:
            yuel = 13 - i
            print("正在交节气，请勿摇卦")

        if i == 11:  # 如果循环结构运行到了第 12 轮，也就是循环了 12 个节气
            year = year - 1  # 则年份减一

    if hour == 23:  # 如果当前时间为 23 时
        h = h + 1
        ric = ric + 1  # 则天干加一,日辰加一

    # 计算年份的干支
    yearg = (year - 3) % 10
    yearz = (year - 3) % 12
    ganStr = gan[yearg]
    zhiStr2 = zhi[yearz]

    # 计算日干支
    h = (h + gap[(year % 4) // 4][month - 1] + day - 1) % 10
    ric = (ric + gap[(year % 4) // 4][month - 1] + day - 1) % 12
    if h == 0:
        h = 10
    ric_h = ric - h
    empty = kongw[(ric_h % 12 + 12) % 12 // 2]

    # 输出结果
    time = ganStr + zhiStr2 + "年 " + zhi[yuel] + "月 " + gan[h % 10] + zhi[ric] + "日 " + zhi[zhiIndex] + "时（空亡：" + \
           empty + "）"

    return yearg, yearz, yuel, h, ric, empty, time"""


def meihuatime():
    from lunardate import LunarDate
    import datetime
    # 获取当前日期
    current_date = datetime.date.today()
    current_hour = datetime.datetime.now().hour

    # 将当前日期转换为农历日期
    lunar_date = LunarDate.fromSolarDate(current_date.year, current_date.month, current_date.day)

    # 分别获取农历日期的年、月和日
    lunar_year = lunar_date.year
    lunar_month = lunar_date.month
    lunar_day = lunar_date.day
    lunar_hour = 1 if current_hour == 23 else (current_hour + 1) // 2 + 1

    # 输出农历日期及每个数字赋值给变量的结果
    print("农历时间：", lunar_month, '月', lunar_day, '日', zhi[lunar_hour % 12], '时')
    # 年月日相加之和
    year_num = (lunar_year - 2019) % 12
    year_num = 12 if year_num == 0 else year_num
    print("年月日的相加和：", UpNum := (year_num + lunar_month + lunar_day), '【', UpNum % 8, '】')
    print("年月日时的加和：", DownNum := (year_num + lunar_month + lunar_day + lunar_hour), '【', DownNum % 8, '】')
    print("动爻：【", DownNum % 6, '】')
    print('*' * 30 + '\n' + ' ' * 10 + '快捷键\n' + '*' * 30)
    print('Alt+Num_1:加载\nAlt+Num_2:保存\nAlt+Num_3:编辑备注csv\nAlt+Num_4:卦名起卦\nAlt+key_Q:复制卦象\nAlt+key_W:访问选中链接')


# 输入日期
currentTime = datetime.datetime.now()
formatted_time = currentTime.strftime("%Y-%m-%d %H:%M:%S")
year = currentTime.year
month = currentTime.month
day = currentTime.day
hour = currentTime.hour

# 查询干支历法日期
ganzhi_day = get_ganzhi_date(year, month, day)

print('*' * 30 + '\n' + ' ' * 10 + '时间信息\n' + '*' * 30)
print(f"公历日期：{formatted_time}")
print(f"干支历法日期：{ganzhi_day}日")
meihuatime()
