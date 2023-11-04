import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, QThread
from splash_window import Splash
from manager_window import Manager
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from components.popups import errorDialog, windowsToast
from components.tools import writeConfig, readConfig, initConfig

initConfig()


class SpicetifyPatcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.splash_window = Splash()
        self.manager_window = Manager()

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

    def closeEvent(self, event):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Exit Confirmation")
        message_box.setText("Are you sure you want to exit?")
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = message_box.exec()
        if response == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    # Check os and redirect to manager

    def show_menu(self):
        if sys.platform == 'win32':
            self.splash_window.hide()
            self.manager_window.show()
            pass
        else:
            self.splash_window.hide()
            errorDialog("This script is only compatible with Windows!")

    def run(self):
        app = QApplication(sys.argv)
        sys.exit(self.app.exec())

# Spotify WatchWitch on new thread (it's helloween)


@Request.application
def application(request):
    if request.path == '/watchwitch/spotify/startup':
        print("Spotify just started!")
        windowsToast("Spicetify Manager", "Spotify just started!")
        return Response('ok', content_type='text/plain')
    return Response('Spicetify Manager is holding this port!!', status=500, content_type='text/plain')


class WerkzeugThread(QThread):
    def run(self):
        print("Server started")
        run_simple('localhost', 1738, application)


if readConfig('Manager', 'watchwitch') == "True":
    watchwitch = WerkzeugThread()
    watchwitch.start()


# start the app
if __name__ == "__main__":
    app = SpicetifyPatcher()

    app.run()
