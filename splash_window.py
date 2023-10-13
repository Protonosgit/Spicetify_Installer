import sys
import os
from PyQt6.QtWidgets import  QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

# Add check=true to subprocess to throw exeptions on failure :) shell is not neccesary

class Splash(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Switch when building
        loadUi("res/splash.ui", self)
        #loadUi(os.path.join(sys._MEIPASS, 'res', 'splash.ui'), self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)