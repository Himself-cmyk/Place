"""
爬虫借用其他网站实现电脑自动起卦
然后用代码自动计算出结果
真正做到：
问什么马上就会有答案
省去了摇卦的时间
"""


def test_get_page():
    try:
        keyword = parse_page()
        return keyword
    except:
        print("不期望的抓取失败。")
        return None


def parse_page():
    import requests

    url = 'https://www.china95.net/paipan/liuyao/liuyao.asp'
    headers = {
        'Host': 'www.china95.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.china95.net/paipan/liuyao/index.asp',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '204',
        'Origin': 'https://www.china95.net',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_b781bc457cceb8bb909ab125fa36811e=1699345665; __gads=ID=aac2965738ee73f8-228f8257b7dc0038:T=1679753086:RT=1699345666:S=ALNI_MYWXYkLAhOrSthQPytnXXkOW7VNZg; __gpi=UID=00000be082c9959b:T=1679753086:RT=1699345666:S=ALNI_MbOYMiYxfxIk2KRVwLNPFiEHOnDBg; ASPSESSIONIDQWTRSTBT=CDMOENOAENPFGNMDBEPOECGP; Hm_lpvt_b781bc457cceb8bb909ab125fa36811e=1699345844',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    import datetime

    # 获取当前时间
    current_time = datetime.datetime.now()
    data = {
        'csyear': str(current_time.year),
        # 'mysex': '男',  # 这里使用了UTF-8编码后的"男"
        'whyarea': '0',
        'year': str(current_time.year),
        'month': str(current_time.month),
        'day': str(current_time.day),
        'hour': str(current_time.hour),
        'minute': str(current_time.minute),
        'mode': '1',
        'hanzi': '',
        'yinyang': '1',
        'upyao': '',
        'downyao': '',
        'dongyao': '1',
        'baosuo': '',
        'dongyao1': '1',
        'yao6': '1',
        'yao5': '1',
        'yao4': '1',
        'yao3': '1',
        'yao2': '1',
        'yao1': '1',
        'ok': '提交'  # 这里使用了UTF-8编码后的"提交"
    }

    response = requests.post(url, data=data, headers=headers)

    response.encoding = 'gbk'  # 指定使用GBK编码解析响应内容
    # 输出服务器返回的 HTML 内容（已使用GBK解码）
    with open('data/response.html', 'w', encoding='gbk') as file:
        file.write(response.text)

    import re

    # 使用正则表达式进行匹配
    time_ptn = r'干支：</b>(.*?)（<font'
    time_res = re.search(time_ptn, response.text)
    pattern = r'宫：(.*?)六神'
    result = re.search(pattern, response.text)

    if result:
        # 使用正则表达式进行替换，去掉不期望的字眼/后缀
        time_extracted = time_res.group(1)
        _string = re.sub(r'干支：</b>', '', time_extracted)
        output_string = re.sub(r'\s+', '', _string)

        extracted_text = result.group(1)
        _string = re.sub(r'(.{1})宫：', '', extracted_text)
        _string = re.sub(r'<br><b>$', '', _string)
        output_string += re.sub(r'\s+', '', _string)

        return output_string.strip()  # 输出提取的文本（去除首尾空格和换行符）
    else:
        print("未找到匹配的文本")


# 调用主程序
if __name__ == '__main__':
    word = test_get_page()
    print(word)
