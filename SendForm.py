import socket
import threading

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QLabel, QFileDialog, QProgressBar

import GlobalVariables as GB
import UtilityClasses
import UtilityFunctions as UF


class SendForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ipAddress = ''

        self.sendButton = QPushButton(parent=self, text='send')

        self.pathButton = QPushButton(parent=self, text='browse')
        self.pathLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'file or files to send:',
                                                        [200, 25], [70, 200], self)
        self.path = ''
        self.fileNames = []
        self.exampleLabel = QLabel(self)
        self.applyAddressButton = QPushButton(self)
        self.sharingCoreLabel = UtilityClasses.QInputWithLabel(QTextEdit(self), 'your sharing code:',
                                                               [250, 50], [70, 65], self)
        self.isCorrectAddress = False
        self.sendFunc = self.sendFileLegacy if GB.isLegacyMode else self.sendFile()
        self.ThFunc = threading.Thread(target=self.sendFIleThreaded, daemon=True)
        self.initUI()
        UF.debugOutput('successfully initialized UI of sending form')

    def initUI(self):
        self.setGeometry(500, 500, GB.WINDOW_SIZE[0], GB.WINDOW_SIZE[1] * 2)
        self.setWindowTitle(GB.WINDOW_NAME)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.sharingCoreLabel.field.setFont(font)

        self.applyAddressButton.action = 'applyAddress'
        self.applyAddressButton.move(70, 125)
        self.applyAddressButton.resize(250, 30)
        self.applyAddressButton.setText('apply')
        self.applyAddressButton.clicked.connect(self.onClick)

        self.exampleLabel.setText('example: c0:a8:1f:7')
        self.exampleLabel.move(70, 20)
        self.exampleLabel.resize(250, 10)

        self.pathButton.action = 'browse'
        self.pathButton.resize(50, 25)
        self.pathButton.move(270, 200)
        self.pathButton.clicked.connect(self.onClick)

        self.sendButton.action = 'send'
        self.sendButton.resize(250, 25)
        self.sendButton.move(70, 240)
        self.sendButton.clicked.connect(self.onClick)

        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(70, 280, 250, 30)
        self.progressBar.setMaximum(100)

        self.updateUI()

    def updateUI(self):
        self.applyAddressButton.setDisabled(self.isCorrectAddress)
        self.sharingCoreLabel.field.setReadOnly(self.isCorrectAddress)
        self.pathButton.setDisabled(not self.isCorrectAddress)
        self.pathLabel.field.setDisabled(not self.isCorrectAddress)
        self.sendButton.setDisabled(not self.isCorrectAddress)

        self.pathLabel.field.setText(', '.join(self.fileNames))

        UF.debugOutput('successfully updated UI of send form')

    def onClick(self):
        UF.debugOutput('click:', self.sender().action)
        try:
            if self.sender().action == 'applyAddress':

                self.isCorrectAddress = UF.checkAddress(self.sharingCoreLabel.field.toPlainText())

                if self.sharingCoreLabel.field.toPlainText() == UF.convertCode(UF.getIP(), False):
                    self.isCorrectAddress = UF.okDialog(
                        'you trying to set your address as target. press ok to continue')

                if self.isCorrectAddress:
                    self.ipAddress = str(UF.convertCode(self.sharingCoreLabel.field.toPlainText(), is_hex=True))

                    UF.debugOutput('set address to', self.ipAddress)
                else:
                    self.sharingCoreLabel.q_label.setText(
                        self.sharingCoreLabel.q_label.text() + ' wrong syntax of sharing code')

                if GB.isDebugEnabled:
                    UF.debugOutput('address verification now is:', self.isCorrectAddress)

            if self.sender().action == 'browse':
                path = QFileDialog.getOpenFileNames(self, 'select file or folder')[0]
                UF.debugOutput('received ', path, 'from QFileDialog.')
                if len(path) == 1:
                    self.path = path

                    UF.debugOutput('set path to', self.path)
                elif len(path) > 1:
                    if UF.okDialog('do you really want to select multiple files(or folder), is it ok?'):
                        zip_path = UF.makeZIP(path)
                        if zip_path:
                            self.path = zip_path
                        UF.debugOutput('set path to local tmp zip file')
                self.fileNames = [i.split('/')[-1] for i in path]

            if self.sender().action == 'send':
                if self.path:
                    while True:
                        if self.sendFileLegacy():
                            UF.okDialog('successfully sent the file!\nPress ok to continue.')
                            break
                        else:
                            if not UF.okDialog('Failed to send the file. Press ok to try again.'):
                                break
                else:
                    UF.okDialog('wrong path to file')

        except Exception as e:

            UF.debugOutput(e)
        self.updateUI()

    def sendFileLegacy(self):
        """
        ||| LEGACY |||
        this function takes self.path and self.ipAddress to get file and target's ip.
        """
        self.sendButton.setDisabled(True)
        UF.debugOutput('trying to send file')
        self.progressBar.setValue(0)
        socketObj = socket.socket()

        try:
            UF.debugOutput('trying connect to target', repr(self.ipAddress))
            socketObj.connect((self.ipAddress, 9999))
        except Exception as e:
            UF.debugOutput('failed to connect to', repr(self.ipAddress))
            return False

        try:
            UF.setStatus(self.setWindowTitle, 'sending...')
            currFile = open(self.path, "rb")

            # take extension of file and send it in 255 bytes
            fileName = self.path.split('/')[-1]
            socketObj.send((fileName + (' ' * (255 - len(fileName)))).encode('utf-8'))

            # take length of file and send it in 255 bytes
            fileLength = UF.fileSize(self.path)
            UF.debugOutput('trying to send file with length of ', [fileLength])
            socketObj.send((str(fileLength) + (' ' * (255 - len(str(fileLength))))).encode('utf-8'))
        except Exception as e:
            UF.debugOutput('failed to send metadata of file to', self.ipAddress, e)
            UF.setStatus(self.setWindowTitle, 'ERROR')
            return False
        try:
            # starting head of file
            sendingFilePart = currFile.read(2048)

            partCount = fileLength // 2048
            percentsSent = 0
            alreadySentCount = 1

            # the whole file after head
            while sendingFilePart:
                percentsSent = (2048 + 1024 * alreadySentCount) // fileLength * 100
                UF.debugOutput('sent ', percentsSent, ' already')
                self.progressBar.setValue(percentsSent)
                socketObj.send(sendingFilePart)
                sendingFilePart = currFile.read(1024)
                alreadySentCount += 1

            socketObj.close()
            UF.setStatus(self.setWindowTitle, 'sent')
            UF.debugOutput('successfully sent ', fileName, ' to ', self.ipAddress)
        except Exception as e:
            UF.debugOutput('failed to send file to', self.ipAddress, e)
            UF.setStatus(self.setWindowTitle, 'ERROR')
            return False

        self.isCorrectAddress = False

        self.updateUI()
        return True

    def sendFile(self):
        try:
            UF.debugOutput('starting sending thread')
            self.ThFunc.start()
            UF.debugOutput('started sending thread')
        except Exception as e:
            UF.debugOutput('failed to start sending thread. stack:', e)
            return False

    def sendFIleThreaded(self):
        """
        this function takes self.path and self.ipAddress to send actual file.
        """
        self.sendButton.setDisabled(True)
        UF.debugOutput('trying to send file')
        self.progressBar.setValue(0)
        socketObj = socket.socket()

        try:
            UF.debugOutput('trying connect to target', repr(self.ipAddress))
            socketObj.connect((self.ipAddress, 9999))

            socketObj.send(GB.TOKEN.encode('utf-8'))

            sock = socket.socket()
            sock.bind((GB.myIP, 9999))
            sock.listen(True)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            conn, incomeIP = sock.accept()
            filePart = conn.recv(1024)
            sock.close()
            conn.close()

        except Exception as e:
            UF.debugOutput('failed to connect to', repr(self.ipAddress))
            return False

        try:
            UF.setStatus(self.setWindowTitle, 'sending...')
            currFile = open(self.path, "rb")

            # take extension of file and send it in 255 bytes
            fileName = self.path.split('/')[-1]
            socketObj.send((fileName + (' ' * (255 - len(fileName)))).encode('utf-8'))

            # take length of file and send it in 255 bytes
            fileLength = UF.fileSize(self.path)
            UF.debugOutput('trying to send file with length of ', [fileLength])
            socketObj.send((str(fileLength) + (' ' * (255 - len(str(fileLength))))).encode('utf-8'))
        except Exception as e:
            UF.debugOutput('failed to send metadata of file to', self.ipAddress, e)
            UF.setStatus(self.setWindowTitle, 'ERROR')
            return False
        try:
            # starting head of file
            sendingFilePart = currFile.read(2048)

            partCount = fileLength // 2048
            percentsSent = 0
            alreadySentCount = 1

            # the whole file after head
            while sendingFilePart:
                percentsSent = (2048 + 1024 * alreadySentCount) // fileLength * 100
                UF.debugOutput('sent ', percentsSent, ' already')
                self.progressBar.setValue(percentsSent)
                socketObj.send(sendingFilePart)
                sendingFilePart = currFile.read(1024)
                alreadySentCount += 1

            socketObj.close()
            UF.setStatus(self.setWindowTitle, 'sent')
            UF.debugOutput('successfully sent ', fileName, ' to ', self.ipAddress)
        except Exception as e:
            UF.debugOutput('failed to send file to', self.ipAddress, e)
            UF.setStatus(self.setWindowTitle, 'ERROR')
            return False

        self.isCorrectAddress = False

        self.updateUI()
        return True
