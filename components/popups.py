from PyQt6.QtWidgets import QErrorMessage, QMessageBox
from windows_toasts import WindowsToaster, Toast, ToastButton, InteractableWindowsToaster

# !!!
# This module will be getting a rework so everything is subject to change!!!
# !!!


def errorDialog(text):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setWindowTitle('Warning an error was detected')
    error_dialog.setText(text)
    error_dialog.exec()


def infoDialog(text):
    info_dialog = QMessageBox()
    info_dialog.setIcon(QMessageBox.Icon.Information)
    info_dialog.setWindowTitle('Information')
    info_dialog.setText(text)
    info_dialog.exec()


def warnDialog(text):
    info_dialog = QMessageBox()
    info_dialog.setIcon(QMessageBox.Icon.Warning)
    info_dialog.setWindowTitle('Warning')
    info_dialog.setText(text)
    info_dialog.exec()


def confirmationModal(title, message):
    return QMessageBox.question(None, title, message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)


def windowsToast(title, message):
    toaster = WindowsToaster('Spicetify Manager')
    toastbuilder = Toast()
    toastbuilder.text_fields = [title, message]
    toaster.show_toast(toastbuilder)

# Unused


def winUpdateToast():
    # unused due to limitations related to the window manager in main.py
    interactableToaster = InteractableWindowsToaster('Spicetify Manager')
    newToast = Toast(['Spicetify is not active'], 'Spicetify Manager')

    newToast.AddAction(ToastButton('Open Manager', 'response=decent'))
    newToast.AddAction(ToastButton('Ignore', 'response=bad'))

    interactableToaster.show_toast(newToast)
