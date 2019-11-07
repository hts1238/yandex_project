import PyQt5
from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

error_dialog = QtWidgets.QErrorMessage()
error_dialog.showMessage('Oh no!')

app.exec_()