from PyQt4 import QtGui, QtCore
from filebrowser_ui import Ui_Form
import os,sys

class DirTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent

        self.extD = ['py','txt','html','htm','css','js','txt']
        if self.afide != None:
            self.extD = self.afide.settings.ext
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        self.ui.le_root.returnPressed.connect(self.loadRoot)
        
##        self.ui.le_root.setText(os.path.abspath(os.path.dirname(__file__)+'../../../'))
        self.ui.le_root.setText(os.path.expanduser('~')) # Start with home directory
        self.loadRoot()
        
        self.ui.tr_dir.contextMenuEvent = self.fileMenu
    
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
                    citm.setIcon(0,QtGui.QIcon(self.afide.iconPath+'folder.png'))
                    dircontents.append(citm)
            # Add Files
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+'/'+f])
                ext = os.path.splitext(f)[1][1:]
                if not f.startswith('.') and not os.path.isdir(pth+'/'+f) and ext in self.extD:
                    
                    ipth = self.afide.iconPath+'files/'+self.extD[ext]+'.png'
                    if os.path.exists(ipth):
                        citm.setIcon(0,QtGui.QIcon(ipth))
                    elif os.path.exists(self.afide.iconPath+'files/'+ext+'.png'):
                        citm.setIcon(0,QtGui.QIcon(self.afide.iconPath+'files/'+ext+'.png'))
                    else:
                        citm.setIcon(0,QtGui.QIcon(self.afide.iconPath+'files/_blank.png'))
                    filecontents.append(citm)

        return dircontents,filecontents
    
    def fileMenu(self,event):
##        print event
        menu = QtGui.QMenu('file menu')
        citm = self.ui.tr_dir.currentItem()
        if citm != None:
            pth = str(citm.text(1))
            ext = os.path.splitext(pth)[1][1:]
            if ext != '':
                if len(self.extD[ext])>1:
                    for e in self.extD[ext]:
                        menu.addAction(QtGui.QIcon(),'Open in '+e)
                else:
                    menu.addAction(QtGui.QIcon(),'Open')
            
                
            for act in menu.actions():  # Set Icon to visible
                act.setIconVisibleInMenu(1)
            act = menu.exec_(self.ui.tr_dir.cursor().pos())
            if act != None:
                acttxt = str(act.text())
                if acttxt == 'Open':
                    self.openFile()
                else:
                    lang = acttxt[8:]
                    self.afide.openFile(pth,editor=lang)
    
    def openFile(self):
        itm = self.ui.tr_dir.currentItem()
        if itm != None:
            pth = str(itm.text(1))
            self.itmClicked(itm,0)
    
def runui():
    app = QtGui.QApplication(sys.argv)
    appui = DirTree()
    appui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
