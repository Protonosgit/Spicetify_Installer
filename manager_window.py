# Project spicy green => Spicetify patcher
# By Protonos ,

import os
import sys
import subprocess
from PyQt6.QtWidgets import  QMainWindow,QMessageBox
from PyQt6.QtCore import Qt, QUrl
from PyQt6.uic import loadUi
from PyQt6.QtGui import QDesktopServices
from components.popups import errorDialog,windowsToast,interactableWindowsToast
from components.shellbridge import InstallSpicetify, watchwitchInjector, UpdateSpicetify, ApplySpicetify, UninstallSpicetify, CustomCommand,checkApplied,blockSpotifyUpdate,checkUpdateSupression
from components.tools import getLatestSpicetifyRelease,readConfig,writeConfig
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
        self.isMarketInstalled = False
        self.isWatchWitched = False
        self.managermode = 0

        self.LOCALSPOTIFYVER = ''
        self.LATESTSPOTIFYVER = ''
        self.LOCALSPICETIFYVER = ''
        self.LATESTSPICETIFYVER = ''

        if getattr(sys, 'frozen', False):
            # Switch to using the frozen resources path
            loadUi(os.path.join(sys._MEIPASS, 'res', 'manager.ui'), self)
        else:
            # Use the regular resources path
            loadUi("res/manager.ui", self)

        self.InitWindow()

        self.bt_master.clicked.connect(self.masterButton)
        self.bt_uninstall.clicked.connect(self.startRemoval)
        self.bt_refresh.clicked.connect(self.SystemSoftStatusCheck)
        self.bt_cmd.clicked.connect(self.Custom)
        self.check_noupdate.stateChanged.connect(self.DisableUpdate)
        self.check_watchwitch.stateChanged.connect(self.PatchWatchWitch)


    # Execute once window is loaded before listeners are enabled
    def InitWindow(self):
        self.SystemSoftStatusCheck()
        if(checkUpdateSupression()):
            self.check_noupdate.setChecked(True)
        else:
            self.check_noupdate.setChecked(False)

    # Master trigger for all requests
    def masterButton(self):
        if self.managermode == 0:
            os.startfile(os.path.join( os.path.expanduser('~'), 'AppData','Roaming/Spotify/Spotify.exe'))
            self.SystemSoftStatusCheck()
        if self.managermode == 1:
            QDesktopServices.openUrl(QUrl('https://download.scdn.co/SpotifySetup.exe'))
            self.SystemSoftStatusCheck()
        elif self.managermode == 2:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_refresh.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Installling Spicetify...")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = InstallSpicetify()
            self.iprocess.finished_signal.connect(self.setup_finished)
            self.iprocess.progress_signal.connect(self.installProgress)
            self.iprocess.start()
        elif self.managermode == 3:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_refresh.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Running apply")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = ApplySpicetify()
            self.iprocess.finished_signal.connect(self.apply_finished)
            self.iprocess.start()
        elif self.managermode == 4:
            killpath1 = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'login.spa')
            killpath2 = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'xpui.spa')
            os.remove(killpath1)
            os.remove(killpath2)
            self.SystemSoftStatusCheck()
        elif self.managermode == 5:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_refresh.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Updating patcher")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = UpdateSpicetify()
            self.iprocess.finished_signal.connect(self.update_finished)
            self.iprocess.progress_signal.connect(self.updateProgress)
            self.iprocess.start()
        elif self.managermode == 6:
            #install marketplace
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_master.setEnabled(False)
            self.bt_refresh.setEnabled(False)
            self.bt_uninstall.setEnabled(False)
            self.l_status.setText("Installling Spicetify...")
            self.l_versioninfo.setText('⏳Please wait⏳')
            self.iprocess = InstallSpicetify()
            self.iprocess.finished_signal.connect(self.setup_finished)
            self.iprocess.progress_signal.connect(self.installProgress)
            self.iprocess.start()

    #Update user about progress while installing spicetify
    def installProgress(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("⚠️ Installer has crashed ⚠️")
            errorDialog("The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        elif (action == "done"):
            self.SystemSoftStatusCheck()
            dialog = Popup(self)
            dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    def updateProgress(self, action):
        if (action == "fail"):
            self.l_status.setStyleSheet("color: red")
            self.l_status.setText("⚠️ Updater has crashed ⚠️")
            errorDialog("The installation of Spicetify has failed due to an unrecoverable error! Check logs or ask for help.")
        elif (action == "done"):
            self.SystemSoftStatusCheck()
            dialog = Popup(self)
            dialog.exec()
        else:
            self.l_status.setStyleSheet("color: Orange")
            self.l_status.setText(action)
            self.l_versioninfo.setText("This process may take a few minutes!")

    # Launch uninstaller task
    def startRemoval(self):
        reply = QMessageBox.question(None, 'Uninstall', 'Are you sure you want to uninstall Spicetify and remove all installed mods/themes ?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.bt_uninstall.setEnabled(False)
            self.bt_refresh.setEnabled(False)
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
        writeConfig('Manager','NoUpdate',str(self.check_noupdate.isChecked()))
        if self.check_noupdate.isChecked():
            reply = QMessageBox.question(None, 'Deactivate Updates', 'This function will try to disable all automatic updates for Spotify! Are you sure you want to do this?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if (blockSpotifyUpdate(self.check_noupdate.isChecked())):
                    pass
                    windowsToast("Update supression change failed!", "")
                else:
                    pass
                    windowsToast("Update supression updated", "")
            else:
                self.check_noupdate.setChecked(not self.check_noupdate.isChecked())
        else:
            if (blockSpotifyUpdate(self.check_noupdate.isChecked())):
                pass
                windowsToast("Update supression change failed", "")
            else:
                pass
                windowsToast("Update supression updated", "")

    def PatchWatchWitch(self):
        writeConfig('Manager','watchwitch',str(self.check_watchwitch.isChecked()))
        watchwitchInjector(self.check_watchwitch.isChecked())


    #Called when spicetify is installed or not?
    def setup_finished(self):
        pass

    #Called when spicetify is updated
    def update_finished(self):
        pass
        
    #Called when spicetify is applied
    def apply_finished(self):
        self.SystemSoftStatusCheck()
        windowsToast("Spicetify has been applied!", "")

    #Called when spicetify is uninstalled
    def uninstall_finished(self):
        self.SystemSoftStatusCheck()
        windowsToast("Spicetify has been uninstalled!", "")

   # Spicetify status check
    def SystemSoftStatusCheck(self):
        self.bt_refresh.setEnabled(False)

        spotipath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Spotify.exe')
        if os.path.exists(spotipath):
            self.isSpotifyInstalled = True
        else:
            self.isSpotifyInstalled = False

        spicypath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'spicetify.exe')
        if os.path.exists(spicypath):
            self.isSpicetifyInstalled = True
            self.LOCALSPICETIFYVER = subprocess.check_output('spicetify --version',shell=True).decode("utf-8").strip()
        else:
            self.isSpicetifyInstalled = False
        
        self.LATESTSPICETIFYVER = getLatestSpicetifyRelease().replace("v","").strip()

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

        marketpath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'xpui', 'spicetify-routes-marketplace.js')
        if os.path.exists(marketpath):
            self.isMarketInstalled = True
        else:
            self.isMarketInstalled = False

        witchpath = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'Spotify', 'Apps', 'xpui', 'index.html')
        patchstring = '''<script>fetch('http://localhost:1738/watchwitch/spotify/startup')</script>'''
        with open(witchpath, 'r+') as file:
            content = file.read()
            if patchstring not in content:
                self.isWatchWitched = False
            else:
                self.isWatchWitched = True
        
        self.installerUiUpdate()

    def installerUiUpdate(self):
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.bt_refresh.setEnabled(True)
        self.bt_uninstall.setEnabled(True)
        self.bt_master.setEnabled(True)

        if (self.isSpotifyInstalled):

            if(self.isSpicetifyInstalled):

                if(self.isApplied):

                    if(self.isActive):

                        if(self.LOCALSPICETIFYVER == self.LATESTSPICETIFYVER):

                            if (self.isMarketInstalled):
                                self.l_status.setText("🔥 Spotify is spiced up 🔥")
                                self.l_status.setStyleSheet("color: lime")
                                self.bt_master.setText("Launch Spotify")
                                self.l_versioninfo.setText('Version: '+self.LOCALSPICETIFYVER)
                                self.managermode = 0
                            else:
                                self.l_status.setText("⚠️ Marketplace is not installed ⚠️")
                                self.l_status.setStyleSheet("color: yellow")
                                self.l_versioninfo.setText('Install now to download mods/themes inside Spotify itself')
                                self.bt_master.setText("Install")
                                self.managermode = 6
                        else:
                            self.l_status.setText("♻️ Update available ♻️")
                            self.l_status.setStyleSheet("color: yellow")
                            self.l_versioninfo.setText('Update now to the latest version: '+self.LATESTSPICETIFYVER)
                            self.bt_master.setText("Update")
                            self.managermode = 5
                    else:
                        self.l_status.setText("⚠️ Spicetify is inactive ⚠️")
                        self.l_status.setStyleSheet("color: yellow")
                        self.l_versioninfo.setText('Press activate to activate Spicetify')
                        self.bt_master.setText("Activate")
                        self.managermode = 4
                else:
                    self.l_status.setText("🩹 Modifications not applied 🩹")
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
                self.bt_uninstall.setEnabled(False)
                self.managermode = 2
        else:
            self.l_status.setText("Spotify is not installed")
            self.l_status.setStyleSheet("color: red")
            self.l_versioninfo.setText('Download Spotify from the official website')
            self.bt_master.setText("Download")
            self.bt_uninstall.setEnabled(False)
            self.managermode = 1
        
        self.check_watchwitch.setChecked(self.isWatchWitched)
