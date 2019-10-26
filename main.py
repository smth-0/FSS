import sys

from PyQt5.QtWidgets import QApplication

import GlobalVariables
import MainForm
import UtilityFunctions as UF

# This is main file which launches the whole program
# just run it
# (C) Lunar


args = sys.argv

UF.debugOutput('program start')
GlobalVariables.isDebugEnabled = True  # todo: make exe read the args

app = QApplication(args)
form = MainForm.MainForm()

try:
    form.show()
except Exception as e:
    UF.debugOutput('main.py, failed to initialize!', e)

sys.exit(app.exec())
