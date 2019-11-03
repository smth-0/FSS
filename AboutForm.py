import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

import GlobalVariables as GB
import UtilityFunctions as UF


class AboutForm(QWidget):
    """
    this is form which tells user who created, debugged and managed all this code
    """

    def __init__(self):
        super().__init__()
        self.upperLabel = QLabel(parent=self, text='made with love.\nby Lunar')
        self.rightlabel = QLabel(parent=self, text='version: ' + GB.VERSION)
        self.picLabelOSLogo = QLabel(self)
        self.picLabelLunarLogo = QLabel(self)
        self.initUI()
        UF.debugOutput('successfully created About Form')

    def initUI(self):
        self.setWindowTitle(GB.WINDOW_NAME)
        self.setGeometry(200, 200, *GB.WINDOW_SIZE)

        self.upperLabel.move(10, 20)

        self.rightlabel.move(300, 150)

        self.picLabelOSLogo.setPixmap(
            QPixmap(UF.resource_path(
                './res/' + ('windowsLogo.png' if os.name == 'nt' else 'linuxLogo.png'))).scaled(100, 100))
        self.picLabelOSLogo.move(150, 20)
        self.picLabelOSLogo.resize(100, 100)

        self.picLabelLunarLogo.setPixmap(QPixmap(UF.resource_path('./res/LunarLogo.png')).scaled(100, 100))
        self.picLabelLunarLogo.move(20, 100)
        self.picLabelLunarLogo.resize(100, 100)
