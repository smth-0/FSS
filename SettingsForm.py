from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel
import GlobalVariables as GB
import UtilityClasses


class SettingsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(GB.WINDOW_SIZE)