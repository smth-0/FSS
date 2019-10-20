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


