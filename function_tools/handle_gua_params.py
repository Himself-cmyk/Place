'''
【基础函数·六爻排盘】
卦象的处理细节比较杂碎
写成函数，存放在这个文件中
调用这个文件的函数
可以让代码变得简洁
'''
from constants import GUA_NUM_TO_LIST
r_to_g = {v:k for k,v in GUA_NUM_TO_LIST.items()}

# 检查 012021，转换为 主卦list/变卦list，找到 gua/biangua
# 特征：len()==6 and .isdigit()


# 检查 25 26，转换为  主卦list/变卦list，找到 012021
# 特征：len()<6

# 分割函数
# 强制把所有的分割符，转化为/

'''raw string -> list'''


def split_n_replace(string: str):
    # if '.' in string:
    # reverse = True
    delimainder = ' .,-，。'
    for deli in delimainder:
        string = string.replace(deli, '/')
    return [int(c) for c in string.split('/') if c.isdigit()]


def isFormat_1(string: str):
    return len(string) == 6 and all(0 <= int(c) <= 3 for c in string)


def isFormat_2(lst: list[int]):
    return len(lst) in [1, 2] and all(0 <= int(c) <= 64 for c in lst)


def handle_coinNum(string: str):
    string = string.strip()
    # format_1:120321
    if isFormat_1(string):
        coinNum = [int(c) for c in string][::-1]  # 返回词典，含有主卦变卦序数，coinNum
        gua, biangua = CoinsNum_to_guaNum(coinNum)
    else:
        split_lst = split_n_replace(string)
        # format_2:1 2 0 3 2 1 or 1.2.0.3.2.1
        if isFormat_1(split_lst):
            coinNum = split_lst  # 返回词典，含有主卦变卦序数，coinNum
            gua, biangua = CoinsNum_to_guaNum(coinNum)

        elif isFormat_2(split_lst):
            gua = int(split_lst[0])
            biangua = int(split_lst[1]) if len(split_lst) == 2 else gua
            coinNum = guaNum_to_CoinsNum(gua, biangua)
        else:
            print('error:', string)
            return

    return {'gua': gua, 'biangua': biangua, 'coinNum': coinNum}
    # 返回词典，含有主卦变卦序数，coinNum


'''parameter process'''


def guaNum_to_CoinsNum(gua_num, bian_gua, Type=int):
    if bian_gua == 64:
        bian_gua = gua_num
    gua_list, biangua_list = GUA_NUM_TO_LIST[gua_num], GUA_NUM_TO_LIST[bian_gua]
    if Type == str:
        return ''.join([str(g) if g == b else '3' if g == 1 else '0' for g, b in zip(gua_list, biangua_list)])
    elif Type == int:
        return [g if g == b else 3 if g == 1 else 0 for g, b in zip(gua_list, biangua_list)]


def CoinsNum_to_guaNum(coinNum):
    gua_li = [1 if r == 3 else 2 if r == 0 else r for r in coinNum]  # 列表 coinsNumber_list 中的每个元素根据其值进行映射
    biangua_li = [2 if r == 3 else 1 if r == 0 else r for r in coinNum]
    gua_num = r_to_g[tuple(gua_li)]
    if all(r in [1, 2] for r in coinNum):
        biangua_num = gua_num
    else:
        biangua_num = r_to_g[tuple(biangua_li)]
    return gua_num, biangua_num
