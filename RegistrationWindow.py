from registration_request import registration_request
from send_email import send_email

from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('C:/Program Files (x86)/Messenger/RegistrationWindow.ui', self)
        self.setFixedSize(650, 700)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.ok_btn.clicked.connect(self.run)

    def run(self):
        email = self.email_text.text()
        name = self.name_text.text()
        handle = self.handle_text.text()
        password = self.password_text.text()
        answer = registration_request(email, name, handle, password)

        if 'Error' not in answer:
            send_email(name, handle, password, email)
            self.token = answer['token']
            print(self.token)
            self.close()
