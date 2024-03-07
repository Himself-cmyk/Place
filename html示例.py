import configparser
import json
import os
import re
import requests
import sys

from datetime import datetime

from PyQt5.QtWidgets import QApplication, QTextBrowser, QHBoxLayout, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont

default_links_set = [
    ('https://tieba.baidu.com/p/4015190599', '朱辰彬的理论怎么样？'),
    ('https://tieba.baidu.com/p/8867943388', '手摇卦，大神们看看这次真的离婚了吗'),
    ('https://tieba.baidu.com/p/8873195316', '工作卦 各位师傅给指点一下，谢谢'),
    ('https://tieba.baidu.com/p/8872576845', '各位老师，麻烦帮忙看下这个卦，谢谢，必有反馈'),
    ('https://tieba.baidu.com/p/8873282340', '大师们帮忙看看'),
    ('https://tieba.baidu.com/p/8873312300', '最近一段时间倒霉的很，不知道是人身后不干净，还是车不干净'),
    ('https://tieba.baidu.com/p/8872426611', '随缘看卦了'),
    ('https://tieba.baidu.com/p/8873264772', '手摇卦 年后相亲能否遇到对的人'),
    ('https://tieba.baidu.com/p/8848625511', '手搓 哪个大佬看看 有三合 但是世爻被克'),
    ('https://tieba.baidu.com/p/8873305862', '男生，问卦象何解'),
    ('https://tieba.baidu.com/p/8872841651', '稿件是否录用 硬币手摇'),
    ('https://tieba.baidu.com/p/8873273616', '学业帖，会反馈'),
    ('https://tieba.baidu.com/p/8811776225', '大风起兮云飞扬。威加海内兮归故乡'),
    ('https://tieba.baidu.com/p/8872657112', '开贴。反馈反馈务必反馈。'),
    ('https://tieba.baidu.com/p/8873233937', '交流练习，手摇带反馈的最好'),
    ('https://tieba.baidu.com/p/8852565068', '在线解卦随缘帮看'),
    ('https://tieba.baidu.com/p/8870583641', '会不会离职'),
    ('https://tieba.baidu.com/p/8873235648', '问收藏的自治药是不是真的，想给我妈买'),
    ('https://tieba.baidu.com/p/8872887010', '求解答，为啥没中奖'),
    ('https://tieba.baidu.com/p/8873335690', '比兑现，S信w，删铁，没办法'),
    ('https://tieba.baidu.com/p/8827291292', '增删新手，开贴练'),
    ('https://tieba.baidu.com/p/8873296115', '女问，和男朋友可以结婚吗？有师傅能帮看一看嘛'),
    ('https://tieba.baidu.com/p/8873250681', '帮我看看这个争议极大的卦，说什么的都有'),
    ('https://tieba.baidu.com/p/8873314053', '问爷爷的病能否好转'),
    ('https://tieba.baidu.com/p/8410892559', '手摇卦，请大家看看他会不会再找我'),
    ('https://tieba.baidu.com/p/8872202365', '男问自己适合什么行业'),
    ('https://tieba.baidu.com/p/8872795848', '求解，会反馈'),
    ('https://tieba.baidu.com/p/8872586021', '感情卦，本人占，男'),
    ('https://tieba.baidu.com/p/8872931940', '答疑解惑，带问题来'),
    ('https://tieba.baidu.com/p/8849576404', '第二次起诉离婚，能离成吗？半月内反馈！'),
    ('https://tieba.baidu.com/p/8871394388', '大师们看一下考试能不能过，成绩出来立马反馈'),
    ('https://tieba.baidu.com/p/8870713158', '有偿 楼上邻居经常敲墙能看看怎么回事怎么解决嘛'),
    ('https://tieba.baidu.com/p/8872798836', '硬币手摇会反馈'),
    ('https://tieba.baidu.com/p/8872725554', '求看结果。能不能上岸'),
    ('https://tieba.baidu.com/p/8873310544', '卜算，卜卦，'),
    ('https://tieba.baidu.com/p/8873075336', '手摇挂，求问公考笔试'),
    ('https://tieba.baidu.com/p/8865698271', '明天面试情况如何'),
    ('https://tieba.baidu.com/p/8851476198', '男问感情。'),
    ('https://tieba.baidu.com/p/8873301501', '新手请教。'),
    ('https://tieba.baidu.com/p/8873206703', '有没有大师解疑一下'),
    ('https://tieba.baidu.com/p/8873045957', '请大家帮忙看下和男友姻缘如何'),
    ('https://tieba.baidu.com/p/8865337458', '求大师看看'),
    ('https://tieba.baidu.com/p/8873293898', '他还会联系我吗？'),
    ('https://tieba.baidu.com/p/8873102831', '还是我，\U0001fae3求助看看中医师承'),
    ('https://tieba.baidu.com/p/8871582481', '202年是否可以找到心仪工作？应期？'),
    ('https://tieba.baidu.com/p/8765784703', '考试能过吗（硬币手摇必反馈）'),
    ('https://tieba.baidu.com/p/8870829643', '女问工作，是跳槽还是留下来，手摇铜币卦。'),
    ('https://tieba.baidu.com/p/8867481375', '23年给老爸摇的六爻掛，卜算寿命长短。'),
    ('https://tieba.baidu.com/p/8872921803', '手工摇卦，我的婚姻发展？'),
    ('https://tieba.baidu.com/p/8873247188', '新开咨询帖。'),
]


class ArticleBrowser(QWidget):
    def __init__(self, callback=None):
        super().__init__()

        # 添加底部按钮
        self.page = 0
        self.callback = callback
        self.homepage_url = 'https://tieba.baidu.com/f?kw=%E5%85%AD%E7%88%BB&fr=index'
        self.nextpage_url = f'https://tieba.baidu.com/f?kw=%E5%85%AD%E7%88%BB&ie=utf-8&pn={50 * self.page}'
        self.text_browser = MyTextBrowser(links=craw_article_links_name(self.homepage_url), callback=self.callback_func)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox.addWidget(self.text_browser)
        self.btn_save = QPushButton('保 存 记 录 🍐', self)
        self.btn_save.clicked.connect(self.text_browser.save_json)
        hbox.addWidget(self.btn_save)

        self.btn_nextpage = QPushButton('下 一 页 🌈', self)
        self.btn_nextpage.clicked.connect(self.next_page)
        hbox.addWidget(self.btn_nextpage)

        self.btn_reload = QPushButton('刷 新 首 页 🔁', self)
        self.btn_reload.clicked.connect(self.home_page)
        hbox.addWidget(self.btn_reload)

        vbox.addLayout(hbox)
        self.setWindowTitle('帖 子 浏 览 器 🐳')
        self.move_to_center()

        # 将按钮布局添加到文本浏览器底部
        self.setLayout(vbox)

    def next_page(self):
        self.page += 1
        self.nextpage_url = f'https://tieba.baidu.com/f?kw=%E5%85%AD%E7%88%BB&ie=utf-8&pn={50 * self.page}'
        # 调用爬虫函数获取links
        links = craw_article_links_name(self.nextpage_url)
        self.text_browser.filter(links)

    def home_page(self):
        self.page = 0
        links = craw_article_links_name(self.homepage_url)
        self.text_browser.filter(links)

    def move_to_center(self):
        # 获取屏幕的尺寸
        screen_size = QApplication.primaryScreen().availableGeometry()

        # 获取窗口的尺寸
        window_size = self.frameSize()

        # 计算窗口左上角的坐标
        x = (screen_size.width() - window_size.width()) / 2

        # 移动窗口到指定位置
        self.move(int(x), 10)

    def callback_func(self, url):

        if self.callback:
            self.callback(url)
        else:
            from io import BytesIO
            from PIL import Image
            from bs4 import BeautifulSoup
            from cnocr import CnOcr
            title, time, message_lst = craw_detail_page_gua_pic(url)
            gua_key = ' '.join(message_lst)
            print(title)
            print(time)
            print(gua_key)
        # 再一个callback，title装在顶行，gua_key装在第三行，url和time装在textbox（事先要清空）


def craw_article_links_name(url):
    # 抓取 贴吧首页的帖子 逻辑
    def extract_links(html):
        pattern = r'<a rel="noopener" href="(/p/\d+)" title="(.*?)"'
        links = re.findall(pattern, html)
        result = [('https://tieba.baidu.com{}'.format(link[0]), link[1]) for link in links]
        return result

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
    }
    page_text = requests.get(url=url, headers=headers).text
    return extract_links(page_text)


def craw_detail_page_gua_pic(url=None):
    if not url:
        url = "https://tieba.baidu.com/p/8862322320"  # 将这里的 url 替换成需要处理的网页地址
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    h3_tag = soup.find('h3', class_='core_title_txt pull-left text-overflow')
    if h3_tag and h3_tag.string:
        title = h3_tag.string.strip()

    else:
        title = '标题找不到!'

    img_tag = soup.find("img", {"class": "BDE_Image"})
    img_src = img_tag.get("src")

    # 获取图片
    img_data = requests.get(img_src).content
    img = Image.open(BytesIO(img_data))

    # 使用 OCR 进行文字识别
    ocr = CnOcr()
    out = ocr.ocr(img)
    time_lst = [item['text'] for item in out if re.match(r'\d{4}', item['text'])]  # -\d{1,2}-\d{1,2}
    if time_lst:
        time = time_lst[0]
    else:
        time = '没有找到时间!'

    texts = [item['text'] for item in out if re.search(r'[甲乙丙丁戊己庚辛壬癸天泽火震风水地山]', item['text'])]
    texts = [text for text in texts if all(s not in text for s in ['父母', '兄弟', '子孙', '妻财', '官鬼'])]

    replace_dict = {'央': '夬', '西': '酉', '成': '戌', '良': '艮'}

    texts = [text if not any(char in text for char in replace_dict.keys()) else ''.join(
        replace_dict.get(char, char) for char in text) for text in texts]

    return title, time, texts


class MyTextBrowser(QTextBrowser):
    def __init__(self, parent=None, links=None, callback=None):
        super().__init__(parent)

        self.saved_html = ""
        self.callback = callback
        self.setMinimumHeight(1600)  # 设置窗口最小高度为1800像素
        self.setMinimumWidth(1000)
        font = QFont(self.font())
        font.setPointSize(14)  # 设置字体大小为14
        self.setFont(font)
        self.category_dict = {}
        if not links:
            links = default_links_set
        self.filter(links=links)

        self.setOpenExternalLinks(False)
        self.anchorClicked.connect(self.onAnchorClicked)

    def setHtml(self, html):
        super().setHtml(html)
        if not self.saved_html:
            self.saved_html = html

    def onAnchorClicked(self, url):
        print('成功')
        print(f"Clicked URL: {url.toString()}")
        self.setHtml(self.saved_html)
        self.callback(url=url.toString())

    def headline(self, title: str):
        string = '*' * 8 + f' {title} ' + '*' * 8
        # self.append(string+ '\n')
        return string + '<br>'

    def filter(self, links=None, category_dict=None):
        self.clear()

        html = self.headline('贴吧帖子列表')

        if not category_dict:
            category_dict = self.parse_config(links)
        for k in category_dict.keys():
            if lks := category_dict[k]:
                html += self.headline(k)
            for link in lks:
                html += f"<a href='{link[0]}'>{link[1]}</a><br>"
        self.setHtml(html)
        self.saved_html = html

        if self.category_dict:
            self.category_dict = merge_dict(self.category_dict, category_dict)
        else:
            self.category_dict = category_dict

    def save_json(self):
        if not self.category_dict:
            return

        # 创建保存 JSON 文件的文件夹
        folder_path = "page_json"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 生成带有时间戳的文件名
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{current_time}浏览帖子.json"

        # 构建保存路径
        file_path = os.path.join(folder_path, file_name)

        # 将词典保存为 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.category_dict, f, ensure_ascii=False)
        print(file_path, '保存成功！')

    def load_json(self):
        # with open():
        # category_dict = json文件
        pass

    # load_json?获取本地文件夹里的所有json并且加载【定位】

    @staticmethod
    def parse_config(links: list[tuple]):
        config_file = "config.ini"
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')

        categories = {}

        for section in config.sections():
            category_name = section  # 获取种类名称，去掉方括号
            if category_name == '博彩相关':
                continue
            keywords = config.get(section, 'kw_lst').split(',')
            categories[category_name] = []

            for link in links:
                title = link[1]
                if any(keyword in title for keyword in keywords):
                    categories[category_name].append(link)

        # 将没有找到分类的链接归类到“其他”分类中
        uncategorized_links = [link for link in links if
                               all(link not in category for category in categories.values())]
        if uncategorized_links:
            categories['其他分类'] = uncategorized_links

        return categories


def merge_dict(dict1: dict, dict2: dict):
    merged_dict = dict1.copy()  # 复制 dict1
    for key, values in dict2.items():
        if key in merged_dict:
            merged_dict[key].extend(values)  # 合并列表
        else:
            merged_dict[key] = values
    return merged_dict


def merge_way(lst: list[dict]):
    result = [merge_dict(a, b) for a, b in zip(lst[::2], lst[1::2])]
    if len(result) > 1:
        return merge_way(result)
    else:
        return result


if __name__ == "__main__":
    app = QApplication(sys.argv)
    text_browser = ArticleBrowser()
    text_browser.show()
    sys.exit(app.exec_())
