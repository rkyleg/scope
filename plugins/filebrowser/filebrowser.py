from PyQt4 import QtGui, QtCore
from filebrowser_ui import Ui_Form
import os,sys

def addDock(parent):
    dock = DirTree(parent)
    return dock


class DirTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
        
        self.iconpth = os.path.abspath(os.path.dirname(__file__))+'/icons/'
        #print self.iconpth
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        
        for f in sorted(os.listdir(os.path.abspath('/'))):
            itm = QtGui.QTreeWidgetItem([f,'/'+f])
            if os.path.isdir('/'+f):
                itm.setIcon(0,QtGui.QIcon(self.iconpth+'folder.png'))
                self.ui.tr_dir.addTopLevelItem(itm)
        
    def itmClicked(self,itm,col):
        pth = str(itm.text(1))
        itm.takeChildren()
        if os.path.isdir(pth):
            try:
                dirlist = sorted(os.listdir(os.path.abspath(pth)))
            except:
                QtGui.QMessageBox.warning(self,'No Access','The folder does not exist or you do not have access to open it')
                dirlist = []
            # Add Folders
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+'/'+f])
                if not f.startswith('.') and  os.path.isdir(pth+'/'+f):
                    citm.setIcon(0,QtGui.QIcon(self.iconpth+'folder.png'))
                    itm.addChild(citm)
            # Add Files
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+'/'+f])
                ext = os.path.splitext(f)[1][1:]
                if not f.startswith('.') and not os.path.isdir(pth+'/'+f) and ext in self.afide.settings['ext']:
                    itm.addChild(citm)
        else:
            self.afide.openFile(pth)
        
        itm.setExpanded(1)
            
        
def runui():
    app = QtGui.QApplication(sys.argv)
    appui = DirTree()
    appui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
