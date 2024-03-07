from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QLabel, QGridLayout

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
            if self.gua_num == self.biangua_num :
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


if __name__ == '__main__':
    app = QApplication([])
    window = Switch_GuaName()
    window.show()
    app.exec_()
