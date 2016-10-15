from PyQt4 import QtGui, QtCore
from .find_replace_ui import Ui_Form
    
class Find_Replace(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.IDE = parent
        
        self.setProperty("class","pluginHorizontal")
        
        self.ui.b_replace_all
        
        self.ui.b_find.clicked.connect(self.find)
        self.ui.b_replace.clicked.connect(self.replace)
        self.ui.b_replace_all.clicked.connect(self.replace_all)
    
    def replaceFocus(self):
        i = self.IDE.ui.sw_bottom.indexOf(self)
        self.IDE.ui.tabbar_bottom.setCurrentIndex(i)
        self.ui.le_find.setFocus()
        self.ui.le_find.selectAll()
    
    def getFindText(self):
        ftxt = self.ui.le_find.text()
        # Fix for lines and tabs
        if self.ui.ckbx_whitespace.isChecked():
            ftxt = ftxt.replace('\\n','\n')
            ftxt = ftxt.replace('\\r','\r')
            ftxt = ftxt.replace('\\t','\t')
        return ftxt

    def getReplaceText(self):
        ftxt = self.ui.le_replace.text()
        # Fix for lines and tabs
        if self.ui.ckbx_whitespace.isChecked():
            ftxt = ftxt.replace('\\n','\n')
            ftxt = ftxt.replace('\\r','\r')
            ftxt = ftxt.replace('\\t','\t')
        return ftxt

    def find(self):
        ftxt = self.getFindText()
        # Fix 
##        ftxt = str(self.ui.le_find.text())
        wdg = self.IDE.currentEditor()
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        if 'find' in dir(wdg):
            wdg.find(ftxt,re,cs,wo)
        
    def replace(self):
##        ftxt = str(self.ui.le_find.text())
##        rtxt = str(self.ui.le_replace.text())
##        ftxt = self.ui.le_find.text()
##        rtxt = self.ui.le_replace.text()
        ftxt = self.getFindText()
        rtxt = self.getReplaceText()
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        wdg = self.IDE.currentEditor()
        if 'replace' in dir(wdg):
            wdg.replace(ftxt,rtxt,re,cs,wo)
        
    def replace_all(self):
##        ftxt = str(self.ui.le_find.text())
##        rtxt = str(self.ui.le_replace.text())
##        ftxt = self.ui.le_find.text()
        ftxt = self.getFindText()
        rtxt = self.getReplaceText()
        re = self.ui.ckbx_re.isChecked()
        cs = self.ui.ckbx_cs.isChecked()
        wo = self.ui.ckbx_wo.isChecked()
        wdg = self.IDE.currentEditor()
        if 'replaceAll' in dir(wdg):
            wdg.replaceAll(ftxt,rtxt,re,cs,wo)