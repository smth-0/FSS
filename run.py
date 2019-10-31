import sys

from PyQt5.QtWidgets import QApplication

import GlobalVariables
import MainForm
import UtilityClasses
import UtilityFunctions

# This is main file which launches the whole program
# just run it
# (C) Lunar



args = sys.argv

GlobalVariables.isDebugEnabled = True
GlobalVariables.myIP = UtilityFunctions.getIP()
conn = UtilityClasses.UtilitySettingsFileManager()
conn.load()

print('>' * 20, GlobalVariables.savePath)


app = QApplication(args)
form = MainForm.MainForm()

try:
    form.show()
except Exception as e:
    UtilityFunctions.debugOutput('main.py, failed to initialize!', e)

sys.exit(app.exec())
