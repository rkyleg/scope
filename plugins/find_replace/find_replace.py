from PyQt4 import QtGui, QtCore
from find_replace_ui import Ui_Form

def addDock(parent):
    dock = Find_Replace(parent)
    return dock
    
class Find_Replace(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
    
        self.ui.b_find.clicked.connect(self.find)
        self.ui.b_replace.clicked.connect(self.replace)
        
    def find(self):
        ftxt = str(self.ui.le_find.text())
        wdg = self.afide.currentWidget()
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        if 'find' in dir(wdg):
            wdg.find(ftxt,re,cs,wo)
        
    def replace(self):
        ftxt = str(self.ui.le_find.text())
        rtxt = str(self.ui.le_replace.text())
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        wdg = self.afide.currentWidget()
        if 'replace' in dir(wdg):
            wdg.replace(ftxt,rtxt,re,cs,wo)