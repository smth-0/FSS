from PyQt5 import QtGui
from PyQt5.QtWidgets import QTextEdit, QFileDialog
from PyQt5.QtWidgets import QWidget, QPushButton

import GlobalVariables as GB
import UtilityClasses
import UtilityFunctions as UF
from AboutForm import AboutForm


class SettingsForm(QWidget):
    """It's settings window of FSS program. updateUI can update UI items on QWidget of this window"""
    def __init__(self):
        super().__init__()

        self.aboutForm = AboutForm()

        self.saveButton = QPushButton(self)
        self.pathButton = QPushButton(self)

        self.pathLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'saving path:',
                                                        [200, 25], [70, 140], self)
        self.sharingCodeLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'your sharing code:',
                                                               [250, 50], [70, 50], self)

        self.savePath = GB.savePath
        self.initUI()

    def initUI(self):
        self.resize(*GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME + ' Settings')
        self.sharingCodeLabel.field.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sharingCodeLabel.field.setFont(font)
        self.sharingCodeLabel.field.setText(UF.convertCode(UF.getIP(), False))

        self.pathButton.action = 'browse'
        self.pathButton.setText('browse')
        self.pathButton.resize(60, 25)
        self.pathButton.move(270, 140)
        self.pathButton.clicked.connect(self.onClick)

        self.saveButton.action = 'save'
        self.saveButton.setText('apply')
        self.saveButton.resize(60, 25)
        self.saveButton.move(GB.WINDOW_SIZE[0] // 2 - 30, GB.WINDOW_SIZE[1] - 30)
        self.saveButton.clicked.connect(self.onClick)

        self.aboutButton = QPushButton(self)
        self.aboutButton.setText('about')
        self.aboutButton.action = 'about'
        self.aboutButton.move(10, GB.WINDOW_SIZE[1] - 30)
        self.aboutButton.resize(60, 25)
        self.aboutButton.setFlat(True)
        self.aboutButton.clicked.connect(self.onClick)

        self.updateUI()
        UF.debugOutput('successfully initialized UI of settings form')

    def updateUI(self):
        self.pathLabel.field.setText(self.savePath)
        self.saveButton.setDisabled(GB.savePath == self.savePath)

    def onClick(self):
        if self.sender().action == 'browse':
            path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if path:
                self.savePath = path
        if self.sender().action == 'save':
            GB.savePath = self.savePath
            # todo: here at is saving of setings
            self.close()
        if self.sender().action == 'about':
            self.aboutForm.show()
        self.updateUI()
