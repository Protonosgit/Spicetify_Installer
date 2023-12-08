import requests
import os
import winreg
import subprocess
import psutil

# Checks for the latest manager version


def managerUpdateCheck():
    try:
        url = f"https://spicetifymanagerapi.netlify.app/.netlify/functions/api/latest/manager"
        response = requests.get(url)

        if response.status_code == 200:
            latest_release = response.json()
            tag_name = latest_release["tag_name"]
            if int(tag_name.replace(".", "")) > 120:
                return True
        else:
            return False
    except:
        return False

# Checks for the latest spicetify version


def getLatestSpicetifyRelease():
    try:
        url = f"https://spicetifymanagerapi.netlify.app/.netlify/functions/api/latest/spicetifycli"
        response = requests.get(url)

        if response.status_code == 200:
            latest_release = response.json()
            tag_name = latest_release["tag_name"]
            return tag_name
        else:
            return '0.0.0'
    except:
        return '0.0.0'


def checkSpotifyRunning():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'Spotify.exe' in process.info['name']:
            return True
    return False


def isAddedToStartup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        _, value, _ = winreg.QueryValueEx(key, "SpicetifyManager")
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print("Error while checking if added to startup")
        print(e)
        return False


def checkUpdateSupression():
    if not os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
        return False
    else:
        return True

# Checks if spicetify is installed by checking appdata folder


def checkInstalled():
    folder_path = os.path.join(os.path.join(
        os.path.expanduser('~'), 'AppData', 'Local'), 'spicetify')
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    else:
        return False

# Checks if spicetify is applied by checking appdata folder of spotify


def checkApplied():
    folder_path = os.path.join(os.path.expanduser(
        '~'), 'AppData', 'Roaming/Spotify/Apps/xpui')
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        return True
    else:
        return False


def spicetifyStatusCheck():
    try:
        LOCALSPICETIFYVER = subprocess.check_output(
            'spicetify --version', shell=True).decode("utf-8").strip()
        LATESTSPICETIFYVER = getLatestSpicetifyRelease().replace("v", "").strip()
        linkpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
        if os.path.exists(linkpath):
            if (LOCALSPICETIFYVER == LATESTSPICETIFYVER):
                return 0
            else:
                return 1
        else:
            return 2
    except:
        return 0
