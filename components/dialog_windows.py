import os
from PyQt6.QtWidgets import QDialog, QDialogButtonBox
from PyQt6.QtCore import pyqtSlot
from PyQt6.uic import loadUi


class AfterInstall(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        parent_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".."))
        pathmaster = os.path.join(
            parent_directory, "res", "afterinstalltip.ui")
        loadUi(pathmaster, self)


class ActionSpicetify(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        parent_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".."))
        pathmaster = os.path.join(
            parent_directory, "res", "afterinstalltip.ui")
        loadUi(pathmaster, self)


class UninstallWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        parent_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".."))
        pathmaster = os.path.join(
            parent_directory, "res", "uninstall.ui")
        loadUi(pathmaster, self)

        self.deacmods = False
        self.remmods = False
        self.unispicetify = False
        self.meisterpropper = False

        self.bt_cancel.clicked.connect(self.close)
        self.bt_apply.clicked.connect(self.ApplyChanges)

        self.check1.stateChanged.connect(self.option1)
        self.check2.stateChanged.connect(self.option2)
        self.check3.stateChanged.connect(self.option3)
        self.check4.stateChanged.connect(self.option4)

    def option1(self):

        self.warning.setStyleSheet("color: rgba(0, 0, 0, 0);")
        self.bt_apply.setEnabled(True)
        self.deacmods = self.check1.isChecked()

    def option2(self):
        self.warning.setStyleSheet("color: red")
        self.bt_apply.setEnabled(True)
        self.check1.setChecked(False)
        self.check1.setEnabled(not self.check2.isChecked())
        self.remmods = self.check2.isChecked()

    def option3(self):
        self.warning.setStyleSheet("color: red")
        self.bt_apply.setEnabled(True)
        self.unispicetify = self.check3.isChecked()

    def option4(self):
        self.warning.setStyleSheet("color: red")
        self.bt_apply.setEnabled(True)
        self.check1.setChecked(False)
        self.check2.setChecked(False)
        self.check3.setChecked(False)
        self.check1.setEnabled(not self.check4.isChecked())
        self.check2.setEnabled(not self.check4.isChecked())
        self.check3.setEnabled(not self.check4.isChecked())
        self.meisterpropper = self.check4.isChecked()

    def ApplyChanges(self):

        print(self.deacmods, self.remmods,
              self.unispicetify, self.meisterpropper)
        self.close()
