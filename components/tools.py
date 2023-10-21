import configparser

def readConfig(file_path,section,key):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config[section][key]