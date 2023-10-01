import sys
import subprocess
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests

class InstallSpicetify(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    def run(self):
        try:
            self.progress_signal.emit("Downloading Spicetify...")
            subprocess.run('iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex' ,check=True)
            self.progress_signal.emit("Creating backup...")
            subprocess.run('spicetify clear',check=True)
            subprocess.run('spicetify backup',check=True)
            self.progress_signal.emit("Activating Spicetify...")
            #subprocess.run('powershell.exe -Command "spicetify apply"',check=True)
            self.progress_signal.emit("Installing Marketplace...")
            subprocess.run('Invoke-WebRequest -UseBasicParsing "https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1" | Invoke-Expression' ,check=True)
        except:
            print("Error detected!")
            self.progress_signal.emit("fail")
        self.finished_signal.emit()
class UpdateSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Update started")
        subprocess.run('spicetify upgrade')
        subprocess.run('spicetify update')
        self.finished_signal.emit()
class UninstallSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        subprocess.run('spicetify restore')
        if sys.platform == 'win32':
            subprocess.run('powershell.exe -Command "rmdir -r -fo $env:APPDATA\spicetify"',check=True)
            subprocess.run('powershell.exe -Command "rmdir -r -fo $env:LOCALAPPDATA\spicetify"',check=True)
        else:
            subprocess.run('rm -rf ~/.spicetify')
            subprocess.run('rm -rf ~/.config/spicetify')
        self.finished_signal.emit()

def getLatestRelease():
    url = f"https://api.github.com/repos/spicetify/spicetify-cli/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        latest_release = response.json()
        tag_name = latest_release["tag_name"]
        return tag_name
    else:
        return None