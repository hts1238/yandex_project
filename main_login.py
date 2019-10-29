import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from LoginWindow import LoginWindow

app = QApplication(sys.argv)
ex = LoginWindow()
ex.open()
sys.exit(app.exec_())
