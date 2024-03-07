import openpyxl
import csv

t1ext = '占题：今日所看柯南剧集\n甲辰年 寅月 乙卯日 申时（空亡：子丑）\n山泽损 (艮宫)   山风蛊 (巽宫,归魂)\n玄武          官鬼寅木′应\n白虎          妻财子水″\n腾蛇          兄弟戌土″\n勾陈 子孙申金 兄弟丑土×世  子孙酉金′\n朱雀          官鬼卯木′\n青龙          父母巳火○    兄弟丑土″'  #
text="""
占题：例假啥时候来
甲辰年 寅月 庚申日 申时（空亡：子丑）
火雷噬嗑 (巽宫)   震为雷 (震宫,六冲)
腾蛇   子孙巳火○    妻财戌土″
勾陈   妻财未土″世
朱雀   官鬼酉金′  
青龙   妻财辰土″  
玄武   兄弟寅木″应
白虎   父母子水′  
"""

# lst[3:]:[['玄武', '官鬼寅木′应'], ['白虎', '妻财子水″'], ['腾蛇', '兄弟戌土″'], ['勾陈', '子孙申金', '兄弟丑土×世', '子孙酉金′'], ['朱雀', '官鬼卯木′'], ['青龙', '父母巳火○', '兄弟丑土″']]
# li in lst[3:]:['腾蛇', '兄弟戌土″']
# li[1]:'兄弟戌土″'
# any(sign in li[1] for sign in "′″×○")
def handle_text2nested_lst(text: str) -> list[list[str]]:
    def If_cent():
        缩进 = False
        for li in nested_lst[3:]:
            if any(sign not in li[1] for sign in "′″×○"):
                缩进 = True
        print('需要缩进？', 缩进)
        return 缩进

    nested_lst = [[n for n in s.split(' ') if n] for s in text.split('\n')]
    nested_lst = [li for li in nested_lst if li]

    if not If_cent():  # 不需要缩进，直接返回结果
        return nested_lst

    for i in range(3, 9):  # 需要缩进，再处理一下
        if any(sign in nested_lst[i][1] for sign in "′″×○"):
            nested_lst[i] = [nested_lst[i][0], ''] + nested_lst[i][1:]

    return nested_lst


# 定义嵌套列表
# nested_list = [
#     ['占题：今日所看柯南剧集'],
#     ['甲辰年', '寅月', '乙卯日', '申时（空亡：子丑）'],
#     ['山泽损', '(艮宫)', '山风蛊', '(巽宫，归魂)'],
#     ['玄武', '', '官鬼寅木′应'],
#     ['白虎', '', '妻财子水″'],
#     ['腾蛇', '', '兄弟戌土″'],
#     ['勾陈', '子孙申金', '兄弟丑土×世', '子孙酉金′'],
#     ['朱雀', '', '官鬼卯木′'],
#     ['青龙', '', '父母巳火○', '兄弟丑土″']
# ]


def write_as_csv(nested_list: list[list[str]]):
    # 打开CSV文件
    with open('../排盘结果.csv', 'w', newline='', encoding='gbk') as csvfile:
        writer = csv.writer(csvfile)

        # 将第一行数据写入CSV文件
        writer.writerow(nested_list[0])

        # 遍历嵌套列表的剩余部分
        for sub_list in nested_list[1:]:
            writer.writerow(sub_list)

    print('CSV文件已生成。')


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
    wb.save(f'{file_name}.xlsx')
    # print('XLSX文件已生成。')


def convert_text_to_xlsx(handle_txt: str, file_name: str = None):
    nested_lst = handle_text2nested_lst(handle_txt)
    write_as_xlsx(nested_lst, file_name)


if __name__ == '__main__':
    convert_text_to_xlsx(text)
