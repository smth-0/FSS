from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel

import GlobalVariables as GB
import UtilityClasses as UC
import UtilityFunctions as UF


class ReceiveForm(QWidget):
    def __init__(self):
        super().__init__()
        self.statusLabel = QLabel(parent=self, text='connection status: ')
        self.sharingCoreLabel = UC.QInputWithLabel(QTextEdit(self), 'your sharing code:',
                                                   [250, 50], [70, 50], self)

        self.status = ''

        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, *GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME)

        self.sharingCoreLabel.field.setReadOnly(True)

        font = QtGui.QFont()
        font.setPointSize(16)

        self.sharingCoreLabel.field.setFont(font)
        self.sharingCoreLabel.field.setText(UF.convertCode(UF.getIP(), False))

        self.statusLabel.setGeometry(70, 100, 250, 50)

        self.updateUI()

    def updateUI(self):
        self.statusLabel.setText('connection status: ' + self.status)
