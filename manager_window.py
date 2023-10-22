# Project spicy green => Spicetify patcher
# By Protonos ,

import os
import sys
import subprocess
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6.QtGui import QDesktopServices
from components.popups import errorDialog, infoDialog, windowsNotification
from components.shellbridge import InstallSpicetify, UpdateSpicetify, ApplySpicetify, UninstallSpicetify, CustomCommand, getLatestRelease,checkApplied,blockSpotifyUpdate

from components.afterinstall_popup import Popup
    

class Manager(QMainWindow):
    #Setup click listeners and load ui and do initial setup
    def __init__(self):
        super().__init__()

        self.isSpotifyInstalled = False
        self.isSpicetifyInstalled = False
        self.isApplied = False
        self.isBackedUp = False
        self.isActive = False
        self.managermode = 0

        self.LOCALSPOTIFYVER = ''
        self.LATESTSPOTIFYVER = ''
        self.LOCALSPICETIFYVER = ''
        self.LATESTSPICETIFYVER = ''

        #Switch when building
        loadUi("res/manager.ui", self)
        #loadUi(os.path.join(sys._MEIPASS, 'res', 'manager.ui'), self)

        self.InitWindow()

        self.bt_master.clicked.connect(self.masterButton)
        self.bt_update.clicked.connect(self.startUpdate)
        self.bt_uninstall.clicked.connect(self.startRemoval)
        self.bt_cmd.clicked.connect(self.Custom)
        self.check_noupdate.stateChanged.connect(self.DisableUpdate)


    # Execute once window is loaded before listeners are enabled
    def InitWindow(self):
        self.SystemSoftStatusCheck()

    #Update user about progress while installing spicetify
    def progressmaster(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("Installation has failed")
            errorDialog("The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")


    # Launch installer task !WIP
    def masterButton(self):
        if self.managermode == 0:
            os.startfile(os.path.join( os.path.expanduser('~'), 'AppData','Roaming/Spotify/Spotify.exe'))
            self.SystemSoftStatusCheck()
        if self.managermode == 1:
            QDesktopServices.openUrl('https://download.scdn.co/SpotifySetup.exe')
            self.SystemSoftStatusCheck()
        elif self.managermode == 2:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_update.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Installling Spicetify...")
            self.iprocess = InstallSpicetify()
            self.iprocess.finished_signal.connect(self.setup_finished)
            self.iprocess.progress_signal.connect(self.progressmaster)
            self.iprocess.start()
        elif self.managermode == 3:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_update.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Running apply")
            self.iprocess = ApplySpicetify()
            self.iprocess.finished_signal.connect(self.apply_finished)
            self.iprocess.start()
        elif self.managermode == 4:
            killpath1 = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'login.spa')
            killpath2 = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'xpui.spa')
            os.remove(killpath1)
            os.remove(killpath2)
            self.SystemSoftStatusCheck()
        else:
            print("Error selection overshoot!")
        

    # Launch uninstaller task
    def startRemoval(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        self.bt_uninstall.setEnabled(False)
        self.bt_update.setEnabled(False)
        self.bt_master.setEnabled(False)
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
            self.bt_master.setEnabled(False)
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
                self.bt_master.setEnabled(True)
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
            windowsNotification("Spicetify Manager", "Update supression failed!")
        else:
            windowsNotification("Spicetify Manager", "Update supression activated!")


    #Called when spicetify is installed or not?
    def setup_finished(self):
        self.SystemSoftStatusCheck()
        dialog = Popup(self)
        dialog.exec()
        windowsNotification("Spicetify Manager", "Spicetify has been installed!")
    #Called when spicetify is applied
    def apply_finished(self):
        self.SystemSoftStatusCheck()
        windowsNotification("Spicetify Manager", "Spicetify has been applied!")
    #Called when spicetify is updated
    def update_finished(self):
        self.SystemSoftStatusCheck()
        windowsNotification("Spicetify Manager", "Spicetify has been updated!")
    #Called when spicetify is uninstalled
    def uninstall_finished(self):
        self.SystemSoftStatusCheck()
        windowsNotification("Spicetify Manager", "Spicetify has been uninstalled!")

   # Spicetify status check V2
    def SystemSoftStatusCheck(self):
        spotipath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Spotify.exe')
        if os.path.exists(spotipath):
            self.isSpotifyInstalled = True
        else:
            self.isSpotifyInstalled = False

        # maybe (also) check executable in local appdata
        spicypath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'spicetify.exe')
        if os.path.exists(spicypath):
            self.isSpicetifyInstalled = True
            self.LOCALSPICETIFYVER = subprocess.check_output('spicetify --version',shell=True).decode("utf-8").strip()
        else:
            self.isSpicetifyInstalled = False
        
        self.LATESTSPICETIFYVER = getLatestRelease().replace("v","").strip()

        workpath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'xpui')
        if os.path.exists(workpath):
            self.isApplied = True
        else:
            self.isApplied = False

        linkpath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'login.spa')
        if os.path.exists(linkpath):
            self.isActive = False
        else:
            self.isActive = True
        
        self.installerUiUpdate()

    def installerUiUpdate(self):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.bt_update.setEnabled(True)
        self.bt_uninstall.setEnabled(True)
        self.bt_master.setEnabled(True)
        if(self.isSpotifyInstalled):
            if(self.isSpicetifyInstalled):
                if(self.isApplied):
                    if(self.isActive):
                        #Implement update checker here
                        self.l_status.setText("Spotify is spiced up!")
                        self.l_status.setStyleSheet("color: lime")
                        self.bt_master.setText("Launch Spotify")
                        self.l_versioninfo.setText('Version: '+self.LOCALSPICETIFYVER)
                        self.managermode = 0
                    else:
                        self.l_status.setText("Spicetify is inactive")
                        self.l_status.setStyleSheet("color: yellow")
                        self.l_versioninfo.setText('Press activate to activate Spicetify')
                        self.bt_master.setText("Activate")
                        self.managermode = 4
                else:
                    self.l_status.setText("Spicetify is not applied yet")
                    self.l_status.setStyleSheet("color: orange")
                    self.l_versioninfo.setText('Press apply to enable modifications')
                    self.bt_master.setText("Apply")
                    self.managermode = 3
            else:
                self.l_status.setText("Spicetify is not installed")
                self.l_status.setStyleSheet("color: White")
                self.l_versioninfo.setText('Press install to start the process')
                #self.l_versioninfo.setText('Latest version: '+self.LATESTSPICETIFYVER)
                self.bt_master.setText("Install")
                self.managermode = 2
        else:
            self.l_status.setText("Spotify is not installed")
            self.l_status.setStyleSheet("color: red")
            self.l_versioninfo.setText('Download Spotify from the official website')
            self.bt_master.setText("Download")
            self.managermode = 1
