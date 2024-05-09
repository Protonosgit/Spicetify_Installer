<img src="./res/icon.png" alt="spicetify manager icon" width="80"/> <br>
# Spicetify Manager
A project for installing and managing Spicetify from a Gui written in python and running on PyQt6.
The manager comes included with tools like block Spotify updates and a mode for running automatically on boot/Spotify startup.

![GitHub release (with filter)](https://img.shields.io/github/v/release/Protonosgit/Spicetify_Installer)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/Protonosgit/Spicetify_Manager)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Protonosgit/Spicetify_Manager)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Protonosgit/Spicetify_Manager)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Protonosgit/Spicetify_Manager)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Protonosgit/Spicetify_Manager)

## Attention:
This repo is looking for a new maintainer!
I personally don't have the time anymore to support this project in the future, so feel free to reach out if you're interested ❤️

![Screenshot](/.ghres/window_preview.png)
## Key Features

- [x] Simple installation,update,removal of Spicetify
- [X] Installation status/version checker
- [x] Automatically update spicetify and apply patches after spotify update
- [X] Detect and solve problems with your spicetify installation
- [X] Block Spotify updates
- [x] Options to manage Spotify in background
- [X] Always use the newest spicetify version
- [x] Custom cli commands
- [x] Suggest new versions of Spicetify / Manager

#### Made with Love by Protonos

 ## Installation and Running
If you do not trust the generated binary you may run the application directly with your local python installation using the provide instructions below.

```bash
  # Download the project
  git clone https://github.com/Protonosgit/Spicetify_Installer.git

  # Install required dependencies
  pip install -r requirements.txt
  
  #Start the application
  python main.py
```

### Important!
**Only** the **main.py** file will start the application!  
The other files are dynamically used as components and windows.

## Building binary

```bash
  # Download the project
  git clone https://github.com/Protonosgit/Spicetify_Installer.git

  # Install required dependencies
  python -m pip install requirements.txt
  python -m pip install pyinstaller

  # Build using pyinstaller and predefined config
  pyinstaller main.spec

  # Alternatively build an optimized version using upx (slower)
  pyinstaller main.spec --upx-dir "./upx"
```

## Usage Guide

[1] After running the main.py file wait a few seconds for the menu to show up

[2] Click on install and wait for the process to finish

[3] Inside the spotify window search for the shopping cart in the sidebar on the left

[4] Click on the icon and download your favorite themes, addons and more...

### Uninstalling

Simply click on the uninstall icon in the bottom right and confirm your choice

### Updating, Activating, Repairing

All of the above will be automatically detected, just confirm the actions!

## Manager API

Due to rate limiting I decided to create my own relay for the official Github api.
It just returns the latest release tag from the spicetify-cli repo.   
You can monitor the status here: [![Netlify Status](https://api.netlify.com/api/v1/badges/a32b6502-e8ec-45a7-b3e3-4af087f5d38e/deploy-status)](https://app.netlify.com/sites/spicetifymanagerapi/deploys)   
There might be more efficient ways to do this so feel free to suggest any improvements as an issue!

## Safety 
This project was flagged by some antivirus programs and I currently don't know how to avoid this!
So feel free to download the executables from **Github actions** and use them instead of the release files (They are identical)

Currently **Windows only**!
If would like to improve support for other Platforms feel free to do so!


## Acknowledgements
- [Spicetify](https://spicetify.app/)
- [Marketplace](https://github.com/spicetify/spicetify-marketplace)
- [Badges by Shields.io](https://shields.io/)
- [Api hosted on Netlify](https://netlify.com)
