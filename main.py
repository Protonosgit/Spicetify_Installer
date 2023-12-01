import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal, QObject, QTimer
from splash_window import Splash
from manager_window import Manager
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from components.popups import errorDialog, windowsToast
from components.tools import writeConfig, readConfig, initConfig, spicetifyStatusCheck

# Initiate ini config file in spicetify folder
initConfig()


class SpicetifyPatcher:

    def __init__(self):
        # load windows (menu is also preloaded due to api requests)
        self.app = QApplication(sys.argv)
        self.splash_window = Splash()
        self.manager_window = Manager()

        # Check if application was launched by windows on boot (cmd argu)
        if not "--startup" in sys.argv:
            self.splash_window.show()

            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.show_menu)
            self.timer.start(5000)
        else:
            # Add task tray icon which makes menu window visible on click
            self.tray = QSystemTrayIcon()
            menu = QMenu()
            self.tray.setContextMenu(menu)
            self.tray.activated.connect(self.show_menu)
            self.tray.setIcon(QIcon(os.path.join(
                os.path.dirname(__file__), 'res', 'icon.png'
            )))
            self.tray.setVisible(True)

    # Check os and redirect to manager window if windows detected

    def show_menu(self):
        if sys.platform == 'win32':
            self.splash_window.hide()
            self.manager_window.show()
            pass
        else:
            self.splash_window.hide()
            errorDialog("This script is only compatible with Windows!")

    def run(self):
        sys.exit(self.app.exec())

#
# Spotify WatchWitch on new thread (it's helloween)
#

# Server request endpoint for watchwitch


@Request.application
def application(request):
    if request.path == '/watchwitch/spotify/startup':
        alertSpicetifyStatus()
        return Response('ok', content_type='text/plain')
    return Response('!! Spicetify Manager is using this port !!', status=500, content_type='text/plain')

# Server configuration


class WerkzeugThread(QThread):
    def run(self):
        print("Server started")
        run_simple('localhost', 1738, application)


# Runs the server if enabled
if readConfig('Manager', 'watchwitch') == "True":
    watchwitch = WerkzeugThread()
    watchwitch.start()

# Checks if spicetify is ok


def alertSpicetifyStatus():
    status = spicetifyStatusCheck()
    if status == 2:
        windowsToast("Spicetify Manager", "Update available!")
        # manager.show_manager_signal.emit()
    elif status == 1:
        windowsToast("Spicetify Manager", "Not applied!")


# start the app
if __name__ == "__main__":
    manager = SpicetifyPatcher()
    manager.run()
