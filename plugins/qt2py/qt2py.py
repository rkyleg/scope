from PyQt4 import QtGui, QtCore
from qt2py_ui import Ui_Form
import os, datetime, subprocess

def addDock(parent):
    dock = Qt2Py(parent)
    return dock
    
class Qt2Py(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
    
        self.ui.b_open.clicked.connect(self.open)
        self.ui.b_convert.clicked.connect(self.convert)
        self.ui.b_qt_designer.clicked.connect(self.open_qt_designer)
        
    def open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Select File","","UI (*.ui)")
        if filename!='':
            self.ui.le_path.setText(filename)
    
    def convert(self):
        filename = str(self.ui.le_path.text())
        if os.path.exists(filename):
            # Convert .ui to .py
            pth = os.path.dirname(str(filename))
            bname = os.path.basename(str(filename))
            os.chdir(pth)
            os.system("pyuic4 "+bname+" > " +bname[:len(bname)-3] + "_ui.py")
            
            self.ui.l_result.setText('Converted '+filename+' on '+datetime.datetime.now().ctime())
    
    def open_qt_designer(self):
        if os.name == 'posix':
            subprocess.Popen('/usr/bin/designer-qt4', stdout=subprocess.PIPE, shell=0)