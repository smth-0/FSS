from PyQt5.QtWidgets import QWidget

import GlobalVariables as GB


class ReceiveForm(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setGeometry(GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME)
