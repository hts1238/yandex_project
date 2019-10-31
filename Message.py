from PyQt5.QtWidgets import QLabel
from time import asctime, time


class Message:
    def __init__(self, text, sender='Вы'):
        self.sender = sender
        self.time = asctime()
        self.text = (text + '\n')
        self.int_time = time()

    def text_to_show(self):
        text = f'{self.sender} ({self.time}):\n{self.text}'
        label = QLabel(text)
        # if self.sender == 'Вы':
        #     label.setStyleSheet('font-size: 25px; color: black')
        # else:
        label.setStyleSheet('''
        font-size: 25px;
        color: black;
        background-color: #BED6FF;
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: white''')
        return label
