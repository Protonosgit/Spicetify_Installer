from PyQt6.QtWidgets import  QErrorMessage, QMessageBox
from plyer import notification

def errorDialog(text):
    error_dialog = QErrorMessage()
    error_dialog.setWindowTitle('Warning an error occured')
    error_dialog.showMessage(text)
    error_dialog.exec()


def infoDialog(title, text):
    info_dialog = QMessageBox()
    info_dialog.setWindowTitle(title)
    info_dialog.setText(text)
    info_dialog.exec()

def confirmDialog(title, text):
    confirm_dialog = QMessageBox()
    confirm_dialog.setWindowTitle(title)
    confirm_dialog.setText(text)
    confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
    confirm_dialog.exec()
    

def windowsNotification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Spicetify Manager",
        timeout=10,
        app_icon=None,
    )