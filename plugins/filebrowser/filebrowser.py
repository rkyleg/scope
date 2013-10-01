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
        
        self.extD = ['py','txt','html','htm','css','js','txt']
        if self.afide != None:
            self.extD = self.afide.settings['ext']
        
        self.iconpth = os.path.abspath(os.path.dirname(__file__))+'/icons/'
        #print self.iconpth
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        self.ui.le_root.returnPressed.connect(self.loadRoot)
        
        self.ui.le_root.setText(os.path.abspath(os.path.dirname(__file__)+'../../../'))
        self.loadRoot()
    
    def loadRoot(self):
        newpath = str(self.ui.le_root.text()).replace('\\','/')
        if not newpath.endswith('/'): newpath +='/'
        if os.path.exists(newpath):
            self.rootpath = newpath

        self.ui.le_root.setText(self.rootpath)
        self.ui.tr_dir.clear()
        
        # Add to Tree
        dircontents,filecontents = self.getDirContents(self.rootpath)
        for citm in dircontents:
            self.ui.tr_dir.addTopLevelItem(citm)
        
        for citm in filecontents:
            self.ui.tr_dir.addTopLevelItem(citm)
        
##        for f in sorted(os.listdir(self.rootpath)):
##            itm = QtGui.QTreeWidgetItem([f,self.rootpath+'/'+f])
##            if os.path.isdir(self.rootpath+'/'+f):
##                itm.setIcon(0,QtGui.QIcon(self.iconpth+'folder.png'))
##                self.ui.tr_dir.addTopLevelItem(itm)
        
    def itmClicked(self,itm,col):
        pth = str(itm.text(1))
        itm.takeChildren()
        if os.path.isdir(pth):
            dircontents,filecontents = self.getDirContents(pth)
            for citm in dircontents:
                itm.addChild(citm)
            
            for citm in filecontents:
                itm.addChild(citm)
            
        else:
            if self.afide != None:
                self.afide.openFile(pth)
        itm.setExpanded(1)

    def getDirContents(self,pth):
        # Return [dirlist,filelist]
        dircontents = []
        filecontents = []
        
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
                    dircontents.append(citm)
            # Add Files
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+'/'+f])
                ext = os.path.splitext(f)[1][1:]
                if not f.startswith('.') and not os.path.isdir(pth+'/'+f) and ext in self.extD:
                    filecontents.append(citm)

        return dircontents,filecontents
    
def runui():
    app = QtGui.QApplication(sys.argv)
    appui = DirTree()
    appui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
