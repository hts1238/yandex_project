from registration_request import registration_request
from send_email import send_email
from generate_password import generate_password
from check_password import check_password
from check_handle import check_handle
from files import *

from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class RegistrationWindow(QDialog):
    """
    Класс окна регистрации пользователя
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi(REGISTRATION_UI, self)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.ok_btn.clicked.connect(self.run)
        self.password_text.setText(generate_password(15))

    def run(self):
        """
        Выполняет процесс регистрации пользователя, ели это возможно
        :return: None
        """
        email = self.email_text.text()
        name = self.name_text.text()
        handle = self.handle_text.text()
        password = self.password_text.text()
        if not check_handle(password):
            self.handle_corr.setText('Incorrect')
            self.handle_corr.setStyleSheet('color: red')
            return
        if not check_password(password):
            self.password.setText('Incorrect')
            self.password.setStyleSheet('color: red')
            return
        answer = registration_request(email, name, handle, password)

        if 'Error' not in answer:
            send_email(name, handle, password, email)
            self.token = answer['token']
            print(self.token)
            self.close()
        else:
            self.handle_corr.setText('Incorrect')
            self.handle_corr.setStyleSheet('color: red')
