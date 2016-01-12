from PyQt4 import QtGui, QtCore
from .filebrowser_ui import Ui_Form
import os,sys, subprocess

class FileBrowser(QtGui.QStackedWidget):
    def __init__(self,parent=None):
        self.ide = parent
        QtGui.QStackedWidget.__init__(self,parent)
        self.workspaceD = {}
        pth = self.ide.settings['plugins']['filebrowser']['defaultPath']
        ntree = self.addFilePage(pth)
        self.setCurrentWidget(ntree)

    def addFilePage(self,pth=None):
        curdir = os.path.abspath('.')
        os.chdir(os.path.dirname(__file__))
        ntree = DirTree(self.ide)
        os.chdir(curdir)
        self.addWidget(ntree)
        if pth == None or not os.path.exists(pth):
            pth = os.path.expanduser('~')
        ntree.ui.le_root.setText(pth) 
        ntree.loadRoot()
        return ntree
        
    def changeWorkspace(self,wksp):
        wksp = str(wksp)
        if wksp == None:
            self.setCurrentIndex(0)
        else:
            if wksp in self.workspaceD:
                self.setCurrentWidget(self.workspaceD[wksp])
        
    def openWorkspace(self,wksp):
        wksp = str(wksp)
        wD=self.ide.workspaces[wksp]
        self.workspaceD[wksp]=self.addFilePage(wD['basefolder'])
        self.workspaceD[wksp].wksp_id = wksp
        self.setCurrentWidget(self.workspaceD[wksp])

class DirTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ide = parent
        self.wksp_id = None
        self.extD = self.ide.settings['extensions']
        
        # Show All
        self.showAll=0
        if 'showAll' in self.ide.settings['plugins']['filebrowser']:
            self.showAll = self.ide.settings['plugins']['filebrowser']['showAll']
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        self.ui.tr_dir.itemExpanded.connect(self.itmExpanded)
        self.ui.tr_dir.mousePressEvent = self.mousePressEvent
        self.ui.le_root.returnPressed.connect(self.loadRoot)
        self.ui.b_browse.clicked.connect(self.browse)
        
        # Set default path
        self.ui.le_root.setText(os.path.expanduser('~')) # Start with home directory
        self.loadRoot()
        
        self.ui.tr_dir.contextMenuEvent = self.fileMenu
        self.ui.tr_dir.keyPressEvent = self.ikeyPressEvent
    
    def viewFileBrowser(self):
        if self.ide.ui.fr_left.isHidden():
            self.ide.ui.fr_left.setVisible(1)
        i=self.ide.ui.tab_left.indexOf(self)
        self.ide.ui.tab_left.setCurrentIndex(i)
    
    def browse(self):
##        print self.ui.le_path.text()
        npth = QtGui.QFileDialog.getExistingDirectory(self,'Select directory to search',self.ui.le_root.text())
        if not npth.isEmpty(): 
            self.ui.le_root.setText(npth)
            self.loadRoot()
    
    def loadRoot(self):
        newpath = os.path.abspath(str(self.ui.le_root.text())).replace('\\','/')
        if not newpath.endswith('/'): newpath +='/'
        if os.path.exists(newpath):
            self.rootpath = newpath
        
        self.ui.le_root.setText(self.rootpath)
        self.ui.tr_dir.clear()
        
        # Set Armadilo path
        self.ide.currentPath = self.rootpath
        
        # Add up directory
        citm = QtGui.QTreeWidgetItem(['..','..'])
        citm.setIcon(0,QtGui.QIcon(self.ide.iconPath+'up.png'))
        self.ui.tr_dir.addTopLevelItem(citm)
        
        # Add to Tree
        dircontents,filecontents = self.getDirContents(self.rootpath)
        for citm in dircontents:
            self.ui.tr_dir.addTopLevelItem(citm)
        
        for citm in filecontents:
            self.ui.tr_dir.addTopLevelItem(citm)
        
        if self.wksp_id != None:
            self.ide.workspaces[self.wksp_id]['basefolder'] = self.rootpath
        
    def itmClicked(self,itm,col):
        # Tree Click Signals
        self.itmClick(itm,col)
    
    def itmClick(self,itm,col,toggleExpanded=1):
        pth = str(itm.text(1))
        
        if pth == '..':
            # Go up a directory
            self.ui.le_root.setText(self.rootpath+'../')
            self.loadRoot()
        else:
            itm.takeChildren()
            if os.path.isdir(pth):
                dircontents,filecontents = self.getDirContents(pth)
                for citm in dircontents:
                    itm.addChild(citm)
                
                for citm in filecontents:
                    itm.addChild(citm)
                
                if toggleExpanded==2:
                    itm.setExpanded(1)
                elif toggleExpanded:
                    itm.setExpanded(not itm.isExpanded())
                
                # Toggle Image
                icn = QtGui.QIcon(self.ide.iconPath+'folder.png')
                
                if itm.isExpanded():
                    icn = QtGui.QIcon(self.ide.iconPath+'folder_open.png')
                
                itm.setIcon(0,icn)
                
            else:
                if self.ide != None:
                    if toggleExpanded == 2:
                        if itm.parent() != None:
                            self.itmClick(itm.parent(),0,toggleExpanded=toggleExpanded)
                        else:
                            self.loadRoot()
                    else:
                        self.ide.openFile(pth)
    
    def mousePressEvent(self, event):
        self.ui.tr_dir.clearSelection()
        self.ui.tr_dir.setCurrentItem(None)
        QtGui.QTreeView.mousePressEvent(self.ui.tr_dir, event)
    
    def itmExpanded(self,itm):
        pth = str(itm.text(1))
        
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
                if not f.startswith('.') and  os.path.isdir(pth+f):
                    citm.setIcon(0,QtGui.QIcon(self.ide.iconPath+'folder.png'))
                    dircontents.append(citm)
            # Add Files
            for f in sorted(dirlist, key=lambda s: s.lower()):
                citm = QtGui.QTreeWidgetItem([f,pth+f])
                
                ext = os.path.splitext(f)[1][1:]
                if not os.path.isdir(pth+f) and ((not f.startswith('.') and ext in self.extD) or self.showAll):
                    
                    ipth = ''
                    if ext in ['png','jpg','jpeg','gif','bmp','ico']:
                        ipth = pth+f
                    elif ext in self.extD:
                        ipth = self.ide.iconPath+'files/'+self.extD[ext]+'.png'
                    if os.path.exists(ipth):
                        citm.setIcon(0,QtGui.QIcon(ipth))
                    elif os.path.exists(self.ide.iconPath+'files/'+ext+'.png'):
                        citm.setIcon(0,QtGui.QIcon(self.ide.iconPath+'files/'+ext+'.png'))
                    else:
                        citm.setIcon(0,QtGui.QIcon(self.ide.iconPath+'files/_blank.png'))
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
        menu = QtGui.QMenu('file menu')
        open_icon = QtGui.QIcon(self.ide.iconPath+'folder_go.png')
        citm = self.ui.tr_dir.currentItem()
        fitm = None
        isfile = 0
        if citm != None:
            pth = str(citm.text(1))
            fpth = pth # Folder path
            fitm = citm
            ext = os.path.splitext(pth)[1][1:]
            if os.path.isfile(pth):
                fpth = os.path.dirname(pth)
                fitm = citm.parent()
                isfile = 1
            
                open_icon = QtGui.QIcon(self.ide.iconPath+'file_go.png')
            
        menu.addAction(open_icon,'Open (external)')
        menu.addSeparator()
        
        if citm != None:
            # New File
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'new.png'),'New File')
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'folder_add.png'),'New Folder')
            menu.addSeparator()
            
            if ext != '':
                # Open menu
                lang = None
                cnt = 0
                if ext in self.ide.settings['extensions']:
                    lang = self.ide.settings['extensions'][ext]
                for edtr in self.ide.editorD:
                    if lang in self.ide.editorD[edtr] or ext in self.ide.editorD[edtr]:
                        menu.addAction(QtGui.QIcon(self.ide.editorPath+'/'+edtr+'/'+edtr+'.png'),'Edit with '+edtr)
                        cnt += 1
                if cnt == 0:
                    menu.addAction(QtGui.QIcon(),'Edit')
            
                menu.addSeparator()
            
##            # Other File Options
##            menu.addAction(QtGui.QIcon(self.ide.iconPath+'forward.png'),'Open (external)')
            

            if os.path.isfile(pth):
                menu.addAction(QtGui.QIcon(self.ide.iconPath+'edit.png'),'Rename')
##                menu.addAction(QtGui.QIcon(self.ide.iconPath+'copy.png'),'Copy File')
##                menu.addSeparator()
                menu.addAction(QtGui.QIcon(self.ide.iconPath+'delete.png'),'Delete File')
            
            for act in menu.actions():  # Set Icon to visible
                act.setIconVisibleInMenu(1)
        else:
            fpth = unicode(self.ui.le_root.text())
            pth = fpth
            # New File
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'new.png'),'New File')
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'folder_add.png'),'New Folder')
            menu.addSeparator()
##            menu.addAction(QtGui.QIcon(),'Open (external)')
##            menu.addSeparator()
            
        
        menu.addSeparator()
        menu.addAction(QtGui.QIcon(self.ide.iconPath+'refresh.png'),'Refresh')
        # Show All files
        showAct=menu.addAction(QtGui.QIcon(),'Show All Files')
        showAct.setCheckable(1)
        showAct.setChecked(self.showAll)
        if not isfile:
            menu.addAction('Set As Root Path')
        
        # Launch Menu
        act = menu.exec_(self.ui.tr_dir.cursor().pos())
        if act != None:
            acttxt = str(act.text())
            if acttxt == 'Edit':
                # Open File
                self.openFile()
            elif acttxt == 'Open (external)':
                externalFileBrowser = None
                fbsD = self.ide.settings['plugins']['filebrowser']
                if os.path.isdir(pth) and 'externalFileBrowser' in fbsD and fbsD['externalFileBrowser']!='':
                    externalFileBrowser = fbsD['externalFileBrowser']
                self.ide.openFileExternal(pth,externalFileBrowser)
            elif acttxt == 'Show All Files':
                self.showAll = showAct.isChecked()
                if citm != None:
                    self.itmClick(citm,0,toggleExpanded=2)
                else:
                    self.loadRoot()
            elif acttxt=='Refresh':
                if citm != None:
                    self.itmClick(citm,0,toggleExpanded=2)
                else:
                    self.loadRoot()
            elif acttxt == 'Set As Root Path':
                if citm != None:
                    pth = citm.text(1)
                    self.ui.le_root.setText(pth)
                    self.loadRoot()
            elif acttxt == 'New File':
                # New File
                resp,ok = QtGui.QInputDialog.getText(self.ide,'New File','Enter the file name and extension.')
                if ok and not resp.isEmpty():
                    if os.path.exists(fpth+'/'+unicode(resp)):
                        QtGui.QMessageBox.warning(self,'File Exists','That file already exists')
                    else:
                        f = open(fpth+'/'+unicode(resp),'w')
                        f.close()
                        if fitm != None:
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                        else:
                            self.loadRoot()
            elif acttxt == 'New Folder':
                # New Folder
                resp,ok = QtGui.QInputDialog.getText(self.ide,'New Folder','Enter the folder name.')
                if ok and not resp.isEmpty():
                    if os.path.exists(fpth+'/'+unicode(resp)):
                        QtGui.QMessageBox.warning(self,'Folder Exists','That folder already exists')
                    else:
                        os.mkdir(fpth+'/'+unicode(resp))
                        if fitm != None:
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                        else:
                            self.loadRoot()
            elif acttxt == 'Rename':
                # Rename the file
                fileopen = self.ide.isFileOpen(pth)
                rename = 1
                if fileopen != -1:
                    rename = 0
                    resp = QtGui.QMessageBox.warning(self,'File is open','The file is currently open and needs to close in order to rename.<br><br>Do you want to close the file now?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                    if resp == QtGui.QMessageBox.Yes:
                        rename = 1
                        self.ide.closeTab(fileopen)
                
                if rename:
                    resp,ok = QtGui.QInputDialog.getText(self.ide,'Rename File','Enter the file name and extension.',QtGui.QLineEdit.Normal,os.path.split(pth)[1])
                    if ok and not resp.isEmpty():
                        newpth = fpth+'/'+unicode(resp)
                        if os.path.exists(newpth):
                            QtGui.QMessageBox.warning(self,'File Exists','That file already exists')
                        else:
                            os.rename(pth,newpth)
                            if fitm != None:
                                self.itmClick(fitm,0,toggleExpanded=0)
                                fitm.setExpanded(1)
                            else:
                                self.loadRoot()
            elif acttxt == 'Delete File':
                # Delete File
                fileopen = self.ide.isFileOpen(pth)
                delfile = 1
                if fileopen != -1:
                    delfile = 0
                    resp = QtGui.QMessageBox.warning(self,'File is open','The file is currently open and needs to close in order to delete.<br><br>Do you want to close the file now?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                    if resp == QtGui.QMessageBox.Yes:
                        delfile = 1
                        self.ide.closeTab(fileopen)
                
                if delfile:
                    resp = QtGui.QMessageBox.warning(self,'Delete File','Are you sure you want to delete the file:<br><br>'+pth,QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                    if resp == QtGui.QMessageBox.Yes:
                        os.remove(pth)
                        if fitm != None:
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                        else:
                            self.loadRoot()
            else:
                # Open file in specific editor
                lang = acttxt[10:]
                self.ide.openFile(pth,editor=lang)
    
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
