from PyQt5.QtWidgets import QLabel
from time import time, ctime
from math import floor
from style import MESSAGE_STYLE


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
