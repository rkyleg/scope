from PyQt4 import QtGui, QtCore
from snippets_ui import Ui_Form

class Snippets(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent