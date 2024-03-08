import csv
import os
import re
from place_addition import GUA_NAME, GAN, ZHI
from constants import GUA_SHU, Sixmode_to_Animals
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel, \
    QGridLayout
from PyQt5.QtCore import Qt

LIU_QIN_NUM_60 = [[36, 37, 14, 51, 52, 17, 6, 7, 20, 33, 34, 23], [12, 13, 50, 27, 28, 53, 42, 43, 56, 9, 10, 59],
                  [48, 49, 26, 3, 4, 29, 18, 19, 32, 45, 46, 35], [0, 1, 38, 15, 16, 41, 30, 31, 44, 57, 58, 47],
                  [24, 25, 2, 39, 40, 5, 54, 55, 8, 21, 22, 11]]
LIU_QIN = ['父母', '兄弟', '子孙', '妻财', '官鬼']
yao_wei = ['六爻', '五爻', '四爻', '三爻', '二爻', '初爻']
卦宫 = [string for string in '乾震坎巽艮坤离兑']
卦宫五行 = [string for string in '土水火木金']

round_12_brif = {'长生': '长', '沐浴': '沐', '冠带': '冠', '临官': '临', '帝旺': '帝', '衰地': '衰', '病地': '病',
                 '死地': '死', '墓库': '墓', '绝地': '绝', '胎地': '胎', '养地': '养'}
长生_60 = {36: {'兄弟': '临', '妻财': '临', '官鬼': '长', '父母': '绝', '子孙': '病'},
           37: {'兄弟': '帝', '妻财': '帝', '官鬼': '沐', '父母': '胎', '子孙': '死'},
           14: {'兄弟': '衰', '妻财': '衰', '官鬼': '冠', '父母': '养', '子孙': '墓'},
           51: {'兄弟': '病', '妻财': '病', '官鬼': '临', '父母': '长', '子孙': '绝'},
           52: {'兄弟': '死', '妻财': '死', '官鬼': '帝', '父母': '沐', '子孙': '胎'},
           17: {'兄弟': '', '妻财': '墓', '官鬼': '衰', '父母': '冠', '子孙': '养'},
           6: {'兄弟': '绝', '妻财': '绝', '官鬼': '病', '父母': '临', '子孙': '长'},
           7: {'兄弟': '胎', '妻财': '胎', '官鬼': '死', '父母': '帝', '子孙': '沐'},
           20: {'兄弟': '养', '妻财': '养', '官鬼': '墓', '父母': '衰', '子孙': '冠'},
           33: {'兄弟': '长', '妻财': '长', '官鬼': '绝', '父母': '病', '子孙': '临'},
           34: {'兄弟': '沐', '妻财': '沐', '官鬼': '胎', '父母': '死', '子孙': '帝'},
           23: {'兄弟': '冠', '妻财': '冠', '官鬼': '养', '父母': '墓', '子孙': '衰'},
           12: {'官鬼': '临', '兄弟': '临', '子孙': '长', '妻财': '绝', '父母': '病'},
           13: {'官鬼': '帝', '兄弟': '帝', '子孙': '沐', '妻财': '胎', '父母': '死'},
           50: {'官鬼': '衰', '兄弟': '衰', '子孙': '冠', '妻财': '养', '父母': '墓'},
           27: {'官鬼': '病', '兄弟': '病', '子孙': '临', '妻财': '长', '父母': '绝'},
           28: {'官鬼': '死', '兄弟': '死', '子孙': '帝', '妻财': '沐', '父母': '胎'},
           53: {'官鬼': '', '兄弟': '墓', '子孙': '衰', '妻财': '冠', '父母': '养'},
           42: {'官鬼': '绝', '兄弟': '绝', '子孙': '病', '妻财': '临', '父母': '长'},
           43: {'官鬼': '胎', '兄弟': '胎', '子孙': '死', '妻财': '帝', '父母': '沐'},
           56: {'官鬼': '养', '兄弟': '养', '子孙': '墓', '妻财': '衰', '父母': '冠'},
           9: {'官鬼': '长', '兄弟': '长', '子孙': '绝', '妻财': '病', '父母': '临'},
           10: {'官鬼': '沐', '兄弟': '沐', '子孙': '胎', '妻财': '死', '父母': '帝'},
           59: {'官鬼': '冠', '兄弟': '冠', '子孙': '养', '妻财': '墓', '父母': '衰'},
           48: {'子孙': '临', '官鬼': '临', '父母': '长', '兄弟': '绝', '妻财': '病'},
           49: {'子孙': '帝', '官鬼': '帝', '父母': '沐', '兄弟': '胎', '妻财': '死'},
           26: {'子孙': '衰', '官鬼': '衰', '父母': '冠', '兄弟': '养', '妻财': '墓'},
           3: {'子孙': '病', '官鬼': '病', '父母': '临', '兄弟': '长', '妻财': '绝'},
           4: {'子孙': '死', '官鬼': '死', '父母': '帝', '兄弟': '沐', '妻财': '胎'},
           29: {'子孙': '', '官鬼': '墓', '父母': '衰', '兄弟': '冠', '妻财': '养'},
           18: {'子孙': '绝', '官鬼': '绝', '父母': '病', '兄弟': '临', '妻财': '长'},
           19: {'子孙': '胎', '官鬼': '胎', '父母': '死', '兄弟': '帝', '妻财': '沐'},
           32: {'子孙': '养', '官鬼': '养', '父母': '墓', '兄弟': '衰', '妻财': '冠'},
           45: {'子孙': '长', '官鬼': '长', '父母': '绝', '兄弟': '病', '妻财': '临'},
           46: {'子孙': '沐', '官鬼': '沐', '父母': '胎', '兄弟': '死', '妻财': '帝'},
           35: {'子孙': '冠', '官鬼': '冠', '父母': '养', '兄弟': '墓', '妻财': '衰'},
           0: {'妻财': '临', '父母': '临', '兄弟': '长', '子孙': '绝', '官鬼': '病'},
           1: {'妻财': '帝', '父母': '帝', '兄弟': '沐', '子孙': '胎', '官鬼': '死'},
           38: {'妻财': '衰', '父母': '衰', '兄弟': '冠', '子孙': '养', '官鬼': '墓'},
           15: {'妻财': '病', '父母': '病', '兄弟': '临', '子孙': '长', '官鬼': '绝'},
           16: {'妻财': '死', '父母': '死', '兄弟': '帝', '子孙': '沐', '官鬼': '胎'},
           41: {'妻财': '', '父母': '墓', '兄弟': '衰', '子孙': '冠', '官鬼': '养'},
           30: {'妻财': '绝', '父母': '绝', '兄弟': '病', '子孙': '临', '官鬼': '长'},
           31: {'妻财': '胎', '父母': '胎', '兄弟': '死', '子孙': '帝', '官鬼': '沐'},
           44: {'妻财': '养', '父母': '养', '兄弟': '墓', '子孙': '衰', '官鬼': '冠'},
           57: {'妻财': '长', '父母': '长', '兄弟': '绝', '子孙': '病', '官鬼': '临'},
           58: {'妻财': '沐', '父母': '沐', '兄弟': '胎', '子孙': '死', '官鬼': '帝'},
           47: {'妻财': '冠', '父母': '冠', '兄弟': '养', '子孙': '墓', '官鬼': '衰'},
           24: {'父母': '临', '子孙': '临', '妻财': '长', '官鬼': '绝', '兄弟': '病'},
           25: {'父母': '帝', '子孙': '帝', '妻财': '沐', '官鬼': '胎', '兄弟': '死'},
           2: {'父母': '衰', '子孙': '衰', '妻财': '冠', '官鬼': '养', '兄弟': '墓'},
           39: {'父母': '病', '子孙': '病', '妻财': '临', '官鬼': '长', '兄弟': '绝'},
           40: {'父母': '死', '子孙': '死', '妻财': '帝', '官鬼': '沐', '兄弟': '胎'},
           5: {'父母': '', '子孙': '墓', '妻财': '衰', '官鬼': '冠', '兄弟': '养'},
           54: {'父母': '绝', '子孙': '绝', '妻财': '病', '官鬼': '临', '兄弟': '长'},
           55: {'父母': '胎', '子孙': '胎', '妻财': '死', '官鬼': '帝', '兄弟': '沐'},
           8: {'父母': '养', '子孙': '养', '妻财': '墓', '官鬼': '衰', '兄弟': '冠'},
           21: {'父母': '长', '子孙': '长', '妻财': '绝', '官鬼': '病', '兄弟': '临'},
           22: {'父母': '沐', '子孙': '沐', '妻财': '胎', '官鬼': '死', '兄弟': '帝'},
           11: {'父母': '冠', '子孙': '冠', '妻财': '养', '官鬼': '墓', '兄弟': '衰'}}

返卦 = ['乾', '坎', '艮', '艮', '震', '巽', '巽', '离', '坤', '坤', '兑', '乾']

FAMILY = ['父母亥水', '父母子水', '父母丑土', '父母寅木', '父母卯木', '父母辰土', '父母巳火', '父母午火', '父母未土',
          '父母申金', '父母酉金', '父母戌土', '兄弟亥水', '兄弟子水', '兄弟丑土', '兄弟寅木', '兄弟卯木', '兄弟辰土',
          '兄弟巳火', '兄弟午火', '兄弟未土', '兄弟申金', '兄弟酉金', '兄弟戌土', '子孙亥水', '子孙子水', '子孙丑土',
          '子孙寅木', '子孙卯木', '子孙辰土', '子孙巳火', '子孙午火', '子孙未土', '子孙申金', '子孙酉金', '子孙戌土',
          '妻财亥水', '妻财子水', '妻财丑土', '妻财寅木', '妻财卯木', '妻财辰土', '妻财巳火', '妻财午火', '妻财未土',
          '妻财申金', '妻财酉金', '妻财戌土', '官鬼亥水', '官鬼子水', '官鬼丑土', '官鬼寅木', '官鬼卯木', '官鬼辰土',
          '官鬼巳火', '官鬼午火', '官鬼未土', '官鬼申金', '官鬼酉金', '官鬼戌土', '官鬼亥水']
HalfGua_TO_IDX = {
    (1, 1, 1): 0, (1, 1, 3): 1, (1, 3, 1): 2, (3, 1, 1): 3, (3, 3, 1): 4, (3, 1, 3): 5, (1, 3, 3): 6, (3, 3, 3): 7,
    (2, 1, 1): 8, (2, 1, 3): 9, (2, 3, 1): 10, (0, 1, 1): 11, (0, 3, 1): 12, (0, 1, 3): 13, (2, 3, 3): 14,
    (0, 3, 3): 15, (1, 2, 1): 16, (1, 2, 3): 17, (1, 0, 1): 18, (3, 2, 1): 19, (3, 0, 1): 20, (3, 2, 3): 21,
    (1, 0, 3): 22, (3, 0, 3): 23, (2, 2, 1): 24, (2, 2, 3): 25, (2, 0, 1): 26, (0, 2, 1): 27, (0, 0, 1): 28,
    (0, 2, 3): 29, (2, 0, 3): 30, (0, 0, 3): 31, (1, 1, 2): 32, (1, 1, 0): 33, (1, 3, 2): 34, (3, 1, 2): 35,
    (3, 3, 2): 36, (3, 1, 0): 37, (1, 3, 0): 38, (3, 3, 0): 39, (2, 1, 2): 40, (2, 1, 0): 41, (2, 3, 2): 42,
    (0, 1, 2): 43, (0, 3, 2): 44, (0, 1, 0): 45, (2, 3, 0): 46, (0, 3, 0): 47, (1, 2, 2): 48, (1, 2, 0): 49,
    (1, 0, 2): 50, (3, 2, 2): 51, (3, 0, 2): 52, (3, 2, 0): 53, (1, 0, 0): 54, (3, 0, 0): 55, (2, 2, 2): 56,
    (2, 2, 0): 57, (2, 0, 2): 58, (0, 2, 2): 59, (0, 0, 2): 60, (0, 2, 0): 61, (2, 0, 0): 62, (0, 0, 0): 63}
HalfGua_TO_NAME = {
    (1, 1, 1): '乾', (2, 1, 1): '兑', (1, 2, 1): '离', (2, 2, 1): '震', (1, 1, 2): '巽', (2, 1, 2): '坎',
    (1, 2, 2): '艮', (2, 2, 2): '坤', (1, 1, 3): '乾化巽', (1, 3, 1): '乾化离', (3, 1, 1): '乾化兑',
    (3, 3, 1): '乾化震', (3, 1, 3): '乾化坎', (1, 3, 3): '乾化艮', (3, 3, 3): '乾化坤', (2, 1, 3): '兑化坎',
    (2, 3, 1): '兑化震', (0, 1, 1): '兑化乾', (0, 3, 1): '兑化离', (0, 1, 3): '兑化巽', (2, 3, 3): '兑化坤',
    (0, 3, 3): '兑化艮', (1, 2, 3): '离化艮', (1, 0, 1): '离化乾', (3, 2, 1): '离化震', (3, 0, 1): '离化兑',
    (3, 2, 3): '离化坤', (1, 0, 3): '离化巽', (3, 0, 3): '离化坎', (2, 2, 3): '震化坤', (2, 0, 1): '震化兑',
    (0, 2, 1): '震化离', (0, 0, 1): '震化乾', (0, 2, 3): '震化艮', (2, 0, 3): '震化坎', (0, 0, 3): '震化巽',
    (1, 1, 0): '巽化乾', (1, 3, 2): '巽化艮', (3, 1, 2): '巽化坎', (3, 3, 2): '巽化坤', (3, 1, 0): '巽化兑',
    (1, 3, 0): '巽化离', (3, 3, 0): '巽化震', (2, 1, 0): '坎化兑', (2, 3, 2): '坎化坤', (0, 1, 2): '坎化巽',
    (0, 3, 2): '坎化艮', (0, 1, 0): '坎化乾', (2, 3, 0): '坎化震', (0, 3, 0): '坎化离', (1, 2, 0): '艮化离',
    (1, 0, 2): '艮化巽', (3, 2, 2): '艮化坤', (3, 0, 2): '艮化坎', (3, 2, 0): '艮化震', (1, 0, 0): '艮化乾',
    (3, 0, 0): '艮化兑', (2, 2, 0): '坤化震', (2, 0, 2): '坤化坎', (0, 2, 2): '坤化艮', (0, 0, 2): '坤化巽',
    (0, 2, 0): '坤化离', (2, 0, 0): '坤化兑', (0, 0, 0): '坤化乾'}


def calculate_time(func):
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'此次{func.__name__}花费了 {end_time - start_time:.4f} 秒。')
        return result

    return wrapper


'''Part 01 : 解析卦象信息 '''


class AnalyModel:
    def __init__(self, TimeList: list[int], empty_str: str, CoinsInfoList, OtherList):
        # 需要什么用什么，自助；不用自己去算
        # coinsNumber_list是(六五四三二初)
        self.rigan, self.month, self.date, self.yearg, self.yearz, self.hour = TimeList
        self.gua_num, self.biangua_num, self.coinsNumber_list = CoinsInfoList
        self.WuXing, self.SixMode, self.mingyao, self.yongshen = OtherList

        num = ZHI.index(empty_str[0])
        self.empty_lst = [num, num + 1]  # 得到空亡地支 的 序数

        self.trigger_li = [1 if r in [3, 0] else 0 for r in self.coinsNumber_list]

        from constants import gua_info_list_calculate, search_self
        self.self_posit, self.other_posit = search_self(self.gua_num)  # 爻位1-6
        self.GuaShu_li = gua_info_list_calculate(self.gua_num, self.biangua_num, self.trigger_li)
        # self.GuaShu_li：18位数组，顺序是Main，After，Hide

        from GIDCoreCode import GuaImageEditor
        GuaImageDict = self.DF_output()
        self.GuaImageData = GuaImageEditor(GuaImageDict).edit_process()

        # function for PC
        self.window = None
        _inner, _out = tuple(self.coinsNumber_list[3:]), tuple(self.coinsNumber_list[:3])
        up_idx, down_idx = HalfGua_TO_IDX[_out], HalfGua_TO_IDX[_inner]
        self.out, self.inner = HalfGua_TO_NAME[_out], HalfGua_TO_NAME[_inner]

        value_dic = {'甲': 0, '乙': 0, '丙': 12, '丁': 12, '戊': 24, '己': 24, '庚': 36, '辛': 36, '壬': 48, '癸': 48}
        date_idx = self.date % 12 + value_dic[GAN[self.rigan % 10]]

        self.cell_params = [
            ('load_csv/Upgua_VaryDay.csv', up_idx + 2, self.date % 12 + 4),  # 爻象只有前三列，第四列开始选择
            ('load_csv/Downgua_VaryDay.csv', down_idx + 2, self.date % 12 + 4),
            ('load_csv/外卦64变配60日.csv', up_idx + 2, date_idx + 1),  # 第一列开始
            ('load_csv/内卦64变配60日.csv', down_idx + 2, date_idx + 1),
            ('load_csv/Gua_Allocation_Month.csv', self.gua_num + 2, self.month % 12 + 7),  # 爻象前六列，从7列开始
            ('load_csv/Gua_Allocation_Date.csv', self.gua_num + 1, self.date % 12 + 7),  # 此表，第一行为乾；卦序，0为乾，所以+1。
            ('load_csv/Gua_Allocation_SixMode.csv', self.gua_num + 2, self.SixMode + 7),  # Sixmode!=6
            ('load_csv/Gua.csv', self.gua_num + 1, 7),  # 此表第一行不是表头
            ('load_csv/静卦配12月10天干.csv', self.gua_num + 2, (self.month % 12) * 6 + self.SixMode + 1),
            ('load_csv/静卦配60日.csv', self.gua_num + 2, date_idx + 1)
        ]
        tp = get_path_idx(self.trigger_li, self.gua_num)
        if tp:
            self.cell_params.append(tp)

    def 主要信息接口(self, TextFile):
        """
        :param TextFile: 知识库txt的路径。该txt文件按照一定的规范书写。
        :return: ConvertTextToCode 类的子方法 查条文() 自带打印功能。
        """
        time = [self.rigan, self.month, self.date, self.yearz, self.hour]
        guainfo = [self.gua_num, self.biangua_num, self.coinsNumber_list, self.trigger_li, self.GuaShu_li, self.WuXing,
                   self.self_posit, self.other_posit, self.SixMode, self.yongshen]
        self.转机器语言工具 = ConvertTextToCode(self.GuaImageData, time, guainfo, TextFile)
        # print(self.GuaImageData)

    '''function for PC'''

    def text_output_func(self):
        """
        这是在给定的csv专门查条文的函数。
        需要吻合csv构造的行列。
        """

        def dedigit(sentence: str):
            # 条文如果是数字，筛选掉；不是数字，加格式。
            if sentence and not sentence.isdigit():  # 找到的条文不是空值，也不是数值；加格式。
                sentence = f"◇{sentence.strip()}\n"
                return sentence
            return None

        articles = []

        for params in self.cell_params:  # 这里提供了表格的行列参数
            try:
                cell = read_specific_cell(*params)
                if wd := dedigit(cell):
                    articles.append(wd)
            except Exception as e:
                print(params[0], e, "，text_output_func 出错了。")

        for sentence in articles:
            print(sentence)

    def write_csv_cell(self):
        li = [i for i in '初二三四五六']
        li_1 = self.trigger_li[::-1]
        string = ''.join(li[i] for i, v in enumerate(li_1) if v != 0)
        string = string + '爻发动' if string else '静卦'

        text = [ZHI[self.date % 12] + "日占得外卦" + self.out,  # 尽可能省去输入的人力劳动
                ZHI[self.date % 12] + "日占得内卦" + self.inner,
                GAN[self.rigan % 10] + "日占得" + GUA_NAME[self.gua_num],
                ZHI[self.month % 12] + "月" + GAN[self.rigan % 10] + "日占得" + GUA_NAME[self.gua_num],
                GAN[self.rigan % 10] + ZHI[self.date % 12] + "日占得外卦" + self.out,
                GAN[self.rigan % 10] + ZHI[self.date % 12] + "日占得内卦" + self.inner,
                GAN[self.rigan % 10] + ZHI[self.date % 12] + "日占得" + GUA_NAME[self.gua_num],

                GUA_NAME[self.gua_num] + "·" + string, ]
        self.window = CellEditorWindow(self.cell_params, text)
        self.window.show()

    def close_csv_cell(self):
        if self.window:
            self.window.close()
            self.window = None

    def mytext_outputf(self):
        articles = mingyao_analy(self.WuXing, self.SixMode, self.mingyao, self.GuaShu_li,
                                 GUA_SHU[self.gua_num][self.self_posit])
        for sentence in articles:
            print(sentence)

    '''general function'''

    def active_lst(self):
        # 输出词典的基本样式
        at_lst = []
        for i in range(12):
            # 遍历卦数的0-11 即主卦、变卦
            num = self.GuaShu_li[i]

            # 遍历到的数 变爻不能是None；主卦必须发动、暗动。两个条件满足其一。
            condition1 = i >= 6 and num is not None
            condition2 = self.trigger_li[i] == 1 or num == xiangchong(self.date) if i < 6 else False
            if condition1 or condition2:
                at_lst.append((i, num))  # 记录（爻位idx，60六亲数***）
        return at_lst

    def self_other_ps(self, skip=False):
        self_other_lst = [''] * 18
        self_other_lst[self.self_posit] = '世'
        self_other_lst[self.other_posit] = '应'
        if not skip:
            max_num = max(self.self_posit, self.other_posit)
            self_other_lst[max_num - 2], self_other_lst[max_num - 1] = '间', '间'
        return self_other_lst

    def DF_output(self):
        活跃列表 = self.active_lst()
        世应列表 = self.self_other_ps()
        六神列表 = Sixmode_to_Animals(self.SixMode)

        GuaImageDict = {'爻序': [], '爻位': [],
                        '六神': [],
                        '世应': [],
                        '六亲': [],
                        '支': [],
                        '五行': [],
                        '返卦': [],
                        '空亡': [],
                        '发动': [],
                        '月生': [],
                        '月合': [],
                        '月地': [], '月刑': [],
                        '日生': [],
                        '日合': [],
                        '日地': [], '日刑': [], '计数刑': [],
                        '60六亲': []
                        }
        for tuples in 活跃列表:
            idx = tuples[0]
            GuaImageDict[str(3 * idx)] = []  # 整除3，生克
            GuaImageDict[str(3 * idx + 1)] = []  # 除3余1，冲合值
            GuaImageDict[str(3 * idx + 2)] = []  # 除3余2，长生十二状态

        Month = LIU_QIN_NUM_60[self.WuXing][self.month % 12]
        Date = LIU_QIN_NUM_60[self.WuXing][self.date % 12]

        def yao_info(wx_int, zhi_int):
            Num = LIU_QIN_NUM_60[wx_int][zhi_int % 12]
            yao = FAMILY[Num]
            return [Num, yao[:2], yao[2], yao[3]]

        for i, num in enumerate(self.GuaShu_li):
            if num is not None:
                Num, lq_str, zhi_str, wx_str = yao_info(self.WuXing, num)
                是否空 = '空亡' if num in self.empty_lst else ''
                if i < 6:
                    if self.trigger_li[i] == 1:
                        是否动 = '发动'
                    elif num == xiangchong(self.date):
                        是否动 = '暗动'  # '暗动'
                    else:
                        是否动 = None
                elif i < 12:
                    是否动 = str(i % 6)  # ['发动']:str
                else:
                    是否动 = None

                li = [i, yao_wei[i % 6], 六神列表[i % 6], 世应列表[i], lq_str, zhi_str, wx_str, 返卦[num % 12], 是否空,
                      是否动,
                      生扶克(num, self.month), 冲合值(num, self.month), 长生_60[Month][lq_str], 刑(num, self.month),
                      生扶克(num, self.date), 冲合值(num, self.date), 长生_60[Date][lq_str], 刑(num, self.date),
                      计数刑(num, 活跃列表), Num]
                for m, n in zip(GuaImageDict.keys(), li):
                    GuaImageDict[m].append(n)  # 填表：对应的key，填充对应的value

                if 活跃列表:
                    for tuples in 活跃列表:
                        idx, value = tuples
                        Number = LIU_QIN_NUM_60[self.WuXing][value % 12]  # 60六亲的数
                        text = 生扶克(num, value, True) if idx >= 6 else 生扶克(num, value)

                        GuaImageDict[str(3 * idx)].append(text)
                        GuaImageDict[str(3 * idx + 1)].append(冲合值(num, value))
                        GuaImageDict[str(3 * idx + 2)].append(长生_60[Number][lq_str])

        for (yao_xu, Num, name) in [(18, Month, '月建'), (19, Date, '日辰')]:
            yao = FAMILY[Num]
            dic = {'爻序': yao_xu, '六神': name, '六亲': yao[:2], '支': yao[2], '五行': yao[3], '返卦': 返卦[Num % 12],
                   '60六亲': Num}
            for key, value in GuaImageDict.items():
                if key in dic:
                    GuaImageDict[key].append(dic[key])
                else:
                    GuaImageDict[key].append('')

        return GuaImageDict

    def 十二宫(self):
        return [FAMILY[num] for num in LIU_QIN_NUM_60[self.WuXing]]


'''Part 02 : 六爻术语文本转机器语言 '''


# 用正则表达式会减低可读性；用表格查询，虽然不直接，但省去思考时间，直接定位行列查询，不必动脑。
# 选定一爻: idx,row_name of information table,index of 'self.GuaImageDict'
# 能够识别的动作: string,as well as col_name of information table,key of 'self.GuaImageDict'
# 上下文的概念: 妻财伏藏，飞神 父母？妻财 化墓 在子孙？子孙在哪判定？。write down as 'self.Memory_idx'
class ConvertTextToCode:
    def __init__(self, GuaImageDict=None, time=None, guainfo=None, TextFilePath=''):

        self.Memory_idx = None
        self.former_idxlst = None
        self.line_belong = None  # 重要，否则，条文无序
        self.last_idx_group = None
        self.save_idx_lst = []
        self.current_file_path, self.suffix_set = '', []
        self.platform = 'PC'  # 'Android' if isAndroid() else
        # self.debug = False

        if not guainfo or not time or not GuaImageDict:
            print('重要数值为空')
        # “卦”的数据表格,main information table: self.GuaImageDict
        from GIDCoreCode import GuaImageEditor
        self.GuaImageDict = GuaImageEditor(GuaImageDict).edit_process()

        # “卦”的主要信息接口:time,guainfo
        self.rigan, self.month, self.date, self.yearz, self.hour = time
        self.gua_num, self.biangua_num, cNlist, self.trigger_li, self.GuaShu_li, self.Gua_wx, \
            self.self_posit, self.other_posit, Sixmode, self.yongshen = guainfo
        self.coinsNumber_list = tuple(cNlist)
        self.biangua_num = self.gua_num if self.biangua_num > 63 else self.biangua_num

        # 传入条文集txt的文件路径
        self.断语词典: list[dict] = self.源文本处理(TextFilePath)  # requirement:需要上文的'self.yongshen'，不要打乱上下文顺序！
        num = min(self.self_posit, self.other_posit)
        lst = self.GuaImageDict['爻序']
        self.暂存箱 = {  # 储存obj:[idx]
            '动墓': [],
            '应爻': [self.other_posit], '间爻': list(range(num + 1, num + 3)),
            '*': list(range(6)), '**': list(range(len(self.GuaImageDict['支']))),
            '动爻化出': [lst.index(i + 6) for i in range(6) if self.trigger_li[i]],
            '应爻化出': [lst.index(self.other_posit + 6)] if self.trigger_li[self.other_posit] else [],
            '六爻化出': [lst.index(6)] if self.trigger_li[0] else [],
            '五爻化出': [lst.index(7)] if self.trigger_li[1] else [],
            '四爻化出': [lst.index(8)] if self.trigger_li[2] else [],
            '三爻化出': [lst.index(9)] if self.trigger_li[3] else [],
            '二爻化出': [lst.index(10)] if self.trigger_li[4] else [],
            '初爻化出': [lst.index(11)] if self.trigger_li[5] else [],
            '变爻两现': find_duplicates(self.GuaImageDict['支'], lst),
            '伏神': self.伏神(),
            '变爻': self.伏神(12, 6),
            '动爻': [i for i, num in enumerate(self.trigger_li) if num],
            '静爻': [i for i, num in enumerate(self.trigger_li) if num == 0]
        }

        self.OtherImforation()

        self.lines_animals = {
            '六爻': 0, '五爻': 1, '四爻': 2, '三爻': 3, '二爻': 4, '初爻': 5,
            '世爻': self.self_posit, '应爻': self.other_posit,
            # 以上作为verb or obj
        }
        Animals = Sixmode_to_Animals(Sixmode)
        for i, animal in enumerate(Animals):
            self.lines_animals[animal] = i

        after_columns_2 = [
            str(1 + 3 * idx) for idx, ident_str in zip(self.GuaImageDict['爻序'][5:], self.GuaImageDict['发动'][5:])
            if ident_str and ident_str.isdigit()]
        # [5:],because idx before 5 is not target,after 6 maybe target,meanwhile min len is 6.
        # str(1 + 3 * idx) is a special way for idx convert to col_name in data table/key in data dict,0 is 生克扶,1 is 冲合,2 is 十二长生
        # ident_str.isdigit() 筛选 self.GuaImageDict['发动'] digital item,这在表格中 代表着 变爻

        self.AcitveColumns = [
            [str(j + 3 * i) for i in range(6) if str(j + 3 * i) in self.GuaImageDict] for j in range(3)]
        active_columns, active_columns_1, active_columns_2 = self.AcitveColumns  # meaning:生克扶,冲合值,十二长生

        # Among above three, everyone is a list of column_name,
        # 以上三个，都是 列名 组成的列表
        # each column_name is the key in self.GuaImageDict,also the column_name in message_table
        # 每一个列名，都是 self.GuaImageDict 中的键，也是 信息表格（计算明细） 的 列名
        # When you search a cell in message_table,you need row:idx and column_name,using in this way:self.GuaImageDict[column_name][idx]

        self_zhi = self.GuaImageDict['支'][self.self_posit]
        other_zhi = self.GuaImageDict['支'][self.other_posit]
        self.convert_string = {
            '外部函数': {  # '合世': [self.self_posit, '合', 冲合值], '冲世': [self.self_posit, '冲', 冲合值],
                # '合应': [self.other_posit, '合', 冲合值], '冲应': [self.other_posit, '冲', 冲合值],
                '生世': [self.self_posit, '生', 生扶克], '克世': [self.self_posit, '克', 生扶克],
                '世爻替身': [self.self_posit, '扶', 生扶克], '生应': [self.other_posit, '生', 生扶克],
            },
            '变爻行标志': {'化空亡': ['空亡', '空亡'], '化月破': ['月合', '冲'], '化月合': ['月合', '合'],
                           '化日冲': ['日合', '冲'], '化日合': ['日合', '合'],
                           '化日辰': ['日合', '值'], '化出世爻': ['支', self_zhi],
                           '化出应爻': ['支', other_zhi], '化父母': ['六亲', '父母'], '化兄弟': ['六亲', '兄弟'],
                           '化子孙': ['六亲', '子孙'], '化妻财': ['六亲', '妻财'], '化官鬼': ['六亲', '官鬼'], },
            '动爻列标志': {'动爻生': [active_columns, '生'], '动爻克': [active_columns, '克'],
                           '动爻冲': [active_columns_1, '冲'], '动爻合': [active_columns_1, '合'],
                           '变爻冲': [after_columns_2, '冲'], '变爻合': [after_columns_2, '合'],
                           '入动墓': [active_columns_2, '墓'], '绝地发动': [active_columns_2, '绝'],
                           '病地发动': [active_columns_2, '病'], '死地发动': [active_columns_2, '死'],
                           '长生发动': [active_columns_2, '长']},  # 利用col_name反向计算 客 的idx
            '在爻位': {'在六爻': ['爻序', 0], '在五爻': ['爻序', 1], '在四爻': ['爻序', 2],
                       '在三爻': ['爻序', 3], '在二爻': ['爻序', 4], '在初爻': ['爻序', 5]},
            '六亲六神': {
                '子孙': ['六亲', '子孙'], '妻财': ['六亲', '妻财'], '官鬼': ['六亲', '官鬼'], '父母': ['六亲', '父母'],
                '兄弟': ['六亲', '兄弟'], '世爻': ['世应', '世'], '应爻': ['世应', '应'], '空亡': ['空亡', '空亡'],
                '青龙': ['六神', '青龙'], '朱雀': ['六神', '朱雀'], '勾陈': ['六神', '勾陈'],
                '腾蛇': ['六神', '腾蛇'], '白虎': ['六神', '白虎'], '玄武': ['六神', '玄武'],
                '子': ['支', '子'], '丑': ['支', '丑'], '寅': ['支', '寅'], '卯': ['支', '卯'],
                '辰': ['支', '辰'], '巳': ['支', '巳'], '午': ['支', '午'], '未': ['支', '未'],
                '申': ['支', '申'], '酉': ['支', '酉'], '戌': ['支', '戌'], '亥': ['支', '亥'],
                '乾': ['返卦', '乾'], '兑': ['返卦', '兑'], '离': ['返卦', '离'], '震': ['返卦', '震'],
                '巽': ['返卦', '巽'], '坎': ['返卦', '坎'], '艮': ['返卦', '艮'], '坤': ['返卦', '坤'],
                '水': ['五行', '水'], '火': ['五行', '火'], '木': ['五行', '木'], '金': ['五行', '金'],
                '土': ['五行', '土'], '世爻同宫': ['返卦', self.GuaImageDict['返卦'][self.self_posit]],
                '六爻': ['爻位', '六爻'], '五爻': ['爻位', '五爻'], '四爻': ['爻位', '四爻'],
                '三爻': ['爻位', '三爻'], '二爻': ['爻位', '二爻'], '初爻': ['爻位', '初爻']
            },

            '日月发动世应': {
                '月扶': ['月生', '扶'], '月生': ['月生', '生'], '月克': ['月生', '克'],
                '月不生': ['月生', ''],
                '月建': ['月合', '值'], '次月': ['支', ZHI[(self.month + 1) % 12]],
                '上个月': ['支', ZHI[(self.month - 1) % 12]],
                '月破': ['月合', '冲'], '月合': ['月合', '合'],
                '入月墓': ['月地', '墓'], '月为死地': ['月地', '死'], '月为绝地': ['月地', '绝'],
                '月为长生': ['月地', '长'], '月为病地': ['月地', '病'], '月刑': ['月刑', '刑'],

                '太岁': ['支', ZHI[self.yearz % 12] if self.yearz else '无'],
                '明年': ['支', ZHI[(self.yearz + 1) % 12] if self.yearz else '无'],
                '日扶': ['日生', '扶'], '日生': ['日生', '生'], '日克': ['日生', '克'],
                '日不生': ['日生', ''],
                '日辰': ['日合', '值'], '明日': ['支', ZHI[(self.date + 1) % 12]],
                '明日冲': ['支', ZHI[(self.date + 7) % 12]], '时辰': ['支', ZHI[self.hour % 12] if self.hour else '无'],
                '时冲': ['支', ZHI[(self.hour + 6) % 12] if self.hour else '无'],
                '昨日': ['支', ZHI[(self.date - 1) % 12]], '昨日冲': ['支', ZHI[(self.date + 5) % 12]],
                '日冲': ['日合', '冲'], '日合': ['日合', '合'], '日害': ['日合', '害'],
                '入日墓': ['日地', '墓'], '日为死地': ['日地', '死'], '日为绝地': ['日地', '绝'],
                '日为长生': ['日地', '长'], '日为病地': ['日地', '病'], '日刑': ['日刑', '刑'],
                '空亡': ['空亡', '空亡'], '非空': ['空亡', ''], '发动': ['发动', '发动'],
                '独发': ['发动', '发动' if sum(self.trigger_li) == 1 else '不存在'],
                '独静': ['发动', None if sum(self.trigger_li) == 5 else '不存在'],
                '暗动': ['发动', '暗动'], '安静': ['发动', None],
                '持世': ['世应', '世'], '临应': ['世应', '应'], '间爻': ['世应', '间']},
        }
        self.add_idxlst()  # update self.暂存箱
        self.查条文()  # 自带打印；查条纹之后，update self.暂存箱，新增了很多内容；struction is two parts:{'obj':idx_list,idx:{'string':True}}
        # for key, value in self.暂存箱.items():
        #     if not value:
        #         continue
        #     print(key, value)

    def OtherImforation(self):
        outer, inner = self.coinsNumber_list[:3], self.coinsNumber_list[3:]
        str_o, str_i = HalfGua_TO_NAME[outer], HalfGua_TO_NAME[inner]

        num = sum(self.trigger_li)
        self.GuaInfo = {
            '主卦': [GUA_NAME[self.gua_num]], '变卦': [GUA_NAME[self.biangua_num]], '卦宫': [卦宫[self.gua_num // 8]],
            '外卦': [str_o] if len(str_o) == 1 else [str_o[0], str_o[1:], str_o],
            '内卦': [str_i] if len(str_i) == 1 else [str_i[0], str_i[1:], str_i],
            '卦宫五行': [卦宫五行[self.Gua_wx]], '日主': [GAN[self.rigan % 10]],
            '静卦': num == 0, '独发': num == 1, '二爻动': num == 2, '三爻动': num == 3, '独静': num == 5,
            # singe obj makes sentence
            '游魂': self.gua_num % 8 == 6, '归魂': self.gua_num % 8 == 7,
            '化游魂': self.biangua_num % 8 == 6, '化归魂': self.biangua_num % 8 == 7, '伏吟': True, '反吟': True,
            '本宫外卦': False, '他宫外卦': False, '本宫内卦': False, '他宫内卦': False,
            '六合': self.gua_num in [3, 9, 17, 33, 41, 43, 49, 57],
            '六冲': self.gua_num % 8 == 0 or self.gua_num in [44, 28],
            '化六合': self.biangua_num in [3, 9, 17, 33, 41, 43, 49, 57],
            '化六冲': self.biangua_num % 8 == 0 or self.biangua_num in [44, 28], }  # 以上作为obj

        for tag, rang in {'伏吟': ['震化乾', '乾化震'], '反吟': ['巽化坤', '坤化巽']}.items():
            for key, string in [('外卦', str_o), ('内卦', str_i)]:
                if string in rang:
                    self.GuaInfo[key].append(tag)
                    break  # for GuaInfo's key '内卦''外卦', value append '反吟''伏吟'
            else:
                self.GuaInfo[tag] = False  # 正难则反
        self.GuaInfo['大象'] = set(self.GuaInfo['外卦'] + self.GuaInfo['内卦'])
        if self.gua_num % 8 <= 4:
            self.GuaInfo['本宫外卦'] = True
        else:
            self.GuaInfo['他宫外卦'] = True
        if self.gua_num % 8 in [0, 7]:
            self.GuaInfo['本宫内卦'] = True
        else:
            self.GuaInfo['他宫内卦'] = True

        # because:some information is not in table,so it's necessary to write down in a special dict,
        # calls 'GuaInfo', a special '暂存箱'
        # example:'日主 丙',this one to one;'外卦 巽/化艮/巽化艮/反吟',this one to more

    @staticmethod
    def readText_removeComments(textfile, platform='PC'):
        if platform == 'PC' and textfile.endswith('.txt'):
            with open(textfile, 'r', encoding='utf-8') as f:
                bigtext = f.read()
        elif platform == 'Android' and isinstance(textfile, str):
            bigtext = textfile
        else:
            return ''

        pattern = r"(/\*.*?\*/|//.*?$)"
        regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

        return regex.sub("", bigtext)

    @staticmethod
    def 替代用神(yongshen: str, bigtext: str):
        # requirement: yongshen in value_dict
        # function:replace some name in BigText with 'yongshen'

        value_lis = ['父母', '兄弟', '子孙', '妻财', '官鬼']  # [定位]世爻元神，怎么替代？
        value_dict = {'用神': '妻财', '闲神': '官鬼', '仇神': '父母', '忌神': '兄弟', '元神': '子孙'}
        if any(key in bigtext for key in value_dict.keys()):

            if yongshen != '妻财' and yongshen in value_lis:
                idx = value_lis.index(yongshen)
                value_dict = {'用神': value_lis[idx], '闲神': value_lis[(idx + 1) % 5],
                              '仇神': value_lis[(idx + 2) % 5],
                              '忌神': value_lis[(idx + 3) % 5], '元神': value_lis[(idx + 4) % 5]}
            for k, v in value_dict.items():
                bigtext = bigtext.replace(k, v)
        return bigtext

    def 源文本处理(self, textfile) -> list[dict]:
        '''
        传入六爻代码文本，返回词典示例：
        [
            {'断语1': [['官鬼', '月扶', '空亡'], ['子孙伏藏']]},
            {'断语2': [['官鬼化出', '月建', '空亡']]}
        ]
        能够支持的文本逻辑：
        obj：详见代码
        string：A或B或C
        不同obj：一个句子用“，”分割
        断语：条件 “：” 断语 “。”
        '''

        # 按句分割文本

        bigtext = self.readText_removeComments(textfile, self.platform)  # 移除注释
        bigtext = self.替代用神(self.yongshen, bigtext)

        articles = bigtext.split('。')
        断语词典 = []

        for article in articles:  # article：一条条文，如“官鬼 发动：有人偷 / 妻财 发动：自己不见了。”
            if article.strip() == "":  # 移除換行、空格
                break
            elif "：" not in article:
                print("此条文没有冒号。", article)
                break

            tmp_dict = {}
            sub_articles = article.split('|')  # sub_articles：分条文，如：“官鬼 发动：有人偷”
            for sub_article in sub_articles:

                # 以冒号作为分割，分为条件和断语
                if "：" in sub_article:
                    idx = sub_article.index("：")
                    condition, saying = sub_article[:idx].strip(), sub_article[idx + 1:]
                else:
                    print('此子条文不包含冒号。', sub_article)
                    break

                # 条件按分号分割，得到分割单元列表
                condition_section = [section for section in condition.split('，') if section]  # if section:防止有空白section

                加工过的条件 = []
                for 子条件 in condition_section:
                    加工过的条件.append([item for item in 子条件.split(' ') if item])  # if item:空格 cannot be a verb

                # 加工过的条件 = [[item for item in 子条件.split(' ') if item] for 子条件 in condition_section]

                tmp_dict[saying] = 加工过的条件
            断语词典.append(tmp_dict)

        return 断语词典

    @staticmethod
    def 词典反编译(dic):
        result = ""

        for key, nested_lst in dic.items():  # key:list[list[str]]
            string = '·'
            for condition in nested_lst:
                sentence = ' '.join(condition).strip()  # 避免牵扯到换行符
                string += sentence + '，'
            result += f"{string[:-1]}：\n{key.strip()}\n"  # 截去最后的，| key通常是一个“结论”，“断语”

        return result

    @calculate_time
    def 查条文(self):
        条文箩筐 = [{}, {}, {}, {}, {}, {}, {}]
        if not self.断语词典:
            print("断语词典为空")
            return None
        for dic in self.断语词典:
            # 取出一对断语、条件，识别条件。条件为真，放进箩筐。属于第几行，放进几号筐。
            for saying, condition_dic in dic.items():
                # print("·【断语和词典】", saying, condition_dic)  # 查看总的断语
                self.line_belong = None
                if self.句子识别(condition_dic):
                    # 在此处替换saying，【bug】puzzle:replace '[逢冲逢值]' by class's element   定位
                    if self.suffix_set:
                        saying += '\n# ' + "\n# ".join(set(self.suffix_set))
                        self.suffix_set = []
                        condition_dic = [[n for n in lst if not n.startswith('%')] for lst in condition_dic]

                    if self.line_belong is None:
                        self.line_belong = 6  # print('line_belong没有定义！',saying)
                    条文箩筐[self.line_belong][saying] = condition_dic
                    self.line_belong = None
                    # print('放进箩筐！')else:print('不放进箩筐~')
                    break  # dic的一个键值对满足了就跳出，不满足继续寻找下一个键值对(spilt by separator '|',end by terminator '。')
        for i, articles_dic in enumerate(条文箩筐):
            if ResulText := self.词典反编译(articles_dic):
                print("line:", i + 1)
                print(ResulText)
            # return ResulText

    def 句子识别(self, nested_lst: list[list[str]] = None) -> bool:
        """
        功能：正常检查token；有以“或”开头的，分组器工作，分组检查token
        :param nested_lst:  形如 nested_list = [
             ["A", "B", "C"],
             ["或D", "E"],
             ["或", "F", "G"],
             ["H", "I", "J"]
         ]
        :return:
        """

        def 生成器分组(or_list, group_list):
            # “或”开头，到下一个“或”分为一组
            for i in range(len(or_list)):
                or_index = or_list[i]
                if i == 0:
                    yield group_list[:or_index]
                if i == len(or_list) - 1:
                    yield group_list[or_index:]
                else:
                    yield group_list[or_index:or_list[i + 1]]

        if any([li[0].startswith("或") for li in nested_lst]):
            或的索引列表 = [i for i, li in enumerate(nested_lst) if li[0].startswith("或")]
            # 如果存在以“或”开头的，触发分类
            genator = 生成器分组(或的索引列表, nested_lst)
            for group_list in genator:
                if all(self.动作识别(li) for li in group_list):
                    return True
            self.line_belong = None
            return False
        else:
            if all(self.动作识别(li) for li in nested_lst):
                # 嵌套列表：[[obj_1,verb,verb,],[obj_2,verb,verb,],[obj,verb,verb,],...]     li：[obj,verb,verb,]
                return True
            else:
                self.line_belong = None
                return False

    def 动作识别(self, condition_section: list[str]) -> bool:  # condition_section：[obj,verb,verb,]

        # 传入condition_section；返回idx列表，condition_section
        # 识别obj，筛选的verb。剔除筛选的verb。

        obj_idx_list, condition_section = self.对象识别(condition_section)
        if not obj_idx_list:
            # 如果obj_idx_list为空/None，说明条件不成立，返回False。
            return False
        elif obj_idx_list is True or len(condition_section) < 2:
            # obj_idx_list is True，提前跳出函数，返回True或False。仅有两个词的【短句子】。
            # 如果 condition_section 长度小于2，下文无法做判断。既然 obj_idx_list 非空，
            return True

        # if '移神' in condition_section: condition_section = [i for i in condition_section if i != '移神']; check = False
        # else:    check = True  # 防止被筛选掉

        # 假如一个【句子】中，所有单词没有以“或”开头的，拿着单词，找词典的value转function
        for string in condition_section[1:]:
            if '或' in string:  # A或B或C：类型分割。
                todo = string.split('或')
                for item in todo:
                    condition_lst = [self.select_cell(idx, item) for idx in obj_idx_list]
                    if any(condition_lst):  # A，B，C只要有一个元素为真，马上打破循环。
                        break
                else:
                    return False
            elif string.startswith('%'):  # 定位亥月癸巳日火天大有天雷无妄
                condition_lst = [True]  # 写这一段目的是什么？
                if string == '%':
                    self.save_idx_lst.extend(obj_idx_list)
                else:
                    obj_idx_list += self.save_idx_lst
                    self.save_idx_lst = []
                    self.add_suggestion_suffix(string, obj_idx_list)  # 运算之后赋值类属性【已加工】

            else:  # A，不带或字
                # obj_idx_list多元素的情况：遍历每个元素，只要有一个True即可，any
                # 原来的代码     condition = any(self.select_cell(idx, string) for idx in obj_idx_list)
                self.tmp = condition_section
                condition_lst = [self.select_cell(idx, string) for idx in obj_idx_list]

                if not any(condition_lst):
                    # condition_section[1:]每一个单词都需要过关，有一个错的就劝退
                    return False

            if (leng := len(condition_lst)) >= 2:  # and check【决定删除】
                obj_idx_list = [obj_idx_list[i] for i in range(leng) if condition_lst[i]]
                # 新改的代码，根据对错，调节obj_idx_list

        # for 循环每一个单词都过关了，才能return True
        # if self.debug:
        #     print(f"〇 condition_section: {condition_section}")
        # if condition_section[1] == '五爻':
        #     pass
        if not self.line_belong:
            self.line_belong = self.GuaImageDict["爻序"][obj_idx_list[0]] % 6
        return True

    def isTargetYao(self, YaoType: str, idx=None) -> bool:
        if idx == None:  # 你是不是想改成 not idx？这可不行，0是可以进函数的。
            idx = self.former_idxlst[0]
        yao_xu_lst = self.GuaImageDict['爻序']
        if YaoType == '变爻':
            condition = 5 < yao_xu_lst[idx] < 12 and yao_xu_lst[idx] - 6 in yao_xu_lst
        elif YaoType == '动爻':
            condition = yao_xu_lst[idx] < 6 and yao_xu_lst[idx] + 6 in yao_xu_lst
        elif YaoType == '伏神':
            condition = 12 < yao_xu_lst[idx] < 18
        elif YaoType == '主卦':
            condition = 0 <= idx < 6
        else:
            condition = False
            print('isTargetYao 进了一个不能识别的：', YaoType)
        return condition

    def 对象识别(self, condition_section) -> tuple[list[int], list[str]]:
        '''
        找到obj_lst，再根据上下文调整condition_section
        :param condition_section:
        :return:obj_lst,condition_section;[idx1,idx2,...],[obj,section1,section2,...]
        '''
        if len(condition_section) >= 3:
            obj, verb_1, verb_2 = condition_section[:3]
        else:
            obj, verb_1, verb_2 = condition_section + [None] * (3 - len(condition_section))  # 考虑下文

        # 主语obj 带有”或“字，需要分割
        if '或' in obj:
            if obj.startswith('或'):  # 只是一个识别的符号，截去，不能带“或”字开头
                obj = obj[1:]
            else:
                obj_lst = []
                for sub_obj in obj.split('或'):
                    result, condition_section = self.对象识别([sub_obj] + condition_section[1:])
                    if isinstance(result, list):
                        obj_lst += result
                    elif result is True:
                        obj_lst = result
                        break
                    elif result is False:
                        obj_lst = result
                    else:
                        print('不希望的主语：', condition_section)
                        return [], condition_section

                return obj_lst, condition_section

        verb_li = [verb for verb in [verb_1, verb_2] if verb in self.lines_animals and verb not in '月建|日辰']  # 起码

        def filter_and_drop(IdxList, ConditionSection):
            # 过滤和筛选：verb_li非空时触发
            for verb in verb_li:
                ConditionSection = [i for i in ConditionSection if i != verb]
                try:
                    IdxList = [num for num in IdxList if self.GuaImageDict['爻序'][num] % 6 == self.lines_animals[verb]]
                except TypeError:
                    lst = [self.GuaImageDict['爻序'][num] for num in IdxList]
                    print('这一条写的有问题：', ConditionSection, '结果是：', lst)
            return IdxList, ConditionSection

        def check_former_idx():
            if not self.former_idxlst:  # 与前文所提及的 主语obj 密切相关
                return []

            idx = self.former_idxlst[0]
            lst = self.GuaImageDict['爻序']
            idx_lst = []

            if obj == '入卦':  # 变爻（爻序）
                idx_lst = self.主卦六亲索引(self.GuaImageDict['六亲'][idx]) if self.isTargetYao(
                    '变爻') else []
            elif obj == '此动爻':
                idx_lst = [lst.index(lst[idx] - 6)] if self.isTargetYao('变爻') else []
            elif obj == '化出':
                idx_lst = [lst.index(lst[idx] + 6)] if self.isTargetYao('动爻') else []
            elif obj == '飞神':
                idx_lst = [lst[idx] % 6] if self.isTargetYao('伏神') else []
            elif obj == '飞神化出':
                cond = self.isTargetYao('伏神') and self.isTargetYao('动爻', lst[idx] % 6)
                idx_lst = [lst.index(lst[idx] - 6)] if cond else []
            return idx_lst

        if obj in self.暂存箱:
            idx_list = self.暂存箱[obj]
            # current:take it out
            # puzzle:some place is up to memory, cannot use 'self.暂存箱[obj] = idx_list' to add to 'self.暂存箱[obj]',
            # solution:this case 'cannot add' can be the following 'elif' ,the case need to add in else (unsure be another loop)

        elif obj in ['墓库', '该爻']:
            idx_list = [self.Memory_idx] if self.Memory_idx else []
        elif obj in ['此动爻', '入卦', '化出', '飞神', '飞神化出']:
            idx_list = check_former_idx()
        elif obj in ['三合局', '半合局', '三刑']:
            idx_list = self.last_idx_group
        elif obj in self.GuaInfo:
            '''
            it is already a 暂存箱 ,can directly access and not necessary to save once again!
            【说明】此类句子只有两个单词.
            example:六合；独发；主卦 谦；卦宫五行 土；外卦 化艮 / 巽化乾 / 巽
            '''
            if not verb_1:  # example:'六合 / 独发:True'
                return self.GuaInfo[obj], condition_section
            elif '或' in verb_1:  # A或B或C：类型分割。
                todo = verb_1.split('或')
                if any(item in self.GuaInfo[obj] for item in todo):  # A，B，C只要有一个元素为真，返回True。
                    return True, condition_section
                return False, condition_section
            else:
                try:
                    condition = verb_1 in self.GuaInfo[obj]
                    return condition, condition_section
                except TypeError:
                    print('为何 verb_1 is bool?', '-'.join(condition_section))
                    return True, condition_section
        else:
            # 找到 并储存 主语obj 对应的 idx_list:[idx:int]
            # all the case of 'obj' in this 'else',write down in 'self.暂存箱[obj]' as a fixed value in the end,so that
            # next time will not go to this 'else'
            if obj in LIU_QIN:
                idx_list = self.主卦六亲索引(obj)
                if verb_1 and verb_1 in ['持世', '临应', '六爻', '五爻', '四爻', '三爻', '二爻', '初爻']:
                    idx_list = [] if idx_list[0] >= 12 else idx_list  # 【bug】以前为了限制'伏神持世'

            elif obj in self.lines_animals:
                idx_list = [self.lines_animals[obj]]  # example: 二爻 生世；朱雀 发动
            elif obj in '子丑寅卯辰巳午未申酉戌亥|金木水火土':
                idx_list = self.idx_set(obj)

            elif obj in ['父母伏藏', '兄弟伏藏', '子孙伏藏', '妻财伏藏', '官鬼伏藏']:
                # using two chars find out 'idx_list',such as : [14],List[int]
                idx_list = self.伏藏索引(obj[:2])

            elif obj in ['父母化出', '兄弟化出', '子孙化出', '妻财化出', '官鬼化出']:
                idx_list = self.变爻索引(obj[:2])

            elif obj in ['父母两现', '兄弟两现', '子孙两现', '妻财两现', '官鬼两现']:
                # FindHide = verb_1!='持世'
                idx_list = self.主卦六亲索引(obj[:2])
                if len(idx_list) != 2:  # 不是两现，劝退
                    return False, condition_section
                if not verb_1:  # 没有下文【verb】就返回对错
                    return True, condition_section
            elif obj in '月建|日辰':
                idx_dic = {'日辰': [-1], '月建': [-2]}
                idx_list = idx_dic[obj]

            else:
                # the case can't identify,must return right now...
                print(f"碰到无法处理的情况。主语是：【{obj}】，完整断语：【{'-'.join(condition_section)}】。")
                return [], []

            self.暂存箱[obj] = idx_list

        if '持世' in verb_li:  # 对‘伏神持世’优化
            idx_list = [n for n in idx_list if n < 6]

        if verb_li:
            idx_list, condition_section = filter_and_drop(idx_list, condition_section)

        self.former_idxlst = idx_list  # 记住前一个obj[new]

        return idx_list, condition_section

    def select_cell(self, idx: int, string: str, add_to_memory=True, condition=False) -> bool:
        """
        检查单元格：选择一个单元格，判断是不是
        实现一次对错判断。并且利用记忆化搜索，尽量保证不再判断第二次。
        :param idx: 形如GID词典={key:[item1,item2,...]}，指定了item的索引，也是表格的行索引
        :param string: 利用此变量，非常灵活的切换检查的行列。规则较为繁琐。
        :param add_to_memory:是否加入记忆，方便记忆化搜索？
        :return: True|False，完成一次对错判断
        """
        if not isinstance(idx, int):
            print(idx, string, '★★★★ 此处有误，类型为', type(idx))
        if idx not in self.暂存箱:  # 若“暂存箱”没有 键idx的记录，则创建
            self.暂存箱[idx] = {}
        elif string in self.暂存箱[idx]:  # 若“暂存箱”已有 键idx、string的记录，则利用
            condition = self.暂存箱[idx][string]
            return condition

        if string.startswith('非'):  # 暂时不加入暂存箱
            string = string[1:]
            return not self.select_cell(idx, string)

        convert_string_alive = {
            '变爻列标志': {
                # using 'idx' to adjust col_name
                '回头生': [str(18 + idx * 3), '生'], '回头克': [str(18 + idx * 3), '克'],
                '化合': [str(19 + idx * 3), '合'],
                '化长生': [str(20 + idx * 3), '长'], '化沐浴': [str(20 + idx * 3), '沐'],
                '化死地': [str(20 + idx * 3), '死'],
                # 为什么是18，19，20？主卦才有化死地，化墓，主卦的idx一定小于6
                '化墓': [str(20 + idx * 3), '墓'],
                '化绝': [str(20 + idx * 3), '绝'], '化进': [str(18 + idx * 3), '进'],
                '化退': [str(18 + idx * 3), '退']},
            '行列重置': {
                '合二爻': [4, str(1 + self.GuaImageDict['爻序'][idx] * 3), '合'],
                # '合世爻': [self.self_posit, str(1 + idx * 3), '合'],
            }
        }

        if string in self.convert_string['外部函数']:
            dizhi, value, funtion = self.convert_string['外部函数'][string]

            self_dizhi = self.GuaShu_li[dizhi] % 12
            active_dizhi = self.GuaImageDict['60六亲'][idx] % 12
            condition = funtion(self_dizhi, active_dizhi) == value

        elif string in self.convert_string['动爻列标志']:
            '''
            检查表格的一列或多列（col_range）。找到符合条件的列时，列号转为动爻的idx，加入记忆。
            例如：
            妻财伏藏 死地发动   pure_posi>=12
            官鬼化出 回头克；   pure_posi<12
            妻财持世 回头克    pure_posi<6     【注】pure_posi 两种范围 代表 主卦和伏藏，is valid_line_range
            '''
            col_range, value = self.convert_string['动爻列标志'][string]
            if self.isTargetYao('变爻', idx) or col_range == []:  # valid_line_range:主卦和伏藏;自检测：list:[key]非空
                self.暂存箱[idx][string] = False
                return False
            for col in col_range:
                if condition := self.GuaImageDict[col][idx] == value:
                    self.Memory_idx = int(col) // 3  # col_range in special decoding way,动爻列(客) 转 idx(主)
                    # convert table_column(动变爻对应的列) to table_row(as well as idx) and save
                    break
            if string == '入动墓' and condition and self.Memory_idx not in self.暂存箱['动墓']:
                self.vary_mort_IdxSet(idx)

        elif string in '阴阳':
            if self.isTargetYao('伏神', idx):
                return False
            string_map = {0: '阴', 1: '阳'}
            condition = string == string_map[self.coinsNumber_list[idx] % 2]

        elif string in ['三合局', '半合局', '外三合局']:
            condition = self.find_sanhe(idx, string)

        else:  # 这些都是通过查询GID（比对dict的key，idx对应的值 == value？）实现判断

            if string in self.convert_string['六亲六神']:  # 包括 所有 六亲、六神、地支、返卦、五行
                key, value = self.convert_string['六亲六神'][string]
            elif string in self.convert_string['日月发动世应']:  # 包括 所有 日月 生克扶、冲合值、十二长生、刑、下一个四值；动爻 类型
                key, value = self.convert_string['日月发动世应'][string]
            elif string in convert_string_alive['变爻列标志']:  # string_value_range:(化墓,化合,回头生) ; valid_idx:for all 动爻
                # 不必变更，按照 上述词典对表格。不符合条件劝退
                if idx >= 6 or self.trigger_li[idx] == 0:  # valid_test:只有 主卦 发动，才有。否则在这里要劝退。
                    self.暂存箱[idx][string] = False
                    return False
                key, value = convert_string_alive['变爻列标志'][string]
            elif string.endswith('同宫'):  # 父母同宫？
                string = string[:-2]

                if string in self.lines_animals:
                    n = self.lines_animals[string]
                    if n == idx:  # 自己和自己同宫，没有意义
                        return False
                    key, value = ['返卦', self.GuaImageDict['返卦'][n]]
            elif string in '外卦|内卦|世上|世下|应上|应下|伏藏':
                rank = self.GuaImageDict['爻序'][idx]
                value_dict = {
                    # '六爻': self.GuaImageDict['爻序'][idx] if self.GuaImageDict['爻序'][idx] % 6 == 0 else False,
                    '外卦': idx if rank % 6 < 3 else False, '内卦': idx if 3 <= rank % 6 <= 5 else False,
                    '世上': self.self_posit - 1 if self.self_posit > 0 else False,
                    '世下': self.self_posit + 1 if self.self_posit < 5 else False,
                    '应上': self.other_posit - 1 if self.other_posit > 0 else False,
                    '应下': self.other_posit + 1 if self.other_posit < 5 else False,
                    '伏藏': idx if rank >= 12 else False,

                }
                key, value = '爻序', value_dict[string]

            elif string in self.convert_string['变爻行标志']:
                # 变更 表格检测行的idx 变更为变爻行idx。加入记忆。不符合条件劝退
                key, value = self.convert_string['变爻行标志'][string]
                if idx >= 6 or self.trigger_li[idx] == 0:  # 【主卦】【发动】才有化空亡、化月破
                    self.暂存箱[idx][string] = False
                    return False

                idx = self.GuaImageDict['爻序'].index(idx + 6)  # 化墓 在子孙；化空亡 在子孙
                self.Memory_idx = idx
                add_to_memory = False  # 不加入记忆

            elif string.endswith('变爻'):  # former_string_range=(变爻冲,变爻合);current_string_range=(世爻变爻,)
                if not 5 < self.Memory_idx <= 11:
                    return False
                string = string[:-2]  # 去掉“变爻”
                key, value = self.convert_string['六亲六神'][string]  # 取 动爻列 and 需要比对的信息
                n = self.GuaImageDict['爻序'].index(self.Memory_idx)
                # 变爻爻位 转 idx，find out the index of 'self.Memory_idx'
                idx = int(self.GuaImageDict['发动'][n])  # 变爻idx 转 动爻idx
                add_to_memory = False

            elif string[0] in '冲|合':
                if string[1:] in LIU_QIN:
                    key, value = f'{string[0]}六亲', string
                elif string[1:] in yao_wei:
                    key, value = f'{string[0]}爻位', string
                elif string[1:] in '世|应':
                    key, value = f'冲合{string[1:]}', string
                else:
                    print(string, f'其中的【{string[1:]}】是不规范的字符！注：冲世|合世|冲应|合应')

            elif string[:2] in '父母|兄弟|子孙|妻财|官鬼|世爻|应爻' and string[2:] in round_12_brif:  # 查询 长生十二长生状态
                key, value = f'{string[:2]}地', string

            elif string in convert_string_alive['行列重置']:  # extend_type.大规模 调整 idx, key, value
                idx, key, value = convert_string_alive['行列重置'][string]
                add_to_memory = False
                if key not in self.GuaImageDict:
                    return False

            elif string.startswith('在'):  # former_string_range=(入动墓,化墓,病地发动);current_string_range=(在子孙,在妻财,)
                string = string[1:]  # 去掉“在”
                key, value = self.convert_string['六亲六神'][string]
                idx = self.Memory_idx
                add_to_memory = False

            try:  # 因为不知道用户会输入什么奇怪的字符
                condition = self.GuaImageDict[key][idx] == value
            except TypeError:
                print(self.tmp, key, idx, '\n※    这里有一个类型错误！')
            except UnboundLocalError:
                print("※    未能识别的字符串:", string, "\n※    当前表格行:", idx, "\n※    完整句子:", self.tmp)

        if add_to_memory:
            self.暂存箱[idx][string] = condition  # 确认添加，则加入记忆

        return condition

    '''all the following fuction is zombie,seldom raise error'''

    def idx_set(self, obj: str) -> list[int]:
        column_dic = {
            '子丑寅卯辰巳午未申酉戌亥': '支',
            '木火土金水': '五行'
        }
        for key in column_dic:
            if obj in key:
                col = column_dic[key]
                return [i for i, item in enumerate(self.GuaImageDict[col]) if obj == item]
        else:
            print('非法的参数obj！', obj)
            return []

    def 主卦六亲索引(self, 主卦六亲: str) -> list[int]:
        li = [i for i in range(6) if self.GuaImageDict['六亲'][i] == 主卦六亲]
        if li == []:
            li = self.伏藏索引(主卦六亲)
        return li

    def 伏神(self, sup=18, low=12):
        idx_lst = []
        lst = self.GuaImageDict['爻序']  # 这是升序的数组，倒着数更快
        for idx in range(len(lst) - 1, -1, -1):
            if low <= lst[idx] < sup:
                idx_lst.append(idx)
            elif lst[idx] < low:
                break
        return idx_lst
        # return [i for i,num in enumerate(self.GuaImageDict['爻序']) if 12 <= lst[i] < 18]，比这个快一倍
        # 伏神函数执行时间： 4.297473999904469e-07 秒，fu_shen函数执行时间： 8.178255999810063e-07 秒

    def 伏藏索引(self, 伏藏六亲: str) -> list[int]:
        # 所有伏藏位置的列为备选，用if筛选
        return [i for i in self.暂存箱['伏神'] if self.GuaImageDict['六亲'][i] == 伏藏六亲]

    def 变爻索引(self, 动爻六亲: str = None, 动爻索引: list[int] = None, 变爻六亲: str = None) -> list[int]:
        # 动爻六亲，求变爻
        # solution:所有变爻位置的列为备选，用if筛选
        yao_xu_lst = self.GuaImageDict['爻序']
        if 动爻六亲:
            return [yao_xu_lst.index(i + 6) for i in self.暂存箱['动爻'] if
                    self.GuaImageDict['六亲'][i] == 动爻六亲]
        elif 动爻索引:
            # 最好加一个限制，动爻索引列表 all in [0,1,2,3,4,5]  ，表格的规律是这样的
            return [yao_xu_lst.index(i + 6) for i in 动爻索引 if self.trigger_li[i]]
        elif 变爻六亲:
            return [i for i in self.暂存箱['变爻'] if self.GuaImageDict['六亲'][i] == 动爻六亲]
        else:
            print('动爻六亲，动爻序号，变爻六亲 必须输入一个！')
            return []

    def vary_mort_IdxSet(self, idx: int):
        # 主卦里 和 '入墓 同六亲' make idx_lst；'入墓又发动 化出' make idx_lst；  '动墓'有两个 【solution】
        li = self.GuaImageDict['六亲']
        rumu = self.主卦六亲索引(li[idx])
        rumu_out = self.变爻索引(动爻索引=rumu)
        vary_mu = [i for i in range(6) if li[self.Memory_idx] == li[i] and self.trigger_li[i]]
        vary_mu_out = self.变爻索引(动爻索引=vary_mu)
        vm_dict = {
            '入墓': rumu, '入墓化出': rumu_out, '入墓逢冲': self.冲用神(idx),
            '动墓': vary_mu, '动墓化出': vary_mu_out
        }  # '化墓'怎么处理？你给我指定一个idx       【solution】用神化出
        self.暂存箱.update(vm_dict)
        # print(self.暂存箱)

    def add_idxlst(self) -> dict:
        # 一爻动变时，启用 || 以下三个函数，后来看不懂了
        onevary_obj_lst = ['独发', '独发化出', '所冲', '所合', '变爻所冲', '变爻所合']
        idx_lst = [self.trigger_li.index(1)] if sum(self.trigger_li) == 1 else []
        self.暂存箱.update(self.find_obj_idxlst(onevary_obj_lst, idx_lst))

        # 世爻发动时，启用
        obj_lst = ['世爻', '世爻化出', '世爻所冲', '世爻所合', '世爻变爻所冲', '世爻变爻所合']
        idx_lst = [self.self_posit] if self.trigger_li[self.self_posit] else []  # 世爻那行 '发动'，留下
        self.暂存箱.update(self.find_obj_idxlst(obj_lst, idx_lst, self.self_posit))

    def find_obj_idxlst(self, obj_lst: list[str], idx_lst: list[int], init_idx=None) -> dict:
        '''
        一个功能性函数，计算obj对应的idx_lst
        好处：使得你的编写的obj命令能指向特定的idx
        '''
        vary_info_dict = dict()
        for obj in obj_lst:
            vary_info_dict[obj] = []  # initial obj to idx_lst's dict.

        if init_idx:  # primary_idx:from 0 to 17. If you do not want all [],and First One must be written down ： ↓
            vary_info_dict[obj_lst[0]] = [init_idx]

        if len(idx_lst) != 1:  # 要求：独发，传入空列表，提前退出
            return vary_info_dict

        active_columns_1 = {  # 键（按照特定的方法，idx换算成键）：col， 值：key_lst
            str(idx_lst[0] * 3 + 1): [obj_lst[2], obj_lst[3]], str(idx_lst[0] * 3 + 19): [obj_lst[4], obj_lst[5]]
        }
        n = self.GuaImageDict['爻序'].index(6 + idx_lst[0])
        vary_info_dict[obj_lst[0]] = idx_lst
        vary_info_dict[obj_lst[1]] = [n]
        for col, obj_lst in active_columns_1.items():
            value = self.GuaImageDict[col]
            vary_info_dict[obj_lst[0]] = [idx for idx, v in enumerate(value) if v == '冲']  # 能找到相冲相合，就加入，找不到，[]
            vary_info_dict[obj_lst[1]] = [idx for idx, v in enumerate(value) if v == '合']
        return vary_info_dict

    def find_sanhe(self, idx: int, mode='半合局') -> bool:
        if mode == '外三合局':
            wx = self.GuaImageDict['五行'][idx]  # '外三合局'：内外卦大象和五行同时满足一组条件
            _out, _inner = self.GuaInfo['外卦'][-1], self.GuaInfo['内卦'][-1]
            condition_1 = (_out, wx) in [('兑化巽', '木'), ('艮化震', '火'), ('离化坤', '金')]
            condition_2 = (_inner, wx) in [('兑化巽', '金'), ('艮化震', '水'), ('离化坤', '木')]
            condition = condition_1 or condition_2
            return condition

        # step:select in ['亥卯未', '申子辰', '巳酉丑', '寅午戌'];采集 符合条件的 IdxSet convert to ZhiSet;selected all in ZhiSet
        # function:find out 完整的 三合局,return True
        target_range = list()
        zhi_value = self.GuaImageDict['支'][idx]
        if not self.GuaImageDict['发动'][idx] or zhi_value not in '子午卯酉':
            return False
        for qroup_str in ['亥卯未', '申子辰', '巳酉丑', '寅午戌']:
            if zhi_value in qroup_str:
                target_range = [i for i in qroup_str]  # '子午卯酉' must have one,so 'target_range' is not []
                break

        idx_li = []  # correct ActiveLine's idx,  【bug】if you want to access other 合局地支,make idx_li global.
        for i, v in enumerate(self.GuaImageDict['发动']):
            if v == '暗动' or v == '发动' or (v and v.isdigit() and int(v) in idx_li):
                idx_li.append(i)
                # v 的可能范围:None,'6','暗动','发动'

        zhi_total = [self.GuaImageDict['支'][i] for i in idx_li]  # for corrected_idx convert to zhi
        zhi_total += [ZHI[self.date % 12]] + [ZHI[self.month % 12]]  # 借日月成局

        if mode == '半合局':
            target_range_lst = [target_range[:2], target_range[1:]]  # 出错说明lst不足，zhi_value不是正常数据
        else:  # '三合局'
            target_range_lst = [target_range]

        idx_lst = []
        condition = False
        for target in target_range_lst:
            if all(ele in zhi_total for ele in target):  # '三合局''半合局'的字 全部都有
                condition = True
                for m, n in zip(idx_li, zhi_total):  # 筛选出 符合条件 idx_lst
                    if n in target:
                        idx_lst.append(m)
            self.last_idx_group = idx_lst

        return condition

    def add_suggestion_suffix(self, string, idx_lst):
        def find_high_accurcy(dic: dict, input_group, accury_rate=0.8):
            # 这个函数，在dic里找到吻合率高的条目，加入self.suffix_set待用，删去dic中已加入的条目，并且返回（保证不会出现第二次）
            written_groups = []
            for group in dic.keys():
                length = len(group)
                match_count = len(set(group) & set(input_group))
                rate = match_count / length
                if rate >= accury_rate:
                    self.suffix_set.append(' '.join(group) + "：" + dic[group])
                    written_groups.append(group)

            for group in written_groups:
                del dic[group]
            return dic

        def ReadTxtFile(bigtext):
            dic = dict()
            articles = bigtext.split('。')
            for article in articles:  # article：一条条文，如“官鬼 发动：有人偷 / 妻财 发动：自己不见了。”
                if article.strip() == "":  # 移除換行、空格
                    break
                if "：" not in article:
                    print("此条文没有冒号。", article)
                    break
                else:
                    idx = article.index("：")
                    condition, saying = article[:idx].strip(), article[idx + 1:]
                    condition = [item for item in condition.split(' ') if item]

                dic[tuple(condition)] = saying
            return dic

        def tap_filter(key, idx):
            if key in self.GuaImageDict:
                return self.GuaImageDict[key][idx]
            elif self.select_cell(idx, key):
                replace_dic = {'化空亡': '空亡', '化月破': '月破', '化日冲': '日冲', '空': '空亡'}
                if key in replace_dic:
                    key = replace_dic[key]
                return key

        extra_idx_lst = []
        if '移神' in string:
            string = string.replace('移神', '')
            lst = self.GuaImageDict['爻序']  # 【移 神 法 则】没让移神就不要移神了，出来太多字了。||没有看懂移神的逻辑。
            idx = idx_lst[0]
            if self.isTargetYao('主卦', idx) or self.isTargetYao('变爻', idx):
                hide_zhi = idx_lst[0] + 12  # 主卦，有伏神的话，需要移神； 变爻，移神入卦的六亲；看不懂，在主卦，你移神移到伏藏干什么？
                idx_lst = idx_lst + [lst.index(hide_zhi)] if hide_zhi in lst else idx_lst
                lq_value = self.GuaImageDict['六亲'][idx_lst[0]]
            elif self.isTargetYao('伏神', idx):
                lq_value = self.GuaImageDict['六亲'][rank % 6]
            else:
                print('obj_idx_list是错误值:', ' '.join(idx_lst))
                return True
            extra_idx_lst = [n for n in self.主卦六亲索引(lq_value) if n not in idx_lst]

        string = string[1:]  # string:'%static_vision（六神，六亲）'appendix=(string,),
        file_name, key_str = string.split('（', 1)
        key_lst_1 = ['爻位', '六神', '六亲', '五行']
        key_lst_2 = ['返卦', '世应', '空亡', '世爻地', '应爻地', '妻财地', '官鬼地', '父母地', '兄弟地', '子孙地']
        key_lst_added = [part for part in key_str[:-1].split('-') if part]

        if self.platform == 'PC':
            file_path = f'data/vision/{file_name}.txt'
        else:
            file_path = 'general_vision_text'

        if file_path != self.current_file_path:
            self.current_file_path = file_path
            text = self.readText_removeComments(file_path, self.platform)  # 打开文件，初步清理
            self.text_dic = ReadTxtFile(text)  # 读取文本，按格式分割

        def get_info_set(key_list: list[str], idx_list: list[int]):
            # 点名几个座位idx，点名几个科目key，放进一个麻袋里，去重
            key_set = set(key_list)
            return set(tap_filter(key, idx) for key in key_set for idx in idx_list)
            # 有缺陷，爻位出来是0-17，世应同宫也不好表示【改进】%移神

        input_set = get_info_set(key_lst_1 + key_lst_2 + key_lst_added, idx_lst)
        if extra_idx_lst:
            extra_input_set = get_info_set(key_lst_1 + key_lst_added, extra_idx_lst)
            input_set.update(extra_input_set)
        input_set.add(self.GuaInfo['卦宫'][0])
        self.text_dic = find_high_accurcy(self.text_dic, input_set)

        return True

    def 冲用神(self, idx: int = None):
        # assume:id only one        一定要找到一个 相冲，找不到 移神 同六亲

        if not idx:
            idx = self.主卦六亲索引(self.yongshen)[0]

        Num_ = self.GuaImageDict['60六亲'][idx]
        try:
            Num = LIU_QIN_NUM_60[self.Gua_wx][xiangchong(Num_) % 12]
        except IndexError:
            print('排查 self.Gua_wx,xiangchong(Num_) = ', self.Gua_wx, xiangchong(Num_))
            return []
        idx_lst = [i for i, m in enumerate(self.GuaImageDict['60六亲']) if m == Num]
        if idx_lst == []:
            idx_lst = self.主卦六亲索引(LIU_QIN[Num // 12])
        return idx_lst


def find_duplicates(lst1: list[str], lst2: list[int]):
    '''
    给定两个相同长度的列表，找到list[str]的第一对相同元素，取list[int]对应位置的元素，俱减6作为列表返回。
    :param lst1: 表格的['支']
    :param lst2: 表格的['爻序']0-17，有缺失
    :return: idx_lst = [动爻1的idx,动爻2的idx],特征是变爻（表格的['爻序']在6-11）有相同的支
    '''
    # hash_dic = {key:num for key,num in zip(lst1,lst2) if 6<=num<=11} 如果两个不同的键映射到相同的值，那么只有最后一个键值对会被保留在字典中
    hash_dic = dict()
    for key, num in zip(lst1, lst2):
        if num < 6 or num > 11:
            continue
        if key in hash_dic:  # 同变爻的两个动爻，6-11减6就是原来的动爻
            return [hash_dic[key] - 6, num - 6]
        else:
            hash_dic[key] = num  # 键就是seen 元素。键未存在，从未见过；键已经存在，取出对应的值使用。
    return []


# 使用示例
# bigtext = "官鬼 月扶 空亡；子孙 持世：有工作不干了。\n官鬼化出 月建 空亡：工作不顺。"

# [一个应用示例demo]
# bigtext = "工作篇.txt"
# 机器语言转换器 = ConvertTextToCode()
# 词典列表 = 机器语言转换器.源文本处理(bigtext)
# print(词典列表)
# text = 机器语言转换器.词典反编译(词典列表)
# print(text)


class CellEditorWindow(QMainWindow):
    def __init__(self, cell_params, text=[]):
        super().__init__()

        self.cell_params = cell_params

        # 创建comobox
        self.combo_box = QComboBox()
        for param in cell_params:
            self.combo_box.addItem(f"{param[0]}")  # 将每个参数项添加到comobox中
        self.combo_box.currentIndexChanged.connect(self.load_cell_content)

        # 创建文本编辑框
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', Courier, monospace;  /* 设置字体为编程字体 */
                font-size: 30px;                                  /* 设置字体大小 */
                line-height: 3;                                 /* 设置行高为字体高度的1.5倍【设置了没用】 */
                border: 1px solid grey;                           /* 设置边框为1px灰色实线 */
                padding: 5px;                                    /* 设置内边距为5像素 */
            }
            QTextEdit:focus {
                border: 2px solid grey;                         /* 设置焦点状态下的边框为2px白色实线 */
            }
        """)
        self.msg_label = QLabel('正在查看内容...')

        # 创建保存按钮
        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_cell)

        # 创建Grid布局
        grid_layout = QGridLayout()
        buttons = ['<物象>', '<人物>', '<人事>', '<气运>', '<财运>', '<名次>', '<工作>', '<文书>', '<失物>', '<身体>',
                   '<姓名>', '<化解>',
                   '<出行>', '【期】', '【事】', '【物】'
                   ]  # 按钮列表
        buttons += text
        for i, button_text in enumerate(buttons):
            button = QPushButton(button_text)
            button.clicked.connect(lambda _, text=button_text: self.insert_char(text))
            grid_layout.addWidget(button, i // 4, i % 4)  # 按钮按4个一排布局

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.msg_label)
        layout.addWidget(self.text_edit)
        layout.addLayout(grid_layout)  # 添加grid布局
        layout.addWidget(save_button)

        # 创建窗口主部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.resize(1200, 1200)
        self.setWindowTitle('编辑备注信息')

        # 初始加载第一个单元格的内容
        self.load_cell_content(0)

    def load_cell_content(self, index):
        csv_file, row_number, column_number = self.cell_params[index]
        # 读取原单元格的内容
        self.cell_content = read_specific_cell(csv_file, row_number, column_number)
        self.text_edit.setPlainText(self.cell_content)

    def save_cell(self):
        new_cell_content = self.text_edit.toPlainText()
        csv_file, row_number, column_number = self.cell_params[self.combo_box.currentIndex()]

        # 保存修改后的内容到原来的CSV单元格
        with open(csv_file, 'r', encoding='gbk', newline='') as file:
            rows = list(csv.reader(file))
            if not rows:
                self.msg_label.setText(f'⚠ 你在一个空文件保存了，至少填写到{row_number}行{column_number}列')
                return
            rows[row_number - 1][column_number - 1] = new_cell_content
        with open(csv_file, 'w', encoding='gbk', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        self.msg_label.setText(f"新内容'{new_cell_content[:9]}',修改成功！")

    def insert_char(self, text):
        cursor = self.text_edit.textCursor()
        # cursor.insertText(cursor.position(), text)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)


"""计算公式"""


def xiangchong(num):
    num = num % 12
    return num - 6 if num > 6 else num + 6


def xianghe(num):
    num = num % 12
    return 3 - num if num < 3 else 15 - num


def 冲合值(地支: int, 活跃地支: int):
    相冲 = xiangchong(活跃地支)
    相合 = xianghe(活跃地支)
    相害 = xianghe(相冲)
    if 地支 == 活跃地支:
        return "值"
    elif 地支 == 相冲:
        return "冲"
    elif 地支 == 相合:
        return "合"
    elif 地支 == 相害:
        return "害"
    else:
        return ""


def 生扶克(地支: int, 活跃地支: int, 变爻=False):
    # 【注意】必须输入0-12，否则就会崩溃
    if 活跃地支 is None or 地支 is None:
        print(f'出错了！！活跃地支是：【{活跃地支}】', f'地支是：【{地支}】')
        return ''

    li = [[2, 5, 8, 11], [9, 10], [1, 13, 12, 0], [3, 4], [6, 7]]
    for i in range(5):
        if 地支 in li[i]:
            地支序 = i
        if 活跃地支 in li[i]:
            活跃地支序 = i
    if 变爻:
        text = "退" if 地支 > 活跃地支 else "进" if 地支 < 活跃地支 else "吟"
        res_li = [text, '生', '克', '', '']
    else:
        res_li = ["扶", '生', '克', '', '']
    try:
        res = res_li[(地支序 - 活跃地支序 + 5) % 5]
        return res

    except UnboundLocalError:
        print('地支，活跃地支：', 地支, 活跃地支)
        return ''


def 刑(地支: int, 活跃地支: int):
    li_item = [[3, 6, 9], [5, 7, 10, 12, 0], [1, 4, 13], [2, 8, 11]]
    if 地支 == 活跃地支 and 地支 not in [5, 7, 10, 12, 0]:
        return ''
    for li in li_item:
        if 地支 in li:  # 如果“地支”在某一组中，再判断“活跃地支”在不在。不在同一组直接break，减少不必要的判断次数。
            if 活跃地支 in li:
                return '刑'
            else:
                return ''


def 计数刑(地支: int, 活跃地支列表: list[int]):
    num = sum(1 for 活跃地支 in 活跃地支列表 if 刑(地支, 活跃地支))
    return num


# def isAndroid():
#     return "ANDROID_DATA" in os.environ

'''for PC which is able to import csv file'''


def get_path_idx(trigger_li: list[int], gua_num: int):
    # get this status's idx
    n = sum(trigger_li)

    if n == 1:
        path = 'load_csv/Gua_OneLineVary.csv'
        idx = trigger_li.index(1) + 7  # 前6列是阴阳，用于定位一个卦；从第7列开始选择
        # example:6爻发动为0，table's column is 对应7；1爻发动为5，table's column is 12
    elif n == 2:
        # path = 'load_csv/Gua_MutiLineVary.csv'
        # idx = coins_to_idx(self.trigger_li, n) + 7
        path = 'load_csv/二爻动.csv'
        idx = trigger_list_to_idx(trigger_li, n) + 1
    elif n == 3:
        path = 'load_csv/三爻动.csv'
        idx = trigger_list_to_idx(trigger_li, n) + 1
    elif n == 4:
        path = 'load_csv/四爻动.csv'
        idx = trigger_list_to_idx(trigger_li, n) + 1
    elif n == 5:
        path = 'load_csv/五爻动.csv'
        idx = trigger_li.index(0) + 1
    else:
        return None

    if 1 <= n <= 5:
        # 检查文件是否存在
        if not os.path.exists(path):
            # 如果文件不存在，则创建文件
            with open(path, 'w', encoding='utf-8') as file:
                # 写入空字符串，代表创建了一个空文件
                file.write('')

        return (path, gua_num + 2, idx)


def trigger_list_to_idx(li, n):
    '''
    计算这个动变的序号。（二爻动，三爻动，四爻动）
    :param li: trigger_list,只有0和1的6位列表。
    :param n: trigger_list为1的个数。
    :return: 序号。
    '''
    # requirement:all(num in [0,1] for num in li),len(li)==6
    li = list(reversed(li))  # 反转变成：[初爻，二爻，三爻，四爻，五爻，六爻]
    if n in [2, 4]:
        idx_1, idx_2 = [i for i, value in enumerate(li) if value == (n / 2) % 2]  # 2==>1,4==>0
        bi_vary_initial_table = [-1, 3, 6, 8, 9]
        return bi_vary_initial_table[idx_1] + idx_2
    elif n == 3:
        idx_1, idx_2, idx_3 = [i for i, value in enumerate(li) if value == 1]
        initial_table = {  # all possible status of [ idx_1, idx_2, idx_3 ]
            (0, 1): -2, (0, 2): 1, (0, 3): 3, (0, 4): 4,
            (1, 2): 7, (1, 3): 9, (1, 4): 10,
            (2, 3): 12, (2, 4): 13, (3, 4): 14
        }
        return initial_table[(idx_1, idx_2)] + idx_3


def read_specific_cell(csv_file, row_number, column_number):
    # 读取词典的某个单元格，节省内存
    try:
        with open(csv_file, 'r', encoding='gbk', newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i + 1 == row_number:  # 找到指定行
                    if column_number <= len(row):  # 确保指定的列存在于该行中
                        return row[column_number - 1]  # 返回指定列的数据
    except FileNotFoundError:
        if not os.path.exists(csv_file):
            # 如果路径不存在，创建路径
            os.makedirs(csv_file)
            with open(csv_file, 'w', encoding='gbk') as file:
                file.write('六,五,四,三,二,初')
                print(f"{csv_file}文件不存在！已为您自动创建...")


"""
使用方法如下：
csv_file = 'Gua_OneLineVary.csv'
row_to_read = 17  # 要读取的行号，卦序号+2
column_to_read = 7  # 要读取的列号，7为六爻，12为初爻
result = read_specific_cell(csv_file, row_to_read, column_to_read)

print(result)

"""

"""命爻部分"""


def import_mingyaoData():
    from collections import defaultdict

    # 创建一个默认字典，当键不存在时，会自动创建对应的默认值
    ddict = defaultdict(list)

    # 打开csv文件，使用csv.reader()函数读取数据
    with open('load_csv/mingyao.csv', 'r', encoding='gbk') as file:
        reader = csv.reader(file)
        # 读取第一行作为键
        keys = next(reader)
        # 读取剩下的行，将数据存入字典中
        for row in reader:
            for col in range(10):
                ddict[keys[col]].append(row[col])

    return ddict


# 【已加工】略为突兀，【定位】还有未处理之事

def mingyao_analy(Guagong_Wuxing, Sixmode, mingyao: int, GuaShu_li, self_zhi_value):
    """
    :param Coins_Number_List: 18位数字，前6位数主卦，后6位数变卦，
    :param mingyao:"亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"
    :param self_zhi_value:世爻地支数！！！不是世爻爻位
    trigger_li应该和主卦卦同方向
    :return:
    """

    tempchar = "命爻：" + mingyao
    article = [tempchar]
    # zhi = ["亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"]
    mingyao = ZHI.index(mingyao)

    # GuaShu_li:18位数字
    colli = xiangchong(mingyao)
    sixhold = xianghe(mingyao)

    # 卦宫五行生数0-5
    wx = Guagong_Wuxing

    # LIU_QIN_NUM_60:此表此处常用；第12位归在0，如果12加进来list out of range

    # 采集断语
    mingyao_data = import_mingyaoData()
    # 导入csv的语句
    if colli in GuaShu_li:
        article.append(mingyao_data['爻冲年命'][LIU_QIN_NUM_60[wx][colli % 12] // 12])
        if colli == self_zhi_value:
            article.append(mingyao_data['爻冲年命'][5])

        animal = Sixmode_to_Animals(Sixmode)
        for i, n in enumerate(GuaShu_li):  # 18位数字
            if colli == n:
                article.append(mingyao_data[f'{animal[i % 6]}冲年命'][LIU_QIN_NUM_60[wx][colli % 12] // 12])

    if sixhold in GuaShu_li:
        article.append(mingyao_data['爻合年命'][LIU_QIN_NUM_60[wx][sixhold % 12] // 12])
        if sixhold == self_zhi_value:
            article.append(mingyao_data['爻合年命'][5])

    return article
