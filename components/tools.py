import configparser
import requests

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