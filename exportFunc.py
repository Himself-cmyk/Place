import csv
import openpyxl
import os
from constants import GAN, ZHI, GUA_NUM_TO_LIST, GUA_SHU

text = """
占题：神奇的示例
甲辰年 寅月 庚申日 申时（空亡：子丑）
火雷噬嗑 (巽宫)   震为雷 (震宫,六冲)
腾蛇   子孙巳火○    妻财戌土″
勾陈   妻财未土″世
朱雀   官鬼酉金′  
青龙   妻财辰土″  
玄武   兄弟寅木″应
白虎   父母子水′  
"""

"""
value:

定义嵌套列表
nested_list = [
    ['占题：今日所看柯南剧集'],
    ['甲辰年', '寅月', '乙卯日', '申时（空亡：子丑）'],
    ['山泽损', '(艮宫)', '山风蛊', '(巽宫，归魂)'],
    ['玄武', '', '官鬼寅木′应'],
    ['白虎', '', '妻财子水″'],
    ['腾蛇', '', '兄弟戌土″'],
    ['勾陈', '子孙申金', '兄弟丑土×世', '子孙酉金′'],
    ['朱雀', '', '官鬼卯木′'],
    ['青龙', '', '父母巳火○', '兄弟丑土″']
]
lst[3:]:
[['玄武', '官鬼寅木′应'], ['白虎', '妻财子水″'], ['腾蛇', '兄弟戌土″'], ['勾陈', '子孙申金', '兄弟丑土×世', '子孙酉金′'], ['朱雀', '官鬼卯木′'], ['青龙', '父母巳火○', '兄弟丑土″']]

li in lst[3:]:
['腾蛇', '兄弟戌土″']

li[1]:
'兄弟戌土″'

any(sign in li[1] for sign in "′″×○")
"""


def handle_text2nested_lst(text: str) -> list[list[str]]:
    def If_cent():
        缩进 = False
        for li in nested_lst[3:]:
            if all(sign not in li[1] for sign in "′″×○"):
                缩进 = True
                break
        # print('需要缩进？', 缩进)
        return 缩进

    lines = [l for l in text.split('\n') if l]
    nested_lst = [[lines[0]]]
    for line in lines[1:]:
        lst = [n for n in line.split(' ') if n]
        nested_lst.append(lst)

    if not If_cent():  # 不需要缩进，直接返回结果
        return nested_lst

    for i in range(3, 9):  # 需要缩进，再处理一下
        if any(sign in nested_lst[i][1] for sign in "′″×○"):
            nested_lst[i] = [nested_lst[i][0], ''] + nested_lst[i][1:]

    return nested_lst


def handle_args(*args: str):
    text_content = ""
    # 将所有的输入字符串写入文档
    for text in args:
        if text == "" or not isinstance(text, str):
            continue
        text_content += text + "\n"

    # 将文档保存到 output 文件夹中
    filename = args[0].split('\n')[0].split('：')[1]  # 第一个参数 是 卦象文字，第一个换行 之后全部掐掉，第一个中文冒号 之前全部掐掉
    return text_content, filename.strip()


def write_as_csv(nested_list: list[list[str]]):
    # 打开CSV文件
    with open('../排盘结果.csv', 'w', newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)

        # 将第一行数据写入CSV文件
        writer.writerow(nested_list[0])

        # 遍历嵌套列表的剩余部分
        for sub_list in nested_list[1:]:
            writer.writerow(sub_list)

    # print('CSV文件已生成。')


def write_as_xlsx(nested_list: list[list[str]], file_name=None):
    # 创建一个新的工作簿
    wb = openpyxl.Workbook()

    # 选择现有的工作表或创建一个新的工作表
    ws = wb.active
    if ws.title == "Sheet":  # 如果默认工作表名称为"Sheet"，则更改标题
        ws.title = "排盘结果"

    # 写入数据
    for sub_list in nested_list:
        ws.append([''] * 5 + sub_list)

    # 保存文件
    if file_name is None:
        file_name = '排盘结果'
    wb.save(f'output/{file_name}.xlsx')
    return f'文档已保存为 “output/{file_name}.xlsx”'  # 返回一段message:str


def pathExistCheck(path='output'):
    # 检查本目录下是否有output文件夹，没有的话创建
    if not os.path.exists(path):
        os.mkdir(path)


def convert_text_to_xlsx(handle_txt: str, file_name: str = None) -> str:
    """
    输入特定格式的排盘文字handle_txt，自动转化和输出xlsx
    最后返回一段message:str
    """
    pathExistCheck()
    nested_lst = handle_text2nested_lst(handle_txt)
    message = write_as_xlsx(nested_lst, file_name)
    return message


def write_as_txt(*args: str) -> str:
    """
    输入任意n段str，经过中间步骤合成整段的text_content，以及生成filename，输出为output下的txt文档。
    最后返回一段message:str
    """
    pathExistCheck()  # 确保 output 文件夹存在
    text_content, filename = handle_args(*args)  # 处理输入参数

    with open(os.path.join('output', f'{filename}.txt'), 'w', encoding='utf-8') as file:
        file.write(text_content)

    return f'文档已保存为 “output/{filename}.txt”'


def copy_csv_files(load_csv_dir='load_csv', copy_dir='copy_csv'):
    import pandas as pd
    # 检查load_csv目录，如果不存在则创建
    if not os.path.exists(load_csv_dir):
        os.makedirs(load_csv_dir)

        # 初始化一个字典来存储csv文件的名称、行数和列数
    csv_details = {}

    # 遍历load_csv目录下的所有文件
    for filename in os.listdir(load_csv_dir):
        if filename.endswith('.csv'):
            # 读取csv文件
            file_path = os.path.join(load_csv_dir, filename)
            df = pd.read_csv(file_path, encoding='gbk')

            # 获取csv文件的行数和列数
            rows, cols = df.shape

            # 将文件名、行数和列数存储到字典中
            csv_details[filename] = {'rows': rows, 'cols': cols}

            # 创建副本文件夹（如果不存在）
            if not os.path.exists(copy_dir):
                os.makedirs(copy_dir)

                # 创建对应csv的副本，内容全部填充1
            copy_file_path = os.path.join(copy_dir, filename)
            df_copy = pd.DataFrame(1, index=range(rows), columns=range(cols))
            df_copy.to_csv(copy_file_path, index=False, header=False)

            # 打印csv文件的详细信息
    print(csv_details)


def init_csv_files():
    try:
        import pandas as pd
    except ImportError:
        print('pandas 没有安装！初始化失败！')
        return
    csv_folder_path = 'load_csv'
    pathExistCheck(csv_folder_path)

    csv_files = {
        'Downgua_VaryDay.csv': {'rows': 63, 'cols': 17}, 'Gua.csv': {'rows': 63, 'cols': 8},
        'Gua_Allocation_Date.csv': {'rows': 63, 'cols': 19}, 'Gua_Allocation_Empty.csv': {'rows': 64, 'cols': 13},
        'Gua_Allocation_Month.csv': {'rows': 63, 'cols': 19},
        'Gua_Allocation_SixMode.csv': {'rows': 64, 'cols': 13},
        'Gua_MutiLineVary.csv': {'rows': 64, 'cols': 24}, 'Gua_OneLineVary.csv': {'rows': 64, 'cols': 13},
        'mingyao.csv': {'rows': 7, 'cols': 10}, 'Upgua_VaryDay.csv': {'rows': 63, 'cols': 18},
        '三爻动.csv': {'rows': 64, 'cols': 21}, '二爻动.csv': {'rows': 64, 'cols': 16},
        '五爻动.csv': {'rows': 64, 'cols': 7}, '内卦64变配60日.csv': {'rows': 63, 'cols': 60},
        '四爻动.csv': {'rows': 64, 'cols': 16}, '外卦64变配60日.csv': {'rows': 63, 'cols': 60},
        '静卦配12月10天干.csv': {'rows': 64, 'cols': 72}, '静卦配60日.csv': {'rows': 64, 'cols': 61}}
    for file_name, detail in csv_files.items():
        file_path = os.path.join(csv_folder_path, file_name)
        if os.path.exists(file_path):
            continue
        df_copy = pd.DataFrame(1, index=range(detail['rows']), columns=range(detail['cols']))
        df_copy.to_csv(file_path, index=False, header=False)
    print('csv文件初始化完成！')


def init_data_db():
    try:
        import sqlite3
    except Exception:
        print('没有安装 sqlite3，后续无法保存数据库！')
        return
    pathExistCheck('data')
    db_file = os.path.join('data', 'database.db')
    # 如果数据库文件不存在，则创建一个新的数据库
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        conn.close()
    print(db_file, '初始化完成！')


if __name__ == '__main__':
    pass
    # 调用函数
    '''这是一个初始化函数，初次运行需要创建一些文件'''
    # init_csv_files();init_data_db()
