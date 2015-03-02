from PyQt4 import QtGui, QtCore
from .qt2py_ui import Ui_Form
import os, datetime, subprocess, sys
import webbrowser
    
class Qt2Py(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
    
        self.ui.b_open.clicked.connect(self.open)
        self.ui.b_convert.clicked.connect(self.convert)
        self.ui.b_qt_designer.clicked.connect(self.open_qt_designer)
        self.ui.b_help.clicked.connect(self.search_help)
        
    def open(self):
        
        # Get current file directory
        try:
            cdir = os.path.abspath(os.path.dirname(self.armadillo.currentEditor().filename))
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
            cdir = os.path.abspath(os.path.dirname(self.armadillo.currentEditor().filename))
        except:
            cdir = None
        
        try:
            if os.name == 'posix':
                subprocess.Popen('/usr/bin/designer-qt4', stdout=subprocess.PIPE, shell=0,cwd=cdir)
            elif os.name == 'nt':
    ##            pypth = os.path.dirname(sys.executable)
                pypth = r'C:\python27'
                
                subprocess.Popen(pypth+'/Lib/site-packages/PyQt4/designer.exe', stdout=subprocess.PIPE, shell=0,cwd=cdir)
        except:
            QtGui.QMessageBox.warning(self,'Qt Designer?','Armadillo could not find Qt Designer. Check to make sure it is installed')
    
    def qtHelp(self):
        i=self.armadillo.ui.sw_bottom.indexOf(self)
        self.armadillo.ui.tabbar_bottom.setCurrentIndex(i)
        self.ui.le_help.setFocus()
        self.ui.le_help.selectAll()
    
    def search_help(self):
        txt = str(self.ui.le_help.text()).lower()
        if not txt.startswith('q'):
            txt = 'q' +txt
        lnk = 'http://qt-project.org/doc/qt-4.8/%s.html' %txt
        
        webbrowser.open(lnk)