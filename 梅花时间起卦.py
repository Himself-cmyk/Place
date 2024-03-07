from lunardate import LunarDate



def meihuatime():
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

    # 输出农历日期及每个数字赋值给变量的结果
    print("农历时间：", lunar_year, lunar_month, lunar_day,current_hour)

    print("当前时辰：", lunar_hour := 1 if current_hour == 23 else (current_hour+1) // 2 + 1)
    # 年月日相加之和
    year_num = (lunar_year - 2019) % 12
    year_num = 12 if year_num == 0 else year_num

    print("年月日相加之和：", UpNum := (year_num + lunar_month + lunar_day), UpNum % 8)
    print("年月日相加之和：", DownNum := (year_num + lunar_month + lunar_day + lunar_hour), DownNum % 8)
    print("动爻：", DownNum % 6)

def path():
    import os
    import lunardate
    print(os.path.dirname(lunardate.__file__))
meihuatime()
path()