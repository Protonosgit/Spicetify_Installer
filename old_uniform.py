import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.uic import loadUi

# Add check=true to subprocess to throw exeptions on failure :) shell is not neccesary

class SetupSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Setup started")
        subprocess.run('powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"')
        self.finished_signal.emit()
class ApplySpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Apply started")
        subprocess.run('powershell.exe -Command "spicetify apply"')
        self.finished_signal.emit()
class BackupSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Backup started")
        subprocess.run('powershell.exe -Command "spicetify clear"')
        subprocess.run('powershell.exe -Command "spicetify backup"')
        self.finished_signal.emit()
class UpdateSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Update started")
        subprocess.run('powershell.exe -Command "spicetify upgrade"')
        subprocess.run('powershell.exe -Command "spicetify update"')
        self.finished_signal.emit()
class DevtoolsSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Devtools started")
        subprocess.run('powershell.exe -Command "spicetify enable-devtools"')
class MarketplaceSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Marketplace started")
        subprocess.run('powershell.exe -Command "Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1" | Invoke-Expression"')
class RestoreSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Restoration started")
        subprocess.run('powershell.exe -Command "spicetify restore"')
        self.finished_signal.emit()
class UninstallSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        subprocess.run('powershell.exe -Command "spicetify restore"')
        subprocess.run('powershell.exe -Command "rmdir -r -fo $env:APPDATA\spicetify"',shell=True)
        subprocess.run('powershell.exe -Command "rmdir -r -fo $env:LOCALAPPDATA\spicetify"',shell=True)
        subprocess.run('powershell.exe -Command "Msg Spicetify Extension Removed"')
        print("Removal started")
        self.finished_signal.emit()


class SpicyGreen(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('untitled.ui', self)

        self.bt_install.clicked.connect(self.InstallSpices)
        self.bt_backup.clicked.connect(self.BackupSpices)
        self.bt_apply.clicked.connect(self.ApplySpices)
        self.bt_update.clicked.connect(self.UpdateSpices)
        self.bt_dev.clicked.connect(self.DevtoolsSpices)
        self.bt_restore.clicked.connect(self.RestoreSpices)
        self.bt_uninstall.clicked.connect(self.RemoveSpices)
        self.bt_marketplace.clicked.connect(self.MarketplaceSpices)
        self.checkSpicetify()

        self.show()

    def InstallSpices(self):
        self.iprocess = SetupSpicetify()
        self.iprocess.finished_signal.connect(self.setup_finished)
        self.iprocess.start()
        self.loading(False)
    def ApplySpices(self):
        self.iprocess = ApplySpicetify()
        self.iprocess.finished_signal.connect(self.apply_finished)
        self.iprocess.start()
        self.loading(False)
    def BackupSpices(self):
        self.iprocess = BackupSpicetify()
        self.iprocess.finished_signal.connect(self.backup_finished)
        self.iprocess.start()
        self.loading(False)
    def UpdateSpices(self):
        self.iprocess = UpdateSpicetify()
        self.iprocess.finished_signal.connect(self.update_finished)
        self.iprocess.start()
        self.loading(False)
    def DevtoolsSpices(self):
        self.iprocess = DevtoolsSpicetify()
        self.iprocess.finished_signal.connect(self.devtools_finished)
        self.iprocess.start()
        self.loading(False)
    def MarketplaceSpices(self):
        self.iprocess = MarketplaceSpicetify()
        self.iprocess.finished_signal.connect(self.marketplace_finished)
        self.iprocess.start()
        self.loading(False)
    def RestoreSpices(self):
        self.iprocess = RestoreSpicetify()
        self.iprocess.finished_signal.connect(self.restore_finished)
        self.iprocess.start()
        self.loading(False)
    def RemoveSpices(self):
        def handle_alert_button_click(button):
            # This slot will be called when a button in the alert is clicked
            if button.text() == 'OK':
                self.iprocess = UninstallSpicetify()
                self.iprocess.finished_signal.connect(self.remove_finished)
                self.iprocess.start()
                self.bt_uninstall.setEnabled(False)
        alert = QMessageBox()
        alert.setWindowTitle('Alert')
        alert.setText('Your Spicetify patch including all themes/plugins will be removed !')
        alert.buttonClicked.connect(handle_alert_button_click)
        alert.exec()

    def setup_finished(self):
        self.loading(True)
    def apply_finished(self):
        self.loading(True)
    def update_finished(self):
        self.loading(True)
    def backup_finished(self):
        self.loading(True)
    def devtools_finished(self):
        self.loading(True)
    def marketplace_finished(self):
        self.loading(True)
    def restore_finished(self):
        self.loading(True)
    def remove_finished(self):
        self.loading(True)

    def checkSpicetify(self):
        #check resources folder
        folder_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Roaming'), 'spicetify')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            self.data_label.setText("Data OK")
            self.data_label.setStyleSheet("color: green")
        else:
            self.data_label.setText("Data missing")
            self.data_label.setStyleSheet("color: red")
        #check data folder
        folder_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify')
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            self.installed_label.setText("Spicetify installed")
            self.installed_label.setStyleSheet("color: green")
        else:
            self.installed_label.setText("Not installed")
            self.installed_label.setStyleSheet("color: red")
    
    def loading(self,status):
        if (status==False):
            self.setCursor(Qt.CursorShape.WaitCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        self.bt_uninstall.setEnabled(status)
        self.bt_restore.setEnabled(status)
        self.bt_marketplace.setEnabled(status)
        self.bt_dev.setEnabled(status)
        self.bt_backup.setEnabled(status)
        self.bt_update.setEnabled(status)
        self.bt_apply.setEnabled(status)
        self.bt_install.setEnabled(status)
        self.checkSpicetify()

def main():
    app = QApplication(sys.argv)
    window = SpicyGreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
