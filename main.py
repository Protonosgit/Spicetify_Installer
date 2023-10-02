import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from splash_window import Splash
from menu_window import Menu
from manager_window import Manager

class SpicetifyPatcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash_window = Splash()
        self.menu_window = Menu()
        self.manager_window = Manager()

        self.splash_window.show()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_menu)
        self.timer.start(5000)

    def show_menu(self):
        self.splash_window.hide()
        self.manager_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = SpicetifyPatcher()
    app.run()







