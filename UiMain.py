from Message import Message
from send_message_server import send_message_server
from check_message import check_message
from refactor_message import refactor_message
from synchronization_server import synchronization_server
from style import *

import sys
import threading
from random import choice
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSizePolicy
from PyQt5.QtWidgets import QPushButton, QScrollBar, QLabel, QLineEdit
from PyQt5.QtCore import Qt

sys.setrecursionlimit(86400)  # Переопределяем предел рекурсии для синхронизации в течение суток

SYNCHRONIZATION_TIME = 1  # Частота синхнонизации (в секундах)


class MyWidget(QMainWindow):
    def __init__(self, users_handles, users_names, dialogs, handle, token):
        super().__init__()

        self.handle = handle
        self.token = token
        self.number_of_users = len(users_handles)
        self.names_of_users = dict()
        self.names_of_users = users_names
        self.handles_of_users = [*users_handles]
        self.users_btn = dict()
        self.users_showed = 0
        self.user_now = None
        self.dialogs = dialogs
        self.messages_number = 0
        self.initUI()

        self.start()

        self.synchronization()

    def initUI(self):
        uic.loadUi('main_window.ui', self)
        self.message_send_button.clicked.connect(self.send_message)

        self.restyle(0)

    def restyle(self, style):
        # self.setStyleSheet('''
        #  background-color: #323232;''')
        # self.setStyleSheet('''background-color: #A9B7C6;''')
        self.setStyleSheet(f'''background-color: {BACKGROUND_COLOR}''')
        self.message_send_button.setStyleSheet(MESSAGE_SEND_BTN_STYLE)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.send_message()
        if event.key() == Qt.Key_Return:
            self.send_message()

    def synchronization(self):
        something_new, new_senders, new_dialogs = \
            synchronization_server(self.handle, self.token, self.handles_of_users, self.dialogs)
        if something_new:  # Новая переписка не учтена
            self.dialogs = new_dialogs
        threading.Timer(SYNCHRONIZATION_TIME, self.synchronization).start()

    def clear_users(self):
        self.users_btn = dict()
        while self.senders.count():
            child = self.senders.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_messages(self):
        while self.messages.count():
            child = self.messages.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def scroll_message_bar(self, n):
        for _ in range(n):
            QApplication.processEvents()
        message_vbar = self.messangesScrollArea.verticalScrollBar()
        message_vbar.setSliderPosition(message_vbar.maximum())
        # message_vbar.setValue(self.message_vbar.maximum())
        # message_vbar.setSliderDown(True)

    def scroll_senders_bar(self):
        QApplication.processEvents()
        self.sendersScrollArea.verticalScrollBar().setSliderPosition(0)

    def send_message(self):
        if not self.user_now:
            return

        text = self.messange_input.text()
        if not check_message(text):
            return

        text = refactor_message(text)

        message = Message(text, self.names_of_users[self.handle])
        self.add_message(message)

        if self.dialogs[self.user_now]:
            self.dialogs[self.user_now].append(message)
        else:
            self.dialogs[self.user_now] = [message]

        # save_dialog(self.user_now, self.dialogs[self.user_now])

        send_message_server(self.handle, self.token, self.user_now, message.text)

        self.messange_input.clear()

        self.start()

    def add_message(self, text):
        if text.sender == self.names_of_users[self.handle]:
            self.messages.addWidget(text.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignRight)

        else:
            self.messages.addWidget(text.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignLeft)
        self.messages_number += 1

        self.scroll_message_bar(2)

    def show_new_user(self, user):
        btn = QPushButton(self.names_of_users[user])
        btn.clicked.connect(self.open_new_dialog)

        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn.setMinimumHeight(150)

        if self.user_now == user:
            btn.setStyleSheet(f'''background-color: {SENDER_NOW_BACKGROUND_COLOR};
                                  font-size: {SENDER_FONT_SIZE}''')
        else:
            btn.setStyleSheet(f'''background-color: {SENDER_BACKGROUND_COLOR};
                                  font-size: {SENDER_FONT_SIZE}''')
        # self.senders.addWidget(btn, self.users_showed, 0, alignment=Qt.AlignVCenter)
        self.senders.addWidget(btn)
        self.users_btn[btn] = user

        self.users_showed += 1

    def open_new_dialog(self):
        self.clear_messages()

        for btn in self.users_btn.keys():
            btn.setStyleSheet(f'''background-color: {SENDER_BACKGROUND_COLOR}; 
                                   font-size: {SENDER_FONT_SIZE}''')

        self.sender().setStyleSheet(f'''background-color: {SENDER_NOW_BACKGROUND_COLOR};
                                        font-size: {SENDER_FONT_SIZE}''')

        sender = self.users_btn[self.sender()]
        self.user_now = sender

        if sender not in self.dialogs:
            self.dialogs[sender] = []

        for message in self.dialogs[sender]:
            self.add_message(message)

        self.scroll_message_bar(0)

        # self.messange_input.setCursorPosition(0)

    def sort_users(self):
        self.clear_users()
        k = lambda l: -self.dialogs[l][-1].int_time if l in self.dialogs and self.dialogs[l] else 0
        self.handles_of_users.sort(key=k)
        # self.scroll_senders_bar()

    def start(self):
        self.sort_users()
        for i in range(self.number_of_users):
            self.show_new_user(self.handles_of_users[i])


def main(users_handles, users_names, dialogs, handle, token):
    try:
        app = QApplication(sys.argv)
        ex = MyWidget(users_handles, users_names, dialogs, handle, token)
        ex.show()
        sys.exit(app.exec_())
    finally:
        # open('data', 'w')
        pass
