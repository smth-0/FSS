import os
import socket

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog, QProgressBar

import GlobalVariables as GB
import UtilityClasses as UC
import UtilityFunctions as UF



class ReceiveForm(QWidget):
    def __init__(self):
        super().__init__()

        self.progressBar = QProgressBar(self)
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
        self.setGeometry(500, 500, GB.WINDOW_SIZE[0], GB.WINDOW_SIZE[1] * 1.5)
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

        self.progressBar.setGeometry(70, 370, 250, 30)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.updateUI()
        UF.debugOutput('successfully initialized UI of receive form')

    def updateUI(self):
        self.pathLabel.field.setText(self.savePath)
        if self.readyFlag:
            self.readyButton.setText('ready to connect!')
            while True:
                if self.receiveFile():
                    UF.okDialog('Successfully received the file.')
                    break
                else:
                    if not UF.okDialog('Failed to receive the file. Press ok to try again.'):
                        break
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

    def receiveFile(self):
        UF.debugOutput('ready flag out, building receiver')
        try:
            # opening connection
            sock = socket.socket()
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((GB.myIP, GB.RES_SOCKET_PORT))

            sock.listen(True)
            conn, incomeIP = sock.accept()
        except Exception as e:
            UF.debugOutput('failed to connect properly aborting; stack:', e)
            try:
                conn.close()
                sock.close()
            except Exception as ee:
                UF.debugOutput('connection established but in wrong method. stack:', ee)
            return False

        # receiving filename of file
        try:
            receivedFilename = UF.sockProtocolConverter(conn.recv(255))
        except Exception as e:
            UF.debugOutput('failed to receive filename. aborting connect. stack:', e)
            conn.close()
            sock.close()
            return False

        # receiving length of file
        try:
            receivedLengthOfFile = int(UF.sockProtocolConverter(conn.recv(255)))
        except Exception as e:
            UF.debugOutput('failed to receive file length. aborting connect. stack:', e)
            conn.close()
            sock.close()
            return False

        try:
            fileEntry = open(receivedFilename, 'w+b')  # open in binary
        except Exception as e:
            UF.debugOutput('failed to create file. aborting connection. stack:', e)
            conn.close()
            sock.close()
            return False

        # receiving head of the file
        try:
            filePart = conn.recv(4096)
            fileEntry.write(filePart)
        except Exception as e:
            UF.debugOutput('failed to receive header of file. aborting connect. stack:', e)
            conn.close()
            sock.close()
            return False

        try:
            while filePart:
                fileEntry.write(filePart)
                self.updateUI()
                filePart = conn.recv(1024)
        except Exception as e:
            UF.debugOutput('failed to receive file after header. aborting connection. stack:', e)
            conn.close()
            sock.close()
            return False
        finally:
            UF.debugOutput('successfully received the file named ', receivedFilename, ' to ', GB.savePath + receivedFilename, ' from ',
                           incomeIP, ' file length should be ', receivedLengthOfFile, ' but received ',
                           UF.fileSize(GB.savePath + r'/' + receivedFilename))

        conn.close()
        sock.close()

        fileEntry.close()
        os.replace(receivedFilename, self.savePath + r'/' + receivedFilename)
        return UF.fileSize(GB.savePath + r'/' + receivedFilename) == receivedLengthOfFile
