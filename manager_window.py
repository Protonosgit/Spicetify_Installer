
import os
import subprocess
from PyQt6.QtWidgets import  QMainWindow, QErrorMessage
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from components.shellbridge import InstallSpicetify, UpdateSpicetify, UninstallSpicetify, getLatestRelease,checkApplied

from components.afterinstall_popup import Popup
    


class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.installmode = True
        loadUi('./res/manager.ui', self)

        self.bt_install.clicked.connect(self.startInstaller)
        self.bt_update.clicked.connect(self.startUpdate)
        self.bt_uninstall.clicked.connect(self.startRemoval)
        self.bt0.clicked.connect(self.show_custom_dialog)

        self.checkSpicetify()

    def show_custom_dialog(self):
        pass

    def progressmaster(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("Installation has failed")
            error_dialog = QErrorMessage()
            error_dialog.setWindowTitle('Warning an error occured')
            error_dialog.showMessage('The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.')
            error_dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes! Please be patient while Spotify restarts(this can happen a fe times!)")

    def startInstaller(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.bt_install.setEnabled(False)
        self.bt_update.setEnabled(False)
        self.bt_uninstall.setEnabled(False)
        self.iprocess = InstallSpicetify()
        self.iprocess.finished_signal.connect(self.setup_finished)
        self.iprocess.progress_signal.connect(self.progressmaster)
        self.iprocess.start()
    def launchSpotify(self):
        os.startfile(os.path.join( os.path.expanduser('~'), 'AppData','Roaming/Spotify/Spotify.exe'))
    def activateSpicetify(self):
        subprocess.check_output('spicetify apply')
        self.checkSpicetify()
    def startRemoval(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.bt_uninstall.setEnabled(False)
        self.bt_update.setEnabled(False)
        self.bt_install.setEnabled(False)
        self.l_status.setStyleSheet("color: Orange")
        self.l_status.setText("Uninstalling Spicetify...")
        self.iprocess = UninstallSpicetify()
        self.iprocess.finished_signal.connect(self.uninstall_finished)
        self.iprocess.start()
    def startUpdate(self):
        try:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_update.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.bt_install.setEnabled(False)
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText("Checking for updates...")
            localversion = subprocess.check_output('spicetify --version',shell=True).decode("utf-8").strip()
            latestrelease = getLatestRelease().replace("v","").strip()
            if(latestrelease == localversion):
                self.l_status.setStyleSheet("color: Green")
                self.l_status.setText("You are up to date!")
                self.setCursor(Qt.CursorShape.ArrowCursor)
                self.bt_update.setEnabled(True)
                self.bt_uninstall.setEnabled(True)
            else:
                self.l_status.setStyleSheet("color: Orange")
                self.l_status.setText("Updating...")
                self.iprocess = UpdateSpicetify()
                self.iprocess.finished_signal.connect(self.update_finished)
                self.iprocess.start()
        except:
            print("E: Error while checking version during update!")

    def setup_finished(self):
        self.checkSpicetify()
        dialog = Popup(self)
        dialog.exec()
    def update_finished(self):
        self.checkSpicetify()
    def uninstall_finished(self):
        self.checkSpicetify()

    def checkSpicetify(self):
        try:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            folder_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify')
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                if not checkApplied():
                    self.l_status.setText("Spicetify is not activated yet")
                    self.l_status.setStyleSheet("color: orange")
                    self.l_versioninfo.setText('Please press activate to apply any modifications')
                    self.bt_uninstall.setEnabled(True)
                    self.bt_update.setEnabled(True)
                    self.bt_install.setEnabled(True)
                    if self.installmode:
                        self.installmode = False
                        self.bt_install.setText("Activate")
                        self.bt_install.clicked.disconnect(self.startInstaller)
                    else:
                        self.bt_install.clicked.disconnect(self.launchSpotify)
                    self.bt_install.clicked.connect(self.activateSpicetify)
                else:
                    self.l_status.setText("Spotify is spiced up!")
                    self.l_status.setStyleSheet("color: green")
                    versionoutput = subprocess.check_output('spicetify --version',shell=True)
                    self.l_versioninfo.setText('Version: '+versionoutput.decode("utf-8"))
                    self.bt_uninstall.setEnabled(True)
                    self.bt_update.setEnabled(True)
                    self.bt_install.setEnabled(True)
                    if self.installmode:
                        self.installmode = False
                        self.bt_install.setText("Launch Spotify")
                        self.bt_install.clicked.disconnect(self.startInstaller)
                        self.bt_install.clicked.connect(self.launchSpotify)
            else:
                self.l_status.setText("Spicetify is not installed")
                self.l_status.setStyleSheet("color: red")
                self.l_versioninfo.setText("")
                self.bt_uninstall.setEnabled(False)
                self.bt_update.setEnabled(False)
                self.bt_install.setEnabled(True)
                if not self.installmode:
                    self.installmode = True
                    self.bt_install.setText("Install")
                    self.bt_install.clicked.disconnect(self.launchSpotify)
                    self.bt_install.clicked.connect(self.startInstaller)
        except Exception as e:
            print("E: Error while checking Spicetify!")
            print(e)
            self.l_status.setText("Spicetify is not installed")
