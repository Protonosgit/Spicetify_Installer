import sys
import subprocess
import time
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.uic import loadUi
from PyQt6.QtGui import QRegion

# Add check=true to subprocess to throw exeptions on failure :) shell is not neccesary

class Splash(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi('./res/splash.ui', self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)