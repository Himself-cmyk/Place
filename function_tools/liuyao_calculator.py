'''
【基础函数·分析卦象】
'''
def identity_transformation(x):
    return x

def get_zhi_wx_relation(zhi: int, active_zhi: int, mode=None):
    """
   获取两个地支之间的五行生克关系。

   :param zhi: 第一个地支的索引（0-11）
   :param active_zhi: 第二个地支的索引（0-11），这个为主，一般是月建日辰动爻
   :return: 两个地支之间的关系（生、克、扶、耗、泄）
   """
    # 【注意】必须输入0-12，否则就会崩溃
    if zhi is None or active_zhi is None:
        print(f'出错了！！活跃地支是：【{active_zhi}】', f'地支是：【{zhi}】')
        return None

    zhi_idx = zhi_to_wx_idx[zhi % 12]
    active_zhi_idx = zhi_to_wx_idx[active_zhi % 12]
    idx = (zhi_idx - active_zhi_idx + 5) % 5

    if idx == 0 and mode == '变爻':
        text = "退" if zhi > active_zhi else "进" if zhi < active_zhi else "吟"
        return text
    else:
        relation = ["扶", '生', '克', '耗', '泄']
        return relation[idx]
# usage
# get_zhi_relation(yao, self.gua.d)

"""计算公式"""


def xiangchong(num):  # range:0-11
    num = num % 12
    return num - 6 if num >= 6 else num + 6


def xianghe(num):
    num = num % 12
    return 3 - num if num <= 3 else 15 - num
