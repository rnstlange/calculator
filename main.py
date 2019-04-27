import sys
from PyQt5 import QtWidgets, QtGui, uic
import yaml

import gui

with open("./data.yaml", "r", encoding="utf-8") as stream:
    data = yaml.safe_load(stream)

# print(data['paper']['Офсетная 80 гр.'])


# menu = {
#    '': 0,
#    'Визитки': 1
# }


class Calculator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_vizitka()

    def init_vizitka(self):
        self.vizitka_pushButton.clicked.connect(self.calc_vizitka_price)

        self.vizitka_col.setValidator(QtGui.QIntValidator())

    def calc_vizitka_price(self):
        col = int(self.vizitka_col.text())
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

        price = ((paper_price + print_cost) / 24) * col * rent_coef + laminate_cost * lam_b + round_cost * round_b

        self.vizitka_price.setText(str(int(price * 100) / 100))
        self.vizitka_pricep1.setText(str(int(price * 100 / col) / 100))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
