import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QAbstractButton


class QInputWithLabel:
    def __init__(self, input_field, qlabel_text, element_size, pos, layout_self):
        self.pos, self.element_size, self.layout_self = list(pos), list(element_size), layout_self
        self.field = input_field
        self.field.resize(*element_size)
        self.field.move(*pos)

        self.qlabel = QLabel(layout_self)
        self.qlabel.move(pos[0], pos[1] - element_size[1])
        self.qlabel.setText(qlabel_text)
        self.qlabel.resize(*element_size)

    def copy(self):
        return QInputWithLabel(self.field, self.qlabel.text(),
                               (*self.element_size,), (*self.pos,), self.layout_self)


class QPicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, parent=None):
        super(QPicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_hover

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def getIP():
    import socket
    return socket.gethostbyname(socket.gethostname())


def convertCode(code, isHex):
    # converts connect code into IP and back
    # hex code looks like "XX#XX#XX#XX"
    # decimal code looks like ipv4 IP "XXX.XXX.XXX.XXX"
    # (c) Lunar
    sepSymbol = ':'
    return '.'.join([str(int('0x' + i, 16)) for i in code.split(sepSymbol)]) \
        if isHex else sepSymbol.join([hex(int(i)).lstrip('0x') for i in code.split('.')])
