from RegistrationWindow import RegistrationWindow
from login_request import login_request
from check_password import check_password


from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import csv


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        # self.remember = True
        self.initUI()

    def initUI(self):
        uic.loadUi('LoginWindow.ui', self)
        self.setFixedSize(650, 700)
        self.ok_btn.clicked.connect(self.run)
        self.registr_btn.clicked.connect(self.registration)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.handle_text.setText('admin')
        self.password_text.setText('admin')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.run()
        if event.key() == Qt.Key_Return:
            self.run()

    def run(self):
        handle = self.handle_text.text()
        password = self.password_text.text()
        if not check_password(password):
            return
        answer = login_request(handle, password)
        if 'Error' not in answer:
            print(handle, password, answer['token'])
            self.save(handle, password, answer['token'])
            self.close()

    def registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.setWindowModality(Qt.ApplicationModal)
        self.registration_window.show()

    def save(self, handle, password, token):
        with open('data.csv', 'w', encoding="utf8") as file:
            print(handle, password, token)
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([handle, password, token])
