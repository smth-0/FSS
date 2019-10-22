import socket
import sys

from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QApplication, QInputDialog, QLineEdit


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.calcButton = QPushButton(self)
        self.path = ''
        self.chooseButton = QPushButton(self)
        self.initUI()

    def initUI(self):
        try:
            self.setGeometry(200, 200, 300, 100)
            self.setWindowTitle(repr(self))
            self.chooseButton.resize(300, 50)
            self.chooseButton.move(0, 0)
            self.chooseButton.setText("click here to choose the file")
            self.chooseButton.clicked.connect(self.selectFile)

            self.calcButton.resize(300, 50)
            self.calcButton.move(0, 50)
            self.calcButton.setText("click here after")
            self.calcButton.clicked.connect(self.send)
        except Exception:
            e = sys.exc_info()
            print(e)

    def selectFile(self):
        try:
            self.path = QFileDialog.getOpenFileName()[0]
            self.chooseButton.setText(self.path)
            self.calcButton.setText("click here")
        except Exception:
            e = sys.exc_info()
            print(e)

    def send(self):
        s = socket.socket()
        sip = self.getText()
        print(1, sip)
        sip = sip.split()
        print(2, sip)
        sip2 = []
        for i in sip:
            print('>', int(''.join(['0x', i]), 16))
            sip2.append(str(int(''.join(['0x', i]), 16)))
            print('>>', i)
        print(3, sip)
        ip = '.'.join(sip2)
        print(4, ip)
        s.connect((ip, 9999))
        f = open(self.path, "rb")
        l = f.read(1024)
        while l:
            s.send(l)
            l = f.read(1024)
        s.close()

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get IP", "Your code:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

app = QApplication([])
form = ImageViewer()
form.show()
sys.exit(app.exec())
