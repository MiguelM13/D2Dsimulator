import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from Escenarios import escenario_1, escenario_2, escenario_3, escenario_4

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self)

        self.choice = 1
        # Events
        self.selector1.toggled.connect(self.set_choice1)
        self.selector2.toggled.connect(self.set_choice2)
        self.selector3.toggled.connect(self.set_choice3)
        self.selector4.toggled.connect(self.set_choice4)
        self.simulBtn.clicked.connect(self.simular)
        # self.setWindowFlags( QtCore.Qt.CustomizeWindowHint)

    def set_choice1(self):
        if self.selector1.isChecked():
            self.choice = 1

    def set_choice2(self):
        if self.selector2.isChecked():
            self.choice = 2

    def set_choice3(self):
        if self.selector3.isChecked():
            self.choice = 3

    def set_choice4(self):
        if self.selector4.isChecked():
            self.choice = 4

    def getScaleFactor(self):
        """
        1m -> 3px
        """
        return 1/3
    def simular(self):
        factor = self.getScaleFactor()
        Nusers = self.users.value()
        NFC = self.femtocells.value()
        radioFC = factor*self.radioFC.value()
        Nsub = self.subCarriers.value()
        radioCar = factor*self.radioCar.value()

        if self.choice == 1:
            escenario_1(Nusers, NFC, radioFC, Nsub, self.playBtn, radioCar)

        if self.choice == 2:
            escenario_2(Nusers, NFC, radioFC, Nsub, self.playBtn, radioCar)

        if self.choice == 3:
            escenario_3(Nusers, NFC, radioFC, Nsub, self.playBtn, radioCar)

        if self.choice == 4:
            escenario_4(Nusers, NFC, radioFC, Nsub, self.playBtn, radioCar)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
