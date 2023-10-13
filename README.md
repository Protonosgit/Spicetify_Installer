# Spicetify Manager

A project for installing and managing Spicetify from a Gui written in python

Contributers wellcome!

![MIT License](https://badgen.net/badge/project/SpicyGreen)
![GitHub release (with filter)](https://img.shields.io/github/v/release/Protonosgit/Spicetify_Manager?filter=*alpha)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/Protonosgit/Spicetify_Manager)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Protonosgit/Spicetify_Manager)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/Protonosgit/Spicetify_Manager)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Protonosgit/Spicetify_Manager)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Protonosgit/Spicetify_Manager)

Current Gui:
![Logo](/.ghres/preview.png)

## Features

- [x] Simple installation / update
- [x] Clean and easy removal
- [x] Cross platform (40% done)
- [ ] Automatically update spicetify and apply patches after spotify update
- [ ] Theme/extension installer

## Installation and Running

Download project from Github and install dependencies

```bash
  git clone https://github.com/Protonosgit/Spicetify_Manager.git

  python -m pip install pyqt6
  python -m pip install pyqt6-tools

  python main.py
```

## Building binary

```bash
  # First build and config setup
  pyinstaller main.py

  # Build using config
  pyinstaller main.spec

```

### Important!

Only the main.py file will start the application!  
The other files are dynamically used as components.

## Usage Guide

[1] After running the main.py file wait for 5 - 8 sec till the menu shows up

[2] Click on install and wait for the process to finish

[3] Inside the spotify window search for the shopping cart in the sidebar on the left

[4] Click on the icon and download your favorite themes, addons and more...

### Uninstalling

Simply click on uninstall in the managers window and wait until spotify has restarted

### Updating

Clicking on the update button will check for version numbers first before initiating the download sequence

## Roadmap

1. Include old manager menu in patcher

2. Run after spotify startup (check for updates)

3. Auto update spicetify

4. Test on Linux / Mac

5. Add plugins/themes browser in application

## Acknowledgements

- [Spicetify](https://spicetify.app/)
- [Marketplace](https://github.com/spicetify/spicetify-marketplace)
- [Badges by Shields.io](https://shields.io/)
