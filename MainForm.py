# It's main "start" windows which launches first.
# it has 2 buttons (send/receive) and settings button.
# this thing actually should work fine always because it's really simple.
# (C) Lunar
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

import GlobalVariables as GB
import UtilityClasses
import UtilityFunctions as UF
from SendForm import SendForm
from SettingsForm import SettingsForm


class MainForm(QWidget):
    """its main window of QWidget which should start first. Requires res folder to be full and not corrupted to work
    properly. """

    def __init__(self):
        super().__init__()
        self.settingsForm = SettingsForm()
        self.sendForm = SendForm()
        # self.receiveForm = todo: here's receive form class creating, just btw
        try:
            self.downloadButton = UtilityClasses.QPicButton(QPixmap(GB.RES_BUTTON_DOWNLOAD),
                                                            QPixmap(GB.RES_BUTTON_DOWNLOAD_HOVERED), self)
            self.uploadButton = UtilityClasses.QPicButton(QPixmap(GB.RES_BUTTON_UPLOAD),
                                                          QPixmap(GB.RES_BUTTON_UPLOAD_HOVERED), self)
            self.settingsButton = UtilityClasses.QPicButton(QPixmap(GB.RES_BUTTON_SETTINGS),
                                                            QPixmap(GB.RES_BUTTON_SETTINGS_HOVERED), self)
        except Exception:
            UF.debugOutput(r"Can't find something from /res folder, check is program data corrupted.")

        self.downloadButtonLabel = QLabel(self)
        self.uploadButtonLabel = QLabel(self)
        self.settingsButtonLabel = QLabel(self)
        self.initUI()
        UF.debugOutput('successfully inited UI of main form')

    def initUI(self):
        self.setGeometry(300, 300, *GB.WINDOW_SIZE)
        self.setWindowTitle(GB.WINDOW_NAME)

        self.downloadButton.action = 'download'
        self.downloadButton.move(75, 20)
        self.downloadButton.resize(100, 100)
        self.downloadButton.clicked.connect(self.onClick)

        self.uploadButton.action = 'upload'
        self.uploadButton.move(225, 20)
        self.uploadButton.resize(100, 100)
        self.uploadButton.clicked.connect(self.onClick)

        SIZE = 20
        self.settingsButton.action = 'settings'
        self.settingsButton.move(*list(map(lambda x: x - SIZE, GB.WINDOW_SIZE)))
        self.settingsButton.resize(SIZE, SIZE)
        self.settingsButton.clicked.connect(self.onClick)

        self.downloadButtonLabel.setText(self.downloadButton.action)
        self.downloadButtonLabel.move(100, 100)

        self.uploadButtonLabel.setText(self.uploadButton.action)
        self.uploadButtonLabel.move(260, 100)

        self.settingsButtonLabel.setText(self.settingsButton.action)
        self.settingsButtonLabel.move(GB.WINDOW_SIZE[0] - SIZE - 40, GB.WINDOW_SIZE[1] - 20)
        if GB.isDebugEnabled:
            print('successfully created the whole interface of MainForm.')

    def onClick(self):
        UF.debugOutput('click button:', self.sender().action)
        try:
            if self.sender().action == 'download':
                pass
                # TODO: form calling
            if self.sender().action == 'upload':
                self.sendForm.show()
            if self.sender().action == 'settings':
                self.settingsForm.show()
        except Exception:
            UF.debugOutput(sys.exc_info())
