# Project spicy green => Spicetify patcher
# By Protonos ,

import os
import sys
import subprocess
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import Qt, QUrl, QThread, QTimer
from PyQt6.uic import loadUi
from PyQt6.QtGui import QDesktopServices, QMovie, QIcon
from components.popups import errorDialog, warnDialog, windowsToast, confirmationModal, spicetifyStatusToast
from components.shellbridge import *
from components.statusInfo import *
from components.tools import *
from components.dialog_windows import AfterInstall, UninstallWindow
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from windows_toasts import ToastActivatedEventArgs, Toast, ToastButton, InteractableWindowsToaster

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
        self.isWatchWitchPatched = False
        self.isRunningOnBoot = False
        self.isAutoClosing = False
        self.isNeverRestarting = False
        self.isAutoPatching = False
        self.isInFaultMode = False
        self.isConnectedToInternet = False
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

        # Add task tray icon which makes menu window visible on click
        if (readConfig('Manager', 'watchwitch') == 'True'):
            self.tray = QSystemTrayIcon()
            menu = QMenu()
            self.tray.setContextMenu(menu)
            self.tray.activated.connect(self.showManagerWindow)
            self.tray.setIcon(QIcon(os.path.join(
                os.path.dirname(__file__), 'res', 'icon.png'
            )))
            self.tray.setVisible(True)

        # Checks if file is run on startup
        if not "--startup" in sys.argv:
            self.InitWindow()
            self.show()

        else:
            # Peek and run
            self.InitWindow()
            self.show()
            self.hide()
            # Status check interval
            self.timer = QTimer(self)
            self.timer.setInterval(120000)
            self.timer.timeout.connect(self.statusUpdate)
            self.timer.start()

        self.bt_master.clicked.connect(self.masterButton)
        self.bt_uninstall.clicked.connect(self.UninstallModal)
        self.bt_cmd.clicked.connect(self.Custom)
        self.check_noupdate.stateChanged.connect(self.DisableUpdate)
        self.check_watchwitch.stateChanged.connect(self.PatchWatchWitch)
        self.check_autoclose.stateChanged.connect(self.AutoClose)
        self.check_autopatch.stateChanged.connect(self.AutoPatchInBackground)
        self.check_startonboot.stateChanged.connect(self.startOnBoot)
        self.check_neverrestart.stateChanged.connect(self.NeverRestart)
        self.check_denymanagerupdate.stateChanged.connect(
            self.denyManagerUpdate)

        # Perform status update after window visible
        self.showEvent = self.statusUpdate()

    # Execute once window is loaded before listeners are enabled

    def InitWindow(self):
        if checkAdminPrivileges():
            #close app with error mesage
            errorDialog("NEVER run sussy programms like this with admin privileges !!")
            sys.exit(0)
        movie = QMovie(os.path.join(
            os.path.dirname(__file__), "res", "retroflicker.gif"))
        self.background_graphics.setMovie(movie)
        self.background_graphics.show()
        movie.start()
        if not readConfig('Manager', 'donotcheckupdate') == 'True':
            self.checkUpdateAvailable()
        # self.statusUpdate()

    # Display manager window

    def showManagerWindow(self):
        self.InitWindow()
        self.show()

    # Ask user to keep manager in background

    def closeEvent(self, event):
        if self.isWatchWitchPatched:
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

    #
    # Master trigger for all actions related to spicetify
    #
    def masterButton(self):
        self.isInFaultMode = False
        # opne spotify
        if self.managermode == 0:
            os.startfile(os.path.join(os.path.expanduser('~'),
                         'AppData', 'Roaming/Spotify/Spotify.exe'))
            self.statusUpdate()
        elif self.managermode == 1:
            # Download spotify installer latest
            QDesktopServices.openUrl(
                QUrl('https://download.scdn.co/SpotifySetup.exe'))
            self.statusUpdate()
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
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Fixing Spotify...")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = ActivateSpicetify()
            self.iprocess.finished_signal.connect(self.activate_finished)
            self.iprocess.start()
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

    #
    # Uninstall Button listener
    #
    def startRemoval(self):
        self.isInFaultMode = False
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
            self.iprocess.progress_signal.connect(self.uninstallProgress)
            self.iprocess.start()
        else:
            return False

    def UninstallModal(self):
        # Show uninstall.ui window
        dialog = UninstallWindow(self)
        dialog.exec()

    #
    # Background worker progress update listener
    #

    # Update user about progress while installing spicetify
    def installProgress(self, action):
        if (action == "fail"):
            self.enterFaultMode(
                "The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        elif (action == "done"):
            self.statusUpdate()
            dialog = AfterInstall(self)
            dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    # Update user about progress while updating spicetify
    def updateProgress(self, action):
        if (action == "fail"):
            self.enterFaultMode(
                "An error occured while updating spicetify! Check logs or ask for help.")
        elif (action == "done"):
            self.statusUpdate()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")
    # Update user about progress while uninstalling spicetify

    def uninstallProgress(self, action):
        if (action == "fail"):
            self.enterFaultMode(
                'The uninstallation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.')
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    # Informs user about patch or other failure
    def enterFaultMode(self, context):
        self.isInFaultMode = True
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.bt_uninstall.setEnabled(True)
        self.bt_master.setEnabled(True)
        self.l_status.setStyleSheet("color: red")
        self.l_status.setText("⚠️ An error occured ⚠️")
        self.l_versioninfo.setText('Task not completed due to crash')
        errorDialog(context)

    #
    # Advanced checkbox changed event receivers
    #

    # Disables Spotify self update function using permissions

    def DisableUpdate(self):
        writeConfig('Manager', 'NoUpdate', str(
            self.check_noupdate.isChecked()))
        if (blockSpotifyUpdate(self.check_noupdate.isChecked())):
            windowsToast("Update supression change failed", "")
        else:
            if self.check_noupdate.isChecked():
                windowsToast("All automatic updates disabled",
                             "No updates will be performed automatically by Spotify")
            else:
                windowsToast("Automatic updates enabled",
                             "Spotify will autoupdate now")

    # Enable Watchwitch server
    def PatchWatchWitch(self):
        writeConfig('Manager', 'watchwitch', str(
            self.check_watchwitch.isChecked()))
        watchwitchInjector(self.check_watchwitch.isChecked())
        if not self.check_startonboot.isChecked() and self.check_watchwitch.isChecked():
            warnDialog(
                "Start on boot is not enabled! \n This will only take effect when the the manager is running (or restart if you prefer this)")

    # Auto close manager after completing actions (does not check for status!)
    def AutoClose(self):
        writeConfig('Manager', 'autoclose', str(
            self.check_autoclose.isChecked()))

    # Never restart Spotify after modifying app
    def NeverRestart(self):
        writeConfig('Manager', 'never_restart', str(
            self.check_neverrestart.isChecked()))

    # Auto patch in background
    def AutoPatchInBackground(self):
        if self.check_autopatch.isChecked() and not self.check_watchwitch.isChecked():
            warnDialog(
                "Start on boot and/or startup listener is not enabled! \n Detection will only work WITH the server!")
        writeConfig('Manager', 'autopatch', str(
            self.check_autopatch.isChecked()))

    # Start on boot
    def startOnBoot(self):
        managerpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'Manager.exe')
        addToStartup(self.check_startonboot.isChecked())
        if not os.path.exists(managerpath) and self.check_startonboot.isChecked():
            folder_path = os.path.join(os.path.join(
                os.path.expanduser('~'), 'AppData', 'Local'), 'spicetify')
            reply = confirmationModal(
                'Executeable not found', 'Please put the manager executeable in the "localappdata/spicetify/Manager.exe" folder or else the manager will not start! \n Do you want to open the folder?')
            if reply == QMessageBox.StandardButton.Yes:
                os.startfile(folder_path)

    # Do not check for manager updates
    def denyManagerUpdate(self):
        writeConfig('Manager', 'donotcheckupdate', str(
            self.check_denymanagerupdate.isChecked()))

    # Run custom command button listener
    def Custom(self):
        self.iprocess = CustomCommand(self.combo_cmd.currentIndex())
        self.iprocess.finished_signal.connect(self.uninstall_finished)
        self.iprocess.start()

    #
    # Background Worker finished signal receivers (checks id successful)
    #

    # Called when spicetify is installed or not
    def setup_finished(self):
        if not self.isInFaultMode:
            if not self.isNeverRestarting:
                self.iprocess = RestartSpotify()
                self.iprocess.start()
            if self.isAutoClosing:
                self.close()

    # Called when spicetify is updated
    def update_finished(self):
        windowsToast("Spicetify update process completed!", "")
        if not self.isNeverRestarting:
            self.iprocess = RestartSpotify()
            self.iprocess.start()
        if self.isAutoClosing:
            self.close()

    # Called when spicetify is applied
    def apply_finished(self):
        if not self.isInFaultMode:
            self.statusUpdate()
            windowsToast("Spicetify has been applied!", "")
            if not self.isNeverRestarting:
                self.iprocess = RestartSpotify()
                self.iprocess.start()
            if self.isAutoClosing:
                self.close()

    # Called when spicetify is uninstalled
    def uninstall_finished(self):
        if not self.isInFaultMode:
            self.statusUpdate()
            windowsToast("Spicetify has been uninstalled!", "")
            if not self.isNeverRestarting:
                self.iprocess = RestartSpotify()
                self.iprocess.start()
            if self.isAutoClosing:
                self.close()

    # Called when spicetify was activated
    def activate_finished(self):
        if not self.isInFaultMode:
            self.statusUpdate()
            windowsToast("Spicetify is now active again!", "")
            if not self.isNeverRestarting:
                self.iprocess = RestartSpotify()
                self.iprocess.start()
            if self.isAutoClosing:
                self.close()

    #
    # Spicetify status check and variables init
    #
    def statusUpdate(self):
        try:
            self.isSpotifyInstalled = checkSpotifyInstalled()
            if self.isSpotifyInstalled:

                self.isSpicetifyInstalled = checkSpicetifyInstalled()
                if self.isSpicetifyInstalled:

                    self.isApplied = checkSpicetifyApplied()
                    self.isActive = checkSpicetifyActive()

                    self.isMarketInstalled = checkMarketplaceInstalled()

                    self.LATESTSPICETIFYVER = getLatestSpicetifyRelease().replace("v", "").strip()

            if self.isSpicetifyInstalled:
                self.LOCALSPICETIFYVER = subprocess.check_output(
                    'spicetify --version', shell=True).decode("utf-8").strip()

            if self.isApplied:
                self.isWatchWitchPatched = checkWatchWitchPatched()

            if (readConfig('Manager', 'autoclose') == 'True'):
                self.isAutoClosing = True
            else:
                self.isAutoClosing = False

            if (readConfig('Manager', 'never_restart') == 'True'):
                self.isNeverRestarting = True
            else:
                self.isNeverRestarting = False

            if (readConfig('Manager', 'autopatch') == 'True'):
                self.isAutoPatching = True
            else:
                self.isAutoPatching = False

            self.isRunningOnBoot = isAddedToStartup()

            self.isConnectedToInternet = checkInternetConnection()

        except Exception as e:
            print('Error while checking spicetify status')
            print(e)

        self.uiUpdate()
    #
    # Define the ui of the manager according to the status of spicetify/spotify
    #

    def uiUpdate(self):
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.bt_uninstall.setEnabled(True)
        self.bt_master.setEnabled(True)

        if (self.isSpotifyInstalled):

            if (self.isSpicetifyInstalled):

                if (self.isApplied):

                    if (self.isActive):

                        if (self.LOCALSPICETIFYVER == self.LATESTSPICETIFYVER) or self.LATESTSPICETIFYVER == 'err':

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

        self.check_noupdate.setChecked(checkUpdateSupression())
        self.check_watchwitch.setChecked(self.isWatchWitchPatched)
        self.check_autoclose.setChecked(self.isAutoClosing)
        self.check_startonboot.setChecked(self.isRunningOnBoot)
        self.check_neverrestart.setChecked(self.isNeverRestarting)
        self.check_autopatch.setChecked(self.isAutoPatching)

        if self.isConnectedToInternet:
            self.network_error_icon.setVisible(False)
        else:
            self.network_error_icon.setVisible(True)

        if (readConfig('Manager', 'donotcheckupdate') == 'True'):
            self.check_denymanagerupdate.setChecked(True)

    # Check if manager has update available
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
if (readConfig('Manager', 'watchwitch') == 'True'):
    watchwitch = WerkzeugThread()
    watchwitch.start()

# Checks if spicetify is ok


newToast = Toast(['Spicetify Manager'])
newToast.AddAction(ToastButton('Open Manager', 'response=manager'))

# Listener for startup of spotify with notifications/autopatcher


def alertSpicetifyStatus():
    status = spicetifyStatusCheck()
    if readConfig('Manager', 'autopatch') == 'True':
        if status == 0:
            windowsToast("Spicetify is updating", "Prepare for restart!")
            subprocess.run('spicetify upgrade -q', shell=True)
        elif status == 1:
            windowsToast("Background Patcher", "Spicetify has been activated!")
    else:
        if status == 0:
            interactableToaster = InteractableWindowsToaster(
                'An update for spicetify is available')
            interactableToaster.show_toast(newToast)
        elif status == 1:
            interactableToaster = InteractableWindowsToaster(
                'Spicetify is not working correctly')
            interactableToaster.show_toast(newToast)


def activated_callback(activatedEventArgs: ToastActivatedEventArgs):
    manager.show()


newToast.on_activated = activated_callback

# start the app
manager = None
if __name__ == "__main__":
    manager = Manager()
    manager.run()
