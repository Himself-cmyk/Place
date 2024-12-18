def main():
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget
    from GUI.table_form import ColorfulPlace
    from classes.place import LiuyaoPlace, GuideComponent
    # 假设 GuideComponent, LiuyaoPlace, 和 ColorfulPlace 已经正确定义并导入

    msg_dict = GuideComponent(input('title'), input('coinNum'), input('Time'))
    model = LiuyaoPlace(msg_dict)
    # model.place(output=True)
    # model.place_to_excel(output=True)

    '''彩色的排盘'''

    data, colors = model.place_to_excel(output=False)
    app = QApplication(sys.argv)
    colorful_place = ColorfulPlace(data=data, colors=colors)
    colorful_place.show()

    sys.exit(app.exec_())


def simple_place():
    from classes.place import LiuyaoPlace, GuideComponent

    msg_dict = GuideComponent(input('title'), input('coinNum'), input('Time'))
    model = LiuyaoPlace(msg_dict)
    model.place(output=True)
    # model.place_to_excel(output=True)

    print(''.join([str(i) for i in model.gua['coinNum']]))

    model.coinNum_change('reverse')
    model.coinNum_change('change')
    input('program finished')


if __name__ == '__main__':
    # main()
    simple_place()
