'''
LiuyaoPlace usage
第一步 通过 GuideComponent 获取用户输入
第二步 调用 LiuyaoPlace类 进行排盘
第三步 LiuyaoPlace.place(返回 排盘文字)
    or LiuyaoPlace.place_to_excel(返回 排盘文字的表格矩阵，还有对应单元格的颜色矩阵)
'''
from constants import GAN, ZHI, ANIMALS, KONG_WANG, GUA_SHU, HIDE_SHU, FULL_GUA_NAME, FAMILY, LIU_QIN_NUM_60
from classes.custom_class import AttrDict
from function_tools.liuyao_calculator import xiangchong
from function_tools.handle_time import time_str_process, GetCurrentTime
from function_tools.handle_gua_params import handle_coinNum

msg_dict = {'title': '', 'my': None, 'coinNum': [], 'gua': None, 'biangua': None,
            'y': None, 'yg': None, 'm': None, 'd': None, 'dg': None, 'h': None}


def input_process():
    '''
    这是一个本文件的示例函数，
    获取了用户输入，完成了 GuideComponent
    修改全局变量 msg_dict
    下一步可以用于排盘。
    '''
    global msg_dict

    title = input('标题：')
    time_str = input('时间：')
    coinNum = input('硬币数组：')
    msg_dict['title'] = title
    msg_dict.update(handle_coinNum(coinNum))  # TODO：
    time_dict = time_str_process(time_str)
    msg_dict.update(time_dict)


def GuideComponent(title, coinNum, time_str):
    msg_dict['title'] = title
    msg_dict.update(handle_coinNum(coinNum))
    time_dict = time_str_process(time_str)
    msg_dict.update(time_dict)
    return msg_dict


class LiuyaoPlace:
    def __init__(self, msg_dict: dict = None):

        self.gua = AttrDict()
        self.gua.update(msg_dict)

        if not isHaveMonthDate(self.gua):  # 通过 time_dict 指定排盘时辰(同时具备月、日、日干)
            self.gua.update(GetCurrentTime(hour=self.gua.get('h'), Mode=int))  # 还可以指定当天，当前时辰

        # self.gua.update({'title': '', 'theme': '', 'coinNum': [int(i) for i in '102012'], 'gua': 25, 'biangua': 26, })
        self.gua['wx'], self.gua['six_mode'] = h_calculate(self.gua.gua, self.gua.dg)
        self.gua['trigger'] = [1 if r in [3, 0] else 0 for r in self.gua.coinNum]
        self.gua['self'], self.gua['other'] = search_self(self.gua.gua)  # 爻位1-6
        self.gua['zhi'] = gua_info_list_calculate(self.gua.gua, self.gua.biangua, self.gua.trigger)
        self.gua['yong_shen'] = '妻财'
        self.gua['db_path'] = '妻财'
        self.gua['file_path'] = '妻财'

        self.cache = AttrDict()
        self.cache.update({'tmp': None, 'line_belong': None, 'former_idxlst': None, 'suffix_set': []})

    def place(self, output=False, isHtml=False):
        '''
        :param output:如果设置为 True，则直接打印输出结果；如果为 False，则返回生成的字符串。
        :param isHtml:一个布尔值，用于决定是否以 HTML 格式输出文本。这会影响某些部分的布局，例如 cent 变量的值
        可以更改为：None,html,excel
        :return:
        '''
        cent = 14 if isHtml else 8  # 在火狐 16 比较合适，在edge或QQ浏览器 14 比较合适
        if 'msg' in self.gua:
            text = f'占题：{self.gua.title}\n公历时间：{self.gua.msg}\n当前时间：{self.gua.time_info}'
        else:
            text = f'占题：{self.gua.title}\n当前时间：{self.gua.time_info}'

        sign = ["×", '′', '″', "○"]
        main_lst, after_lst, hide_lst = [], [], []
        Family = palace_12(self.gua.wx)
        for rank, num in enumerate(self.gua.zhi):
            string = Family[num % 12] if num else ''
            if rank < 6:
                main_lst.append(string)
            elif rank < 12:
                after_lst.append(string)
            else:
                hide_lst.append(string)
        if any(hide_lst):
            hide_lst = [n if n else ' ' * cent for n in hide_lst]

        self_other = [n if n else ' ' * 2 for n in self_other_ps(self.gua.self, self.gua.other, skip=True)[:6]]
        six_animals = Sixmode_to_Animals(self.gua.six_mode)

        condition = self.gua.biangua != self.gua.gua and self.gua.biangua != 64
        headline = ' ' * 6 + FULL_GUA_NAME[self.gua.biangua] if condition else ''
        text += '\n' + FULL_GUA_NAME[self.gua.gua] + headline

        for i in range(6):
            n = self.gua.coinNum[i]
            lst = [six_animals[i], hide_lst[i], main_lst[i] + sign[n], self_other[i],
                   after_lst[i] + sign[(n + 3) // 3] if after_lst[i] else '']
            line = ' '.join(lst)
            text += '\n' + line

        if output:
            print(text)
        else:
            return text

    def place_to_excel(self, output=False) -> list[list]:
        condition = self.gua.biangua != self.gua.gua and self.gua.biangua != 64
        headline = ' ' * 6 + FULL_GUA_NAME[self.gua.biangua] if condition else ''
        gua_name_line = FULL_GUA_NAME[self.gua.gua] + headline

        result_excel = [
            [f'占题：{self.gua.title}'],
            [f'公历时间：{self.gua.msg}' if 'msg' in self.gua else '公历时间：未知'],
            [f'当前时间：{self.gua.time_info}'],
            [gua_name_line]
        ]

        sign = ["×", '′', '″', "○"]
        main_lst, after_lst, hide_lst = [], [], []
        Family = palace_12(self.gua.wx)
        for rank, num in enumerate(self.gua.zhi):
            string = Family[num % 12] if num else ''
            if rank < 6:
                main_lst.append(string)
            elif rank < 12:
                after_lst.append(string)
            else:
                hide_lst.append(string)
        if any(hide_lst):
            hide_lst = [n if n else ' ' * 8 for n in hide_lst]

        self_other = [n if n else ' ' * 2 for n in self_other_ps(self.gua.self, self.gua.other, skip=True)[:6]]
        six_animals = Sixmode_to_Animals(self.gua.six_mode)

        for i in range(6):
            n = self.gua.coinNum[i]
            lst = [six_animals[i], hide_lst[i], main_lst[i] + sign[n], self_other[i],
                   after_lst[i] + sign[(n + 3) // 3] if after_lst[i] else '']
            result_excel.append(lst)

        if output:
            for line in result_excel:
                print('—'.join(line))
        else:
            # 腾蛇用灰色  #acadb2，白虎为黑色 none，玄武为蓝色 #4078f2，青龙为绿色 #4b9e5f，朱雀为红色 #f86d43，勾陈为土黄色 #c18401
            six_animals_map = {
                '腾蛇': '#acadb2', '白虎': '', '玄武': '#4078f2', '青龙': '#4b9e5f', '朱雀': '#f86d43',
                '勾陈': '#c18401'
            }
            li = [num % 12 for num in self.gua.zhi[:6]]
            isAnDong = xiangchong(self.gua.d) in li

            colors = [
                ['', '', '', ''] + [six_animals_map[item] for item in six_animals],
                ['', '', '', ''] + [self.calculate_score(item, isAnDong) for item in self.gua.zhi[12:]],
                # 伏神。<=-8休囚用用鲜红色 #ff5733，<=-4过弱深红色 #861527，>=4旺相用土黄色 #c18401，过旺>=8用亮黄色 #fdf402，空亡用灰色 #acadb2，
                ['', '', '', ''] + [self.calculate_score(item, isAnDong) for item in self.gua.zhi[:6]],  # 主卦
                ['', '', '', '', '', '', '', '', '', ''],  # 世应
                ['', '', '', ''] + [self.calculate_score(item) for item in self.gua.zhi[6:12]],  # 变爻
            ]
            return result_excel, colors

    def calculate_score(self, zhi: int, an_dong=False):
        from constants import month_score, date_score, date_score_an_dong

        if not zhi and zhi != 0:
            return ''

        zhi = zhi % 12
        if an_dong:
            temp_map = date_score_an_dong
        else:
            temp_map = date_score

        # 月建为亥月0，看寅爻3的分数，month_score[0][3]
        score = month_score[self.gua.m][zhi]
        score += temp_map[self.gua.d][zhi]

        color = ''
        if score >= 8:
            color = '#f2cc47'
        elif score >= 4:
            color = '#c18401'
        elif score <= -4:
            color = '#ff5733'
        elif score <= -8:
            color = '#861527'
        elif zhi in [self.gua.empty, (self.gua.empty + 1) % 12]:
            color = '#acadb2'

        return color

    def coinNum_change(self, mode='reverse'):
        if mode == 'reverse':
            self.gua.coinNum = [self.gua.coinNum[5 - i] for i in range(6)]
        elif mode == 'change':
            self.gua.coinNum = [3 - n for n in self.gua.coinNum]

        print('already changed to :', ''.join([str(i) for i in self.gua['coinNum']]))


def isHaveMonthDate(dic) -> bool:
    return bool(dic) and all(n is not None for n in [dic['m'], dic['d'], dic['dg']])


'''排盘辅助函数'''


def h_calculate(gua_num: int, ri_gan: int):
    REMINDER_TO_WU_XING = [4, 3, 1, 3, 0, 0, 2, 4]
    REMAINDER_TO_SIX_MODE = [0, 1, 1, 2, 2, 3, 4, 5, 5, 0]
    return REMINDER_TO_WU_XING[gua_num // 8], REMAINDER_TO_SIX_MODE[ri_gan % 10]


def gua_info_list_calculate(gua_num: int, biangua_num: int, trigger_li: list[int]):
    def search_After():
        li = [None] * 6
        if biangua_num <= 63:  # 不是静卦的话
            Biangua_li = GUA_SHU[biangua_num]
            for i, n in enumerate(trigger_li):
                if n:
                    li[i] = Biangua_li[i]
        return li

    # 顺序是Main，After，Hide
    li = GUA_SHU[gua_num].copy()  # 直接赋值的话，li将会直接在gua_shu的内存上修改extend，影响下次赋值。
    li.extend(search_After())
    li.extend(HIDE_SHU[gua_num])  # GuaShu_li.extend(search_hide(self.gua_num))
    return li


def search_self(Guanum: int):
    '''
    给卦的序号，找出世应的idx
    :param Guanum:卦的序号
    :return: List[self_idx,other_idx]（5-0代表初爻到六爻）
    '''
    remain = Guanum % 8
    # idx_to_selfposit = [6, 1, 2, 3, 4, 5, 4, 3]原本是1-6代表初爻到六爻
    REMAINDER_SELF = [0, 5, 4, 3, 2, 1, 2, 3]  # 现在是5-0代表初爻到六爻，贴合gua_shu的习惯
    REMAINDER_OTHER = [3, 2, 1, 0, 5, 4, 5, 0]
    return [REMAINDER_SELF[remain], REMAINDER_OTHER[remain]]


def self_other_ps(self_posit, other_posit, skip=False):
    self_other_lst = [''] * 18
    self_other_lst[self_posit] = '世'
    self_other_lst[other_posit] = '应'
    if not skip:
        max_num = max(self_posit, other_posit)
        self_other_lst[max_num - 2], self_other_lst[max_num - 1] = '间', '间'
    return self_other_lst


def Sixmode_to_Animals(Sixmode: int) -> list[str]:
    li = [ANIMALS[(Sixmode + 10 - i) % 6] for i in range(6)]
    return li


def palace_12(WuXing):
    return [FAMILY[num] for num in LIU_QIN_NUM_60[WuXing]]


if __name__ == "__main__":
    # usage
    msg_dict = {'title': '', 'my': None, 'coinNum': [1, 2, 1, 2, 1, 2], 'gua': 25, 'biangua': 26,
                'y': None, 'yg': None, 'm': None, 'd': None, 'dg': None, 'h': None}
    m = LiuyaoPlace(msg_dict)
    m.place(output=True)
    print('年支', m.gua.y)
    print('年干', m.gua.yg)
    print('月建', m.gua.m)
    print('日辰', m.gua.d)
    print('日干', m.gua.dg)
    print('时辰', m.gua.h)
