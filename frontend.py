from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QDialog
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.uic import loadUi
import subprocess
import json
import os
import sys
import time
from decrypt import ImageSignalEmitter

class PasswordDialog(QDialog):
    def __init__(self, image_name, parent=None):
        super().__init__(parent)
        self.image_name = image_name
        self.setWindowTitle(f"Enter Password for {image_name}")
        self.setGeometry(100, 100, 400, 150)
        self.label = QLabel(f"Enter password for {image_name}:", self)
        self.password_edit = QLineEdit(self)
        self.ok_button = QPushButton('OK', self)
        self.cancel_button = QPushButton('Cancel', self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        self.setStyleSheet("QDialog { background-color: #f5f5f5; }"
                           "QLabel { font-size: 14px; }"
                           "QLineEdit { background-color: #ffffff; font-size: 14px; border: 1px solid #dcdcdc; padding: 3px; }"
                           "QPushButton { background-color: #4CAF50; color: white; border: none; padding: 5px 10px; font-size: 14px; }"
                           "QPushButton:hover { background-color: #45a049; }")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def get_password(self):
        return self.password_edit.text()

class Worker(QObject):
    show_tick = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            if os.path.exists('completed.txt'):
                self.show_tick.emit()
                os.remove('completed.txt')
            time.sleep(1)

class ImageSignalEmitter(QObject):
    image_ready = pyqtSignal(str)

class ImageEncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('load_ui.ui', self)
        
        encrypt_button = self.findChild(QPushButton, 'encrypt')
        encrypt_button.clicked.connect(self.show_folder_dialog)

        decrypt_button = self.findChild(QPushButton, 'decrypt')
        decrypt_button.clicked.connect(self.run_decrypt_window)

        self.passwords_array = []

        self.gif_label = self.findChild(QLabel, 'gif')
        if self.gif_label:
            self.gif_label.hide()
        
        self.tick = self.findChild(QLabel, 'tick')
        if self.tick:
            self.tick.hide()

        self.worker = Worker()
        self.worker_thread = QThread()

        self.worker.moveToThread(self.worker_thread)
        self.worker.show_tick.connect(self.load_and_display_tick)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

        self.signal_emitter = ImageSignalEmitter()
        self.signal_emitter.image_ready.connect(self.handle_image_ready)
        print("Image ready signal connected")

    def show_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder Containing Images')

        if folder_path:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            for image_file in image_files:
                password = self.get_password(image_file)
                if password:
                    self.passwords_array.append((image_file, password))

            passwords_json = json.dumps(self.passwords_array)

            subprocess.Popen(['python', 'encr.py', folder_path, passwords_json])

            self.load_and_display_gif()

    def get_password(self, image_file):
        password_dialog = PasswordDialog(image_file, self)
        result = password_dialog.exec_()
        if result == QDialog.Accepted:
            return password_dialog.get_password()
        else:
            return None

    def load_and_display_gif(self):
        if self.gif_label:
            self.gif_label.show()
            movie = QMovie('giphy.gif')
            self.gif_label.setMovie(movie)
            movie.start()

    def load_and_display_tick(self):
        if self.tick:
            self.tick.show()
            movie = QMovie('tick.gif')
            self.tick.setMovie(movie)
            movie.start()

    def run_decrypt_window(self):
        if self.tick:
            self.tick.hide()
        if self.gif_label:
            self.gif_label.hide()
        subprocess.Popen(['python', 'decryptwindow.py'])

    @pyqtSlot(str)
    def handle_image_ready(self, image_path):
        print("Received signal with image path:", image_path)
        pixmap = QPixmap(image_path)
        self.decrypted_image_label.setPixmap(pixmap)
        self.decrypted_image_label.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageEncryptionApp()
    window.showMaximized()
    sys.exit(app.exec_())
