import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread
from splash_window import Splash
from manager_window import Manager
from bottle import route, run
from components.popups import errorDialog,windowsToast
from components.tools import writeConfig,readConfig,initConfig

initConfig()

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

# Spotify WatchWitch on new thread (it's helloween)

@route('/watchwitch/spotify/startup')
def index():
    windowsToast("Spicetify Manager", "Spotify just started!")
    return 'ok'

class BottleThread(QThread):
    def run(self):
        print("Server started")
        run(host='localhost', port=1738)

if (readConfig('Manager','watchwitch') == "True"):
    watchwitch = BottleThread()
    watchwitch.start()
#start the app
if __name__ == "__main__":
    app = SpicetifyPatcher()
    app.run()