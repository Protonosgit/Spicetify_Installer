
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import  QMainWindow,QMessageBox
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.uic import loadUi
from components.tools import selfUpdate

# Add check=true to subprocess to throw exeptions on failure :) shell is not neccesary

class Splash(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Switch when building
        loadUi("res/splash.ui", self)
        #loadUi(os.path.join(sys._MEIPASS, 'res', 'splash.ui'), self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.checkUpdateAvailable()
        
    def checkUpdateAvailable(self):
            if(selfUpdate()):
                reply = QMessageBox.question(None, 'Update', 'A new version of Spicetify Manager is available!\nWould you like to download it?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    QDesktopServices.openUrl(QUrl('https://github.com/Protonosgit/Spicetify_Installer/releases'))