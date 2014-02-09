from PyQt4 import QtGui, QtCore
from filebrowser_ui import Ui_Form
import os,sys, subprocess

class DirTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent

##        self.extD = ['py','txt','html','htm','css','js','txt']
##        if self.armadillo != None:
        self.extD = self.armadillo.settings.ext
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        self.ui.tr_dir.itemExpanded.connect(self.itmExpanded)
        self.ui.le_root.returnPressed.connect(self.loadRoot)
        
##        self.ui.le_root.setText(os.path.abspath(os.path.dirname(__file__)+'../../../'))
        self.ui.le_root.setText(os.path.expanduser('~')) # Start with home directory
        self.loadRoot()
        
        self.ui.tr_dir.contextMenuEvent = self.fileMenu
        self.ui.tr_dir.keyPressEvent = self.ikeyPressEvent
    
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
        # Tree Click Signals
        self.itmClick(itm,col)
    
    def itmClick(self,itm,col,toggleExpanded=1):
        pth = str(itm.text(1))
        itm.takeChildren()
        if os.path.isdir(pth):
            dircontents,filecontents = self.getDirContents(pth)
            for citm in dircontents:
                itm.addChild(citm)
            
            for citm in filecontents:
                itm.addChild(citm)
            
            if toggleExpanded:
                itm.setExpanded(not itm.isExpanded())
            
            # Toggle Image
            icn = QtGui.QIcon(self.armadillo.iconPath+'folder.png')
            
            if itm.isExpanded():
                icn = QtGui.QIcon(self.armadillo.iconPath+'folder_open.png')
            
            itm.setIcon(0,icn)
            
        else:
            if self.armadillo != None:
                self.armadillo.openFile(pth)
        
    def itmExpanded(self,itm):
        pth = str(itm.text(1))
##        if os.path.isdir(pth):
##            icn = QtGui.QIcon(self.armadillo.iconPath+'folder.png')
##            
##            if itm.isExpanded():
##                icn = QtGui.QIcon(self.armadillo.iconPath+'folder_open.png')
##            
##            itm.setIcon(0,icn)
        
    def getDirContents(self,pth):
        # Return [dirlist,filelist]
        dircontents = []
        filecontents = []
        
        if os.path.isdir(pth):
            if not pth.endswith('/'): pth += '/'
            try:
                dirlist = sorted(os.listdir(os.path.abspath(pth)))
            except:
                QtGui.QMessageBox.warning(self,'No Access','The folder does not exist or you do not have access to open it')
                dirlist = []
            # Add Folders
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+f])
##                citm.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.DontShowIndicator)
                if not f.startswith('.') and  os.path.isdir(pth+f):
                    citm.setIcon(0,QtGui.QIcon(self.armadillo.iconPath+'folder.png'))
                    dircontents.append(citm)
            # Add Files
            for f in dirlist:
                citm = QtGui.QTreeWidgetItem([f,pth+f])
                
                ext = os.path.splitext(f)[1][1:]
                if not f.startswith('.') and not os.path.isdir(pth+f) and ext in self.extD:
                    
                    ipth = self.armadillo.iconPath+'files/'+self.extD[ext]+'.png'
                    if os.path.exists(ipth):
                        citm.setIcon(0,QtGui.QIcon(ipth))
                    elif os.path.exists(self.armadillo.iconPath+'files/'+ext+'.png'):
                        citm.setIcon(0,QtGui.QIcon(self.armadillo.iconPath+'files/'+ext+'.png'))
                    else:
                        citm.setIcon(0,QtGui.QIcon(self.armadillo.iconPath+'files/_blank.png'))
                    filecontents.append(citm)

        return dircontents,filecontents

    def ikeyPressEvent(self,event):
        ky = event.key()
        handled = 0
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return]:
            self.itmClicked(self.ui.tr_dir.currentItem(),0)
            handled = 1
        if not handled:
            QtGui.QTreeWidget.keyPressEvent(self.ui.tr_dir,event)

        
    def fileMenu(self,event):
##        print event
        menu = QtGui.QMenu('file menu')
        citm = self.ui.tr_dir.currentItem()
        if citm != None:
            pth = str(citm.text(1))
            fpth = pth # Folder path
            fitm = citm
            ext = os.path.splitext(pth)[1][1:]
            if os.path.isfile(pth):
                fpth = os.path.dirname(pth)
                fitm = citm.parent()
                
            if ext != '':
                # Open menu
                lang = None
                cnt = 0
                if ext in self.armadillo.settings.ext:
                    lang = self.armadillo.settings.ext[ext]
                for edtr in self.armadillo.editorD:
                    if lang in self.armadillo.editorD[edtr] or ext in self.armadillo.editorD[edtr]:
                        menu.addAction(QtGui.QIcon(self.armadillo.editorPath+'/'+edtr+'/'+edtr+'.png'),'Edit with '+edtr)
                        cnt += 1
                if cnt == 0:
                    menu.addAction(QtGui.QIcon(),'Edit')
            
                menu.addSeparator()
            
            # New File
            if os.path.isdir(pth):
                menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'new.png'),'New File')
                menu.addSeparator()
            
            # Other File Options
##            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'file_open.png'),'Open')
            menu.addAction(QtGui.QIcon(),'Open')
                
            if os.path.isfile(pth):
                menu.addAction(QtGui.QIcon(),'Rename')
                menu.addSeparator()
                menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'delete.png'),'Delete File')
                
            
            for act in menu.actions():  # Set Icon to visible
                act.setIconVisibleInMenu(1)
            
            # Launch Menu
            act = menu.exec_(self.ui.tr_dir.cursor().pos())
            if act != None:
                acttxt = str(act.text())
                if acttxt == 'Edit':
                    # Open File
                    self.openFile()
                elif acttxt == 'Open':
                    try:
                        os.startfile(pth)
                    except:
                        subprocess.Popen(['xdg-open', pth])
                elif acttxt == 'New File':
                    # New File
                    resp,ok = QtGui.QInputDialog.getText(self.armadillo,'New File','Enter the file name and extension.')
                    if ok and not resp.isEmpty():
                        if os.path.exists(fpth+'/'+unicode(resp)):
                            QtGui.QMessageBox.warning(self,'File Exists','That file already exists')
                        else:
                            f = open(fpth+'/'+unicode(resp),'w')
                            f.close()
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                elif acttxt == 'Rename':
                    # Rename the file
                    fileopen = self.armadillo.isFileOpen(pth)
                    rename = 1
                    if fileopen != -1:
                        rename = 0
                        resp = QtGui.QMessageBox.warning(self,'File is open','The file is currently open and needs to close in order to rename.<br><br>Do you want to close the file now?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        if resp == QtGui.QMessageBox.Yes:
                            rename = 1
                            self.armadillo.closeTab(fileopen)
                    
                    if rename:
                        resp,ok = QtGui.QInputDialog.getText(self.armadillo,'Rename File','Enter the file name and extension.',QtGui.QLineEdit.Normal,os.path.split(pth)[1])
                        if ok and not resp.isEmpty():
                            newpth = fpth+'/'+unicode(resp)
                            if os.path.exists(newpth):
                                QtGui.QMessageBox.warning(self,'File Exists','That file already exists')
                            else:
                                os.rename(pth,newpth)
                                self.itmClick(fitm,0,toggleExpanded=0)
                                fitm.setExpanded(1)
                elif acttxt == 'Delete File':
                    # Delete File
                    fileopen = self.armadillo.isFileOpen(pth)
                    delfile = 1
                    if fileopen != -1:
                        delfile = 0
                        resp = QtGui.QMessageBox.warning(self,'File is open','The file is currently open and needs to close in order to delete.<br><br>Do you want to close the file now?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        if resp == QtGui.QMessageBox.Yes:
                            delfile = 1
                            self.armadillo.closeTab(fileopen)
                    
                    if delfile:
                        resp = QtGui.QMessageBox.warning(self,'Delete File','Are you sure you want to delete the file:<br><br>'+pth,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        if resp == QtGui.QMessageBox.Yes:
                            os.remove(pth)
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                else:
                    # Open file in specific editor
                    lang = acttxt[10:]
                    print lang
                    self.armadillo.openFile(pth,editor=lang)
    
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
