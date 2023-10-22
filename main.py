import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from splash_window import Splash
from manager_window import Manager
from components.popups import errorDialog

class SpicetifyPatcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash_window = Splash()
        self.manager_window = Manager()

        self.splash_window.show()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_menu)
        self.timer.start(5000)

    # Check os and redirect to manager
    def show_menu(self):
        if sys.platform == 'win32':
            self.splash_window.hide()
            self.manager_window.show()
        else:
            self.splash_window.hide()
            errorDialog("This script is only compatible with Windows!")
            
    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = SpicetifyPatcher()
    app.run()
