from PyQt5.QtWidgets import QLabel
from time import asctime, time


class Message:
    def __init__(self, text, sender, int_time=time()):
        self.sender = sender
        self.time = asctime()  # Надо переделать
        self.text = text
        self.int_time = int(int_time)

    def text_to_show(self):
        text = f'{self.sender} ({self.time}):\n{self.text}'
        label = QLabel(text)
        label.setStyleSheet('''
        font-size: 25px;
        color: black;
        background-color: #BED6FF;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: white''')
        label.setMaximumSize(500, 100)
        return label
