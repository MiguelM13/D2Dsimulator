import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from Escenarios import escenario_1, escenario_2, escenario_3, escenario_4,escenario_5,escenario_6


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
        # self.selector5.toggled.connect(self.set_choice5)
        # self.selector6.toggled.connect(self.set_choice6)
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

    def set_choice5(self):
        if self.selector5.isChecked():
            self.choice = 5

    def set_choice6(self):
        if self.selector6.isChecked():
            self.choice = 6

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
        radioCar = factor*self.radioCar.value()
        clusters = self.clusters.isChecked()
        d2d = self.d2d.isChecked()

        if self.choice == 1:
            escenario_1(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)

        if self.choice == 2:
            escenario_2(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)

        if self.choice == 3:
            escenario_3(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)

        if self.choice == 4:
            escenario_4(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)

        if self.choice == 5:
            escenario_5(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)

        if self.choice == 6:
            escenario_6(Nusers=Nusers, NFC=NFC, radioFC=radioFC, radioCar=radioCar, playBtn=self.playBtn, d2d=d2d, clusters=clusters)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
