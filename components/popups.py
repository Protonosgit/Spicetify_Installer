import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set dialog properties
        self.setWindowTitle("My Dialog")
        self.setGeometry(100, 100, 400, 200)

        # Create a layout for the dialog
        layout = QVBoxLayout()

        # Create a label
        label = QLabel("This is a dialog box.")
        layout.addWidget(label)

        # Create an "OK" button to accept the dialog
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)  # Close the dialog with accept() when OK is clicked
        layout.addWidget(ok_button)

        # Create a "Cancel" button to reject (cancel) the dialog
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Close the dialog with reject() when Cancel is clicked
        layout.addWidget(cancel_button)

        # Set the layout for the dialog
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    dialog = MyDialog()
    result = dialog.exec()

    if result == QDialog.DialogCode.Accepted:
        print("OK button was clicked.")
    else:
        print("Cancel button was clicked or the dialog was closed.")

if __name__ == "__main__":
    main()
