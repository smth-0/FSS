import sys
from PyQt5.QtWidgets import QApplication
import MainForm
import GlobalVariables

# This is main file which launches the whole program
# just run it
# optional keys:
optionalKeys = {'debug': 'forces the whole program to output debug logs to terminal. Default - False.'}
# (C) Lunar

args = sys.argv
print('arguments =', args)
GlobalVariables.isDebugEnabled = any([i in optionalKeys.keys() for i in args])
app = QApplication(args)
form = MainForm.MainForm()
form.show()
sys.exit(app.exec())
