import sys
from PyQt5.QtWidgets import QApplication
from LoginWindow import LoginWindow

"""
Запуск процесса авторизции пользователя
"""

app = QApplication(sys.argv)
ex = LoginWindow()
ex.open()
sys.exit(app.exec_())
