import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


def create_table(data=None, colors=None):
    # 创建应用和主窗口
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    # 初始化表格
    table = QTableWidget(10, 5)  # 10行5列
    layout.addWidget(table)

    default_font = table.font()  # 获取当前默认字体
    default_font.setFamily('楷体')
    default_font.setPointSize(14)  # 设置默认字体的大小为 12 点
    table.setFont(default_font)  # 应用新的默认字体设置

    # 字符矩阵和颜色矩阵
    if not data:
        data = [
            ["abc", "def", "ghi", "jkl", ""],
            ["mno", "pqr", "stu", "vwx", ""],
            ["yz", "123", "456", "789", ""],
            ["abc1", "def2", "ghi3", "jkl4", ""],
            ["a", "b", "c", "d", "e"],
            ["f", "g", "h", "i", "j"],
            ["k", "l", "m", "n", "o"],
            ["p", "q", "r", "s", "t"],
            ["u", "v", "w", "x", "y"],
            ["z", "1", "2", "3", "4"]
        ]

    if not colors:
        colors = [
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],
            # 六神。腾蛇用灰色 #acadb2，白虎为红色 #ff5733，玄武为黑色 none，青龙为绿色 #4b9e5f，朱雀为橙色 #f86d43，勾陈为土黄色 #c18401，
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],
            # 伏神。休囚用深红色 ，过弱用鲜红色 #ff5733，旺相用土黄色 #c18401，过旺用亮黄色，空亡用灰色 #acadb2，
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],  # 主卦
            ['', '', '', '', '', '', '', '', '', ''],  # 世应
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '', ''],
            # 变爻,如果设置空字符，代表这一单元格保持原来的黑色字体，非空字符，设置对应的颜色
        ]

    # 设置表格的数据和颜色
    for i in range(10):
        for j in range(5):
            if j >= len(data[i]):
                break
            item = QTableWidgetItem(data[i][j])

            # 检查颜色矩阵对应的颜色值
            if j < len(colors):  # 确保不越界
                color_code = colors[j][i]  # 获取颜色
                if color_code != '':  # 如果颜色非空
                    item.setForeground(QColor(color_code))  # 设置字体颜色

            table.setItem(i, j, item)

    # 合并前四列
    table.setSpan(0, 0, 1, 5)  # 第一行，合并前4列
    table.setSpan(1, 0, 1, 5)  # 第二行，合并前4列
    table.setSpan(2, 0, 1, 5)  # 第三行，合并前4列
    table.setSpan(3, 0, 1, 5)  # 第四行，合并前4列

    # 设置窗口大小适应表格内容
    adjust_table_size(table)  # 【根据长宽最大的一个单元格，设置长宽】
    # table.resizeRowsToContents() # 根据每行中最高的单元格内容，自动调整每行的高度。

    # 设置表格显示
    window.setMinimumSize(1100, 660)
    window.setLayout(layout)
    window.setWindowTitle("字符矩阵展示")

    # 显示窗口
    window.show()
    sys.exit(app.exec_())


class ColorfulPlace(QWidget):
    def __init__(self, data=None, colors=None):
        super().__init__()
        self.data = data if data else self.default_data()
        self.colors = colors if colors else self.default_colors()
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)

        # 初始化表格
        self.table = QTableWidget(10, 5)  # 10行5列
        layout.addWidget(self.table)

        self.button = QPushButton('总列长度：0')
        self.button.clicked.connect(self.check_width)
        layout.addWidget(self.button)

        # 设置表格的字体和大小
        default_font = self.table.font()
        default_font.setFamily('楷体')
        default_font.setPointSize(14)  # 设置默认字体的大小为 14 点
        self.table.setFont(default_font)

        # 合并前四列
        self.table.setSpan(0, 0, 1, 5)  # 第一行，合并前4列
        self.table.setSpan(1, 0, 1, 5)  # 第二行，合并前4列
        self.table.setSpan(2, 0, 1, 5)  # 第三行，合并前4列
        self.table.setSpan(3, 0, 1, 5)  # 第四行，合并前4列

        # 设置窗口属性
        self.setMinimumSize(1100, 750)
        self.setWindowTitle("字符矩阵展示")

        # 设置表格的数据和颜色
        self.set_table_data_and_colors()

        # 设置窗口大小适应表格内容
        adjust_table_size(self.table)

    def default_data(self):
        return [
            ["abc", "def", "ghi", "jkl", ""],
            ["mno", "pqr", "stu", "vwx", ""],
            ["yz", "123", "456", "789", ""],
            ["abc1", "def2", "ghi3", "jkl4", ""],
            ["a", "b", "c", "d", "e"],
            ["f", "g", "h", "i", "j"],
            ["k", "l", "m", "n", "o"],
            ["p", "q", "r", "s", "t"],
            ["u", "v", "w", "x", "y"],
            ["z", "1", "2", "3", "4"]
        ]

    def default_colors(self):
        return [
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456', '#ff5733'],
            ['', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '#c18401', '#acadb2', '#4078f2', '#ff5733', '', '']
        ]

    def set_table_data_and_colors(self, data=None, colors=None):
        self.table.clearContents()

        if data:
            self.data = data
        if colors:
            self.colors = colors

        for i in range(10):
            for j in range(5):
                if j >= len(self.data[i]):
                    break
                item = QTableWidgetItem(self.data[i][j])

                # 检查颜色矩阵对应的颜色值
                if j < len(self.colors):  # 确保不越界
                    color_code = self.colors[j][i]  # 获取颜色
                    if color_code != '':  # 如果颜色非空
                        item.setForeground(QColor(color_code))  # 设置字体颜色

                self.table.setItem(i, j, item)

    def check_width(self):
        if self.table.rowCount() == 0 or self.table.columnCount() == 0:
            self.button.setText("总列长度：表格为空")
            return
        total_width = sum(self.table.columnWidth(col) for col in range(self.table.columnCount()))
        self.button.setText(f"总列长度：{total_width}")


def adjust_table_size(table):
    title_per_length = 24  # 你可以调节此倍数来适配具体的字体（默认字体8->18，当前12->22,14->25）x_0=10,Δ=1
    word_per_length = 39  # 你可以调节此倍数来适配具体的字体（默认字体8->28，当前12->35，14->39）x_0=10,Δ=3.5

    # 获取列数和行数
    row_count = table.rowCount()
    column_count = table.columnCount()

    whole_width = 0
    # 遍历每列，计算最大宽度
    for col in range(1, column_count):
        max_width = 0
        for row in range(row_count):
            item = table.item(row, col)
            if item is not None:
                # text_width = item.fontMetrics().boundingRect(item.text()).width()# 不用这么复杂的，根据文本的长度大概确定text_width
                text_length = len(item.text().strip())  # 计算文本长度
                # 假设每个字符宽度为 8 像素，可以根据实际情况调整
                estimated_width = text_length * word_per_length
                max_width = max(max_width, estimated_width, 80)
        # 设置列宽为最大宽度
        table.setColumnWidth(col, max_width + 10)  # +10是为了留些额外的空间
        whole_width += max_width + 10

    max_width = 0
    for row in range(row_count):
        item = table.item(row, 0)
        text_length = len(item.text().strip())  # 计算文本长度
        estimated_width = text_length * title_per_length
        max_width = max(max_width, estimated_width, 900)

    table.setColumnWidth(0, max_width - whole_width)

    # 遍历每行，计算最大高度
    for row in range(row_count):
        # max_height = 0
        # for col in range(column_count):
        #     item = table.item(row, col)
        #     if item is not None:
        #         text_height = item.fontMetrics().boundingRect(item.text()).height()
        #         max_height = max(max_height, text_height)
        # 设置行高为最大高度
        # table.setRowHeight(row, max_height + 5)  # +5是为了留些额外的空间
        table.setRowHeight(row, 15)  # +5是为了留些额外的空间


if __name__ == "__main__":
    # create_table()
    app = QApplication(sys.argv)
    colorful_place = ColorfulPlace()
    colorful_place.show()
    sys.exit(app.exec_())

'''
每个单元格设置不同的颜色，沿用上述代码。
若同一列设置一样的颜色，可以使用以下代码:

colors = [
        '#c18401', '#acadb2', '#4078f2', '#ff5733', '#123456'
    ]
for i in range(10):
    for j in range(5):
        item = QTableWidgetItem(data[i][j])
        if j < 4:  # 前四列设置字体颜色
            item.setForeground(QColor(colors[j]))
        table.setItem(i, j, item)
'''
