import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QComboBox, QGroupBox, QGridLayout, QStyledItemDelegate, \
    QStyleOptionViewItem, QHeaderView, QStyle, QTableView, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
import sqlite3
from PyQt5.QtGui import QColor, QPainter, QFont, QPalette, QPixmap


class ImageSwitcher(QWidget):
    def __init__(self, callback=None):
        super().__init__()

        self.callback = callback
        self.image_timer1 = QTimer(self)
        self.image_timer2 = QTimer(self)
        self.image_timer3 = QTimer(self)

        self.image_timer1.timeout.connect(self.switch_image1)
        self.image_timer2.timeout.connect(self.switch_image2)
        self.image_timer3.timeout.connect(self.switch_image3)

        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_stop_switching)

        self.layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()

        self.hbox_layout.addWidget(self.create_image_label())
        self.hbox_layout.addWidget(self.create_image_label())
        self.hbox_layout.addWidget(self.create_image_label())

        self.layout.addLayout(self.hbox_layout)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)

        self.labels = []
        yang = 'img/0.jpg'
        ying = 'img/1.jpg'
        self.images = [yang,ying]
        self.current_index1 = 0
        self.current_index2 = 0
        self.current_index3 = 0

        self.total_sum = 0
        self.count = 0
        self.sum_label = QLabel()
        self.sum_label.setText("结果：0")
        self.coinsNumber_list = []

        self.layout.addWidget(self.sum_label)

    def create_image_label(self):
        label = QLabel()
        label.setFixedSize(148, 148)
        return label

    def start_stop_switching(self):
        if not self.image_timer1.isActive():
            if self.count >= 6:
                # 列表合成字符串
                li_str = [str(num) for num in self.coinsNumber_list]
                string = ".".join(li_str)

                # 执行回调函数
                self.callback(string=string)
                self.close()

            self.image_timer1.start(10)
            self.image_timer2.start(20)
            self.image_timer3.start(40)
            self.start_button.setText("停止")


        else:
            self.image_timer1.stop()
            self.image_timer2.stop()
            self.image_timer3.stop()
            self.calculate_sum()
            self.show_result()
            if self.count >= 6:
                self.start_button.setText("返回主界面")
            else:
                self.start_button.setText("开始")

    def switch_image1(self):
        pixmap = QPixmap(self.images[self.current_index1])
        label = self.hbox_layout.itemAt(0).widget()
        label.setPixmap(pixmap)
        self.current_index1 = (self.current_index1 + 1) % 2

    def switch_image2(self):
        pixmap = QPixmap(self.images[self.current_index2])
        label = self.hbox_layout.itemAt(1).widget()
        label.setPixmap(pixmap)
        self.current_index2 = (self.current_index2 + 1) % 2

    def switch_image3(self):
        pixmap = QPixmap(self.images[self.current_index3])
        label = self.hbox_layout.itemAt(2).widget()
        label.setPixmap(pixmap)
        self.current_index3 = (self.current_index3 + 1) % 2

    def calculate_sum(self):
        self.total_sum = 0
        self.total_sum += self.current_index1
        self.total_sum += self.current_index2
        self.total_sum += self.current_index3
        self.sum_label.setText(f"结果：{self.total_sum}")
        self.coinsNumber_list.append(self.total_sum)

    def show_result(self):
        gua_image = ['▅▅　▅▅ × ▅▅▅▅▅', '▅▅▅▅▅    ▅▅▅▅▅', '▅▅　▅▅    ▅▅　▅▅', '▅▅▅▅▅ ○ ▅▅　▅▅']
        self.count = len(self.labels) + 1
        result_label = QLabel()
        result_label.setText(f"第{self.count}次摇卦结果：{gua_image[self.total_sum]}")
        self.labels.append(result_label)

        image_layout = QVBoxLayout()
        # 清空 new_layout 的子部件
        while image_layout.count():
            item = image_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 将 self.labels 列表的标签倒序添加到 self.layout 中
        for label in reversed(self.labels):
            image_layout.addWidget(label)

        self.layout.addLayout(image_layout)

        if self.count == 6:
            List_label = QLabel()
            List_label.setText(f"最终摇卦结果：{self.coinsNumber_list}")
            self.layout.addWidget(List_label)
            self.labels.append(List_label)

    def get_coinsNumber_list(self):
        return self.coinsNumber_list


class Switch_GuaName(QWidget):
    def __init__(self, callback=None):
        super().__init__()
        palace = ['乾宫', '震宫', '坎宫', '巽宫', '艮宫', '坤宫', '离宫', '兑宫']
        self.guaname = [
            '乾', '姤', '遁', '否', '观', '剥', '晋', '大有', '震', '豫', '解', '恒', '升', '井', '大过', '随',
            '坎', '节', '屯', '既济', '革', '丰', '明夷', '师', '巽', '小畜', '家人', '益', '无妄', '噬嗑', '颐', '蛊',
            '艮', '贲', '大畜', '损', '睽', '履', '中孚', '渐', '坤', '复', '临', '泰', '大壮', '夬', '需', '比',
            '离', '旅', '鼎', '未济', '蒙', '涣', '讼', '同人', '兑', '困', '萃', '咸', '蹇', '谦', '小过', '归妹']
        self.gua_num = 64
        self.biangua_num = 64
        self.output = ""
        self.callback = callback

        # 创建布局管理器
        main_layout = QVBoxLayout()
        group_layouts = []

        # 创建8个QGroupBox和每个GroupBox内的8个QPushButton
        for i in range(8):
            group_box = QGroupBox(f"{palace[i]}")
            group_layout = QHBoxLayout()
            group_layouts.append(group_layout)

            for j in range(8):
                button = QPushButton(f"{self.guaname[i * 8 + j]}")
                button.clicked.connect(lambda checked, idx=i * 8 + j: self.update_status_label(idx))
                group_layout.addWidget(button)

            group_box.setLayout(group_layout)
            main_layout.addWidget(group_box)

        # 创建状态标签和确定按钮
        button_layout = QGridLayout()
        self.status_label = QLabel("请选择卦象...")
        self.result_label = QLabel("")
        self.confirm_button = QPushButton("确 定")
        self.confirm_button.clicked.connect(self.on_confirm_clicked)
        self.clear_button = QPushButton("清 除")
        self.clear_button.clicked.connect(self.clear_label)

        button_layout.addWidget(self.status_label, 0, 0)
        button_layout.addWidget(self.result_label, 0, 1)
        button_layout.addWidget(self.confirm_button, 1, 0)
        button_layout.addWidget(self.clear_button, 1, 1)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_status_label(self, idx):
        self.status_label.setText(f"按下了序号： {idx}")

        if self.gua_num == 64:
            # 主卦没有数，idx赋值给他
            self.gua_num = idx
        elif self.biangua_num == 64:
            # 变卦没有数，idx赋值给他
            self.biangua_num = idx
        else:
            # 都有数，idx赋值，轮换
            self.gua_num = self.biangua_num
            self.biangua_num = idx

        if self.biangua_num != 64:
            # 主卦变卦都有数，相同只显示一个，不同都显示。
            if self.gua_num == self.biangua_num:
                string = f"主卦:{self.guaname[self.gua_num]}"
                self.output = f"{self.gua_num}"
            else:
                string = f"主卦:{self.guaname[self.gua_num]}；变卦:{self.guaname[self.biangua_num]}"
                self.output = f"{self.gua_num} {self.biangua_num}"
        elif self.gua_num != 64:
            # 只有主卦有数。
            string = f"主卦:{self.guaname[self.gua_num]}"
            self.output = f"{self.gua_num}"
        else:
            string = ""
            self.output = ""

        self.result_label.setText(string)

    def on_confirm_clicked(self):
        # 在这里执行确认操作
        if self.output:
            self.callback(string=self.output)
            self.close()
        else:
            self.status_label.setText("不能空手而归！请选择卦象...")

    def clear_label(self):
        self.status_label.setText("请选择卦象...")
        self.result_label.clear()

        self.gua_num = 64
        self.biangua_num = 64
        self.output = ""

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            if self.clear_button.hasFocus():
                self.clear_label()
            else:
                self.on_confirm_clicked()
        else:
            super().keyPressEvent(event)


# 分3个区域，QGroupBox多条件查询
class Database(QMainWindow):
    def __init__(self, path=None, callback=None):
        super().__init__()
        self.path = path if path else 'lottery.db'
        self.current_page = 1
        self.format = "SELECT * FROM data"
        self.callback_function = callback if callback else your_callback_function
        relax_mode = [300, 80, 80, 80, 130, 130, 130, 160, 160, 160, 130]  # 调整column宽的数值
        lottery_mode = [80, 40, 40, 40, 120, 120, 120, 40, 40, 900, None]
        find_mode = [600, 60, 60, 60, 120, 120, 120, 40, 40, 100, None]
        self.all_mode = [relax_mode, lottery_mode, find_mode]

        self.init_UI()
        self.setWindowTitle("卦例数据库")
        self.setGeometry(100, 100, 1800, 1600)

        # 初始化生成器
        self.generator = None
        # 初始化数据库的页面
        self.get_last_300_records()

    def init_UI(self):

        # 创建关键字标签和输入框
        self.Label_1 = QLabel(self)
        self.Label_1.setText("搜索字段：（'/'号分割'或'的条件）")

        self.Entry_kw1 = QLineEdit(self)
        self.Entry_kw1.setPlaceholderText("请输入查询关键字")
        self.Entry_kw2 = QLineEdit(self)
        self.Entry_kw2.setPlaceholderText("请输入查询关键字")
        self.Entry_kw3 = QLineEdit(self)
        self.Entry_kw3.setPlaceholderText("请输入查询数组开头")
        self.Entry_kw4 = QLineEdit(self)
        self.Entry_kw4.setPlaceholderText("请输入查询数组结尾")
        for lineedit in [self.Entry_kw1, self.Entry_kw2, self.Entry_kw3, self.Entry_kw4]:
            lineedit.textChanged.connect(self.search)

        self.combo_r = QComboBox(self)
        self.combo_r2 = QComboBox(self)
        for item in ['标题', '月', '日干', '日支', '主卦', '变卦', '硬币数', '卦象', '分析', '备注']:
            # 添加10个选项，对应列索引从0到9
            self.combo_r.addItem(item)
            self.combo_r2.addItem(item)
        self.combo_r.setCurrentIndex(4)  # 设置combo_r默认选中'主卦'
        self.combo_r2.setCurrentIndex(8)  # 设置combo_r2默认选中'分析'

        # 创建查询按钮
        # self.btn_search = QPushButton(self)
        # self.btn_search.setText("查询")  # 查询
        # self.btn_search.clicked.connect(self.search)

        self.btn_new100 = QPushButton(self)
        self.btn_new100.setText("加载最新的100条记录")
        self.btn_new100.clicked.connect(self.get_last_300_records)

        self.btn_previous = QPushButton(self)
        self.btn_previous.setText("上一页")
        self.btn_previous.clicked.connect(self.on_previous_page)

        self.btn_next = QPushButton(self)
        self.btn_next.setText("下一页")
        # self.btn_load_more.setEnabled(False)
        self.btn_next.clicked.connect(self.on_next_page)

        # 使用QGroupBox封装部分
        search_box = QGroupBox("查询条件", self)
        # search_box.setGeometry(20, 20, 200, 100)
        search_layout = QGridLayout()
        search_layout.addWidget(self.Label_1, 0, 0)
        search_layout.addWidget(self.combo_r, 1, 0)
        search_layout.addWidget(self.combo_r2, 1, 1)
        search_layout.addWidget(self.Entry_kw3, 1, 2)
        search_layout.addWidget(self.Entry_kw1, 2, 0)
        search_layout.addWidget(self.Entry_kw2, 2, 1)
        search_layout.addWidget(self.Entry_kw4, 2, 2)

        search_layout.addWidget(self.btn_new100, 3, 0)
        search_layout.addWidget(self.btn_previous, 3, 1)
        search_layout.addWidget(self.btn_next, 3, 2)
        search_box.setLayout(search_layout)

        self.adjust_btn = QPushButton(self)
        self.adjust_btn.setText("调整长宽")
        self.adjust_btn.clicked.connect(self.adjust_width)

        self.del_btn = QPushButton(self)
        self.del_btn.setText("删除“可以删除”")
        self.del_btn.clicked.connect(self.del_specical_form)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.adjust_btn)
        btn_layout.addWidget(self.del_btn)

        # 创建表格用于显示数据
        self.table_widget = QTableWidget()
        self.table_widget.cellClicked.connect(self.callback)
        try:
            self.table_widget.setColumnCount(11)
        except (TypeError, ValueError) as e:
            try:
                self.table_widget.setColumnCount(10)
                QMessageBox.warning(self, '报错', f'{e}的错误发生了！\n注意这是10列的DB数据库！')
            except Exception as e:
                QMessageBox.warning(self, '报错', f'{e}的错误发生了！\nDB数据库的列数不符合规范！')
        self.table_widget.setHorizontalHeaderLabels(
            ['标题', '月', '日干', '日支', '主卦', '变卦', '硬币数', '卦象', '分析', '备注', '卦例序号'])

        self.idx = 0
        self.adjust_width()

        # 创建布局管理器
        layout = QVBoxLayout()
        layout.addWidget(search_box)
        layout.addLayout(btn_layout)

        # 创建滚动区域并将表格放入其中
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table_widget)

        # 将滚动区域添加到布局
        layout.addWidget(scroll_area)

        # 创建一个容器窗口，将布局设置为容器窗口的布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search(self):
        '''
        目标：   多条件筛选
        有一个不为空，加一个后缀，WHERE开头，AND分割
        全都为空，default format
        '''

        def generate_sql(head_s: str, middle_s: str, end_s: str):
            # 实现的目标：string = "("+" OR ".join([split_lst])+")"，无“/”则正常输出。
            # 示例结果：(gua LIKE '%name1%' OR gua LIKE '%name2%')
            if '/' in middle_s:
                middle_lst = [head_s + n + end_s for n in middle_s.split('/') if n]
                return "(" + " OR ".join(middle_lst) + ")"
            else:
                return head_s + middle_s + end_s

        self.kw1 = self.Entry_kw1.text()
        self.kw2 = self.Entry_kw2.text()
        self.start = self.Entry_kw3.text()
        self.end = self.Entry_kw4.text()
        self.r = self.combo_r.currentIndex()
        self.r2 = self.combo_r2.currentIndex()
        input_lst = [self.kw1, self.kw2, self.start, self.end]

        name = ['title', 'yuel', 'h', 'ric', 'gua', 'biangua', 'coinsNumber_list', 'content1', 'content2', 'content3']
        self.format = "SELECT * FROM data"
        # 更新查询公式
        if any(input_lst):
            conditions = []
            if self.kw1:
                s = generate_sql(f"{name[self.r]} LIKE '%", self.kw1, "%'")
                conditions.append(s)
            if self.kw2:
                s = generate_sql(f"{name[self.r2]} LIKE '%", self.kw2, "%'")
                conditions.append(s)
            if self.start:
                s = generate_sql("coinsNumber_list LIKE '", self.start, "%'")
                conditions.append(s)
            if self.end:
                s = generate_sql("coinsNumber_list LIKE '%", self.end, "'")
                conditions.append(s)
            self.format += " WHERE " + " AND ".join(conditions)

        self.get_records()

        # 连接到数据库并执行查询语句
        # conn = sqlite3.connect(self.path)
        # cursor = conn.cursor()

        # 清空表格内容
        # self.table_widget.setRowCount(0)

        # 重置生成器，暂存100行数据
        # self.generator = self.get_records(cursor)

        # 逐行获取查询结果并进行判断，加载100条记录
        # self.load_more()

        # conn.close()
        # self.table_widget.scrollToBottom()
        # 查询只给出100条记录。生成当前页码和最大页码、最小页码。
        # 设置两个函数，分别是“下一页”，“上一页”。根据当前页码和最大页码、最小页码的关系，设置禁用为True或者False。
        # 这俩函数都是调整页码，然后发起类似get_last_300_records的请求

    '''def get_records(self, cursor):

        count = 0  # 记录已经插入的行数
        while True:
            row = cursor.fetchone()
            if row is None:  # 如果获取的行是None，则结束循环
                return

            # 第二道查询公式
            if row[6].startswith(self.start) and row[6].endswith(self.end):
                yield row

                count += 1
                if count % 100 == 0:  # 每100次暂停一次
                    self.btn_load_more.setEnabled(True)
                    yield None

    def load_more(self):
        if self.generator is None:  # 如果生成器为空，则直接返回
            return

        try:
            for _ in range(100):
                row = next(self.generator)
                if row is None:  # 如果返回None，则暂停函数
                    return
                self.insert_row(row)  # 插入一行记录
        except StopIteration:  # 生成器已经结束
            self.generator = None
            self.btn_load_more.setEnabled(False)  # 禁用"继续加载"按钮'''

    def insert_row(self, row):
        row_index = self.table_widget.rowCount()
        self.table_widget.insertRow(row_index)
        for i, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            self.table_widget.setItem(row_index, i, item)

    def get_last_300_records(self):  # 这是一开始默认执行的函数
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        # 获取表中总行数
        cursor.execute("SELECT COUNT(*) FROM data")
        self.total_rows = cursor.fetchone()[0]

        conn.close()

        start_offset = self.total_rows - 300
        self.get_records(300, start_offset)

    def get_records(self, page_item=100, start_offset=None):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        if not start_offset:
            start_offset = (self.current_page - 1) * 100

        # 清空表格内容
        self.table_widget.setRowCount(0)
        # 查询latest300条记录
        cursor.execute(self.format + f" LIMIT {page_item} OFFSET {start_offset}")
        rows = cursor.fetchall()
        for row in rows:
            self.insert_row(row)

        conn.close()
        self.table_widget.scrollToBottom()
        """通过ORDER BY rowid DESC将结果按照降序排列，LIMIT 100限制结果数量，OFFSET {self.total_rows - 100}指定查询的起始位置为总行数减去300"""

    # 下一页按钮点击事件
    def on_next_page(self):
        self.current_page += 1
        if self.current_page * 100 > self.total_rows:
            self.current_page = int(self.total_rows / 100) + 1
            self.btn_next.setEnabled(False)
        else:
            self.btn_next.setEnabled(True)
        self.btn_previous.setEnabled(True)

        self.get_records()

    # 上一页按钮点击事件
    def on_previous_page(self):
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = 1

        if self.current_page == 1:
            self.btn_previous.setEnabled(False)
        else:
            self.btn_previous.setEnabled(True)
        self.btn_next.setEnabled(True)

        self.get_records()

    def del_specical_form(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        # cursor.execute("DELETE FROM data  WHERE title = 'title'  AND yuel = 'Feb'  AND coinsNumber_list = '123315'")
        # cursor.execute("DELETE FROM data  WHERE title LIKE '测试用例%' ")
        cursor.execute("DELETE FROM data  WHERE content3 = '可以删除' ")
        conn.commit()
        conn.close()
        self.close()

    def adjust_width(self):
        mode_lst = self.all_mode[self.idx]
        for i in range(11):
            if mode_lst[i]:
                self.table_widget.setColumnWidth(i, mode_lst[i])
        self.idx = (self.idx + 1) % 3

    def callback(self, row):
        # 获取需要的行
        selected_row = []
        for i in range(10):
            selected_row.append(self.table_widget.item(row, i).text())

        """Title = self.table_widget.item(row, 0).text()
        GuaImage = self.table_widget.item(row, 7).text()
        Analysis = self.table_widget.item(row, 8).text()
        Comment = self.table_widget.item(row, 9).text()"""

        # 执行回调函数
        self.callback_function(selected_row)


class ColorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.data() == "冲":
            option.palette.setColor(QPalette.Text, QColor("#fa5a57"))  # 设置字体颜色为红色
        elif index.data() == "生":
            option.palette.setColor(QPalette.Text, QColor("#05bd63"))  # 设置字体颜色为绿色
        elif index.data() in ["值", "扶"]:
            option.palette.setColor(QPalette.Text, QColor("#faf002"))  # 设置字体颜色为黄色:#faf002
        elif index.data() == "病":
            option.palette.setColor(QPalette.Text, QColor("#a626a4"))  # 设置字体颜色为粉色
        elif index.data() == "墓":
            option.palette.setColor(QPalette.Text, QColor("#c28606"))  # 设置字体颜色为棕色
        elif index.data() in ["死", "绝"]:
            option.palette.setColor(QPalette.Text, QColor("#b3924d"))  # 设置字体颜色为灰色

        super().paint(painter, option, index)

        # 绘制文字
        font = QFont()
        painter.setFont(font)
        # from PyQt5.QtCore import QRect
        # painter.drawText(option.rect, Qt.AlignCenter,index.data())


# painter.fillRect(option.rect, QColor("#707b8d"))


class GuaImageReader(QMainWindow):
    def __init__(self, data_dict):
        super().__init__()

        self.data_dict = data_dict
        self.initUI()

    def initUI(self):
        self.setWindowTitle("排盘计算结果")
        self.setGeometry(100, 100, 1700, 1200)

        self.mode_comobox = QComboBox()
        self.mode_comobox.addItem("输出文本")
        self.mode_comobox.addItem("输出数字")
        self.mode_comobox.setCurrentIndex(0)
        # print(self.mode_comobox.currentText())

        # 使用QGroupBox封装部分
        search_box = QGroupBox("查询条件", self)
        search_layout = QGridLayout()
        search_layout.addWidget(QLabel('输出模式：'), 0, 0)
        search_layout.addWidget(self.mode_comobox, 1, 0)
        search_layout.addWidget(QComboBox(), 1, 1)
        search_layout.addWidget(QLineEdit(), 1, 2)
        search_layout.addWidget(QLabel('关键字2'), 2, 0)
        search_layout.addWidget(QLineEdit(), 2, 1)
        search_layout.addWidget(QLineEdit(), 2, 2)
        search_box.setLayout(search_layout)

        # 创建查询按钮
        self.btn_search = QPushButton(self)
        self.btn_search.setText("输出为excel")
        self.btn_search.move(20, 80)
        self.btn_search.clicked.connect(self.OutputExl)

        self.btn_load_more = QPushButton(self)
        self.btn_load_more.setText("输出为excel")
        self.btn_load_more.setEnabled(False)
        # self.btn_load_more.clicked.connect(self.load_more)

        self.btn_new100 = QPushButton(self)
        self.btn_new100.setText("加载最新的100条记录")
        # self.btn_new100.clicked.connect(self.get_last_100_records)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_load_more)
        btn_layout.addWidget(self.btn_new100)

        # 创建表格用于显示数据
        self.table_widget = QTableWidget()
        # self.table_widget.cellClicked.connect(self.callback)
        length = len(self.data_dict)
        self.table_widget.setColumnCount(length)
        for i in range(length):
            self.table_widget.setColumnWidth(i, 70)

        # 设置委托
        delegate = ColorDelegate(self.table_widget)
        self.table_widget.setItemDelegate(delegate)

        # 设置表头
        self.table_widget.setHorizontalHeaderLabels(list(self.data_dict.keys()))
        self.table_widget.setRowCount(len(self.data_dict['爻位']))
        self.table_widget.clearContents()

        # 添加行数据
        for i in range(len(self.data_dict['爻位'])):
            row = [self.data_dict[k][i] for k in self.data_dict]
            self.table_widget.setRowHeight(i, 60)
            for j in range(len(row)):
                item = QTableWidgetItem(str(row[j]))
                self.table_widget.setItem(i, j, item)

        # 创建布局管理器
        layout = QVBoxLayout()
        layout.addWidget(search_box)
        layout.addLayout(btn_layout)

        # 创建滚动区域并将表格放入其中
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table_widget)

        # 将滚动区域添加到布局
        layout.addWidget(scroll_area)

        # 创建一个容器窗口，将布局设置为容器窗口的布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def OutputExl(self):
        import pandas as pd
        import datetime

        # 转换为DataFrame
        df = pd.DataFrame.from_dict(self.data_dict, orient='index')

        # 转置DataFrame，使得表头在上方，数据在下方
        df = df.transpose()

        # 输出到Excel
        try:
            df.to_excel(f'file/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_op.xlsx', index=False)
        # 如果不存在file文件夹
        except FileNotFoundError:
            import os
            os.mkdir('file')
            df.to_excel(f'file/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_op.xlsx', index=False)


def your_callback_function(row):
    # 在这里执行你的回调函数逻辑
    # 更新！！
    print("Callback function executed with values:", row[9])


if __name__ == '__main__':
    app = QApplication([])
    data_dict = {'爻位': ['Value1', 'Value2', 'Value3', 'Value2', 'Value3'],
                 'Key2': ['Value4', 'Value5', 'Value6', 'Value2', 'Value3']}
    window = GuaImageReader(data_dict)
    window.show()
    app.exec_()
