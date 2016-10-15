import sip, importlib
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
        
        # Open File
        icn = QtGui.QIcon(parent.iconPath+'/file_open.png')
        a=self.addAction(icn,'Open')
        a.setData('open')
        
        # Open With
        icn = QtGui.QIcon(parent.iconPath+'/file_open.png')
        owmenu = QtGui.QMenu('Open With',self)
        owmenu.setIcon(icn)
        self.addMenu(owmenu)
        for e in sorted(parent.editorD):
            icn = ( QtGui.QIcon(parent.editorPath+'/'+e+'/'+e+'.png'))
            a=owmenu.addAction(icn,e)
            a.setData('open_with:'+e)
        
        self.addSeparator()
        
        # Blank Text
        icn = QtGui.QIcon(parent.iconPath+'/files/text.png')
        self.addAction(icn,'text')
        
        # Add Favorites First
        for lang in parent.settings['prog_lang']:
            if not lang in ['default','text'] and parent.settings['prog_lang'][lang]['fave']:
                icn = None
                if os.path.exists(parent.iconPath+'/files/'+lang+'.png'):
                    icn = QtGui.QIcon(parent.iconPath+'/files/'+lang+'.png')
                else:
                    icn = QtGui.QIcon(parent.iconPath+'/files/blank.png')
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
                        icn = QtGui.QIcon(parent.iconPath+'/files/blank.png')
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
        if editor == 'open':
            self.parent.openFile()
        elif editor.startswith('open_with'):
            self.parent.openFile(editor=editor.split(':')[1])
        else:
            if editor == '': editor = None
            self.parent.addEditorWidget(str(event.text()),editor=editor)

class WorkspaceMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('&Workspaces')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'workspace.png'))
        self.loadMenu()
        self.triggered.connect(self.loadWorkspace)
        
        fnt = self.font()
        fnt.setPointSize(11)
        self.setFont(fnt)
    
    def loadMenu(self):
        self.clear()
        self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_add.png'),'New Workspace')
        
        if os.path.exists(self.parent.settingPath+'/workspaces'):
            self.addSeparator()
            for wsp in sorted(os.listdir(self.parent.settingPath+'/workspaces'),key=lambda x: x.lower()):
                self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace.png'),wsp)
                
        self.addSeparator()
        self.saveWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_save.png'),'Save Workspace')
        self.renameWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_edit.png'),'Rename Workspace')
        self.deleteWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_delete.png'),'Delete Workspace')
        
        self.addSeparator()
        self.saveWact.setDisabled(1)
        self.closeWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'close.png'),'Close Current Workspace')
        self.closeWact.setDisabled(1)
    
    def loadWorkspace(self,event):
        if str(event.text()) == 'New Workspace':
            self.parent.workspaceNew()
        elif str(event.text()) == 'Save Workspace':
            self.parent.workspaceSave()
        elif str(event.text()) == 'Close Current Workspace':
            self.parent.workspaceClose(askSave=1,openStart=1)
        elif str(event.text()) == 'Delete Workspace':
            if os.path.exists(self.parent.settingPath+'/workspaces'):
                resp,ok = QtGui.QInputDialog.getItem(self.parent,'Delete Workspace','Select the workspace to delete',QtCore.QStringList(sorted(os.listdir(self.parent.settingPath+'/workspaces'))),editable=0)

                if ok:
                    wksp = str(resp)
                    if wksp in self.parent.workspaces:
                        self.parent.workspaceClose(wksp)
                    os.remove(self.parent.settingPath+'/workspaces/'+str(resp))
                    self.loadMenu()
            else:
                QtGui.QMessageBox.warning(self,'No Workspaces','There are no workspaces to delete')
        elif str(event.text()) == 'Rename Workspace':
            self.parent.workspaceRename()
        else:
            self.parent.workspaceOpen(str(event.text()))
            self.saveWact.setDisabled(0)
            self.closeWact.setDisabled(0)

class EditorMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        
        # Save
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAction = self.addAction(icn,'&Save',self.parent.editorSave)
        self.menuSaveAction.setEnabled(0) # Default to disabled
        
        # Save As
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAsAction = self.addAction(icn,'Save As',self.parent.editorSaveAs)
        self.menuSaveAsAction.setEnabled(0) # Default to disabled
        
        self.addSeparator()
        
##        self.addSeparator()
        
        #---Edit
        emenu = QtGui.QMenu('&Edit',self)
        self.editMenu = emenu
        self.addMenu(emenu)
        
        # Indent
        icn = QtGui.QIcon(self.parent.iconPath+'indent.png')
        emenu.addAction(icn,'Indent (tab)',self.parent.editorIndent)
        
        # UnIndent
        icn = QtGui.QIcon(self.parent.iconPath+'unindent.png')
        emenu.addAction(icn,'Unindent (shift + tab)',self.parent.editorUnindent)
        
        # Comment
        icn = QtGui.QIcon(self.parent.iconPath+'comment.png')
        emenu.addAction(icn,'Comment (Ctrl + E)',self.parent.editorToggleComment)
        
        # Color
        icn = QtGui.QIcon(self.parent.iconPath+'color_swatch.png')
        emenu.addAction(icn,'Insert rgb Color',self.parent.colorPicker)
        
        #---Run
        rmenu = QtGui.QMenu('&Run',self)
        self.runMenu = rmenu
        self.addMenu(rmenu)
        
        # Run
        icn = QtGui.QIcon(self.parent.iconPath+'run.png')
        rmenu.addAction(icn,'Run (F5)',self.parent.editorRun)
        
        # Open External
        icn = QtGui.QIcon(self.parent.iconPath+'file_go.png')
        rmenu.addAction(icn,'Open (external)',self.parent.openFileExternal)
        
        # Compile
        icn = QtGui.QIcon(self.parent.iconPath+'compile.png')
        rmenu.addAction(icn,'Compile (F6)',self.parent.editorCompile)
        
        #---View
        vmenu = QtGui.QMenu('&View',self)
        self.viewMenu = vmenu
        self.addMenu(vmenu)
        # Whitespace
        icn = QtGui.QIcon(self.parent.iconPath+'whitespace.png')
        self.whitespaceAction = vmenu.addAction(icn,'Toggle Whitespace',self.parent.editorToggleWhitespace)
        
        # Wordwrap
        icn = QtGui.QIcon(self.parent.iconPath+'wordwrap.png')
        self.wordwrapAction = vmenu.addAction(icn,'Toggle Wordwrap (Ctrl+W)',self.parent.editorWordWrap)
        
        vmenu.addSeparator()
        
        # Stats
        icn = QtGui.QIcon()
        self.statsAction = vmenu.addAction(icn,'Statistics (Alt+S)',self.parent.editorStats)
        
        #---Window
        self.windowMenu=QtGui.QMenu('&Window',self)
        self.addMenu(self.windowMenu)
        
        icn = QtGui.QIcon(self.parent.iconPath+'left_pane.png')
        self.windowMenu.addAction(icn,'Toggle Left Pane (F2)',self.parent.toggleLeftPlugin)
        
        icn = QtGui.QIcon(self.parent.iconPath+'right_pane.png')
        self.windowMenu.addAction(icn,'Toggle Right Pane (F3)',self.parent.toggleRightPlugin)
        
        icn = QtGui.QIcon(self.parent.iconPath+'bottom_pane.png')
        self.windowMenu.addAction(icn,'Toggle Bottom Pane (F4)',self.parent.toggleBottomPlugin)
        
        icn = QtGui.QIcon()
        self.windowMenu.addAction(icn,'Toggle Toolbar',self.parent.toggleToolbar)
        
        self.windowMenu.addSeparator()
        
        # Full Editor Mode
        icn = QtGui.QIcon(self.parent.iconPath+'full_editor.png')
        self.fullEditorAction = self.windowMenu.addAction(icn,'Full Editor Mode (F10)',self.parent.toggleFullEditor)
        
        # Full Screen
        icn = QtGui.QIcon(self.parent.iconPath+'fullscreen.png')
        self.fullScreenAction = self.windowMenu.addAction(icn,'Full Screen (F11)',self.parent.toggleFullscreen)

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
        self.addAction(icn,'E&xit Scope',self.parent.close)
