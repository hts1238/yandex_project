"""
█   █ ███ ███ ███ ███ █  █ ████ ███ ████
██ ██ █   █   █   █   ██ █ █    █   █  █
█ █ █ ███ ███ ███ ███ █ ██ █ ██ ███ ████
█   █ █     █   █ █   █  █ █  █ █   █ █
█   █ ███ ███ ███ ███ █  █ ████ ███ █ █
"""

import sys
import time
import copy
import csv
import requests
import json
import imaplib
import smtplib
import platform
from time import time, ctime
from math import floor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtWidgets import QPushButton, QInputDialog, QLabel, QDialog

# sys.path.insert(1, 'C:/Program Files (x86)/Messenger/')


sys.setrecursionlimit(86400)  # Переопределяем предел рекурсии для синхронизации в течение суток

SYNCHRONIZATION_TIME = 5  # Частота синхнонизации (в секундах)

START_DIALOG_MESSAGE_TEXT = 'Hi'

MAIN_WINDOW_UI = 'main_window.ui'
LOGIN_UI = 'LoginWindow.ui'
REGISTRATION_UI = 'RegistrationWindow.ui'

DATA = 'data.csv'

if platform.system() == 'Windows':
    LOGIN_PY = 'main_login.py'
elif platform.system() == 'Linux':
    LOGIN_PY = 'python3 main_login.py'

BACKGROUND_STYLE = '''
    background-color: #334;
    font-family: sans-serif;
'''

SENDER_BACKGROUND_STYLE = '''
    background-color: #334;
    color: #fff;
    font-size: 35px;
'''

INPUT_DIALOG_BACKGROUND_STYLE = '''
    background-color: #334;
    color: #fff;
    font-size: 25px;
'''

SENDER_NOW_BACKGROUND_STYLE = '''
    background-color: #557;
    color: #fff;
    font-size: 35px;
'''

MESSAGE_STYLE = '''
    font-size: 25px;
    color: #fff;
    background-color: #557;
    border: 2px outset #668;
    border-radius: 10px;
    min-width: 10em;
    padding: 6px;
'''

MESSAGE_SEND_BTN_STYLE = '''
    background-color: #334;
    border: 2px outset #668;
    border-radius: 10px;
    min-width: 10em;
    padding: 6px;
'''


class UiLoginWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 700)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.password_corr = QtWidgets.QLabel(Dialog)
        self.password_corr.setText("")
        self.password_corr.setObjectName("password_corr")
        self.gridLayout.addWidget(self.password_corr, 2, 2, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ok_btn.setFont(font)
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.ok_btn, 4, 0, 1, 3)
        self.login_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_label.sizePolicy().hasHeightForWidth())
        self.login_label.setSizePolicy(sizePolicy)
        self.login_label.setMinimumSize(QtCore.QSize(100, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.login_label.setFont(font)
        self.login_label.setTextFormat(QtCore.Qt.AutoText)
        self.login_label.setScaledContents(False)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setOpenExternalLinks(True)
        self.login_label.setObjectName("login_label")
        self.gridLayout.addWidget(self.login_label, 0, 0, 1, 3)
        self.registr_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.registr_btn.setFont(font)
        self.registr_btn.setObjectName("registr_btn")
        self.gridLayout.addWidget(self.registr_btn, 5, 0, 1, 3)
        self.password_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 2, 0, 1, 1)
        self.handle_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.handle_text.sizePolicy().hasHeightForWidth())
        self.handle_text.setSizePolicy(sizePolicy)
        self.handle_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.handle_text.setFont(font)
        self.handle_text.setStyleSheet("border-style: outset;\n"
                                       "border-width: 2px;\n"
                                       "border-radius: 10px")
        self.handle_text.setText("")
        self.handle_text.setObjectName("handle_text")
        self.gridLayout.addWidget(self.handle_text, 1, 1, 1, 1)
        self.password_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_text.sizePolicy().hasHeightForWidth())
        self.password_text.setSizePolicy(sizePolicy)
        self.password_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password_text.setFont(font)
        self.password_text.setStyleSheet("border-style: outset;\n"
                                         "border-width: 2px;\n"
                                         "border-radius: 10px")
        self.password_text.setText("")
        self.password_text.setObjectName("password_text")
        self.gridLayout.addWidget(self.password_text, 2, 1, 1, 1)
        self.handle_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(80)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.handle_label.sizePolicy().hasHeightForWidth())
        self.handle_label.setSizePolicy(sizePolicy)
        self.handle_label.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.handle_label.setFont(font)
        self.handle_label.setObjectName("handle_label")
        self.gridLayout.addWidget(self.handle_label, 1, 0, 1, 1)
        self.handle_corr = QtWidgets.QLabel(Dialog)
        self.handle_corr.setText("")
        self.handle_corr.setObjectName("handle_corr")
        self.gridLayout.addWidget(self.handle_corr, 1, 2, 1, 1)
        self.remember_btn = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remember_btn.sizePolicy().hasHeightForWidth())
        self.remember_btn.setSizePolicy(sizePolicy)
        self.remember_btn.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.remember_btn.setFont(font)
        self.remember_btn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.remember_btn.setObjectName("remember_btn")
        self.gridLayout.addWidget(self.remember_btn, 3, 1, 1, 2)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ok_btn.setText(_translate("Dialog", "Ок"))
        self.login_label.setText(_translate("Dialog", "Авторизируйтесь:"))
        self.registr_btn.setText(_translate("Dialog", "Регистрация"))
        self.password_label.setText(_translate("Dialog", "Password:"))
        self.handle_label.setText(_translate("Dialog", "Handle:"))
        self.remember_btn.setText(_translate("Dialog", "Запомнить логин и пароль"))


class UiRegistrationWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(700, 700)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.password_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_label.sizePolicy().hasHeightForWidth())
        self.password_label.setSizePolicy(sizePolicy)
        self.password_label.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 4, 0, 1, 1)
        self.password_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_text.sizePolicy().hasHeightForWidth())
        self.password_text.setSizePolicy(sizePolicy)
        self.password_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password_text.setFont(font)
        self.password_text.setStyleSheet("border-style: outset;\n"
                                         "border-width: 2px;\n"
                                         "border-radius: 10px")
        self.password_text.setText("")
        self.password_text.setObjectName("password_text")
        self.gridLayout.addWidget(self.password_text, 4, 1, 1, 1)
        self.handle_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.handle_text.sizePolicy().hasHeightForWidth())
        self.handle_text.setSizePolicy(sizePolicy)
        self.handle_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.handle_text.setFont(font)
        self.handle_text.setStyleSheet("border-style: outset;\n"
                                       "border-width: 2px;\n"
                                       "border-radius: 10px")
        self.handle_text.setText("")
        self.handle_text.setObjectName("handle_text")
        self.gridLayout.addWidget(self.handle_text, 2, 1, 1, 1)
        self.handle_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(80)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.handle_label.sizePolicy().hasHeightForWidth())
        self.handle_label.setSizePolicy(sizePolicy)
        self.handle_label.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.handle_label.setFont(font)
        self.handle_label.setObjectName("handle_label")
        self.gridLayout.addWidget(self.handle_label, 2, 0, 1, 1)
        self.name_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.gridLayout.addWidget(self.name_label, 1, 0, 1, 1)
        self.name_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_text.sizePolicy().hasHeightForWidth())
        self.name_text.setSizePolicy(sizePolicy)
        self.name_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.name_text.setFont(font)
        self.name_text.setStyleSheet("border-style: outset;\n"
                                     "border-width: 2px;\n"
                                     "border-radius: 10px")
        self.name_text.setObjectName("name_text")
        self.gridLayout.addWidget(self.name_text, 1, 1, 1, 1)
        self.email_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.email_label.setFont(font)
        self.email_label.setObjectName("email_label")
        self.gridLayout.addWidget(self.email_label, 3, 0, 1, 1)
        self.email_text = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_text.sizePolicy().hasHeightForWidth())
        self.email_text.setSizePolicy(sizePolicy)
        self.email_text.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.email_text.setFont(font)
        self.email_text.setStyleSheet("border-style: outset;\n"
                                      "border-width: 2px;\n"
                                      "border-radius: 10px")
        self.email_text.setObjectName("email_text")
        self.gridLayout.addWidget(self.email_text, 3, 1, 1, 1)
        self.name_corr = QtWidgets.QLabel(Dialog)
        self.name_corr.setObjectName("name_corr")
        self.gridLayout.addWidget(self.name_corr, 1, 2, 1, 1)
        self.handle_corr = QtWidgets.QLabel(Dialog)
        self.handle_corr.setObjectName("handle_corr")
        self.gridLayout.addWidget(self.handle_corr, 2, 2, 1, 1)
        self.email_corr = QtWidgets.QLabel(Dialog)
        self.email_corr.setObjectName("email_corr")
        self.gridLayout.addWidget(self.email_corr, 3, 2, 1, 1)
        self.password = QtWidgets.QLabel(Dialog)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 4, 2, 1, 1)
        self.ok_btn = QtWidgets.QPushButton(Dialog)
        self.ok_btn.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ok_btn.setFont(font)
        self.ok_btn.setObjectName("ok_btn")
        self.gridLayout.addWidget(self.ok_btn, 5, 0, 1, 3)
        self.registr_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registr_label.sizePolicy().hasHeightForWidth())
        self.registr_label.setSizePolicy(sizePolicy)
        self.registr_label.setMinimumSize(QtCore.QSize(100, 180))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.registr_label.setFont(font)
        self.registr_label.setTextFormat(QtCore.Qt.AutoText)
        self.registr_label.setScaledContents(False)
        self.registr_label.setAlignment(QtCore.Qt.AlignCenter)
        self.registr_label.setOpenExternalLinks(True)
        self.registr_label.setObjectName("registr_label")
        self.gridLayout.addWidget(self.registr_label, 0, 0, 1, 3)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.password_label.setText(_translate("Dialog", "Password:"))
        self.handle_label.setText(_translate("Dialog", "Handle:"))
        self.name_label.setText(_translate("Dialog", "Name:"))
        self.email_label.setText(_translate("Dialog", "E-Mail:"))
        self.name_corr.setText(_translate("Dialog", " "))
        self.handle_corr.setText(_translate("Dialog", " "))
        self.email_corr.setText(_translate("Dialog", " "))
        self.password.setText(_translate("Dialog", " "))
        self.ok_btn.setText(_translate("Dialog", "Ок"))
        self.registr_label.setText(_translate("Dialog", "Регистрация:"))


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 650)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: #334;\n"
                                 "color: #fff;")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setStyleSheet("border: 0;")
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sendersScrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.sendersScrollArea.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendersScrollArea.sizePolicy().hasHeightForWidth())
        self.sendersScrollArea.setSizePolicy(sizePolicy)
        self.sendersScrollArea.setMinimumSize(QtCore.QSize(100, 0))
        self.sendersScrollArea.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.sendersScrollArea.setFont(font)
        self.sendersScrollArea.setStyleSheet("margin: 0;\n"
                                             "border: 0;\n"
                                             "border-right: 1px solid #668;")
        self.sendersScrollArea.setWidgetResizable(True)
        self.sendersScrollArea.setObjectName("sendersScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 398, 648))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        self.scrollAreaWidgetContents.setFont(font)
        self.scrollAreaWidgetContents.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.scrollAreaWidgetContents.setStyleSheet("border: 0;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.top_panel_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_panel_2.sizePolicy().hasHeightForWidth())
        self.top_panel_2.setSizePolicy(sizePolicy)
        self.top_panel_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.top_panel_2.setStyleSheet("border: 0;\n"
                                       "border-radius: 0;")
        self.top_panel_2.setObjectName("top_panel_2")
        self.top_panel = QtWidgets.QHBoxLayout(self.top_panel_2)
        self.top_panel.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.top_panel.setContentsMargins(5, 5, 5, 5)
        self.top_panel.setSpacing(5)
        self.top_panel.setObjectName("top_panel")
        self.new_dialog_btn = QtWidgets.QPushButton(self.top_panel_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_dialog_btn.sizePolicy().hasHeightForWidth())
        self.new_dialog_btn.setSizePolicy(sizePolicy)
        self.new_dialog_btn.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.new_dialog_btn.setFont(font)
        self.new_dialog_btn.setStyleSheet("background-color: #222;\n"
                                          "border: 1px solid #333;\n"
                                          "border-radius: 10px;")
        self.new_dialog_btn.setObjectName("new_dialog_btn")
        self.top_panel.addWidget(self.new_dialog_btn)
        self.exit_btn = QtWidgets.QPushButton(self.top_panel_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_btn.sizePolicy().hasHeightForWidth())
        self.exit_btn.setSizePolicy(sizePolicy)
        self.exit_btn.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.exit_btn.setFont(font)
        self.exit_btn.setStyleSheet("background-color: #222;\n"
                                    "border: 1px solid #333;\n"
                                    "border-radius: 10px;")
        self.exit_btn.setObjectName("exit_btn")
        self.top_panel.addWidget(self.exit_btn)
        self.verticalLayout_4.addWidget(self.top_panel_2)
        self.senders_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.senders_2.setStyleSheet("border-width: 0;\n"
                                     "border-radius: 0;")
        self.senders_2.setObjectName("senders_2")
        self.senders = QtWidgets.QGridLayout(self.senders_2)
        self.senders.setContentsMargins(0, 0, 0, 0)
        self.senders.setSpacing(0)
        self.senders.setObjectName("senders")
        self.verticalLayout_4.addWidget(self.senders_2)
        self.sendersScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.sendersScrollArea)
        self.message_panel = QtWidgets.QWidget(self.centralWidget)
        self.message_panel.setAutoFillBackground(False)
        self.message_panel.setStyleSheet("border: 0;")
        self.message_panel.setObjectName("message_panel")
        self.message_field = QtWidgets.QGridLayout(self.message_panel)
        self.message_field.setContentsMargins(0, 0, 0, 0)
        self.message_field.setSpacing(0)
        self.message_field.setObjectName("message_field")
        self.messangesScrollArea = QtWidgets.QScrollArea(self.message_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messangesScrollArea.sizePolicy().hasHeightForWidth())
        self.messangesScrollArea.setSizePolicy(sizePolicy)
        self.messangesScrollArea.setStyleSheet("border: 0")
        self.messangesScrollArea.setWidgetResizable(True)
        self.messangesScrollArea.setObjectName("messangesScrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 600, 530))
        self.scrollAreaWidgetContents_2.setStyleSheet("border: 0;")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messages_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.messages_2.setStyleSheet("border: 0;")
        self.messages_2.setObjectName("messages_2")
        self.messages = QtWidgets.QGridLayout(self.messages_2)
        self.messages.setContentsMargins(11, 11, 11, 11)
        self.messages.setSpacing(0)
        self.messages.setObjectName("messages")
        self.verticalLayout.addWidget(self.messages_2)
        self.messangesScrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.message_field.addWidget(self.messangesScrollArea, 1, 0, 1, 1)
        self.info_panel = QtWidgets.QWidget(self.message_panel)
        self.info_panel.setMaximumSize(QtCore.QSize(16777215, 50))
        self.info_panel.setStyleSheet("border-bottom: 1px solid #668;")
        self.info_panel.setObjectName("info_panel")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.info_panel)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.message_field.addWidget(self.info_panel, 0, 0, 1, 1)
        self.send_message_panel = QtWidgets.QWidget(self.message_panel)
        self.send_message_panel.setMaximumSize(QtCore.QSize(16777215, 70))
        self.send_message_panel.setStyleSheet("border: 0;\n"
                                              "border-top: 1px solid #668;")
        self.send_message_panel.setObjectName("send_message_panel")
        self.do_messange = QtWidgets.QHBoxLayout(self.send_message_panel)
        self.do_messange.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.do_messange.setContentsMargins(0, 0, 0, 0)
        self.do_messange.setSpacing(0)
        self.do_messange.setObjectName("do_messange")
        self.messange_input = QtWidgets.QLineEdit(self.send_message_panel)
        self.messange_input.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(25)
        self.messange_input.setFont(font)
        self.messange_input.setStyleSheet("margin: 10px;\n"
                                          "background-color: #555;\n"
                                          "border: 1px solid #444;\n"
                                          "border-radius: 10px")
        self.messange_input.setObjectName("messange_input")
        self.do_messange.addWidget(self.messange_input)
        self.message_send_button = QtWidgets.QPushButton(self.send_message_panel)
        self.message_send_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        self.message_send_button.setFont(font)
        self.message_send_button.setStyleSheet("background-image: url(\"icons/send_icon.png\");\n"
                                               "/*background-color: #334;*/\n"
                                               "border: 0;\n"
                                               "border-radius: 10px;\n"
                                               "padding: 0 10px;\n"
                                               "margin: 0 5px;")
        self.message_send_button.setObjectName("message_send_button")
        self.do_messange.addWidget(self.message_send_button)
        self.message_field.addWidget(self.send_message_panel, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.message_panel)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Messenger"))
        self.new_dialog_btn.setText(_translate("MainWindow", "Начать новый диалог"))
        self.exit_btn.setText(_translate("MainWindow", "Выход"))
        self.message_send_button.setText(_translate("MainWindow", "Отправить"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionReset.setShortcut(_translate("MainWindow", "Ctrl+R"))


def synchronization_server(handle, token, senders, dialogs, names_of_users):
    def get_senders():
        from get_senders_server import get_senders_server
        return get_senders_server(handle, token)

    def get_name_from_handle(handle):
        return names_of_users[handle]

    def get_dialog(sender):
        from get_messages_server import get_messages_server
        from Message import Message
        return [Message(message[2], get_name_from_handle(message[0]), message[3]) for message in
                get_messages_server(handle, sender, token)['result']]

    new_senders = get_senders()

    something_new = bool(set(senders) != set(new_senders))
    senders = new_senders
    for sender in senders:
        old_dialog = dialogs[sender] if sender in dialogs else []
        new_dialog = get_dialog(sender)
        if not old_dialog or old_dialog[-1] != new_dialog[-1]:
            something_new = True
            dialogs[sender] = new_dialog

    return something_new, new_senders, dialogs


def refactor_message(message):
    n = 30
    ans = ''
    for i in range(len(message) // n + 1):
        ans += message[i * n:(i + 1) * n] + '\n'
    return ans.rstrip()


def check_handle(handle):
    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/check_handle.php', data=data)

    answer = json.loads(response.text)

    return answer['res']


def check_message(message):
    return 0 < len(message) < 500


def send_message_server(from_handle, token, to_handle, text):
    if not text:
        return
    print(from_handle, token, to_handle, text.rstrip())
    data = {'from_handle': from_handle, 'token': token, 'to_handle': to_handle, 'text': text}
    response = requests.post('https://tim-ur.ru/yandex/send_message.php', data=data)

    answer = json.loads(response.text)

    print(answer)


def get_name_from_handle_server(handle):
    data = {'handle': handle}
    response = requests.post('https://tim-ur.ru/yandex/get_info.php', data=data)

    answer = json.loads(response.text)

    return answer['res']['name']


def get_senders_server(handle, token):
    data = {'handle': handle, 'token': token}
    response = requests.post('https://tim-ur.ru/yandex/get_message_list.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer.keys() if answer else []


def get_messages_server(handle, to_handle, token):
    data = {'handle': handle, 'token': token, 'to_handle': to_handle}
    response = requests.post('https://tim-ur.ru/yandex/get_messages.php', data=data)

    answer = json.loads(response.text)

    return answer


def login_request(handle, password):
    data = {'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/login.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer


def generate_password(m):
    """
    Функция генерирования стандартного пароля высокой сложности
    :param m: длина пароля
    :return: пароль высокой сложности
    """
    from random import choice

    maybe = []
    maybe.extend('qwertyupasdifghjkzxcvbnmQWERTYUPASDIFGHJKZXCVBNM0123456789')
    vv = []
    if m <= 56:
        while 1:
            for _ in range(m):
                f = True
                i = 0
                while 1:
                    i += 1
                    s = choice(maybe)
                    if s not in vv:
                        break
                    if i > 2 * m:
                        vv = []
                        f = False
                        break
                vv.append(s)
                if not f:
                    break
            vv = ''.join(vv)
            if m >= 3:
                if [True for _ in vv if _ in 'qwertyulpasdfghjkzxcvbnm'.upper()]:
                    if [True for _ in vv if _ in 'qwertyulpasdfghjkzxcvbnm']:
                        if [True for _ in vv if _ in '0123456789']:
                            return ''.join(vv)
                        else:
                            vv = []
                    else:
                        vv = []
                else:
                    vv = []
            else:
                return ''.join(vv)
    else:
        while 1:
            for _ in range(m):
                s = choice(maybe)
                vv.append(s)
            vv = ''.join(vv)
            if [True for _ in vv if _ in 'qwertyulpasdfghjkzxcvbnm'.upper()]:
                if [True for _ in vv if _ in 'qwertyulpasdfghjkzxcvbnm']:
                    if [True for _ in vv if _ in '23456789']:
                        return ''.join(vv)
                    else:
                        vv = []
                else:
                    vv = []
            else:
                vv = []


class Message:
    def __init__(self, text, sender, int_time=None):
        self.sender = sender
        self.text = text
        self.int_time = int(int_time) if int_time else floor(time())
        self.time = ctime(self.int_time)

    def __eq__(self, other):
        return self.sender == other.sender and \
               self.text == other.text and abs(self.int_time - other.int_time) <= 3

    def text_to_show(self):
        text = f'{self.sender} ({self.time}):\n{self.text}'
        label = QLabel(text)
        label.setStyleSheet(MESSAGE_STYLE)
        label.setFixedSize(label.sizeHint())
        return label


def registration_request(email, name, handle, password):
    data = {'email': email, 'name': name, 'handle': handle, 'password': password}
    response = requests.post('https://tim-ur.ru/yandex/register_user.php', data=data)

    answer = json.loads(response.text)

    print(answer)

    return answer


def check_password(password):
    return 5 <= len(password) <= 30 and \
           all(_ in 'qwertyupasdifghjkzxcvbnmQWERTYUPASDIFGHJKZXCVBNM0123456789' for _ in password)


def send_email(name, acc_login, acc_password, toAdr):
    login = 'yourmesseger@yandex.ru'
    password = 'passwordforyandex111'
    server = 'imap.yandex.ru'
    mail = imaplib.IMAP4_SSL(server)
    mail.login(login, password)
    SMTPserver = 'smtp.' + ".".join(server.split('.')[1:])

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()  # Создаём прототип сообщения
    msg['From'] = login
    msg['To'] = toAdr
    msg['Subject'] = 'Регистрация в Messenger'

    body = f'''{name}, поздравляем!!!
Регистрция в Messenger прошла успешно.
Ваш логин: {acc_login}
Ваш пароль: {acc_password}'''
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTPserver, 587)  # отправляем
    server.starttls()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(login, toAdr, text)
    server.quit()


class MainWindow(QMainWindow, UiMainWindow):
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
        self.last_synchronization_time = time()

        self.setMouseTracking(True)

        self.initUI()

        self.start()

    def initUI(self):
        self.setupUi(self)

        self.message_send_button.clicked.connect(self.send_message)

        self.exit_btn.clicked.connect(self.exit_user)

        self.new_dialog_btn.clicked.connect(self.start_new_dialog)

        self.restyle()

    def restyle(self):
        self.setStyleSheet(BACKGROUND_STYLE)
        self.message_send_button.setStyleSheet(MESSAGE_SEND_BTN_STYLE)

    def keyPressEvent(self, event):
        if time() - self.last_synchronization_time > SYNCHRONIZATION_TIME:
            self.synchronization()
            self.last_synchronization_time = time()
        if event.key() == Qt.Key_Enter:
            self.send_message()
        if event.key() == Qt.Key_Return:
            self.send_message()

    def mouseMoveEvent(self, event):
        if time() - self.last_synchronization_time > 1:
            self.synchronization()
            self.last_synchronization_time = time()

    def synchronization(self):
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
        if message.sender == self.names_of_users[self.handle]:
            self.messages.addWidget(message.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignRight)

        else:
            self.messages.addWidget(message.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignLeft)
        self.messages_number += 1

        self.scroll_message_bar(2)

    def show_new_user(self, user):
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
        k = lambda l: -self.dialogs[l][-1].int_time if l in self.dialogs and self.dialogs[l] else 0
        self.handles_of_users.sort(key=k)
        # self.scroll_senders_bar()

    def start(self):
        self.clear_users()
        self.sort_users()
        for i in range(self.number_of_users):
            self.show_new_user(self.handles_of_users[i])
        self.scroll_senders_bar()

    def start_new_dialog(self):
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
        open(DATA, 'w')
        self.close()
        exit(0)


class RegistrationWindow(QDialog, UiRegistrationWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.ok_btn.clicked.connect(self.run)
        self.password_text.setText(generate_password(15))

    def run(self):
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


class LoginWindow(QDialog, UiLoginWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.run)
        self.registr_btn.clicked.connect(self.registration)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        # self.handle_text.setText('admin')
        # self.password_text.setText('admin')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.run()
        if event.key() == Qt.Key_Return:
            self.run()

    def run(self):
        handle = self.handle_text.text()
        password = self.password_text.text()
        if check_handle(handle):
            self.handle_corr.setText('Incorrect')
            self.handle_corr.setStyleSheet('color: red')
        else:
            self.handle_corr.setText('')

        if not check_password(password):
            self.password_corr.setText('Incorrect')
            self.password_corr.setStyleSheet('color: red')
        else:
            self.password_corr.setText('')
        answer = login_request(handle, password)
        if 'Error' not in answer:
            print(handle, password, answer['token'])
            self.save(handle, password, answer['token'])
            self.close()
        else:
            if 'handle' in answer['Error']:
                self.handle_corr.setText('Incorrect')
                self.handle_corr.setStyleSheet('color: red')
            else:
                self.password_corr.setText('Incorrect')
                self.password_corr.setStyleSheet('color: red')

    def registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.setWindowModality(Qt.ApplicationModal)
        self.registration_window.show()

    def save(self, handle, password, token):
        with open(DATA, 'w', encoding="utf8") as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([handle, password, token, self.remember_btn.isChecked()])


def start_ui(users_handles, users_names, dialogs, handle, token, remember):
    try:
        app = QApplication(sys.argv)
        ex = MainWindow(users_handles, users_names, dialogs, handle, token)
        ex.show()
        sys.exit(app.exec_())
    finally:
        if remember == 'False':
            open(DATA, 'w')


def login_main():
    app = QApplication(sys.argv)
    ex = LoginWindow()
    ex.open()
    if app.exec_():
        return


def main():
    with open(DATA, encoding="utf8") as file:
        reader = list(csv.reader(file, delimiter=';', quotechar='"'))
        reader = reader[0] if reader else []
        data = reader
        if len(data) < 4:
            login = ''
            password = ''
            token = ''
            remember = False
        else:
            login, password, token, remember = data

    if login and password:
        token = login_request(login, password)['token']
    else:
        login_main()
        # os.startfile('main_login.pyw')

    with open(DATA, encoding="utf8") as file:
        reader = list(csv.reader(file, delimiter=';', quotechar='"'))
        reader = reader[0] if reader else []
        data = reader
        print(data)
        if len(data) < 4:
            exit(228)
        else:
            login, password, token, remember = data

    # with open('C:/Program Files (x86)/Messenger/data.py') as file:
    #     data = file.read().split('\n')

    users_handles = list(get_senders_server(login, token))
    if login not in users_handles:
        users_handles.append(login)

    users_names = dict()

    for handle in users_handles:
        users_names[handle] = get_name_from_handle_server(handle)

    dialogs = dict()
    for sender in users_handles:
        dialog = get_messages_server(login, sender, token)['result']
        for message in dialog:
            if sender not in dialogs:
                dialogs[sender] = [Message(message[2], users_names[message[0]], message[3])]
            else:
                dialogs[sender].append(Message(message[2], users_names[message[0]], message[3]))
        if not dialog:
            dialogs[sender] = []

    start_ui(users_handles, users_names, dialogs, login, token, remember)


if __name__ == '__main__':
    main()
