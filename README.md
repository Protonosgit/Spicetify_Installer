# Spicetify Manager

A project for installing and managing Spicetify from a Gui written in python

![Logo](/.ghres/preview.png)

## Roadmap

- Include old manager menu in patcher

- Run after spotify startup (check for updates)

- Add custom patches / themes in application

- ... Clean up stuff

- Test on Linux / Mac

## Installation and Running

Download project from Github and install dependencies

```bash
  git clone https://github.com/Protonosgit/Spicetify_Manager.git

  python -m pip install pyqt6
  python -m pip install pyqt6-tools

  python main.py
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

## Acknowledgements

- [Spicetify](https://spicetify.app/)
- [Marketplace](https://github.com/spicetify/spicetify-marketplace)
