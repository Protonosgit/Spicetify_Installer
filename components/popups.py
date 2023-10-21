from PyQt6.QtWidgets import  QErrorMessage, QMessageBox

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
