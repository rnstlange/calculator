import sys
from PyQt5 import QtWidgets, QtGui

import gui
from data import data


class Widget:
    def __init__(self, window, name, colorful='', fill=''):
        self.window = window
        self.name = name
        self.colorful = colorful
        self.fill = fill

    def get_col(self):
        return int(getattr(self.window, self.name + '_col').text() or '0')

    def get_obj_max_col(self, obj, col):
        result = list(obj.keys())[0]
        for i in obj:
            if i <= col:
                result = i
        return result

    def get_obj_max(self, obj, col):
        return obj[self.get_obj_max_col(obj, col)]

    def get_paper(self):
        return getattr(self.window, self.name + '_paper').currentText()

    def get_paper_price(self):
        return data['paper'][self.get_paper()]

    def get_colorful(self):
        if not self.colorful:
            return getattr(self.window, self.name + '_colorful').currentText()
        else:
            return self.colorful

    def get_fill(self):
        if not self.fill:
            return getattr(self.window, self.name + '_fill').currentText()
        else:
            return self.fill

    def get_print_cost(self):
        return data['print'][self.get_colorful()][self.get_fill()]

    def get_lamination(self):
        lamination = 0
        if getattr(self.window, self.name + '_lamination').isChecked():
            lamination = 1
        return lamination

    def get_lamination_cost(self):
        max_col = self.get_obj_max_col(data['extra']['laminate'], self.get_col())
        return data['extra']['laminate'][max_col] * self.get_lamination()

    def get_rounding(self):
        rounding = 0
        if getattr(self.window, self.name + '_rounding').isChecked():
            rounding = 1
        return rounding

    def get_rounding_cost(self):
        max_col = self.get_obj_max_col(data['extra']['rounding'], self.get_col())
        return data['extra']['rounding'][max_col] * self.get_rounding()

    def get_format(self):
        return getattr(self.window, self.name + '_format').currentText()

    def get_big(self):
        return int(getattr(self.window, self.name + '_big').text() or '0')

    def get_big_cost(self):
        return self.get_obj_max(data['extra']['big'], self.get_big())

    def get_red_value(self):
        return data['types'][self.name][self.get_format()]['value']

    def set_price(self, price):
        getattr(self.window, self.name + '_price').setText(str(int(price * 100) / 100))

    def set_pricep1(self, price):
        getattr(self.window, self.name + '_pricep1').setText(str(int(price * 100) / 100))


class Calculator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init()

    def init(self):

        self.vizitka_pushButton.clicked.connect(self.calc_vizitka_price)
        self.vizitka_col.setValidator(QtGui.QIntValidator())

        self.listovka_pushButton.clicked.connect(self.calc_listovka_price)
        self.listovka_col.setValidator(QtGui.QIntValidator())
        self.listovka_big.setValidator(QtGui.QIntValidator())

    def calc_vizitka_price(self):
        widget = Widget(self, 'vizitka', fill='100%')

        paper_price = widget.get_paper_price()
        col = widget.get_col()
        colorful = widget.get_colorful()
        print_cost = widget.get_print_cost()
        rent_coef = widget.get_obj_max(data['types']['vizitka'][colorful], col)
        laminate_cost = widget.get_lamination_cost()
        round_cost = widget.get_rounding_cost()

        dop = laminate_cost + round_cost
        summ = ((paper_price + print_cost) / 24) * rent_coef
        price = col and (summ * col + dop)
        pricep1 = summ + dop / (col or 1)
        widget.set_price(price)
        widget.set_pricep1(pricep1)

    def calc_listovka_price(self):
        widget = Widget(self, 'listovka', fill='100%')

        paper_price = widget.get_paper_price()
        col = widget.get_col()
        print_cost = widget.get_print_cost()
        colorful = widget.get_colorful()
        lamination_cost = widget.get_lamination_cost()
        rounding_cost = widget.get_rounding_cost()
        big_cost = widget.get_big_cost()
        rent_coef = widget.get_obj_max(data['types']['listovka'][widget.get_format()][colorful], col)
        red_value = widget.get_red_value()

        summ = ((paper_price + print_cost) / red_value) * rent_coef
        dop = lamination_cost + rounding_cost + big_cost
        print(big_cost, dop)

        price = col and (summ * col + dop)
        pricep1 = summ + dop / (col or 1)

        widget.set_price(price)
        widget.set_pricep1(pricep1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
