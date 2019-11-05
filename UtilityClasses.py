from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QAbstractButton

import GlobalVariables as GB
import UtilityFunctions


class QInputWithLabel:
    def __init__(self, input_field, q_label_text, element_size, pos, layout_self):
        self.pos, self.element_size, self.layout_self = list(pos), list(element_size), layout_self
        self.field = input_field
        self.field.resize(*element_size)
        self.field.move(*pos)

        self.q_label = QLabel(layout_self)
        self.q_label.move(pos[0], pos[1] - element_size[1])
        self.q_label.setText(q_label_text)
        self.q_label.resize(*element_size)

    def copy(self):
        return QInputWithLabel(self.field, self.q_label.text(),
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


class UtilitySettingsFileManager:
    """
    this class is for fast and easy encapsulated input-output of settings to file
    """

    def save(self):
        try:
            fileEntry = open(GB.RES_DB_SETTINGS, 'w+')
            fileEntry.write(GB.savePath)
        except Exception as e:
            UtilityFunctions.debugOutput('failed to read from settings.txt. stack:', e)
            return
        finally:
            UtilityFunctions.debugOutput('successfully loaded settings')

    def load(self):
        try:
            fileEntry = open(GB.RES_DB_SETTINGS, 'r')
            sett = ''.join(fileEntry.readlines())
            UtilityFunctions.debugOutput('read ', sett, ' from file of settings')
            GB.savePath = sett
            UtilityFunctions.debugOutput('loaded settings from file. now GB.savePath = ', GB.savePath)

        except Exception as e:
            UtilityFunctions.debugOutput('failed to read from settings.txt. creating it. stack:', e)
            # fileEntry = open(GB.RES_DB_SETTINGS, 'w+')
            GB.savePath = UtilityFunctions.get_download_path()
            # fileEntry.close()
            return
        finally:
            UtilityFunctions.debugOutput('successfully loaded settings')
