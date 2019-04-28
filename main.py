import sys
from PyQt5 import QtWidgets, QtGui

import gui
from data import data


class Calculator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init()

    def init(self):

        self.vizitka_pushButton.clicked.connect(self.calc_vizitka_price)
        self.vizitka_col.setValidator(QtGui.QIntValidator())

    def calc_vizitka_price(self):
        col = int(self.vizitka_col.text() or '0')
        max_col = 50
        for i in [50, 100, 200, 300, 400, 500, 1000, 2000]:
            if col / i >= 1:
                max_col = i
        paper = self.vizitka_paper.currentText()
        colorful = self.vizitka_colorful.currentText()
        lam_b = 0
        if self.vizitka_lamination.isChecked():
            lam_b = 1
        round_b = 0
        if self.vizitka_rounding.isChecked():
            round_b = 1
        paper_price = data['paper'][paper]
        print_cost = data['print'][colorful]['100%']
        rent_coef = data['types']['vizitka'][colorful][max_col]
        laminate_cost = data['extra']['laminate'][max_col]
        round_cost = data['extra']['rounding'][max_col]
        dop = laminate_cost * lam_b + round_cost * round_b
        summ = ((paper_price + print_cost) / 24) * rent_coef
        price = str(int(col and (summ * col + dop) * 100) / 100)
        pricep1 = str(int((summ + dop / (col or 1)) * 100) / 100)
        self.vizitka_price.setText(price)
        self.vizitka_pricep1.setText(pricep1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
