from PyQt4 import QtGui, QtCore
from find_replace_ui import Ui_Form
    
class Find_Replace(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
        
        self.ui.b_replace_all
        
        self.ui.b_find.clicked.connect(self.find)
        self.ui.b_replace.clicked.connect(self.replace)
        self.ui.b_replace_all.clicked.connect(self.replace_all)
        
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
        
    def replace_all(self):
        ftxt = str(self.ui.le_find.text())
        rtxt = str(self.ui.le_replace.text())
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        wdg = self.afide.currentWidget()
        if 'replaceAll' in dir(wdg):
            wdg.replaceAll(ftxt,rtxt,re,cs,wo)