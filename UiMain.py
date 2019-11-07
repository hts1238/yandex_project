import sys
import time
import copy
import threading
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtWidgets import QPushButton, QInputDialog

from Message import Message
from send_message_server import send_message_server
from check_message import check_message
from check_handle import check_handle
from refactor_message import refactor_message
from synchronization_server import synchronization_server
from get_name_from_handle_server import get_name_from_handle_server
from files import *
from style import *

sys.setrecursionlimit(86400)  # Переопределяем предел рекурсии для синхронизации в течение суток

SYNCHRONIZATION_TIME = 5  # Частота синхнонизации (в секундах)

START_DIALOG_MESSAGE_TEXT = 'Hi'


class MainWindow(QMainWindow):
    """
    Класс главног окна.
    """

    def __init__(self, users_handles, users_names, dialogs, handle, token):
        """
        :param users_handles: список хэндлов пользователей, с которыми есть переписка
        :param users_names: словарь <хэндл пользователя>: <имя пользователя>
        :param dialogs: словарь <хэндл пользователя>: <спосок объектов класса Message (сообщений)>
        :param handle: хэндл пользователя
        :param token: токен пользователя
        """
        super().__init__()

        self.handle = handle
        self.token = token
        self.number_of_users = len(users_handles)
        self.names_of_users = dict()
        self.names_of_users = users_names
        self.handles_of_users = [*users_handles]
        self.users_btn = dict()
        self.user_now = None
        self.dialogs = dialogs
        self.messages_number = 0
        self.last_synchronization_time = time.time()

        self.setMouseTracking(True)

        self.initUI()

        self.start()

    def initUI(self):
        """
        Функция отрисовки основного окна
        :return: None
        """
        uic.loadUi(MAIN_WINDOW_UI, self)

        self.message_send_button.clicked.connect(self.send_message)

        self.exit_btn.clicked.connect(self.exit_user)

        self.new_dialog_btn.clicked.connect(self.start_new_dialog)

        self.restyle()

    def restyle(self):
        """
        Фукция установки стилей. Все стили прописываются в файле style.py
        :return: None
        """
        self.setStyleSheet(BACKGROUND_STYLE)
        self.message_send_button.setStyleSheet(MESSAGE_SEND_BTN_STYLE)

    def keyPressEvent(self, event):
        if time.time() - self.last_synchronization_time > SYNCHRONIZATION_TIME:
            self.synchronization()
            self.last_synchronization_time = time.time()
        if event.key() == Qt.Key_Enter:
            self.send_message()
        if event.key() == Qt.Key_Return:
            self.send_message()

    def mouseMoveEvent(self, event):
        if time.time() - self.last_synchronization_time > 1:
            self.synchronization()
            self.last_synchronization_time = time.time()

    def synchronization(self):
        """
        Функция сингхронизации. При вызове с сервера получает все диалоги пользователя
         и сравнивает их с нынешними. При несовпадении обновляет информацию, сортирует спиок
         юзеров по времени последнего сообщения. Если диалог открыт сейчас,
         то добавляет новое сообщение
        :return: None
        """
        saved_dialogs = copy.deepcopy(self.dialogs)
        something_new, new_senders, new_dialogs = synchronization_server(self.handle,
                                                                         self.token,
                                                                         self.handles_of_users,
                                                                         self.dialogs,
                                                                         self.names_of_users)
        if something_new:
            print('something_new')  # Что-то новое
            if self.user_now and saved_dialogs[self.user_now] != new_dialogs[self.user_now]:
                for message in new_dialogs[self.user_now]:
                    if message not in saved_dialogs[self.user_now]:
                        self.add_message(message)
            self.dialogs = copy.deepcopy(new_dialogs)
            self.number_of_users = len(self.dialogs)
            self.start()
        # threading.Timer(SYNCHRONIZATION_TIME, self.synchronization).start()

    def clear_users(self):
        """
        При вызове очищает поле юзеров
        :return: None
        """
        self.users_btn = dict()
        while self.senders.count():
            child = self.senders.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_messages(self):
        """
        При вызове очищает поле сообщений
        :return: None
        """
        while self.messages.count():
            child = self.messages.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def scroll_message_bar(self, n):
        """
        Прокручивает поле сообщений до конца
        :param n: Коллтчество processEvents перед очисткой
        :return: None
        """
        for _ in range(n):
            QApplication.processEvents()
        message_vbar = self.messangesScrollArea.verticalScrollBar()
        message_vbar.setSliderPosition(message_vbar.maximum())
        # message_vbar.setValue(self.message_vbar.maximum())
        # message_vbar.setSliderDown(True)

    def scroll_senders_bar(self):
        """
        Прокручивает поле юзеров в начало
        :return: None
        """
        QApplication.processEvents()
        self.sendersScrollArea.verticalScrollBar().setSliderPosition(0)

    def send_message(self):
        """
        Отправляет введенное сообщение на сервер,
         добавляет его в поле сообщений,
         заносит в диалог с нынешним юзером
        :return: None
        """
        if not self.user_now:
            return

        text = self.messange_input.text()
        if not check_message(text):
            return

        text = refactor_message(text)

        self.messange_input.clear()

        message = Message(text, self.names_of_users[self.handle])
        self.add_message(message)

        if self.dialogs[self.user_now]:
            self.dialogs[self.user_now].append(message)
        else:
            self.dialogs[self.user_now] = [message]

        # save_dialog(self.user_now, self.dialogs[self.user_now])

        send_message_server(self.handle, self.token, self.user_now, message.text)

        self.start()

    def add_message(self, message):
        """
        Добавляет в поле сообщенией переданное сообщение
        :param message: объект класса Message
        :return: None
        """
        if message.sender == self.names_of_users[self.handle]:
            self.messages.addWidget(message.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignRight)

        else:
            self.messages.addWidget(message.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignLeft)
        self.messages_number += 1

        self.scroll_message_bar(2)

    def show_new_user(self, user):
        """
        Добарляет пользователя по переданному хэндлу в поле юзеров
        :param user: хэндл пользователя
        :return: None
        """
        btn = QPushButton(self.names_of_users[user])
        btn.clicked.connect(self.open_new_dialog)

        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn.setMinimumHeight(150)

        btn.setStyleSheet(SENDER_BACKGROUND_STYLE if user != self.user_now
                          else SENDER_NOW_BACKGROUND_STYLE)

        # self.senders.addWidget(btn, self.users_showed, 0, alignment=Qt.AlignVCenter)
        self.senders.addWidget(btn)

        self.users_btn[btn] = user

    def open_new_dialog(self):
        """
        Открывает новый диалог, вызов доступен только по нажатию на кнопку юзера из self.users_btn
        :return: None
        """
        self.clear_messages()

        for btn in self.users_btn.keys():
            btn.setStyleSheet(SENDER_BACKGROUND_STYLE)

        self.sender().setStyleSheet(SENDER_NOW_BACKGROUND_STYLE)

        sender = self.users_btn[self.sender()]
        self.user_now = sender

        if sender not in self.dialogs:
            self.dialogs[sender] = []

        for message in self.dialogs[sender]:
            self.add_message(message)

        self.scroll_message_bar(0)

        # self.messange_input.setCursorPosition(0)

    def sort_users(self):
        """
        Сортирует self.handles_of_users по времени последнего сообщения
        :return: None
        """
        k = lambda l: -self.dialogs[l][-1].int_time if l in self.dialogs and self.dialogs[l] else 0
        self.handles_of_users.sort(key=k)
        # self.scroll_senders_bar()

    def start(self):
        """
        Обновляет поле юзеров
        :return: None
        """
        self.clear_users()
        self.sort_users()
        for i in range(self.number_of_users):
            self.show_new_user(self.handles_of_users[i])
        self.scroll_senders_bar()

    def start_new_dialog(self):
        """
        Открывает поле для ввода хэндла юзера, с которым необходимо начать переписку
        Если хэндл существует и диалог еще не начет, то открывается диалог и
        отправляется сообщение START_DIALOG_MESSAGE_TEXT
        :return: None
        """
        input_dialog = QInputDialog
        input_dialog.setStyleSheet(self, INPUT_DIALOG_BACKGROUND_STYLE)
        handle, okBtnPressed = QInputDialog.getText(self, 'Новый диалог',
                                                    'Введите handle пользователя')
        if okBtnPressed and handle not in self.handles_of_users:
            if not check_handle(handle):
                self.handles_of_users.append(handle)
                self.names_of_users[handle] = get_name_from_handle_server(handle)
                send_message_server(self.handle, self.token, handle, START_DIALOG_MESSAGE_TEXT)
                self.synchronization()

    def exit_user(self):
        """
        Осуществляет выход пользователя из системы
        (Очищает запомненные данные пользователя)
        :return: None
        """
        open(DATA, 'w')
        self.close()
        exit(0)


def main(users_handles, users_names, dialogs, handle, token, remember):
    """
    Функция запуска главнго окна приложения Messenger
    :param users_handles: список хэндлов юзеров, с которыми есть переписка
    :param users_names: словарь <хэндл пользователя>: <имя пользователя>
    :param dialogs: словарь <хэндл пользователя>: <спосок объектов класса Message (сообщений)>
    :param handle: хэндл пользователя
    :param token: токен пользователя
    :param remember: нужно ли запоминать логин и пароль пользователя для автоматического входа
    :return: None
    """
    try:
        app = QApplication(sys.argv)
        ex = MainWindow(users_handles, users_names, dialogs, handle, token)
        ex.show()
        sys.exit(app.exec_())
    finally:
        if remember == 'False':
            open(DATA, 'w')
