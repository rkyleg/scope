from PyQt4 import QtGui, QtCore
from qt2py_ui import Ui_Form
import os, datetime, subprocess, sys

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
        
        # Get current file directory
        try:
            cdir = os.path.abspath(os.path.dirname(self.afide.currentWidget().filename))
        except:
            cdir = ''
        
        filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",cdir,"UI (*.ui)")
        if filename!='':
            self.ui.le_path.setText(filename)
    
    def convert(self):
        filename = str(self.ui.le_path.text())
        if os.path.exists(filename):
            # Convert .ui to .py
            pth = os.path.dirname(str(filename))
            bname = os.path.basename(str(filename))
            curdir = os.path.abspath('.')
            os.chdir(pth)
            os.system("pyuic4 "+bname+" > " +bname[:len(bname)-3] + "_ui.py")
            os.chdir(curdir)
            self.ui.l_result.setText('Converted '+filename+' on '+datetime.datetime.now().ctime())
    
    def open_qt_designer(self):
        
        # Get current file directory
        try:
            cdir = os.path.abspath(os.path.dirname(self.afide.currentWidget().filename))
        except:
            cdir = None
        
        if os.name == 'posix':
            subprocess.Popen('/usr/bin/designer-qt4', stdout=subprocess.PIPE, shell=0,cwd=cdir)
        elif os.name == 'nt':
            pypth = os.path.dirname(sys.executable)
            
            subprocess.Popen(pypth+'/Lib/site-packages/PyQt4/designer.exe', stdout=subprocess.PIPE, shell=0,cwd=cdir)
            