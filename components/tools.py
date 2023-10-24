import configparser
import requests
import os

#Reads config files
def readConfig(file_path,section,key):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config[section][key]

#Checks for the latest spicetify version
def getLatestRelease():
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
    
#Writes a short info about the installation status to a text file in spicetifys folder
def writeManagerPoint(data):
    with open(os.path.join(os.path.join( os.path.expanduser('~'), 'AppData','Local'), 'spicetify', 'protonosmanager.txt'), 'w') as f:
        f.write(data)