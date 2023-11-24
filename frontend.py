import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from encr import process_images_in_folder, select_folder

class ImageEncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Encryption App")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        encrypt_button = QPushButton("Encrypt Images")
        encrypt_button.clicked.connect(self.encrypt_images)
        layout.addWidget(encrypt_button)

        central_widget.setLayout(layout)

    def encrypt_images(self):
        folder_path = select_folder()
        if folder_path:
            process_images_in_folder(folder_path)

def run_app():
    app = QApplication(sys.argv)
    window = ImageEncryptionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()
