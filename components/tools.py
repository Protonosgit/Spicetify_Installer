import configparser
import requests
import os
import winreg

#Initiates the Manager.ini config file
def initConfig():
    file_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'Manager.ini')
    if (os.path.exists(file_path)):
        return
    config_dict ='''
    [Manager]

    [Spicetify]

    [Settings]
    '''
    try:
        with open(file_path, 'w') as f:
            f.write(config_dict)
    except:
        print("Error while creating config file")


#Reads config files
def readConfig(section,key):
    file_path=os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'Manager.ini')
    config = configparser.ConfigParser()
    config.read(file_path)
    if key in config[section]:
        return config[section][key]
    else:
        return ''

#Writes config files
def writeConfig(section,key,value):
    file_path=os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'Manager.ini')
    config = configparser.ConfigParser()
    config.read(file_path)
    config[section][key] = value
    with open(file_path, 'w') as configfile:
        config.write(configfile)

#Checks for the latest spicetify version
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
    
def selfUpdate():
    try:
        url = f"https://spicetifymanagerapi.netlify.app/.netlify/functions/api/latest/manager"
        response = requests.get(url)

        if response.status_code == 200:
            latest_release = response.json()
            tag_name = latest_release["tag_name"]
            if int(tag_name.replace(".","")) > 110:
                return True
        else:
            return False
    except:
        return False

# Add exe to startup of windows /remove it again
def addToStartup(mode):
    if mode:
        folder_path = os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify','Manager.exe')
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SpicetifyManager", 0, winreg.REG_SZ, folder_path)
        winreg.CloseKey(key)
    else:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "SpicetifyManager")
        winreg.CloseKey(key)