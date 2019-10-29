from RegistrationWindow import RegistrationWindow
from login_request import login_request

from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('C:/Program Files (x86)/Messenger/LoginWindow.ui', self)
        self.setFixedSize(650, 700)
        self.ok_btn.clicked.connect(self.run)
        self.registr_btn.clicked.connect(self.registration)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)

    def run(self):
        handle = self.handle_text.text()
        password = self.password_text.text()
        answer = login_request(handle, password)
        if 'Error' not in answer:
            self.save(handle, password, answer['token'])
            self.close()

    def registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.setWindowModality(Qt.ApplicationModal)
        self.registration_window.show()

    def save(self, handle, password, token):
        with open('C:/Program Files (x86)/Messenger/data', 'w') as file:
            file.write(handle + '\n')
            file.write(password + '\n')
            file.write(token)
