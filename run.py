import sys

from PyQt5.QtWidgets import QApplication

import GlobalVariables
import MainForm
import UtilityClasses
import UtilityFunctions

# This is main file which launches the whole program
# just run it
# (C) Lunar

print(UtilityFunctions.convertCode('85.117.31.129', False))


args = sys.argv
try:

    GlobalVariables.isDebugEnabled = True
    GlobalVariables.myIP = UtilityFunctions.getIP()
    conn = UtilityClasses.UtilitySettingsFileManager()
    conn.load()

    app = QApplication(args)
    form = MainForm.MainForm()

    form.show()
except Exception as e:
    UtilityFunctions.debugOutput('main.py, failed to initialize!', e)

sys.exit(app.exec())
