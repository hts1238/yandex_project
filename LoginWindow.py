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
        self.close()

    def registration(self):
        pass

# app = QApplication(sys.argv)
# ex = LoginWindow()
# ex.show()
# sys.exit(app.exec_())
