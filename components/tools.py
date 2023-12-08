import configparser
import os
import winreg

# Initiates the Manager.ini config file


def initConfig():
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
        print("Error while checking config file")
    try:
        with open(file_path, 'w') as f:
            f.write(config_dict)
    except:
        print("Error while creating config file")


# Reads config files
def readConfig(section, key):
    try:
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

# Patches Spotify with WatchWitch


def watchwitchInjector(mode):
    try:
        witchpath = os.path.join(os.path.join(os.path.expanduser(
            '~'), 'AppData', 'Roaming'), 'Spotify', 'Apps', 'xpui', 'index.html')
        patchstring = '''<script>fetch('http://localhost:1738/watchwitch/spotify/startup')</script>'''
        if mode:
            with open(witchpath, 'a', encoding='utf-8') as file:
                print("patching")
                file.write(patchstring)
        else:
            with open(witchpath, 'r+', encoding='utf-8') as file:
                print("unpatching")
                content = file.read()
                updated_content = content.replace(patchstring, '')
                file.seek(0)
                file.write(updated_content)
                file.truncate()
    except:
        print("Error while patching")
