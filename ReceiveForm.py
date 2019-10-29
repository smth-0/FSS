from socket import socket

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog

import GlobalVariables as GB
import UtilityClasses as UC
import UtilityFunctions as UF



class ReceiveForm(QWidget):
    def __init__(self):
        super().__init__()

        self.savePath = GB.savePath
        self.readyFlag = False

        self.sharingCodeLabel = UC.QInputWithLabel(QTextEdit(self), 'your sharing code:',
                                                   [250, 50], [70, 50], self)
        self.pathLabel = UC.QInputWithLabel(QTextEdit(self), 'saving path:',
                                            [200, 25], [70, 130], self)

        self.pathButton = QPushButton(self)
        self.readyButton = QPushButton(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, *GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME)

        self.sharingCodeLabel.field.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.sharingCodeLabel.field.setFont(font)
        self.sharingCodeLabel.field.setText(UF.convertCode(UF.getIP(), False))

        self.pathButton.action = 'browse'
        self.pathButton.setText('browse')
        self.pathButton.setGeometry(270, 130, 60, 25)
        self.pathButton.clicked.connect(self.onClick)

        self.readyButton.setGeometry(70, 160, 260, 30)
        self.readyButton.action = 'ready'
        self.readyButton.clicked.connect(self.onClick)

        self.updateUI()
        UF.debugOutput('successfully initialized UI of receive form')

    def updateUI(self):
        self.pathLabel.field.setText(self.savePath)
        if self.readyFlag:
            self.readyButton.setText('ready to connect!')
            self.onReady()
        else:
            self.readyButton.setText('be ready!')

    def onClick(self):
        UF.debugOutput('click:', self.sender().action)
        if self.sender().action == 'browse':
            path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            if path:
                self.savePath = path
                UF.debugOutput('set output location to ', self.savePath)
                self.updateUI()
        if self.sender().action == 'ready':
            self.readyFlag = True
        self.updateUI()

    def onReady(self):
        UF.debugOutput('ready flag out, building receiver')

        # opening connection
        sock = socket()
        sock.bind((GB.myIP, 9999))
        sock.listen(True)
        conn, incomeIP = sock.accept()

        # receiving filename of file
        try:
            receivedFilename = UF.sockProtocolConverter(conn.recv(255))
        except Exception as e:
            UF.debugOutput('failed to receive filename. aborting connect. stack:', e)
            conn.close()
            return False

        # receiving length of file
        try:
            receivedLengthOfFile = int(UF.sockProtocolConverter(conn.recv(255)))
        except Exception as e:
            UF.debugOutput('failed to receive file length. aborting connect. stack:', e)
            conn.close()
            return False

        # receiving head of the file
        try:
            filePart = conn.recv(2048)
        except Exception as e:
            UF.debugOutput('failed to receive header of file. aborting connect. stack:', e)
            conn.close()
            return False

        try:
            fileEntry = open(receivedFilename, 'wb')  # open in binary
        except Exception as e:
            UF.debugOutput('failed to create file. aborting connection. stack:', e)
            conn.close()
            return False

        try:
            while filePart:
                fileEntry.write(filePart)
                filePart = conn.recv(1024)
        except Exception as e:
            UF.debugOutput('failed to receive file after header. aborting connection. stack:', e)
            conn.close()
            return False
        finally:
            UF.debugOutput('successfully received the file named ', receivedFilename, ' from ', incomeIP)

        fileEntry.close()

        return UF.fileSize(receivedFilename) == receivedLengthOfFile
