import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QMovie
import subprocess

class ImageEncryptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Decryption")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("QMainWindow { background-color: black; }"
                   "QLabel { font-size: 14px; color: white; font-weight: bold; }"
                   "QLineEdit { background-color: #ffffff; font-size: 14px; border: 1px solid #dcdcdc; padding: 3px; color: black; }"
                   "QPushButton { background-color: #4CAF50; color: white; border: none; padding: 5px 10px; font-size: 14px; }"
                   "QPushButton:hover { background-color: #45a049; }")

        layout = QVBoxLayout()
        self.label = QLabel("Select Encrypted Image:")
        layout.addWidget(self.label)
        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.get_image_path)
        layout.addWidget(self.button)
        self.password_label = QLabel("Enter Password:")
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit()
        layout.addWidget(self.password_edit)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.retrieve_password)
        layout.addWidget(self.ok_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_image_path(self):
        options = QFileDialog.Options()
        encrypted_image_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if encrypted_image_path:
            self.encrypted_image_path = encrypted_image_path

    def retrieve_password(self):
        password = self.password_edit.text()
        if hasattr(self, 'encrypted_image_path'):
            self.load_and_display_gif()
            self.run_decryption_script(password, self.encrypted_image_path)

    def run_decryption_script(self, password, image_path):
        try:
            subprocess.run(["python", "decrypt.py", password, image_path], check=True)
        except subprocess.CalledProcessError:
            pass

    def load_and_display_gif(self):
        if hasattr(self, 'gif_label'):
            self.gif_label.show()
            movie = QMovie('giphy.gif')
            self.gif_label.setMovie(movie)
            movie.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEncryptionWindow()
    window.show()
    sys.exit(app.exec_())
