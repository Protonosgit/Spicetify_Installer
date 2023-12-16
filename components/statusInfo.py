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
            return 'err'
    except:
        return 'err'


def checkSpotifyRunning():
    try:
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'Spotify.exe' in process.info['name']:
                return True
        return False
    except:
        return False


def checkWatchWitchPatched():
    try:
        witchpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui', 'index.html')
        patchstring = '''<script>fetch('http://localhost:1738/watchwitch/spotify/startup')</script>'''
        with open(witchpath, 'r+') as file:
            content = file.read()
            if patchstring in content:
                return True
            else:
                return False
    except:
        return False


def isAddedToStartup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, "SpicetifyManager")
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def checkUpdateSupression():
    try:
        if not os.path.exists(os.path.join(os.environ['LOCALAPPDATA'], "Spotify", "Update")):
            return False
        else:
            return True
    except:
        return False

# Checks if spicetify is installed by checking appdata folder


def checkSpicetifyInstalled():
    try:
        spicypath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'spicetify.exe')
        if os.path.exists(spicypath):
            return True
        else:
            return False
    except:
        return False


def checkSpotifyInstalled():
    try:
        spotipath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Spotify.exe')
        if os.path.exists(spotipath):
            return True
        else:
            return False
    except:
        return False


def checkSpicetifyApplied():
    try:
        workpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui')
        if os.path.exists(workpath):
            return True
        else:
            return False
    except:
        return False


def checkSpicetifyActive():
    try:
        linkpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'login.spa')
        if os.path.exists(linkpath):
            return False
        else:
            return True
    except:
        return False


def checkMarketplaceInstalled():
    try:
        marketpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui', 'spicetify-routes-marketplace.js')
        if os.path.exists(marketpath):
            return True
        else:
            return False
    except:
        return False


def spicetifyStatusCheck():
    try:
        if checkSpicetifyInstalled():
            spicetifylatest = getLatestSpicetifyRelease().replace("v", "").strip()
            spicetifylocal = subprocess.check_output(
                'spicetify --version', shell=True).decode("utf-8").strip()
            if checkSpicetifyActive():
                if spicetifylatest == spicetifylocal:
                    return 0
                else:
                    return 2
            else:
                return 1
        return 0
    except:
        return 0
