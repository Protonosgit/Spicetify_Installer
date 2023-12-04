import configparser
import requests
import os
import winreg
import subprocess

# Initiates the Manager.ini config file


def initConfig():
    print('!! Temporary Action3 called !!')
    try:
        file_path = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'Manager.ini')
        if (os.path.exists(file_path)):
            return
        config_dict = '''
[Manager]
watchwitch = False
noupdate = False
autoclose = False
    '''
    except:
        print("Error while creating config file")
    try:
        with open(file_path, 'w') as f:
            f.write(config_dict)
    except:
        print("Error while creating config file")


# Reads config files
def readConfig(section, key):
    print('!! Temporary Action1 called !!')
    try:
        print(key)
        file_path = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'Manager.ini')
        config = configparser.ConfigParser()
        config.read(file_path)
        if key in config[section]:
            return config[section][key]
        else:
            return ''
    except:
        print("Error while reading config file")
        return ''

# Writes config files


def writeConfig(section, key, value):
    print('!! Temporary Action2 called !!')
    try:
        file_path = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Local'), 'spicetify', 'Manager.ini')
        config = configparser.ConfigParser()
        config.read(file_path)
        config[section][key] = value
        with open(file_path, 'w') as configfile:
            config.write(configfile)
    except:
        print("Error while writing config file")

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

# Checks if a new version of the manager is available


def managerUpdateCheck():
    try:
        url = f"https://spicetifymanagerapi.netlify.app/.netlify/functions/api/latest/manager"
        response = requests.get(url)

        if response.status_code == 200:
            latest_release = response.json()
            tag_name = latest_release["tag_name"]
            if int(tag_name.replace(".", "")) > 112:
                return True
        else:
            return False
    except:
        return False

# Add exe to startup of windows /remove it again


def addToStartup(mode):
    try:
        if mode:
            folder_path = os.path.join(os.path.join(os.path.expanduser(
                '~'), 'AppData', 'Local'), 'spicetify', 'Manager.exe')
            args = '--startup'
            command = f'"{folder_path}" {args}'
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SpicetifyManager",
                              0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
        else:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SpicetifyManager")
            winreg.CloseKey(key)
    except:
        print("Error while adding to startup")


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
        print(e)
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
