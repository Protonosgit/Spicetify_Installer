# Project spicy green => Spicetify patcher
# By Protonos ,

import os
import sys
import subprocess
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QUrl, QThread
from PyQt6.uic import loadUi
from PyQt6.QtGui import QDesktopServices, QMovie, QIcon
from components.popups import errorDialog, infoDialog, windowsToast, confirmationModal
from components.shellbridge import InstallSpicetify, UpdateSpicetify, ApplySpicetify, UninstallSpicetify, CustomCommand, blockSpotifyUpdate
from components.statusInfo import *
from components.tools import *
from components.dialog_windows import AfterInstall
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

initConfig()


class Manager(QMainWindow):
    # Setup click listeners and load ui and do initial setup
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        self.isSpotifyInstalled = False
        self.isSpicetifyInstalled = False
        self.isApplied = False
        self.isActive = False
        self.isMarketInstalled = False
        self.isWatchWitched = False
        self.isAutoClosing = False
        self.managermode = 0

        self.LOCALSPICETIFYVER = ''
        self.LATESTSPICETIFYVER = ''

        if getattr(sys, 'frozen', False):
            # Switch to using the frozen resources path
            loadUi(os.path.join(sys._MEIPASS, 'res', 'manager.ui'), self)
        else:
            # Use the regular resources path
            loadUi("res/manager.ui", self)
            print('Launching in debug mode...')

        if not "--startup" in sys.argv:
            # if "--startup" in sys.argv:
            self.InitWindow()
            self.show()
        else:
            # Add task tray icon which makes menu window visible on click
            self.tray = QSystemTrayIcon()
            menu = QMenu()
            self.tray.setContextMenu(menu)
            # self.tray.activated.connect()
            self.tray.setIcon(QIcon(os.path.join(
                os.path.dirname(__file__), 'res', 'icon.png'
            )))
            self.tray.setVisible(True)
            # Check if window is visible and toggle visibility

        self.bt_master.clicked.connect(self.masterButton)
        self.bt_uninstall.clicked.connect(self.startRemoval)
        self.bt_cmd.clicked.connect(self.Custom)
        self.check_noupdate.stateChanged.connect(self.DisableUpdate)
        self.check_watchwitch.stateChanged.connect(self.PatchWatchWitch)
        self.check_autoclose.stateChanged.connect(self.AutoClose)

    # Execute once window is loaded before listeners are enabled

    def InitWindow(self):
        self.SystemSoftStatusCheck()
        if (checkUpdateSupression()):
            self.check_noupdate.setChecked(True)
        else:
            self.check_noupdate.setChecked(False)

        movie = QMovie(os.path.join(
            os.path.dirname(__file__), "res", "retroflicker.gif"))

        self.background_graphics.setMovie(movie)
        self.background_graphics.show()
        movie.start()

    # Ask user to keep manager in background

    def closeEvent(self, event):
        if "--startup" in sys.argv:
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Move to background")
            message_box.setText(
                "Would you like to keep the Manager running in the background?")
            message_box.setIcon(QMessageBox.Icon.Question)
            message_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            response = message_box.exec()
            if response == QMessageBox.StandardButton.Yes:
                event.ignore()
                self.hide()
            else:
                event.accept()
        else:
            event.accept()

    # Master trigger for all actions related to spicetify

    def masterButton(self):
        # opne spotify
        if self.managermode == 0:
            os.startfile(os.path.join(os.path.expanduser('~'),
                         'AppData', 'Roaming/Spotify/Spotify.exe'))
            self.SystemSoftStatusCheck()
        elif self.managermode == 1:
            # Download spotify installer latest
            QDesktopServices.openUrl(
                QUrl('https://download.scdn.co/SpotifySetup.exe'))
            self.SystemSoftStatusCheck()
        elif self.managermode == 2:
            # Install spicetify
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Installling Spicetify...")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = InstallSpicetify()
            self.iprocess.finished_signal.connect(self.setup_finished)
            self.iprocess.progress_signal.connect(self.installProgress)
            self.iprocess.start()
        elif self.managermode == 3:
            # Apply spicetify
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Running apply")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = ApplySpicetify()
            self.iprocess.finished_signal.connect(self.apply_finished)
            self.iprocess.start()
        elif self.managermode == 4:
            # Re-apply after spotify update
            try:
                killpath1 = os.path.join(os.path.join(os.path.expanduser(
                    '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
                killpath2 = os.path.join(os.path.join(os.path.expanduser(
                    '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui.spa')
                os.remove(killpath1)
                os.remove(killpath2)
            except:
                print("Error while removing login.spa and xpui.spa")
            self.SystemSoftStatusCheck()
        elif self.managermode == 5:
            # update spicetify cli
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Updating patcher")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = UpdateSpicetify()
            self.iprocess.finished_signal.connect(self.update_finished)
            self.iprocess.progress_signal.connect(self.updateProgress)
            self.iprocess.start()
        elif self.managermode == 6:
            # install marketplace
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Installling Spicetify...")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = InstallSpicetify()
            self.iprocess.finished_signal.connect(self.setup_finished)
            self.iprocess.progress_signal.connect(self.installProgress)
            self.iprocess.start()

    # Update user about progress while installing spicetify
    def installProgress(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("⚠️ Installer has crashed ⚠️")
            errorDialog(
                "The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        elif (action == "done"):
            self.SystemSoftStatusCheck()
            dialog = AfterInstall(self)
            dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    # Update user about progress while updating spicetify
    def updateProgress(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("⚠️ Updater has crashed ⚠️")
            errorDialog(
                "The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        elif (action == "done"):
            self.SystemSoftStatusCheck()
            dialog = AfterInstall(self)
            dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    # Launch uninstaller task
    def startRemoval(self):
        reply = confirmationModal(
            'Uninstall', 'Are you sure you want to uninstall Spicetify and remove all installed mods/themes ?')
        if reply == QMessageBox.StandardButton.Yes:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_uninstall.setEnabled(False)
            self.bt_master.setEnabled(False)
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText("Uninstalling Spicetify...")
            self.iprocess = UninstallSpicetify()
            self.iprocess.finished_signal.connect(self.uninstall_finished)
            self.iprocess.start()
        else:
            return False

    # Run custom commands

    def Custom(self):
        self.iprocess = CustomCommand(self.combo_cmd.currentIndex())
        self.iprocess.finished_signal.connect(self.uninstall_finished)
        self.iprocess.start()

    # Disables Spotify self update function using permissions

    def DisableUpdate(self):
        writeConfig('Manager', 'NoUpdate', str(
            self.check_noupdate.isChecked()))
        if self.check_noupdate.isChecked():
            reply = confirmationModal(
                'Disable Updates', 'Are you sure you want to disable all automatic updates for Spotify?')
            if reply == QMessageBox.StandardButton.Yes:
                if (blockSpotifyUpdate(self.check_noupdate.isChecked())):
                    pass
                    windowsToast("Update supression change failed!", "")
                else:
                    pass
                    windowsToast("Update supression updated", "")
            else:
                self.check_noupdate.setChecked(
                    not self.check_noupdate.isChecked())
        else:
            if (blockSpotifyUpdate(self.check_noupdate.isChecked())):
                pass
                windowsToast("Update supression change failed", "")
            else:
                pass
                windowsToast("Update supression updated", "")

    # Apply Watchwitch server
    def PatchWatchWitch(self):
        folder_path = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'Manager.exe')
        if os.path.exists(folder_path):
            writeConfig('Manager', 'watchwitch', str(
                self.check_watchwitch.isChecked()))
            watchwitchInjector(self.check_watchwitch.isChecked())
            addToStartup(self.check_watchwitch.isChecked())
        else:
            self.check_watchwitch.setChecked(False)
            folder_path = os.path.join(os.path.join(
                os.path.expanduser('~'), 'AppData', 'Local'), 'spicetify')
            reply = confirmationModal(
                'Executeable not found', 'Please put the manager executeable in the "localappdata/spicetify/Manager.exe" folder! \n Do you want to open the folder?')
            if reply == QMessageBox.StandardButton.Yes:
                os.startfile(folder_path)
    # Auto close manager after completing actions (does not check for status!)

    def AutoClose(self):
        writeConfig('Manager', 'autoclose', str(
            self.check_autoclose.isChecked()))

    # Called when spicetify is installed or not

    def setup_finished(self):
        if self.isAutoClosing:
            self.close()

    # Called when spicetify is updated
    def update_finished(self):
        if self.isAutoClosing:
            self.close()

    # Called when spicetify is applied
    def apply_finished(self):
        self.SystemSoftStatusCheck()
        windowsToast("Spicetify has been applied!", "")
        if self.isAutoClosing:
            self.close()

    # Called when spicetify is uninstalled
    def uninstall_finished(self):
        self.SystemSoftStatusCheck()
        windowsToast("Spicetify has been uninstalled!", "")
        if self.isAutoClosing:
            self.close()

   # Spicetify status check (read var names for context)
    def SystemSoftStatusCheck(self):
        try:

            spotipath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Spotify.exe')
            if os.path.exists(spotipath):
                self.isSpotifyInstalled = True
            else:
                self.isSpotifyInstalled = False

            spicypath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Local'), 'spicetify', 'spicetify.exe')
            if os.path.exists(spicypath):
                self.isSpicetifyInstalled = True
                self.LOCALSPICETIFYVER = subprocess.check_output(
                    'spicetify --version', shell=True).decode("utf-8").strip()
            else:
                self.isSpicetifyInstalled = False

            self.LATESTSPICETIFYVER = getLatestSpicetifyRelease().replace("v", "").strip()

            workpath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui')
            if os.path.exists(workpath):
                self.isApplied = True
            else:
                self.isApplied = False

            linkpath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
            if os.path.exists(linkpath):
                self.isActive = False
            else:
                self.isActive = True

            marketpath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui', 'spicetify-routes-marketplace.js')
            if os.path.exists(marketpath):
                self.isMarketInstalled = True
            else:
                self.isMarketInstalled = False

            witchpath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui', 'index.html')
            patchstring = '''<script>fetch('http://localhost:1738/watchwitch/spotify/startup')</script>'''
            try:
                if (self.isApplied):
                    with open(witchpath, 'r+') as file:
                        content = file.read()
                        if patchstring not in content:
                            self.isWatchWitched = False
                        else:
                            self.isWatchWitched = True

            except:
                print("Error while reading watchwitch file")

            if (readConfig('Manager', 'autoclose') == 'True'):
                self.check_autoclose.setChecked(True)
                self.isAutoClosing = True
            else:
                self.check_autoclose.setChecked(False)
                self.isAutoClosing = False
        except Exception as e:
            print('Error while checking spicetify status')
            print(e)

        self.installerUiUpdate()

# Define the ui of the manager according to the status of spicetify/spotify
    def installerUiUpdate(self):
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.bt_uninstall.setEnabled(True)
        self.bt_master.setEnabled(True)

        if (self.isSpotifyInstalled):

            if (self.isSpicetifyInstalled):

                if (self.isApplied):

                    if (self.isActive):

                        if (self.LOCALSPICETIFYVER == self.LATESTSPICETIFYVER):

                            if (self.isMarketInstalled):
                                self.l_status.setText(
                                    "🔥 Spotify is spiced up 🔥")
                                self.l_status.setStyleSheet("color: lime")
                                self.bt_master.setText("Launch Spotify")
                                self.l_versioninfo.setText(
                                    'Version: '+self.LOCALSPICETIFYVER)
                                self.managermode = 0
                            else:
                                self.l_status.setText(
                                    "⚠️ Marketplace is not installed ⚠️")
                                self.l_status.setStyleSheet("color: yellow")
                                self.l_versioninfo.setText(
                                    'Install now to download mods/themes inside Spotify itself')
                                self.bt_master.setText("Install")
                                self.managermode = 6
                        else:
                            self.l_status.setText("♻️ Update available ♻️")
                            self.l_status.setStyleSheet("color: yellow")
                            self.l_versioninfo.setText(
                                'Update Spicetify to the latest version: '+self.LATESTSPICETIFYVER)
                            self.bt_master.setText("Update")
                            self.managermode = 5
                    else:
                        self.l_status.setText("⚠️ Spicetify is inactive ⚠️")
                        self.l_status.setStyleSheet("color: yellow")
                        self.l_versioninfo.setText(
                            'Press activate to activate Spicetify')
                        self.bt_master.setText("Activate")
                        self.managermode = 4
                else:
                    self.l_status.setText("🩹 Modifications not applied 🩹")
                    self.l_status.setStyleSheet("color: orange")
                    self.l_versioninfo.setText(
                        'Press apply to enable modifications')
                    self.bt_master.setText("Apply")
                    self.managermode = 3
            else:
                self.l_status.setText("Spicetify is not installed")
                self.l_status.setStyleSheet("color: White")
                self.l_versioninfo.setText(
                    'Press install to start the setup process')
                # self.l_versioninfo.setText('Latest version: '+self.LATESTSPICETIFYVER)
                self.bt_master.setText("Install")
                self.bt_uninstall.setEnabled(False)
                self.managermode = 2
        else:
            self.l_status.setText("Spotify is not installed")
            self.l_status.setStyleSheet("color: red")
            self.l_versioninfo.setText(
                'Download Spotify from the official website')
            self.bt_master.setText("Download")
            self.bt_uninstall.setEnabled(False)
            self.managermode = 1

        self.check_watchwitch.setChecked(self.isWatchWitched)

    def checkUpdateAvailable(self):
        if (managerUpdateCheck()):
            reply = confirmationModal(
                'Update', 'A new version of Spicetify Manager is available!\nWould you like to download it?')
            if reply == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(
                    QUrl('https://github.com/Protonosgit/Spicetify_Installer/releases'))

    def run(self):
        sys.exit(self.app.exec())


#
# Start Spotify WatchWitch on new thread (it's helloween)
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
if (isAddedToStartup()):
    watchwitch = WerkzeugThread()
    watchwitch.start()

# Checks if spicetify is ok


def alertSpicetifyStatus():
    status = spicetifyStatusCheck()
    if status == 2:
        windowsToast("Spicetify Manager", "Update available!")
    elif status == 1:
        windowsToast("Spicetify Manager", "Not applied!")


# start the app
if __name__ == "__main__":
    manager = Manager()
    manager.run()
