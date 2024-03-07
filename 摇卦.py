import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


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
        ying = 'img/0.jpg'
        yang = 'img/1.jpg'
        self.images = [yang,ying,]
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSwitcher()
    window.show()
    sys.exit(app.exec_())

# self.layout.addWidget(result_label)
# self.labels.append(result_label)

# 查找要插入的位置索引
# index = min(self.count - 1, len(self.labels))

# 将新的标签插入到布局中的指定位置
# self.layout.insertWidget(index, result_label)
# self.labels.insert(index, result_label)
