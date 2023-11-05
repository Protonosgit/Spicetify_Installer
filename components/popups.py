from PyQt6.QtWidgets import QErrorMessage, QMessageBox
from windows_toasts import WindowsToaster, Toast, ToastButton, InteractableWindowsToaster


def errorDialog(text):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setWindowTitle('Warning an error was detected')
    error_dialog.setText(text)
    error_dialog.exec()


def infoDialog(title, text):
    info_dialog = QMessageBox()
    info_dialog.setIcon(QMessageBox.Icon.Information)
    info_dialog.setWindowTitle(title)
    info_dialog.setText(text)
    info_dialog.exec()


def confirmDialog(title, text):
    confirm_dialog = QMessageBox()
    confirm_dialog.setIcon(QMessageBox.Icon.Question)
    confirm_dialog.setWindowTitle(title)
    confirm_dialog.setText(text)
    confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
    confirm_dialog.exec()


def windowsToast(title, message):
    toaster = WindowsToaster('Spicetify Manager')
    toastbuilder = Toast()
    toastbuilder.text_fields = [title, message]
    toaster.show_toast(toastbuilder)


def interactableWindowsToast(title, message):

    interactableToaster = InteractableWindowsToaster('Spicetify Manager')
    newToast = Toast(['Can you dive?'])

    # Add two actions (buttons)
    newToast.AddAction(ToastButton('Definitely', 'response=decent'))
    newToast.AddAction(ToastButton('Nope', 'response=bad'))

    # Display it like usual
    interactableToaster.show_toast(newToast)
