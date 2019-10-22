from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QTextEdit, QFileDialog

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QLabel

import GlobalVariables as GB
import UtilityClasses


class SettingsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(*GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME + ' Settings')

        self.sharingCoreLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'your sharing code:',
                                                               [250, 50], [70, 50], self)
        self.sharingCoreLabel.field.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sharingCoreLabel.field.setFont(font)
        self.sharingCoreLabel.field.setText(UtilityClasses.convertCode(UtilityClasses.getIP(), False))

        self.pathLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'saving path:',
                                                        [200, 25], [70, 160], self)
        self.pathButton = QPushButton(self)
        self.pathButton.action = 'browse'
        self.pathButton.setText('browse')
        self.pathButton.resize(60, 25)
        self.pathButton.move(270, 160)
        self.pathButton.clicked.connect(self.onClick)



        self.updateUI()

    def updateUI(self):
        self.pathLabel.field.setText(GB.savePath)

    def onClick(self):
        if self.sender().action == 'browse':
            path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if path:
                GB.savePath = path
        self.updateUI()
