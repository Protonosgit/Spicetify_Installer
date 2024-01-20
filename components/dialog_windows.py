import os
from PyQt6.QtWidgets import QDialog
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

        self.accepted.connect(self.onAccept)

    @pyqtSlot()
    def onAccept(self):
        print("Accept button clicked!")
