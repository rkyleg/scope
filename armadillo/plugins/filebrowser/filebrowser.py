from PyQt4 import QtGui, QtCore
from .filebrowser_ui import Ui_Form
import os,sys, subprocess

class DirTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent

        self.extD = self.armadillo.settings['extensions']
        
        # Show All
        self.showAll=0
        if 'showAll' in self.armadillo.settings['plugins']['filebrowser']:
            self.showAll = int(self.armadillo.settings['plugins']['filebrowser']['showAll'])
        
        self.ui.tr_dir.itemDoubleClicked.connect(self.itmClicked)
        self.ui.tr_dir.itemExpanded.connect(self.itmExpanded)
        self.ui.tr_dir.mousePressEvent = self.mousePressEvent
        self.ui.le_root.returnPressed.connect(self.loadRoot)
        
        # Set default path
        self.ui.le_root.setText(os.path.expanduser('~')) # Start with home directory
        if self.armadillo.settings['plugins']['filebrowser']['defaultPath']!='':
            if os.path.exists(self.armadillo.settings['plugins']['filebrowser']['defaultPath']):
                self.ui.le_root.setText(self.armadillo.settings['plugins']['filebrowser']['defaultPath']) 
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
            
            if toggleExpanded==2:
                itm.setExpanded(1)
            elif toggleExpanded:
                itm.setExpanded(not itm.isExpanded())
            
            # Toggle Image
            icn = QtGui.QIcon(self.armadillo.iconPath+'folder.png')
            
            if itm.isExpanded():
                icn = QtGui.QIcon(self.armadillo.iconPath+'folder_open.png')
            
            itm.setIcon(0,icn)
            
        else:
            if self.armadillo != None:
                if toggleExpanded == 2:
                    if itm.parent() != None:
                        self.itmClick(itm.parent(),0,toggleExpanded=toggleExpanded)
                    else:
                        self.loadRoot()
                else:
                    self.armadillo.openFile(pth)
    
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
                    citm.setIcon(0,QtGui.QIcon(self.armadillo.iconPath+'folder.png'))
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
        menu = QtGui.QMenu('file menu')
        open_icon = QtGui.QIcon(self.armadillo.iconPath+'folder_go.png')
        citm = self.ui.tr_dir.currentItem()
        fitm = None
        if citm != None:
            pth = str(citm.text(1))
            fpth = pth # Folder path
            fitm = citm
            ext = os.path.splitext(pth)[1][1:]
            if os.path.isfile(pth):
                fpth = os.path.dirname(pth)
                fitm = citm.parent()
            
                open_icon = QtGui.QIcon(self.armadillo.iconPath+'file_go.png')
            
        menu.addAction(open_icon,'Open (external)')
        menu.addSeparator()
        
        if citm != None:
            # New File
            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'new.png'),'New File')
            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'folder_add.png'),'New Folder')
            menu.addSeparator()
            
            if ext != '':
                # Open menu
                lang = None
                cnt = 0
                if ext in self.armadillo.settings['extensions']:
                    lang = self.armadillo.settings['extensions'][ext]
                for edtr in self.armadillo.editorD:
                    if lang in self.armadillo.editorD[edtr] or ext in self.armadillo.editorD[edtr]:
                        menu.addAction(QtGui.QIcon(self.armadillo.editorPath+'/'+edtr+'/'+edtr+'.png'),'Edit with '+edtr)
                        cnt += 1
                if cnt == 0:
                    menu.addAction(QtGui.QIcon(),'Edit')
            
                menu.addSeparator()
            
##            # Other File Options
##            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'forward.png'),'Open (external)')
            

            if os.path.isfile(pth):
                menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'edit.png'),'Rename')
##                menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'copy.png'),'Copy File')
##                menu.addSeparator()
                menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'delete.png'),'Delete File')
            
            for act in menu.actions():  # Set Icon to visible
                act.setIconVisibleInMenu(1)
        else:
            fpth = unicode(self.ui.le_root.text())
            pth = fpth
            # New File
            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'new.png'),'New File')
            menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'folder_add.png'),'New Folder')
            menu.addSeparator()
##            menu.addAction(QtGui.QIcon(),'Open (external)')
##            menu.addSeparator()
            
        # Show All files
        menu.addSeparator()
        showAct=menu.addAction(QtGui.QIcon(),'Show All Files')
        
        showAct.setCheckable(1)
        showAct.setChecked(self.showAll)
        
        menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'refresh.png'),'Refresh')
        
        
        # Launch Menu
        act = menu.exec_(self.ui.tr_dir.cursor().pos())
        if act != None:
            acttxt = str(act.text())
            if acttxt == 'Edit':
                # Open File
                self.openFile()
            elif acttxt == 'Open (external)':
                fbsD = self.armadillo.settings['plugins']['filebrowser']
                if os.name=='nt':pth = pth.replace('/','\\')
                dpth = os.path.dirname(pth)
                if os.path.isdir(pth) and 'externalFileBrowser' in fbsD and fbsD['externalFileBrowser']!='':
                    # Use specified file browser
                    subprocess.Popen([fbsD['externalFileBrowser'],pth],cwd=dpth)
                else:
                    # use default filebrowser
                    curdir = os.path.abspath('.')
                    os.chdir(os.path.dirname(pth))
                    if os.name == 'nt':
##                        subprocess.Popen(pth,shell=True,cwd=dpth)
                        os.startfile(pth)
                    elif os.name=='posix':
                        subprocess.Popen(['xdg-open', pth],cwd=dpth)
##                    elif os.name=='mac':
##                        subprocess.Popen(['open', pth],cwd=dpth)
                    os.chdir(curdir)
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
            elif acttxt == 'New File':
                # New File
                resp,ok = QtGui.QInputDialog.getText(self.armadillo,'New File','Enter the file name and extension.')
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
                resp,ok = QtGui.QInputDialog.getText(self.armadillo,'New Folder','Enter the folder name.')
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
                            if fitm != None:
                                self.itmClick(fitm,0,toggleExpanded=0)
                                fitm.setExpanded(1)
                            else:
                                self.loadRoot()
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
                        if fitm != None:
                            self.itmClick(fitm,0,toggleExpanded=0)
                            fitm.setExpanded(1)
                        else:
                            self.loadRoot()
            else:
                # Open file in specific editor
                lang = acttxt[10:]
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
