
import sys
import os
import subprocess
import psutil
import shutil
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests

# Installer task for both windows and linux/mac with progress and error handling
class InstallSpicetify(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    def run(self):
        try:
            if sys.platform == 'win32':
                self.progress_signal.emit("Downloading Spicetify...")
                subprocess.run('powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"',check=True)
                self.progress_signal.emit("Creating backup...")
                subprocess.run('spicetify clear',check=True)
                subprocess.run('spicetify backup apply enable-devtools',check=True)
                self.progress_signal.emit("Installing Marketplace...")
                subprocess.run('powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1 | iex"',check=True)
            else:
                self.progress_signal.emit("Downloading Spicetify...")
                subprocess.run('curl -fsSL https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.sh | sh',check=True)
                self.progress_signal.emit("Creating backup...")
                subprocess.run('spicetify clear',check=True)
                subprocess.run('spicetify backup apply enable-devtools',check=True)
                self.progress_signal.emit("Installing Marketplace...")
                subprocess.run('curl -fsSL https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.sh | sh',check=True)
        except Exception as e:
            print("Error detected!")
            print(e)
            self.progress_signal.emit("fail")
        self.finished_signal.emit()
# Updater task
class UpdateSpicetify(QThread):
    finished_signal = pyqtSignal()
    def run(self):
        print("Update started")
        subprocess.run('spicetify upgrade')
        subprocess.run('spicetify update')
        self.finished_signal.emit()
# Uninstaller task
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
    
# Custom command task
class CustomCommand(QThread):
    def __init__(self, index):
        super().__init__()
        self.cmnumber = index

    finished_signal = pyqtSignal()
    def run(self):
        commandList = [
        'spicetify --version',
        'spicetify backup',
        'spicetify clear',
        'spicetify apply',
        'spicetify update',
        'spicetify upgrade',
        'spicetify enable-devtools',
        'spicetify restore',
        ]
        try:
            subprocess.run(commandList[self.cmnumber])
        except:
            print("Error while running custom command!")


#Checks github for latest spicetify version
def getLatestRelease():
    url = f"https://api.github.com/repos/spicetify/spicetify-cli/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        latest_release = response.json()
        tag_name = latest_release["tag_name"]
        return tag_name
    else:
        return None
    
#Checks if spicetify is installed by checking appdata folder
def checkInstalled():
    folder_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify')
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    else:
        return False

#Checks if spicetify is applied by checking appdata folder of spotify
def checkApplied():
    folder_path = os.path.join( os.path.expanduser('~'), 'AppData','Roaming/Spotify/Apps/xpui')
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    else:
        return False
#Checks if spicetify is running using a tasksearch
def checkSpotifyRunning():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'Spotify.exe' in process.info['name']:
            return True
    return False
#Try blocking spotify updates by changing permissions (Windows only) 
#Warning this function is unstable!
def blockSpotifyUpdate(active):
    if active:
        try:
            #Check for existance before deleting update path and making it
            if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
                shutil.rmtree(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update"))
            os.makedirs(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update"))

            subprocess.run(f'cmd /c icacls %localappdata%\\Spotify\\Update /deny %username%:D', shell=True, check=True)
            subprocess.run(f'cmd /c icacls %localappdata%\\Spotify\\Update /deny %username%:R', shell=True, check=True)
            return
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.returncode}. patcher failed.')
            return e.returncode
    else:
        try:
            subprocess.run(f'cmd /c icacls %localappdata%\\Spotify\\Update /reset', shell=True)
            if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
                shutil.rmtree(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update"))
            return
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.returncode}. patcher failed.')
            return e.returncode

# Checks if spotify updates are blocked (unfinished)
def checkSpotifyBlockedUpdate():

    directory_path = r'C:\path\to\directory'
    permission_to_check = 'D'

    command = f'icacls "{directory_path}"'

    try:
        result = subprocess.check_output(command, shell=True, text=True)
    
        if f'"{permission_to_check}":(R)' in result:
            print(f'Permission {permission_to_check} is active on {directory_path}')
        else:
            print(f'Permission {permission_to_check} is not active on {directory_path}')
    except subprocess.CalledProcessError as e:
        print(f'Error: {e.returncode}. Failed to check permissions.')

