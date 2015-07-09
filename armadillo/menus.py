import sip
##sip.setapi('QString',1)
sip.setapi('QVariant',1)

import os,sys
from PyQt4 import QtCore, QtGui


class NewMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('&New')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'new.png'))
        
        icn = QtGui.QIcon(parent.iconPath+'/files/text.png')
        self.addAction(icn,'text')
        self.addSeparator()
        
        # Add Favorites First
        for lang in parent.settings['prog_lang']:
            if not lang in ['default','text'] and parent.settings['prog_lang'][lang]['fave']:
                icn = None
                if os.path.exists(parent.iconPath+'/files/'+lang+'.png'):
                    icn = QtGui.QIcon(parent.iconPath+'/files/'+lang+'.png')
                else:
                    icn = QtGui.QIcon(parent.iconPath+'/files/_blank.png')
                self.addAction(icn,lang)
        
        self.addSeparator()
        
        # Add Editor languages
        for e in sorted(parent.editorD):
            ld = parent.editorD[e]
            if ld != []:
                lmenu = QtGui.QMenu(e,self)
                for l in ld:
                    if os.path.exists(parent.iconPath+'/files/'+l.lower()+'.png'):
                        icn = QtGui.QIcon(parent.iconPath+'/files/'+l.lower()+'.png')
                    else:
                        icn = QtGui.QIcon(parent.iconPath+'/files/_blank.png')
                    a=lmenu.addAction(icn,l)
                    a.setData(e)
                self.addMenu(lmenu)
                lmenu.setIcon( QtGui.QIcon(parent.editorPath+'/'+e+'/'+e+'.png'))
            else:
                icn = QtGui.QIcon(parent.editorPath+'/'+e+'/'+e+'.png')
                a=self.addAction(icn,e)
                a.setData(e)
    
        self.triggered.connect(self.newEditor)
    
    def newEditor(self,event):
        editor = str(event.data().toString())
        if editor == '': editor = None
        self.parent.addEditorWidget(str(event.text()),editor=editor)
##        self.parent.removeStart()

class WorkspaceMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('&Workspaces')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'workspace.png'))
        self.loadMenu()
        self.triggered.connect(self.loadWorkspace)
    
    def loadMenu(self):
        self.clear()
        self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_add.png'),'New Workspace')
        self.saveWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_save.png'),'Save Workspace')
        self.saveWact.setDisabled(1)
        
        if os.path.exists(self.parent.settingPath+'/workspaces'):
            self.addSeparator()
            for wsp in sorted(os.listdir(self.parent.settingPath+'/workspaces'),key=lambda x: x.lower()):
                self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace.png'),wsp)
                
        self.addSeparator()
        self.renameWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_edit.png'),'Rename Workspace')
        self.deleteWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_delete.png'),'Delete Workspace')
        
        self.addSeparator()
        self.closeWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'close.png'),'Close Current Workspace')
        self.closeWact.setDisabled(1)
    
    def loadWorkspace(self,event):
        if str(event.text()) == 'New Workspace':
            self.parent.newWorkspace()
        elif str(event.text()) == 'Save Workspace':
            self.parent.saveWorkspace()
        elif str(event.text()) == 'Close Current Workspace':
            self.parent.closeWorkspace(askSave=1,openStart=1)
        elif str(event.text()) == 'Delete Workspace':
            if os.path.exists(self.parent.settingPath+'/workspaces'):
                resp,ok = QtGui.QInputDialog.getItem(self.parent,'Delete Workspace','Select the workspace to delete',QtCore.QStringList(sorted(os.listdir(self.parent.settingPath+'/workspaces'))),editable=0)

                if ok:
                    os.remove(self.parent.settingPath+'/workspaces/'+str(resp))
                    if str(resp) == self.parent.currentWorkspace:
                        self.parent.currentWorkspace=None
                    self.loadMenu()
            else:
                QtGui.QMessageBox.warning(self,'No Workspaces','There are no workspaces to delete')
        elif str(event.text()) == 'Rename Workspace':
            if os.path.exists(self.parent.settingPath+'/workspaces'):
                resp,ok = QtGui.QInputDialog.getItem(self.parent,'Rename Workspace','Select the workspace to rename',QtCore.QStringList(sorted(os.listdir(self.parent.settingPath+'/workspaces'))),editable=0)

                if ok:
                    owskp=str(resp)
                    pth = self.parent.settingPath+'/workspaces/'+owskp
                    resp,ok = QtGui.QInputDialog.getText(self,'Rename Workspace','Enter Workspace Name',QtGui.QLineEdit.Normal,str(owskp))
                    if ok and not resp.isEmpty():
                        npth = self.parent.settingPath+'/workspaces/'+str(resp)
                        os.rename(pth,npth)
                        self.loadMenu()
                        if owskp == self.parent.workspace:
                            self.parent.workspace=str(resp)
            else:
                QtGui.QMessageBox.warning(self,'No Workspaces','There are no workspaces to delete')
        else:
            self.parent.loadWorkspace(str(event.text()))
            self.saveWact.setDisabled(0)
            self.closeWact.setDisabled(0)

class ArmadilloMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        # New
        self.addMenu(self.parent.newMenu)
        
        # Open
        icn = QtGui.QIcon(self.parent.iconPath+'file_open.png')
        act = self.addAction(icn,'&Open',self.parent.openFile)
        
        # Save
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAction = self.addAction(icn,'&Save',self.parent.editorSave)
        self.menuSaveAction.setEnabled(0) # Default to disabled
        
        # Save As
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAsAction = self.addAction(icn,'Save As',self.parent.editorSaveAs)
        self.menuSaveAsAction.setEnabled(0) # Default to disabled
        
        self.addSeparator()
        
        # Workspace
        self.addMenu(self.parent.workspaceMenu)
        
        #---Editor
        self.editorMenu=QtGui.QMenu('&Editor')
        self.addMenu(self.editorMenu)
        
        # Tab Indent
        icn = QtGui.QIcon(self.parent.iconPath+'indent.png')
        self.indentAction = self.editorMenu.addAction(icn,'Indent',self.parent.editorIndent)
        icn = QtGui.QIcon(self.parent.iconPath+'indent_remove.png')
        self.unindentAction = self.editorMenu.addAction(icn,'Unindent',self.parent.editorUnindent)
        
        self.editorMenu.addSeparator()
        
        # Comment
        icn = QtGui.QIcon(self.parent.iconPath+'comment.png')
        self.commentAction = self.editorMenu.addAction(icn,'Comment/Uncomment',self.parent.editorToggleComment)
        
        # Whitespace
        icn = QtGui.QIcon(self.parent.iconPath+'whitespace.png')
        self.whitespaceAction = self.editorMenu.addAction(icn,'Toggle Whitespace',self.parent.editorToggleWhitespace)
        
        # Wordwrap
        icn = QtGui.QIcon(self.parent.iconPath+'wordwrap.png')
        self.wordwrapAction = self.editorMenu.addAction(icn,'Toggle Wordwrap',self.parent.editorWordWrap)
        
        self.editorMenu.addSeparator()
        
        # Run
        icn = QtGui.QIcon(self.parent.iconPath+'tri_right.png')
        self.runAction = self.editorMenu.addAction(icn,'Run (F5)',self.parent.editorRun)
        
        self.editorMenu.addSeparator()
        
        # Stats
        icn = QtGui.QIcon()
        self.statsAction = self.editorMenu.addAction(icn,'Statistics',self.parent.editorStats)
        
        #---Window
        self.viewMenu=QtGui.QMenu('W&indow')
        self.addMenu(self.viewMenu)
        
        icn = QtGui.QIcon(self.parent.iconPath+'left_pane.png')
        self.viewMenu.addAction(icn,'Toggle Left Pane (F4)',self.parent.toggleLeftPlugin)
        
        icn = QtGui.QIcon(self.parent.iconPath+'right_pane.png')
        self.viewMenu.addAction(icn,'Toggle Right Pane (F8)',self.parent.toggleRightPlugin)
        
        icn = QtGui.QIcon(self.parent.iconPath+'bottom_pane.png')
        self.viewMenu.addAction(icn,'Toggle Bottom Pane (F9)',self.parent.toggleBottomPlugin)
        
        self.viewMenu.addSeparator()
        
        # Full Editor Mode
        icn = QtGui.QIcon(self.parent.iconPath+'full_editor.png')
        self.fullEditorAction = self.viewMenu.addAction(icn,'Full Editor Mode (F10)',self.parent.toggleFullEditor)
        
        # Full Screen
        icn = QtGui.QIcon(self.parent.iconPath+'fullscreen.png')
        self.fullScreenAction = self.viewMenu.addAction(icn,'Full Screen (F11)',self.parent.toggleFullscreen)
        
        # Home
        icn = QtGui.QIcon(self.parent.iconPath+'home.png')
        act = self.addAction(icn,'&Home',self.parent.showHUD)
        
        # Settings
        icn = QtGui.QIcon(self.parent.iconPath+'wrench.png')
        act = self.addAction(icn,'Se&ttings',self.parent.openSettings)
        
        self.addSeparator()
        
        # Check for file changes
        icn = QtGui.QIcon()
        act = self.addAction(icn,'&Check file changes',self.parent.checkFileChanges)

        # -----
        # Print
        self.addSeparator()
        icn = QtGui.QIcon(self.parent.iconPath+'printer.png')
        self.printAction = self.addAction(icn,'Print',self.parent.editorPrint)
        
        # Close
        self.addSeparator()
        icn = QtGui.QIcon(self.parent.iconPath+'close.png')
        self.addAction(icn,'Exit',self.parent.close)