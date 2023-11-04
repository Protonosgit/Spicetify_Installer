<img src="./res/icon.png" alt="spicetify manager icon" width="80"/> <br>
# Spicetify Manager
A project for installing and managing Spicetify from a Gui written in python

Contributers wellcome!

![GitHub release (with filter)](https://img.shields.io/github/v/release/Protonosgit/Spicetify_Installer)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/Protonosgit/Spicetify_Manager)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Protonosgit/Spicetify_Manager)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Protonosgit/Spicetify_Manager)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Protonosgit/Spicetify_Manager)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Protonosgit/Spicetify_Manager)

![Logo](/.ghres/preview.png)

## Features

- [x] Simple installation / update
- [X] Installation status/version checker
- [x] Clean and easy removal
- [x] Custom cli commands
- [x] Suggest new versions of Spicetify / Manager
- [ ] Automatically update spicetify and apply patches after spotify update

 Currently **Windows only**!
 If would like to improve support for other Platforms feel free to do so!
 ## Installation and Running

Download project from Github and install dependencies

```bash
  # Download the project
  git clone https://github.com/Protonosgit/Spicetify_Installer.git

  # Some dependencies might not be used to run the project
  python -m pip install requirements.txt

  python main.py
```

### Important!
**Only** the **main.py** file will start the application!  
The other files are dynamically used as components and windows.

## Building binary

```bash
  # Download the project
  git clone https://github.com/Protonosgit/Spicetify_Installer.git

  # Some dependencies might not be used to run the project
  python -m pip install requirements.txt

  # Build using pyinstaller and predefined config
  pyinstaller main.spec


  # Alternatively overwrite with your own config
  pyinstaller main.py

```

## Usage Guide

[1] After running the main.py file wait a few seconds for the menu to show up

[2] Click on install and wait for the process to finish

[3] Inside the spotify window search for the shopping cart in the sidebar on the left

[4] Click on the icon and download your favorite themes, addons and more...

### Uninstalling

Simply click on uninstall in the managers window and wait until spotify has restarted

### Updating

Clicking on the update button will check for version numbers first before initiating the download sequence

## Roadmap (will be implemented in 1.1.0 !)

1. Run after spotify startup (check for updates)

2. Auto apply spicetify after updates

## Manager API

Due to rate limiting I decided to create my own relay for the official Github api.
It just returns the latest release tag from the spicetify-cli repo.   
You can monitor the status here: [![Netlify Status](https://api.netlify.com/api/v1/badges/a32b6502-e8ec-45a7-b3e3-4af087f5d38e/deploy-status)](https://app.netlify.com/sites/spicetifymanagerapi/deploys)   
There might be more efficient ways to do this so feel free to suggest any improvements as an issue!


## Acknowledgements
- [Spicetify](https://spicetify.app/)
- [Marketplace](https://github.com/spicetify/spicetify-marketplace)
- [Badges by Shields.io](https://shields.io/)
- Inspired by Spicetify Easyinstall
