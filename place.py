import os
import sys
import configparser
from PyQt5.QtCore import pyqtSlot, Qt, QStringListModel, QUrl
from PyQt5.QtGui import QTextCursor, QIcon, QFont, QKeySequence, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, \
    QGroupBox, QGridLayout, QComboBox, QLabel, QMainWindow, QCheckBox, QCompleter, QMessageBox, QShortcut, QMenu, \
    QAction
from place_addition import identify_GuaName, identify_60HuaJia, main_input  # 主动识别字符串，更新“排盘输入框”的值
from exportFunc import convert_text_to_xlsx, write_as_txt

# import site
# site.addsitedir('D:\...\cnocr')
# sys.path.append('D:\...\lib\site-packages')
# [cause]已经解决的bug；【bug】尚未解决的bug


"""
tips：
（1）输入 并且 提交：
断语+ or 断语- ：实时更新一次应验率
"""


# 数据库:多条件筛选数据的功能，点击加载卦象
# 粘贴一行字，读时间（癸巳 癸巳 甲戌 甲戌）；读卦象为"num1 num2"输入input2
# 切换提示：左侧加一行字，"\n\n\n天时 \n道路 \n门前 \n床位 \n宅灶 \n走路 "
# 切换解析模式：

class MainPlace(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.child_windows = []
        self.default_db_path = "data/database.db"  # py文件同目录必须有一个data文件夹
        self.mode_value = None
        self.yongshen_value = "世"
        self.mingyao = None  # 定义为类成员变量，并初始化为 None；这部分的变量不是很重要
        self.Ifcal = None
        self.IfWrite = None
        self.family = []
        self.analy_model = None
        # self.stay_stop = False

    def initUI(self):
        def wrap_data(output_type):
            gua_text = self.gua_image_label.text()

            if not gua_text:
                self.message_label.setText("⚠没有卦象，不能输出~")
                return

            if output_type == "xlsx":
                title = self.input1.text()
                res_text = convert_text_to_xlsx(gua_text, file_name=title)
            elif output_type == "txt":
                report_text = self.text_box.toPlainText()
                other_text = self.note_textbox.toPlainText()
                res_text = write_as_txt(gua_text, report_text, other_text)

            self.message_label.setText(res_text)

        # 创建菜单栏
        self.menuBar = self.menuBar()

        # 创建文件菜单
        self.fileMenu = QMenu('文件', self)
        self.menuBar.addMenu(self.fileMenu)

        # 创建导出为xlsx的动作
        self.exportXlsxAction = QAction('导出为xlsx', self)
        self.exportXlsxAction.triggered.connect(lambda: wrap_data('xlsx'))
        self.fileMenu.addAction(self.exportXlsxAction)

        # 创建导出为txt的动作
        self.exportWordAction = QAction('导出为txt', self)
        self.exportWordAction.triggered.connect(lambda: wrap_data('txt'))
        self.fileMenu.addAction(self.exportWordAction)

        # 添加横杠作为分隔符
        self.fileMenu.addSeparator()

        # 创建导出为txt的动作
        self.configChangeAction = QAction('修改配置', self)
        self.configChangeAction.triggered.connect(lambda: self.open_window("config_change"))
        self.fileMenu.addAction(self.configChangeAction)

        self.exportWordAction = QAction('万能的按钮', self)
        self.exportWordAction.triggered.connect(write_as_txt)
        self.fileMenu.addAction(self.exportWordAction)

        # 创建输入框和两个按钮
        main_window = ALL_Widget()
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(main_window)

        self.input1 = main_window.input1
        self.input2 = main_window.input2
        self.input3 = main_window.input3
        self.button1 = main_window.button1
        self.button2 = main_window.button2
        self.button3 = main_window.button3

        self.input1.textChanged.connect(lambda widget=self.input1: self.identify_text(widget))  # input分割识别输入的文本
        self.input3.textChanged.connect(lambda widget=self.input3: self.identify_text(widget))

        self.button1.clicked.connect(self.placeClicked)  # 按钮的 clicked 信号连接槽函数
        self.button2.clicked.connect(self.copyClicked)
        self.button3.clicked.connect(self.meihua_placeClicked)

        # 功能区域
        self.yongshen_combox = main_window.combo_box1
        self.mingyao_combox = main_window.combo_box2
        self.switch_db_comobox = main_window.switch_db_comobox
        self.switch_mode_comobox = main_window.switch_mode_comobox
        self.select_TxtComb = main_window.select_analy_mode
        self.chk_box = main_window.chk_box
        self.write_cell_btn = main_window.write_cell_btn
        self.browser_btn = main_window.browser_btn
        self.shake_btn = main_window.shake_btn
        self.name_btn = main_window.name_btn
        self.save_btn = main_window.save_btn
        self.load_btn = main_window.load_btn

        self.yongshen_combox.currentIndexChanged.connect(self.update_yongshen)  # 连接信号和槽
        self.mingyao_combox.currentIndexChanged.connect(self.update_mingyao)  # 连接信号和槽
        self.switch_db_comobox.currentIndexChanged.connect(self.update_default_path)
        self.switch_mode_comobox.currentIndexChanged.connect(self.update_mode_value)
        self.select_TxtComb.currentIndexChanged.connect(self.update_txt_path)
        self.chk_box.stateChanged.connect(self.update_Ifcal)  # 连接信号槽
        self.write_cell_btn.clicked.connect(self.write_cell)  # 连接信号槽
        self.browser_btn.clicked.connect(lambda: self.open_window("text_browser"))
        self.shake_btn.clicked.connect(lambda: self.open_window("image_switcher"))
        self.name_btn.clicked.connect(lambda: self.open_window("switch_name"))
        self.load_btn.clicked.connect(lambda: self.open_window("load_database"))
        self.save_btn.clicked.connect(self.save_to_database)

        # 对话区域
        self.input_dialog = main_window.input_dialog
        self.conf_btn = main_window.confir_btn
        self.export_btn = main_window.export_btn

        self.auto_completer = QCompleter([])  # 连接自动完成器
        self.input_dialog.setCompleter(self.auto_completer)
        self.input_dialog.textChanged.connect(self.dialog_completer)
        self.conf_btn.clicked.connect(self.commit_dialog)  # 连接信号和槽

        # 文本区域
        self.gua_image_label = main_window.gua_image_label
        self.other_label = main_window.other_label
        self.note_textbox = main_window.note_textbox
        self.message_label = main_window.message_label
        self.text_box = main_window.text_box

        self.note_textbox.textChanged.connect(self.notebox_format)  # 输入文本，进行处理成特殊格式。删掉影响不大。

        self.createShortcut(Qt.ALT + Qt.Key_1, lambda: self.open_window("load_database"))
        self.createShortcut(Qt.ALT + Qt.Key_2, self.save_to_database)  # 左手键位，快捷键
        self.createShortcut(Qt.ALT + Qt.Key_3, self.write_cell)
        self.createShortcut(Qt.ALT + Qt.Key_4, lambda: self.open_window("switch_name"))
        self.createShortcut(Qt.ALT + Qt.Key_Q, self.copyClicked)
        self.createShortcut(Qt.ALT + Qt.Key_W, self.text_box.open_url)
        self.createShortcut(Qt.CTRL + Qt.Key_Plus, lambda: self.open_window("load_database"))
        self.createShortcut(Qt.CTRL + Qt.Key_Minus, self.save_to_database)  # 右手键位

        # 创建一个中心部件      QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(MainLayout)

        # 设置窗口标题和大小
        self.setWindowTitle('任叶三沐风排盘')
        self.resize(600, 400)

    '''提交对话'''

    def commit_dialog(self):
        text = self.input_dialog.text()
        text = text.strip()

        if text[-1] in ['+', '-']:
            from place_addition import replace_text_in_file

            file = self.select_TxtComb.currentText()
            if file:
                path = f'data/{file}'
                replace_text_in_file(path, text)

                self.setText(f"{file} 更改成功！🆗")  # emoji
            else:
                # [cause]传入 'data/' ，将会报错 PermissionError: [Errno 13] Permission denied
                self.setText('⚠ 您尚未指定“知识库文件”！')
        elif text:
            self.text_box.append(text)

        self.input_dialog.clear()
        # 把text交给哪里处理？？？触发一个函数生成对话！！！期待更新〇〇〇〇〇

    def dialog_completer(self, text):
        # 输入了char的一部分
        if any(text in char for char in self.family):
            self.set_li_as_model(self.family)
        # 没有输入char，只输入开头
        elif all(char not in text for char in self.family):
            li = [text + char for char in self.family]
            self.set_li_as_model(li)

        # 完整输入char，继续续写！！！
        else:
            for char in self.family:
                if char in text:
                    # 把char发送出去，收到一个列表。触发一个函数生成对话！！！期待更新
                    """result_li = Function(char)
                    li = [text + char for char in result_li]
                    self.set_li_as_model(li)"""
                    break

    def set_li_as_model(self, li):
        model = QStringListModel(li)
        self.auto_completer.setModel(model)

    """按钮的槽函数"""

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            if self.button1.hasFocus():
                self.placeClicked()
            elif self.button2.hasFocus():
                self.copyClicked()
            elif self.input_dialog.hasFocus():
                self.commit_dialog()
        else:
            super().keyPressEvent(event)

    def copyClicked(self):
        import win32clipboard
        if result := self.gua_image_label.text():
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(result)
            win32clipboard.CloseClipboard()
            self.setText("已复制到剪贴板！🆗")

    def save_to_database(self):
        def check_and_create_folder(path):
            folder_path = os.path.dirname(path)
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                    print(f"文件夹 {folder_path} 创建成功！")
                except OSError as e:
                    print(f"创建文件夹 {folder_path} 失败：{e}")

        # 指定查询条件的数据
        title = self.input1.text()
        content1 = self.gua_image_label.text()
        content2 = self.text_box.toPlainText()
        content3 = self.note_textbox.toPlainText()

        if not title:
            self.setText('⚠ 不允许无标题！')
            return
        elif title not in content1:  # 弹出消息框请求用户确认,do_something_requiring_confirmation
            reply = QMessageBox.question(None, '确认操作', '卦象与当前标题不符，您确定要坚持保存吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                self.setText('⚠ 用户取消保存！')
                return

        import sqlite3

        # 检查路径，连接到数据库
        check_and_create_folder(self.default_db_path)
        conn = sqlite3.connect(self.default_db_path)

        # 创建游标对象
        cursor = conn.cursor()

        # 查询数据
        try:
            query = "SELECT * FROM data WHERE title=? AND content1=?"
            cursor.execute(query, (title, content1))
            result = cursor.fetchone()
        except Exception:
            result = False

        if result:
            # 找到匹配的数据，进行更新
            query = "UPDATE data SET content2=?, content3=? WHERE title=? AND content1=?"
            cursor.execute(query, (content2, content3, title, content1))

            self.setText(f"{self.default_db_path}写入记录成功！")
        else:
            from place_addition import GUA_NAMES, GAN, ZHI
            str_li = ''.join(str(num) for num in self.coinsNumber_list)

            # 没有找到匹配的数据，创建新记录
            cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                                    title TEXT,
                                    yuel TEXT,
                                    h TEXT,
                                    ric TEXT,
                                    gua TEXT,
                                    biangua TEXT,
                                    coinsNumber_list TEXT,
                                    content1 TEXT,
                                    content2 TEXT,
                                    content3 TEXT, 
                                    gid INTEGER PRIMARY KEY AUTOINCREMENT
                                )''')

            query = "INSERT INTO data (title, yuel, h, ric, gua, biangua, coinsNumber_list, content1, content2, content3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (
                title, ZHI[self.month % 12], GAN[self.rigan % 10], ZHI[self.richen % 12], GUA_NAMES[self.gua_num],
                GUA_NAMES[self.biangua_num], str_li, content1, content2, content3))

            self.setText(f"{self.default_db_path}已覆盖原来记录！")
        conn.commit()

        # 关闭游标和数据库连接
        cursor.close()
        conn.close()

    def meihua_placeClicked(self):
        from main_format import meihua_calucate, lunar_convert_to_num
        title, gua_code, time_code = self.input1.text(), self.input2.text(), self.input3.text()
        if '时' in gua_code:
            self.time_Str = gua_code
            self.coinsNumber_list = lunar_convert_to_num(gua_code)
        else:
            Time_list, _, self.time_Str, self.coinsNumber_list = main_input(gua_code, time_code)
            self.rigan, self.month, self.richen, self.yearg, self.yearz, _ = Time_list

        gua_article = f"占题：{title}\n{self.time_Str}\n" + meihua_calucate(self.coinsNumber_list)

        self.text_box.clear()

        self.gua_image_label.setText(gua_article)
        self.gua_image_label.setAlignment(Qt.AlignLeft)

        self.note_textbox.setVisible(False)
        self.note_textbox.clear()
        self.other_label.setText("")

    def placeClicked(self):
        if not self.input2.text():
            self.setText('⚠ 第二个输入框不可为空！\n(点击下方按钮“摇卦”或“起卦”)')  # QMessageBox.warning(self, '报错', '')
            return

        from gettime import search_god
        from constants import gua_information
        from main_format import gua_calculate, h_caculate, liuyao_caculate

        # 计算对象：时间，空亡，coinsNumber_list
        Time_list, self.empty, self.time_Str, self.coinsNumber_list = main_input(self.input2.text(), self.input3.text())
        self.rigan, self.month, self.richen, self.yearg, self.yearz, _ = Time_list

        # 输入检查：coinsNumber_list
        if (length := len(self.coinsNumber_list)) in [1, 2]:
            if any(num not in range(64) for num in self.coinsNumber_list):
                self.setText('⚠ 卦名排盘的序号必须在[0,63]范围内！')
                return None
            from place_addition import guaNum_to_coinsList
            # 没有输入6个硬币数，可能采用卦名排卦，输入1-2个卦象数（卦序 转 硬币数组），再不然就是出错了
            self.coinsNumber_list = guaNum_to_coinsList(self.coinsNumber_list)
        elif length == 6:
            if any(num not in [0, 1, 2, 3] for num in self.coinsNumber_list):
                self.setText('⚠ 硬币数必须在[0,3]范围内！')
                return None
        else:
            self.setText('⚠ 硬币数组的length有误！不期望的输入！')
            return None

        # 计算对象：动变列表，主变卦序数
        # 注意此处self.trigger_li的顺序：
        self.trigger_li, self.gua_num, self.biangua_num = gua_calculate(
            self.coinsNumber_list)

        self.WuXing, self.SixMode = h_caculate(self.gua_num, self.rigan)
        l0, l1, l2, l3, l4, l5, l6 = liuyao_caculate(self.gua_num, self.WuXing, self.SixMode, self.biangua_num,
                                                     self.trigger_li)

        self.liuyao = [l0, l6, l5, l4, l3, l2, l1]
        title = self.input1.text()
        title = title[:20] if len(title) > 20 else title

        gua_article = f"占题：{title}\n{self.time_Str}\n"
        for line in self.liuyao:
            gua_article += line + "\n"

        self.liuyao = [l0, l1, l2, l3, l4, l5, l6]
        lines = gua_article
        word = self.yongshen_value
        if self.yongshen_value in ["世", "应"]:  # 检查此时的用神是不是世应，方法太过原始
            words = [lines[lines.index(word) - 5], lines[lines.index(word) - 4]]
            self.yongshen_value = ''.join(words)

        # 填充卦象：gua_image_label
        self.gua_image_label.setText(gua_article)
        self.gua_image_label.setAlignment(Qt.AlignLeft)

        # 填充笔记：note_textbox，comment
        text = search_god(self.gua_num, self.rigan, self.richen, self.month, self.yearz)
        self.note_textbox.setVisible(True)
        self.note_textbox.setText(text)

        gua_information(gua_num=self.gua_num, wuxing=self.WuXing, SixMode=self.SixMode)

        self.setText("排卦成功！")

        # 实例化一个模型：analy_model   整合
        from model import AnalyModel
        self.analy_model = AnalyModel(
            Time_list, self.empty,
            [self.gua_num, self.biangua_num, self.coinsNumber_list],
            [self.WuXing, self.SixMode, self.mingyao, self.yongshen_value]
        )

        self.analy_model.text_output_func()  # 【第二处显示】
        self.data_dict = self.analy_model.GuaImageData
        self.family = self.analy_model.十二宫()
        self.analy_model.close_csv_cell()

        # print(k,len(v),v)

        if self.Ifcal:
            self.open_window("dict_reader", data=self.data_dict)
            # self.DictReader(self.data_dict)
        if self.mingyao:
            self.analy_model.mytext_outputf()
        if self.select_TxtComb.currentText():
            file = self.select_TxtComb.currentText()
            TextFilePath = os.path.join('data', file)
            print(f'< {file[:-4]} >')
            self.analy_model.主要信息接口(TextFilePath)

    """更新类变量"""

    def update_Ifcal(self):
        self.Ifcal = self.chk_box.isChecked()

    def write_cell(self):
        if self.analy_model:
            self.analy_model.write_csv_cell()
            self.child_windows.append(self.analy_model.window)
        else:
            self.setText('点击☞ 排盘 之后修改备注信息！')

    def createShortcut(self, key, slot):
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(slot)

    def update_yongshen(self, index):
        self.yongshen_value = self.yongshen_combox.itemData(index)

    def update_mingyao(self):
        self.mingyao = self.mingyao_combox.currentText()

    def update_default_path(self):
        folder_path = 'data'
        self.default_db_path = os.path.join(folder_path, self.switch_db_comobox.currentText())

    def update_txt_path(self):
        folder_path = 'data'
        file = self.select_TxtComb.currentText()
        if self.analy_model and file:
            TextFilePath = os.path.join(folder_path, file)
            print(f'< {file[:-4]} >')
            self.analy_model.主要信息接口(TextFilePath)

    @pyqtSlot(int)
    def update_mode_value(self):
        self.mode_value = self.switch_mode_comobox.currentText()
        if self.mode_value == "梅花排卦":
            self.setText("已切换<梅花排卦>模式！")
            self.note_textbox.setVisible(False)
            self.button3.setVisible(True)
            self.button1.setVisible(False)
            self.input2.setPlaceholderText("请输入数组（-号分割）")
        else:
            self.setText("已切换<传统排卦>模式！")
            self.input2.setPlaceholderText("请输入硬币数：6-5-4-3-2-1 or 123456")
            self.button3.setVisible(False)
            self.button1.setVisible(True)

    """打开子窗口，回调函数"""

    def open_window(self, window_type: str, data=None) -> None:
        if window_type == "image_switcher":
            from subwindow import ImageSwitcher
            window = ImageSwitcher(callback=self.callback_Numberli)
        elif window_type == "text_browser":
            from html示例 import ArticleBrowser
            window = ArticleBrowser(callback=self.callback_gua_message)
        elif window_type == "switch_name":
            from subwindow import Switch_GuaName
            window = Switch_GuaName(callback=self.callback_Numberli)
        elif window_type == "dict_reader":
            from subwindow import GuaImageReader
            window = GuaImageReader(data_dict=data)
        elif window_type == "config_change":
            from subwindow import ConfigEditor
            window = ConfigEditor()
        elif window_type == "load_database":
            from subwindow import Database
            for child_window in self.child_windows:
                if child_window.windowTitle() == '卦例数据库':
                    child_window.close()
            window = Database(path=self.default_db_path, callback=self.callback_Guaimage)

        window.show()
        self.child_windows.append(window)

    def callback_Numberli(self, string: str):
        # 摇卦结束的回调函数
        self.setText(f"收到参数: {string}")
        self.input2.setText(string)

    def callback_gua_message(self, url):
        self.setText('从浏览器获得了参数！')
        self.text_box.auto_open_url(url)

        result = craw_detail_page_gua_pic(url)  # 可用
        if result:
            title, time, message_lst = result
        else:
            return

        gua_key = ' '.join(message_lst)
        self.input1.setText(title)
        self.input3.setText(gua_key)
        self.text_box.clear()
        self.text_box.append(f'{url}\n{time}\n{gua_key}\n')

    def callback_Guaimage(self, row):
        # 数据库选中记录，执行的回调函数
        self.setText("卦象加载完成！")

        title, month, rigan, richen, GUANAME, BIANGUA, _, GuaImage, Analysis, Comment = row
        self.input1.setText(title)
        self.input3.setText(f"{month}月{rigan}{richen}日{GUANAME}{BIANGUA}")
        # 卦象文本，本来可能是居中的：
        self.gua_image_label.setText(GuaImage)
        self.gua_image_label.setAlignment(Qt.AlignLeft)
        self.text_box.clear()
        self.text_box.setText(Analysis)
        # 笔记盒，本来可能是隐藏的：
        self.note_textbox.clear()
        self.note_textbox.setVisible(True)
        self.note_textbox.setText(Comment)

    """清理QLabel文字"""

    def setText(self, text: str):
        prev_text = self.message_label.text()
        if text == prev_text:
            text += '👉 +1'
        elif text in prev_text and ' +' in prev_text:
            lst = list(prev_text.split('+'))
            num = int(lst[-1])
            text = lst[0] + '+' + str(num+1)
        self.message_label.setText(text)

    """自动处理文本"""

    def identify_text(self, widget, max_match=False):
        # widget是一个QLineEdit，文本变动时传入
        indentify_string = widget
        if len(indentify_string) > 20:
            max_match = True

        # 主动识别字符串，执行”选择数据库“，“选择用神”的自动化处理。
        cfg = configparser.ConfigParser()  # configparser方法虽好，也造成迁移麻烦。迁移时，没有数据库，只选择用神
        cfg.read('config.ini', encoding='utf-8')  # 重新读取，使用过程中可以改动

        for section in cfg.sections():
            if any(kw in indentify_string for kw in cfg.get(section, 'kw_lst').split(',')):
                self.auto_switch_comb(cfg.get(section, 'yongshen'), cfg.get(section, 'db_path'),
                                      cfg.get(section, 'method'))  # 【bug】自动到下拉选项中寻找，这并不代表准确地址

        s = identify_GuaName(indentify_string, max_match)
        if s:
            self.input2.setText(s)

        s = identify_60HuaJia(indentify_string)
        if s:
            self.input3.setText(s)
            # self.stay_stop = True

    def auto_switch_comb(self, yongshen: str, db_path: str, txt_path: str = ''):
        lis = [(yongshen, self.yongshen_combox), (db_path, self.switch_db_comobox), (txt_path, self.select_TxtComb)]
        for value, UI_combox in lis:
            if not value:
                continue
            for index in range(UI_combox.count()):
                if UI_combox.itemText(index) == value:
                    UI_combox.setCurrentIndex(index)
                    break

    def notebox_format(self):
        # 接收文本对象，执行删改；特定的格式需要修改，删除影响不大。
        text = self.note_textbox.toPlainText()
        if "[" not in text:
            return

        import re
        pattern = r'\[(蓝|红|绿|土|水|金|火|木)\]'
        result = re.sub(pattern, '', text)
        if result != text:
            self.note_textbox.setText(result)

    """关闭事件"""

    def closeEvent(self, event):
        # 在这里放置关闭窗口时需要执行的代码
        for child_window in self.child_windows:
            try:
                child_window.close()
            except:
                print(child_window, '关闭失败')
        sys.stdout = sys.__stdout__
        print("窗口关闭了")
        event.accept()  # 接受关闭事件


def craw_detail_page_gua_pic(url=None):
    try:
        from bs4 import BeautifulSoup
        from cnocr import CnOcr
        import re
        import requests

    except ImportError as e:
        print(e, '发生了导入故障，导致不能启动爬虫!')
        return None

    if not url:
        url = "https://tieba.baidu.com/p/8862322320"  # 将这里的 url 替换成需要处理的网页地址
    try:
        html = requests.get(url).text
    except requests.exceptions.ConnectionError as e:
        print(e, '请确认是否有网络通信！')
        return

    soup = BeautifulSoup(html, "html.parser")

    h3_tag = soup.find('h3', class_='core_title_txt pull-left text-overflow')
    if h3_tag and h3_tag.string:
        title = h3_tag.string.strip()

    else:
        title = '标题找不到!'

    img_tag = soup.find("img", {"class": "BDE_Image"})
    if not img_tag:
        return None
    img_src = img_tag.get("src")

    # 获取图片
    img_data = requests.get(img_src).content
    with open("file/temp.jpg", "wb") as f:
        f.write(img_data)

    # 使用 OCR 进行文字识别
    ocr = CnOcr()
    out = ocr.ocr("file/temp.jpg")
    # img = Image.open(BytesIO(img_data))    # ocr = CnOcr()    # out = ocr.ocr(img)
    time_lst = [item['text'] for item in out if re.match(r'\d{4}', item['text'])]  # -\d{1,2}-\d{1,2}
    if time_lst:
        time = time_lst[0]
    else:
        time = '没有找到时间!'

    texts = [item['text'] for item in out if re.search(r'[甲乙丙丁戊己庚辛壬癸天泽火震风水地山]', item['text'])]
    texts = [text for text in texts if all(s not in text for s in ['父母', '兄弟', '子孙', '妻财', '官鬼', ':'])]

    replace_dict = {'央': '夬', '夫': '夬', '宽': '贲', '责': '贲', '松': '讼', '良': '艮',
                    '已': '己', '王': '壬', '主': '壬', '黄': '寅', '西': '酉', '成': '戌', }  # 错别字

    texts = [text if not any(char in text for char in replace_dict.keys()) else ''.join(
        replace_dict.get(char, char) for char in text) for text in texts]

    return title, time, texts


class DragLineEdit(QLineEdit):
    # QQ浏览器的拖拽功能做的非常好；edge也可以，但是不能拖拽百度文库；火狐最差
    # 拖拽后不会删除原来文本
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.setText(event.mimeData().text())


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CustomTextEdit, self).__init__(parent)

    def contextMenuEvent(self, event):
        # 创建右键菜单
        menu = self.createStandardContextMenu()
        action_visit = QAction("访问", self)
        action_visit.triggered.connect(self.open_url)

        menu.addAction(action_visit)

        # 显示菜单
        menu.exec_(event.globalPos())
        event.accept()

    def open_url(self):
        # 获取当前光标位置的文本
        cursor = self.textCursor()
        selected_text = cursor.selectedText().strip()  # 三击选中，一般带有换行符

        # 检查是否是URL，使用系统的默认浏览器打开URL
        self.auto_open_url(selected_text)

    def auto_open_url(self, url):
        if url and url.startswith('http'):
            QDesktopServices.openUrl(QUrl(url))


class ALL_Widget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建左侧物件：左上，左下
        self.input1 = DragLineEdit()
        self.input2 = DragLineEdit()
        self.input3 = DragLineEdit()
        self.input1.setPlaceholderText("请输入占题")
        self.input2.setPlaceholderText("请输入硬币数:6-5-4-3-2-1 or 123456")
        self.input3.setPlaceholderText("请输入日干，月令，日辰")
        self.button1 = QPushButton("排 盘 🚀")  # 传统排卦的按钮，emoji
        self.button2 = QPushButton("复 制 🌻")
        self.button3 = QPushButton("排 盘 ✈️")  # 梅花排卦的按钮
        self.button3.setVisible(False)

        self.combo_box1 = QComboBox()
        self.combo_box2 = QComboBox()
        self.switch_db_comobox = QComboBox()
        self.switch_mode_comobox = QComboBox()
        self.select_analy_mode = QComboBox()
        self.init_fill_combobox()
        self.init_fill_db_combobox()

        self.chk_box = QCheckBox('是否计算明细', self)  # 创建一个QRadioButton对象
        self.chk_dialog = QCheckBox('是否启用对话功能', self)  # 创建一个QRadioButton对象
        self.chk_dialog.setChecked(False)
        self.chk_dialog.stateChanged.connect(self.show_dialog)
        self.write_cell_btn = QPushButton('修 改 备 注 🐳')  # emoji
        self.browser_btn = QPushButton('打 开 贴 吧 🌍')
        self.shake_btn = QPushButton("摇 卦 ☘️")
        self.save_btn = QPushButton("保 存 🕊️")
        self.name_btn = QPushButton("卦 名 起 卦 🪁")
        self.load_btn = QPushButton("加 载 📁")
        self.auto_btn = QPushButton("电 脑 起 卦 🐧")
        self.extract_tags_btn = QPushButton("提 取 标 签 📜")
        self.extract_tags_btn.clicked.connect(self.extract_tags)
        self.auto_btn.clicked.connect(self.craw_page_gua)

        # 创建右侧物件：右上，右中，右下
        self.gua_image_label = QLabel('*' * 8 + " 任叶三沐风排盘 " + '*' * 8)
        self.gua_image_label.setAlignment(Qt.AlignCenter)
        self.gua_image_label.setFont(QFont('楷体', 12))  # 设置字体为Arial，大小为20
        self.other_label = QLabel()
        self.other_label.setFont(QFont('楷体', 12))  # 设置字体为Arial，大小为20
        self.note_textbox = QTextEdit()
        self.note_textbox.setVisible(False)
        self.note_textbox.setMinimumWidth(360)
        self.note_textbox.setMaximumHeight(600)

        self.message_label = QLabel("就绪")
        self.message_label.setAlignment(Qt.AlignCenter)

        self.text_box = CustomTextEdit()
        self.text_box.setFont(QFont('楷体', 12))  # 设置字体字号
        self.text_box.setMinimumHeight(600)

        stdout_redirector = StdoutRedirector(self.text_box)
        sys.stdout = stdout_redirector

        self.input_dialog = QLineEdit()
        # 连接QLineEdit的按键按下事件
        self.input_dialog.installEventFilter(self)
        self.confir_btn = QPushButton('确 定')
        self.export_btn = QPushButton('导 出')

        self.initUI()
        self.show_dialog()

    def initUI(self):
        # 放置左上物件
        left_up_layout = QVBoxLayout()
        left_up_layout.addWidget(self.input1)
        left_up_layout.addWidget(self.input2)
        left_up_layout.addWidget(self.input3)

        left_inner_layout = QHBoxLayout()
        left_inner_layout.addWidget(self.button1)
        left_inner_layout.addWidget(self.button3)
        left_inner_layout.addWidget(self.button2)
        left_up_layout.addLayout(left_inner_layout)

        # 放置左下物件
        left_down_layout = QGridLayout()
        left_down_layout.addWidget(QLabel("用神"), 0, 0)
        left_down_layout.addWidget(self.combo_box1, 1, 0)
        left_down_layout.addWidget(QLabel("命爻"), 0, 1)
        left_down_layout.addWidget(self.combo_box2, 1, 1)
        left_down_layout.addWidget(QLabel("当前数据库"), 2, 0)
        left_down_layout.addWidget(self.switch_db_comobox, 3, 0)
        left_down_layout.addWidget(QLabel("切换模式"), 2, 1)
        left_down_layout.addWidget(self.switch_mode_comobox, 3, 1)
        left_down_layout.addWidget(self.select_analy_mode, 4, 0)
        left_down_layout.addWidget(self.chk_box, 5, 0)
        left_down_layout.addWidget(self.chk_dialog, 5, 1)
        left_down_layout.addWidget(self.write_cell_btn, 6, 0)
        left_down_layout.addWidget(self.browser_btn, 6, 1)
        left_down_layout.addWidget(self.shake_btn, 7, 0)
        left_down_layout.addWidget(self.save_btn, 7, 1)
        left_down_layout.addWidget(self.name_btn, 8, 0)
        left_down_layout.addWidget(self.load_btn, 8, 1)
        left_down_layout.addWidget(self.auto_btn, 9, 0)
        left_down_layout.addWidget(self.extract_tags_btn, 9, 1)

        # 创建左上布局
        LEFT_Layout = QVBoxLayout()
        left_up_region = QGroupBox("排盘区域")
        left_up_region.setLayout(left_up_layout)

        # 创建左下布局
        left_down_region = QGroupBox("功能区域")
        left_down_region.setLayout(left_down_layout)

        LEFT_Layout.addWidget(left_up_region)
        LEFT_Layout.addWidget(left_down_region)

        # 创建右上布局
        RIGHT_Layout = QVBoxLayout()

        right_up_layout = QHBoxLayout()
        right_up_layout.addWidget(self.gua_image_label)
        right_up_layout.addWidget(self.other_label)
        right_up_layout.addWidget(self.note_textbox)

        right_down_layout = QVBoxLayout()
        right_down_layout.addWidget(self.message_label)
        right_down_layout.addWidget(self.text_box)

        self.dialog_layout = QVBoxLayout()
        self.dialog_layout.addWidget(self.input_dialog)
        inner_dialog_layout = QHBoxLayout()
        inner_dialog_layout.addWidget(self.confir_btn)
        inner_dialog_layout.addWidget(self.export_btn)
        self.dialog_layout.addLayout(inner_dialog_layout)

        right_down_layout.addLayout(self.dialog_layout)

        RIGHT_Layout.addLayout(right_up_layout)
        RIGHT_Layout.addLayout(right_down_layout)

        # 创建平行布局
        main_layout = QHBoxLayout()
        main_layout.addLayout(LEFT_Layout)
        main_layout.addLayout(RIGHT_Layout)

        self.setLayout(main_layout)  # QWidgt才能这样设置

    def init_fill_combobox(self):
        yongshen_options = [("世", "世"), ("应", "应"), ("父母", "父母"), ("兄弟", "兄弟"), ("子孙", "子孙"),
                            ("妻财", "妻财"), ("官鬼", "官鬼"), ]
        liuqin_options = ["亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"]
        mode_optins = ["传统排卦", "梅花排卦"]

        # 添加选项
        for text, value in yongshen_options:
            self.combo_box1.addItem(text, value)

        # 添加选项
        for value in liuqin_options:
            self.combo_box2.addItem(value)

        for value in mode_optins:
            self.switch_mode_comobox.addItem(value)

        self.combo_box2.setCurrentIndex(-1)

    def init_fill_db_combobox(self):
        folder_path = "data"
        print(f"数据库文件储存路径:{folder_path}")

        if not os.path.exists(folder_path):  # 如果文件夹不存在，则创建它
            os.makedirs(folder_path)

        db_files = [f for f in os.listdir(folder_path) if f.endswith('.db')]  # 获取文件夹内的所有数据库文件名
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]  # 获取文件夹内的所有数据库文件名
        self.select_analy_mode.clear()  # 清空现有的选项
        self.select_analy_mode.addItem("")
        self.select_analy_mode.addItems(txt_files)
        self.switch_db_comobox.clear()  # 清空现有的选项

        if len(db_files) > 0:
            self.switch_db_comobox.addItems(db_files)  # 将数据库文件名添加到选项中
            self.switch_db_comobox.setCurrentIndex(0)  # 默认选中第一个选项
        else:
            print("没有其他文件，只有database.db")
            default_db_file = 'database.db'  # 默认数据库文件名
            self.switch_db_comobox.addItem(default_db_file)  # 添加默认选项
            self.switch_db_comobox.setCurrentIndex(0)  # 默认选中默认选项

    def craw_page_gua(self):
        from 爬取八卦 import test_get_page
        if text := test_get_page():
            self.input3.setText(text)
            self.message_label.setText(f'🆗已返回参数:“{text[-10:]}”!')

    def show_dialog(self):
        '''
        设置dialog_layout布局可见性，该布局包括：输入栏LineEdit，提交按钮，导出按钮
        用一个复选框的状态check
        '''
        if self.chk_dialog.isChecked():
            self.input_dialog.setVisible(True)
            self.confir_btn.setVisible(True)
            self.export_btn.setVisible(True)
        else:
            self.input_dialog.setVisible(False)
            self.confir_btn.setVisible(False)
            self.export_btn.setVisible(False)

    def extract_tags(self):
        content = self.text_box.toPlainText()
        tags = re.findall(r'·(.*?)：', content)

        # 使用列表推导式去除每个元素内部的空格
        tags = ['·' + tag.replace(' ', '') for tag in tags]

        if tags:
            self.note_textbox.append('标签')
            self.note_textbox.append('\n'.join(tags))

            print()  # 可以将提取出的标签打印出来，也可以将其添加到列表中进行后续处理


class StdoutRedirector:
    def __init__(self, widget):
        self.widget = widget  # 输出流重定向

    def write(self, text):
        cursor = self.widget.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.widget.setTextCursor(cursor)
        self.widget.ensureCursorVisible()


if __name__ == '__main__':
    app = QApplication([])
    window = MainPlace()
    icon = QIcon(r"D:\python文件\place\64.ico")
    window.setWindowIcon(icon)
    window.show()
    app.exec_()
