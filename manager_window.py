# Project spicy green => Spicetify patcher
# By Protonos ,

import os
import sys
import subprocess
from PyQt6.QtWidgets import  QMainWindow, QErrorMessage, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from components.popups import errorDialog, infoDialog
from components.shellbridge import InstallSpicetify, UpdateSpicetify, UninstallSpicetify, CustomCommand, getLatestRelease,checkApplied,blockSpotifyUpdate

from components.afterinstall_popup import Popup
    

class Manager(QMainWindow):
    #Setup click listeners and load ui and do initial setup
    def __init__(self):
        super().__init__()
        self.installmode = True

        #Switch when building
        loadUi("res/manager.ui", self)
        #loadUi(os.path.join(sys._MEIPASS, 'res', 'manager.ui'), self)

        self.InitWindow()
        
        self.bt_install.clicked.connect(self.startInstaller)
        self.bt_update.clicked.connect(self.startUpdate)
        self.bt_uninstall.clicked.connect(self.startRemoval)
        self.bt_cmd.clicked.connect(self.Custom)
        self.check_noupdate.stateChanged.connect(self.DisableUpdate)


    # Execute once window is loaded before listeners are enabled
    def InitWindow(self):
        self.checkSpicetify()
    #Update user about progress while installing spicetify
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

    # Launch installer task
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
    # Applies spicetify
    def activateSpicetify(self):
        subprocess.check_output('spicetify apply')
        self.checkSpicetify()
    # Launch uninstaller task
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
    # Launch updater task
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
                self.bt_install.setEnabled(True)
            else:
                self.l_status.setStyleSheet("color: Orange")
                self.l_status.setText("Updating...")
                self.iprocess = UpdateSpicetify()
                self.iprocess.finished_signal.connect(self.update_finished)
                self.iprocess.start()
        except:
            print("E: Error while checking version during update!")

    # Run custom commands
    def Custom(self):
        self.iprocess = CustomCommand(self.combo_cmd.currentIndex())
        self.iprocess.finished_signal.connect(self.uninstall_finished)
        self.iprocess.start()
    # Disables Spotify self update function using permissions
    def DisableUpdate(self):
        if not (blockSpotifyUpdate(self.check_noupdate.isChecked())):
            infoDialog("Success", " The process has finished !")
        else:
            errorDialog("Error", "The process has failed ! You might need to remove the Update folder from Spotify manually.")


    #Called when spicetify is installed of case of failure?
    def setup_finished(self):
        self.checkSpicetify()
        dialog = Popup(self)
        dialog.exec()
    #Called when spicetify is updated
    def update_finished(self):
        self.checkSpicetify()
    #Called when spicetify is uninstalled
    def uninstall_finished(self):
        self.checkSpicetify()

    # Check if spicetify is installed and applied (mainly ui work)
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
