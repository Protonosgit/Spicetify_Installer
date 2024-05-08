import sys
import os
import subprocess
import shutil
import time
from PyQt6.QtCore import QThread, pyqtSignal
from components.statusInfo import checkSpotifyRunning,checkAdminPrivileges

# Installer task for both windows and linux/mac with progress and error handling


class InstallSpicetifyold(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def run(self):
        try:
            if sys.platform == 'win32':
                self.progress_signal.emit("Downloading Spicetify...")
                subprocess.run(
                    'powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"', check=True, shell=True)
                self.progress_signal.emit("Cleaning up...")
                subprocess.run('spicetify clear -n -q', check=True, shell=True)
                self.progress_signal.emit("Creating backup...")
                subprocess.run('spicetify backup -n -q',
                               check=True, shell=True)
                self.progress_signal.emit("Enabling devtools...")
                subprocess.run('spicetify enable-devtools -n -q',
                               check=True, shell=True)
                self.progress_signal.emit("Applying modifications...")
                subprocess.run('spicetify apply -n -q', check=True, shell=True)
                self.progress_signal.emit("Installing Marketplace...")
                subprocess.run(
                    'powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1 | iex"', check=True, shell=True)
                self.progress_signal.emit("done")
        except Exception as e:
            print("Error detected!")
            print(e)
            self.progress_signal.emit("fail")

        self.finished_signal.emit()

class InstallSpicetify(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def run(self):
        try:
            if sys.platform == 'win32':
                self.progress_signal.emit("Installing Spicetify...")
                subprocess.run(
                    'echo y | powershell.exe -Command "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"', check=True, shell=True)
                self.progress_signal.emit("done")
        except Exception as e:
            print("Error detected!")
            print(e)
            self.progress_signal.emit("fail")

        self.finished_signal.emit()

# Update spicetify task


class UpdateSpicetify(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def run(self):
        print("Update started")
        try:
            self.progress_signal.emit("Auto Updating...")
            # subprocess.run('spicetify update -q -n', shell=True, check=True)
            subprocess.run('spicetify restore -q -n', shell=True, check=True)
            subprocess.run('spicetify upgrade -q -n', shell=True, check=True)
            subprocess.run('spicetify apply -q -n', shell=True, check=True)
            self.progress_signal.emit("done")
        except Exception as e:
            self.progress_signal.emit("fail")
            print("Error detected!")
            print(e)
        self.finished_signal.emit()

# Apply mods task


class ApplySpicetify(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        print("Apply started")
        try:
            subprocess.check_output(
                'spicetify apply -q -n', shell=True, check=True)
        except:
            pass
        self.finished_signal.emit()

# Uninstall  spicetify task


class UninstallSpicetify(QThread):
    finished_signal = pyqtSignal()
    progress_signal = pyqtSignal(str)

    def run(self):
        try:
            self.progress_signal.emit("Restoring Spotify from backup")
            subprocess.run('spicetify restore -q -n', shell=True, check=True)
            self.progress_signal.emit("Removing Spicetify data folder")
            subprocess.run(
                'powershell.exe -Command "rmdir -r -fo $env:APPDATA\spicetify"', check=True, shell=True)
            self.progress_signal.emit("Removing Spicetify config folder")
            subprocess.run(
                'powershell.exe -Command "rmdir -r -fo $env:LOCALAPPDATA\spicetify"', check=True, shell=True)
            self.progress_signal.emit("done")
        except:
            self.progress_signal.emit("fail")
            print("Error while uninstalling!")
        self.finished_signal.emit()

# Activate spicetify  task


class ActivateSpicetify(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        print("Activation started")
        try:
            killpath1 = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
            killpath2 = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui.spa')
            os.remove(killpath1)
            os.remove(killpath2)
        except:
            print("Error while removing login.spa and xpui.spa")
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
            'spicetify refresh',
            'spicetify upgrade',
            'spicetify enable-devtools',
            'spicetify restore',
        ]
        try:
            subprocess.run(commandList[self.cmnumber])
        except:
            print("Error while running custom command!")


# Try blocking spotify updates by changing permissions (Windows only)
def blockSpotifyUpdate(active):
    if active:
        try:
            # Check for existance before deleting update path and making it
            if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
                return
            os.makedirs(os.path.join(
                os.environ['LOCALAPPDATA'], "Spotify", "Update"))

            subprocess.run(
                f'cmd /c icacls %localappdata%\\Spotify\\Update /deny %username%:D', shell=True, check=True)
            subprocess.run(
                f'cmd /c icacls %localappdata%\\Spotify\\Update /deny %username%:R', shell=True, check=True)
            return
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.returncode}. patcher failed.')
            return e.returncode
    else:
        try:
            subprocess.run(
                f'cmd /c icacls %localappdata%\\Spotify\\Update /reset', shell=True)
            if os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
                shutil.rmtree(os.path.join(
                    os.environ['LOCALAPPDATA'], "Spotify", "Update"))
            return
        except subprocess.CalledProcessError as e:
            print(f'Error: {e.returncode}. patcher failed.')
            return e.returncode

# Restart Spotify


class RestartSpotify(QThread):
    # Warning this will probably replaced with spicetify restart in the future!
    def run(self):
        print("Restarting Spotify")
        if checkSpotifyRunning():
            subprocess.run('taskkill /f /im Spotify.exe')
            time.sleep(2)
            spotipath = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Roaming'), 'Spotify', 'Spotify.exe')
            subprocess.Popen(spotipath)


def backgroundActivate():
    try:
        killpath1 = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
        killpath2 = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui.spa')
        os.remove(killpath1)
        os.remove(killpath2)
    except:
        print("Error while removing login.spa and xpui.spa")
