# --------------------------------------------------------------------------------
# Armadillo IDE
# Copyright 2013-2014 Cole Hagen
#
# Armadillo is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

# VERSION
__version__ = '1.5.1'


import sys, json, codecs, time, importlib
from PyQt4 import QtCore, QtGui, QtWebKit
from armadillo_ui import Ui_Form
import os,shutil,datetime, webbrowser, threading

class Events(QtCore.QObject):
    editorAdded = QtCore.pyqtSignal(QtGui.QWidget)
    editorTabChanged = QtCore.pyqtSignal(QtGui.QWidget)
    editorSaved = QtCore.pyqtSignal(QtGui.QWidget)
    editorVisibleLinesChanged = QtCore.pyqtSignal(QtGui.QWidget,tuple)
    close=QtCore.pyqtSignal()
    editorTabClosed = QtCore.pyqtSignal(QtGui.QWidget)
    
class NewMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('New')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'new.png'))
        
        # Add Favorites First
        for lang in sorted(parent.settings['prog_lang']):
            if lang != 'default':
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
        self.parent.removeStart()

class WorkspaceMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('Workspaces')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'workspace.png'))
        self.loadMenu()
        self.triggered.connect(self.loadWorkspace)
    
    def loadMenu(self):
        self.clear()
        self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_add.png'),'New Workspace')
        self.saveWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_save.png'),'Save Workspace')
        self.saveWact.setDisabled(1)
        self.closeWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'close.png'),'Close Current Workspace')
        self.closeWact.setDisabled(1)
        self.addSeparator()
        self.deleteWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_delete.png'),'Delete Workspace')
    
        if os.path.exists(self.parent.settingPath+'/workspaces'):
            self.addSeparator()
            for wsp in sorted(os.listdir(self.parent.settingPath+'/workspaces'),key=lambda x: x.lower()):
                self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace.png'),wsp)
                self.deleteWact.setDisabled(0)
    
    def loadWorkspace(self,event):
        if str(event.text()) == 'New Workspace':
            self.parent.newWorkspace()
        elif str(event.text()) == 'Save Workspace':
            self.parent.saveWorkspace()
        elif str(event.text()) == 'Close Current Workspace':
            self.parent.closeWorkspace(askSave=1,openStart=1)
        elif str(event.text()) == 'Delete Workspace':
            resp,ok = QtGui.QInputDialog.getItem(self.parent,'Delete Workspace','Select the workspace to delete',QtCore.QStringList(sorted(os.listdir(self.parent.settingPath+'/workspaces'))),editable=0)

            if ok:
                os.remove(self.parent.settingPath+'/workspaces/'+str(resp))
                if str(resp) == self.parent.workspace:
                    self.parent.workspace=None
                self.loadMenu()
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
        
        # Workspace
        self.addMenu(self.parent.workspaceMenu)
        
        # Open
        icn = QtGui.QIcon(self.parent.iconPath+'file_open.png')
        act = self.addAction(icn,'Open',self.parent.openFile)
        
        # Save
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAction = self.addAction(icn,'Save',self.parent.editorSave)
        self.menuSaveAction.setEnabled(0) # Default to disabled
        
        # Save As
        icn = QtGui.QIcon(self.parent.iconPath+'save.png')
        self.menuSaveAsAction = self.addAction(icn,'Save As',self.parent.editorSaveAs)
        self.menuSaveAsAction.setEnabled(0) # Default to disabled
        
        self.addSeparator()
        
        # Plugins
##        plugmenu = self.parent.createPopupMenu()
##        plugmenu.setTitle('Plugins')
##        plugmenu.setIcon(QtGui.QIcon(self.parent.iconPath+'plugin.png'))
##        self.addMenu(plugmenu)
        
        #---Editor
        self.editorMenu=QtGui.QMenu('Editor')
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
        self.viewMenu=QtGui.QMenu('Window')
        self.addMenu(self.viewMenu)
        
        icn = QtGui.QIcon(self.parent.iconPath+'left_pane.png')
        self.viewMenu.addAction(icn,'Toggle Left Pane (F4)',self.parent.toggleLeftPlugin)
        icn = QtGui.QIcon(self.parent.iconPath+'bottom_pane.png')
        self.viewMenu.addAction(icn,'Toggle Bottom Pane (F9)',self.parent.toggleBottomPlugin)
        
        icn = QtGui.QIcon(self.parent.iconPath+'right_pane.png')
        self.viewMenu.addAction(icn,'Toggle Right Pane (F8)',self.parent.toggleRightPlugin)
        
        self.viewMenu.addSeparator()
        
        # Full Editor Mode
        icn = QtGui.QIcon(self.parent.iconPath+'full_editor.png')
        self.fullEditorAction = self.viewMenu.addAction(icn,'Full Editor Mode (F10)',self.parent.toggleFullEditor)
        
        # Full Screen
        icn = QtGui.QIcon(self.parent.iconPath+'fullscreen.png')
        self.fullScreenAction = self.viewMenu.addAction(icn,'Full Screen (F11)',self.parent.toggleFullscreen)
        
        # Home
        icn = QtGui.QIcon(self.parent.iconPath+'home.png')
        act = self.addAction(icn,'Home',self.parent.addStart)
        
        # Settings
        icn = QtGui.QIcon(self.parent.iconPath+'wrench.png')
        act = self.addAction(icn,'Settings',self.parent.openSettings)
        
        self.addSeparator()
        
        # Check for file changes
        icn = QtGui.QIcon()
        act = self.addAction(icn,'Check file changes',self.parent.checkFileChanges)

        # -----
        # Print
        self.addSeparator()
        icn = QtGui.QIcon(self.parent.iconPath+'printer.png')
        self.printAction = self.addAction(icn,'Print',self.parent.editorPrint)
        
        # Close
        self.addSeparator()
        icn = QtGui.QIcon(self.parent.iconPath+'close.png')
        self.addAction(icn,'Exit',self.parent.close)
        
class Armadillo(QtGui.QWidget):
    def __init__(self, parent=None):

        # Version
        self.version = __version__

        # Setup UI
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #--- Paths
        self.iconPath=os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/img/'
        self.settingPath = os.path.expanduser('~').replace('\\','/')+'/.armadillo'
        self.pluginPath = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/plugins/'
        self.editorPath = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/editors/'
        
        # Settings
        self.workspace = None
        self.loadSettings()
##        self.startinit = 1
        self.fileLastCheck = time.time()
        QtGui.QApplication.setStyle(self.settings['widgetstyle'])
        
        self.setAcceptDrops(1)
        
##        # Filesystem watercher - NOT USED CAUSE TO MANY SIGNALS FIRE OFF
##        self.filesystemwatcher = QtCore.QFileSystemWatcher(self)
##        self.filesystemwatcher.fileChanged.connect(self.file_changed)
        
        # Style
        style_path = 'styles/'+self.settings['style']+'.style'
        if not os.path.exists(style_path):
            style_path = 'styles/default.style'
        f = open(style_path,'r')
        style = f.read()
        f.close()
        self.setStyleSheet(style)
        
        #--- Window Setup
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        coords= QtGui.QApplication.desktop().screenGeometry(screen).getCoords() 
        if self.settings['window']['openMode']=='1':
            # get margins from settings
            dl=int(self.settings['window']['margin']['left'])
            dr=int(self.settings['window']['margin']['right'])
            dt=int(self.settings['window']['margin']['top'])
            db=int(self.settings['window']['margin']['bottom'])
            
            # set up width and height
            ws=coords[2]-coords[0] # screen width
            hs=coords[3]-coords[1] # screen height
            wd = self.settings['window']['size']['width'].strip()
            hd = self.settings['window']['size']['height'].strip()
            if wd.endswith('%'):
                w=float(wd[:-1])/100.0*ws
            else:
                try:
                    w=int(wd)
                except:
                    w=ws
            if hd.endswith('%'):
                h=float(hd[:-1])/100.0*hs
            else:
                try:
                    h=int(hd)
                except:
                    h=hs
            # Almost full screen
##            dx = 50
            self.setGeometry(coords[0]+dl,coords[1]+dt,(w-dl-dr),(h-dt-db))
            QtGui.QApplication.processEvents()
        elif self.settings['window']['openMode']=='2':
            # Fullscreen
            self.showMaximized()
##            self.setGeometry(coords[0]+dx,coords[1]+dx,(coords[2]-coords[0]-2*dx),(coords[3]-coords[1]-2*dx))
            QtGui.QApplication.processEvents()
            
        # Setup plugin views
        # Bottom
        h=int(self.settings['window']['pluginBottom']['height'])
        self.ui.split_bottom.setSizes([self.height()-h,h])
        if self.settings['window']['pluginBottom']['visible']!='1':
            self.ui.sw_bottom.setHidden(1)
        
        # Left
        lw=int(self.settings['window']['pluginLeft']['width'])
        self.ui.split_left.setSizes([lw,self.width()-lw])
        if self.settings['window']['pluginLeft']['visible']!='1':
            self.ui.fr_left.setVisible(0)
        
        # Right
        rw=self.settings['window']['pluginRight']['width']
        if rw.endswith('%'):
            rw = float(rw[:-1])/100*(self.width()-lw)
        else:
            rw=int(rw)
        
        self.ui.split_right.setSizes([self.width()-rw-lw,rw])
        if self.settings['window']['pluginRight']['visible']!='1':
            self.ui.tab_right.setVisible(0)

        # Tab Direction
        tabLocD = {'top':QtGui.QTabWidget.North,'bottom':QtGui.QTabWidget.South}
        self.ui.tab_left.setTabPosition(tabLocD[self.settings['window']['pluginLeft']['tabPosition']])
        self.ui.tab_right.setTabPosition(tabLocD[self.settings['window']['pluginRight']['tabPosition']])

        # File Tabs
        self.ui.tab = QtGui.QTabBar()
        self.ui.tab.setObjectName('editorTabs')
        self.ui.tab.setTabsClosable(True)
        self.ui.tab.setMovable(True)
        self.ui.tab.setProperty("class","editorTabs")
        self.ui.tab.setObjectName('editorTabBar')
        self.ui.tab.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
        self.ui.fr_tabs.layout().addWidget(self.ui.tab)
        self.ui.tab.currentChanged.connect(self.changeTab)
        self.ui.tab.tabCloseRequested.connect(self.closeTab)
        self.ui.tab.setExpanding(0)
        
        #--- Signals
        self.ui.b_open.clicked.connect(self.openFile)
        self.ui.b_save.clicked.connect(self.editorSave)

        self.ui.b_indent.clicked.connect(self.editorIndent)
        self.ui.b_unindent.clicked.connect(self.editorUnindent)
        self.ui.b_comment.clicked.connect(self.editorToggleComment)
        
##        self.ui.b_whitespace.clicked.connect(self.editorToggleWhitespace)
        
        self.ui.b_run.clicked.connect(self.editorRun)
##        self.ui.b_wordwrap.clicked.connect(self.editorWordWrap)
        self.ui.b_settings.clicked.connect(self.openSettings)
        self.ui.b_help.clicked.connect(self.addStart)
        
        self.ui.b_find.clicked.connect(self.editorFind)
        self.ui.le_goto.returnPressed.connect(self.editorGoto)

        # Editor Signals
        self.evnt = Events()
        self.tabD={}
        
        #--- Key Shortcuts
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_E,self,self.editorToggleComment) #Toggle Comment
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F,self,self.findFocus) # Find
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_G,self,self.gotoFocus) # Goto
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_N,self,self.ui.b_new.click) # New
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Q,self,self.qtHelp) # Qt Help
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_R,self,self.replaceFocus) # Replace
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_S,self,self.editorSave) # Save
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_W,self,self.editorWordWrap) # Toggle Wordwrap
        
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Tab,self,self.nextTab) # Toggle Wordwrap

        QtGui.QShortcut(QtCore.Qt.Key_F1,self,self.addStart) # Add Start Page
        QtGui.QShortcut(QtCore.Qt.Key_F2,self,self.viewFileBrowser) # View Filebrowser
        QtGui.QShortcut(QtCore.Qt.Key_F3,self,self.updateOutline) # Update Outline
        QtGui.QShortcut(QtCore.Qt.Key_F4,self,self.toggleLeftPlugin) # Toggle Left Plugin
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F4,self,self.nextLeftPlugin) # show next left plugin
        QtGui.QShortcut(QtCore.Qt.Key_F5,self,self.editorRun) # Run
        QtGui.QShortcut(QtCore.Qt.Key_F7,self,self.toggleRightPluginFull) # Toggle Hide editor
        QtGui.QShortcut(QtCore.Qt.Key_F8,self,self.toggleRightPlugin) # Toggle RIght Plugins
        QtGui.QShortcut(QtCore.Qt.Key_F9,self,self.toggleBottomPlugin) # Hide Bottom Tab
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F9,self,self.nextBottomPlugin) # Show next bottom tab
        
        QtGui.QShortcut(QtCore.Qt.Key_F10,self,self.toggleFullEditor) # Editor full screen, but keep tabs
        QtGui.QShortcut(QtCore.Qt.Key_F11,self,self.toggleFullscreen) # Fullscreen Zen
##        QtGui.QShortcut(QtCore.Qt.Key_F12,self,self.viewPythonShell) # Fullscreen Zen
        
        # File Dictionary
        self.fileCount = -1
        
        #--- Get Editor Languages
        self.editorD = {}
        
        for e in self.settings['activeEditors']:
            
            try:
                mod = importlib.import_module('editors.'+e)
                ld = mod.getLang()
            except:
                QtGui.QMessageBox.warning(self,'Failed to Load Editor','The editor, '+e+' failed to load')
                ld = []
            
            if ld != []:
                self.editorD[e] = ld

                for l in ld:
                    if l not in self.settings['extensions']:
                        self.settings['extensions'][l]=l
        
        #--- Plugins
        # Plugin tab bar
##        self.ui.fr_left_hidden.hide()
        self.ui.tabbar_bottom = QtGui.QTabBar()
        self.ui.fr_bottom.layout().addWidget(self.ui.tabbar_bottom)
        self.ui.tabbar_bottom.currentChanged.connect(self.pluginBottomChange)
        self.ui.tabbar_bottom.setShape(1)
        self.ui.tabbar_bottom.setExpanding(0)
        # Add down arrow
        self.ui.tabbar_bottom.addTab(QtGui.QIcon(self.iconPath+'tri_down.png'),'')
        
        # Add Plugins
        self.pluginD = {}
        self.prevPlugin=1
        curdir = os.path.abspath('.')
        for plug in self.settings['activePlugins']:
            self.addPlugin(plug)
        os.chdir(curdir)
        self.ui.tabbar_bottom.setCurrentIndex(0)
        
        #--- Other Setup
        # Default zen mode
        self.fullscreen_mode = 0
        self.editor_fullmode = 0
        
        # Load FileCheck Thread
        self.fileLastCheck = time.time()
##        self.fileModD = {}
##        fmt = threading.Thread(target=self.checkFileChanges,args=(self))
##        fmt.start()

        # New Button Menu
        self.newMenu = NewMenu(self)
        self.ui.b_new.setMenu(self.newMenu)
        
        # Workspace Button Menu
        self.workspaceMenu = WorkspaceMenu(self)
        self.ui.b_workspace.setMenu(self.workspaceMenu)
        
        # add Main Button to tabbar
        self.armadilloMenu = ArmadilloMenu(self)
        self.ui.b_main.setMenu(self.armadilloMenu)
        
##        # Load custom setup
##        self.loadSetup()
        
        # Add Start
        self.addStart()
        
        # Open file if in sys arg
        # print "SYS",sys.argv
        if len(sys.argv)>1:
            if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
                self.openFile(sys.argv[1])
        
        self.setFocus()
        
    #---Events
    def closeEvent(self,event):
        cancelled = 0
        # Check if anything needs saving
        for i in range(self.ui.tab.count()):
            file_id = self.ui.tab.tabData(i).toInt()[0]
            wdg = self.tabD[file_id]
            ok = self.checkSave(wdg)
            if not ok:
                cancelled = 1
                break

        if cancelled:
            event.ignore()
        else:
            # Save Settings
            self.saveSettings()
            
            # Other Events
            self.evnt.close.emit()

    def dropEvent(self,event):
        handled=False
        if event.mimeData().urls():
            for f in event.mimeData().urls():
                self.openFile(str(f.toLocalFile()))
            handled=True

        if not handled:
            QtGui.QWidget.dropEvent(self,event)

    def dragEvent(self,event):
        event.accept()
    
    def dragEnterEvent(self,event):
        event.accept()
    
    #---Fullscreen Modes
    def toggleFullEditor(self):
        self.editor_fullmode = not self.editor_fullmode
        zen=self.editor_fullmode
        self.ui.l_statusbar.setVisible(not zen)
        self.ui.fr_toolbar.setVisible(not zen)
        self.ui.fr_left.setVisible(not zen)
        self.ui.sw_bottom.setVisible(not zen)
        self.ui.fr_bottom.setVisible(not zen)
        self.ui.tab_right.setVisible(not zen)
        if zen:
            self.pluginBottomChange(0)
        else:
            self.pluginBottomChange(self.ui.tabbar_bottom.currentIndex())
        
        if self.editor_fullmode:
            self.armadilloMenu.fullEditorAction.setText('Exit Full Editor Mode')
        else:
            self.armadilloMenu.fullEditorAction.setText('Full Editor Mode (F10)')
            
    def toggleFullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        if self.fullscreen_mode:
            self.showFullScreen()
            self.editor_fullmode=0
            self.toggleFullEditor()
            self.armadilloMenu.fullScreenAction.setText('Exit Full Screen Mode (F11)')
        else:
            self.armadilloMenu.fullScreenAction.setText('Full Screen (F11)')
            self.showNormal()
            if self.editor_fullmode:
                self.toggleFullEditor()

    #---File
    def isFileOpen(self,filename):
        # Check if file open and return tab index
        fileopen = -1
        for i in range(self.ui.tab.count()):
            file_id = self.ui.tab.tabData(i).toInt()[0]
            wdg = self.tabD[file_id]
            if wdg.filename != None and os.path.abspath(wdg.filename) == os.path.abspath(filename):
                self.ui.tab.setCurrentIndex(i)
                fileopen = i
                break
        return fileopen
        
    def openFile(self,filename=None,editor=None):
        if not filename:
            # Ask for filename if not specified
            filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",self.pluginD['filebrowser'].ui.le_root.text()," (*.*)")
            if filename=='':
                filename = None
            else:
                filename = str(filename)
        if filename != None:
            if os.path.isfile(filename):
                # Check if file already open
                file_open = self.isFileOpen(filename)
                if file_open !=-1:
                    self.ui.tab.setCurrentIndex(file_open)
##                    self.updateOutline()
                else:
                    ext = os.path.splitext(str(filename))[1][1:]
                    lang = ext

                    if ext in self.settings['extensions']:
                        lang = self.settings['extensions'][ext]
                    
                    # Load Image
                    if lang in ['png','jpg','bmp','gif','ico']:
                        w = self.ui.sw_main.width()-20
                        if os.name =='nt':
                            pfx="file:///"
                        else:
                            pfx="file://"
                        pth=pfx+os.path.abspath(filename).replace('\\','/')
                        html='<img src="'+pth+'" style="max-width:'+str(w)+';">'
                        self.webview_preview(html,filename)
                    else:
                        title = os.path.basename(filename)
                        if int(self.settings['view_folder']):
                            title = os.path.split(os.path.dirname(filename))[1]+'/'+title
                        elif lang == 'python' and title=='__init__.py':
                            title = os.path.split(os.path.dirname(filename))[1]+'/init'
                        
                        try:
                            f = codecs.open(filename,'r','utf-8')
                            txt = f.read()
                            f.close()
                            
                        except:
                            QtGui.QMessageBox.warning(self,'Error Opening File','The following file could not be read.  Make sure it is ascii or utf-8 encoded<br><br>'+filename)
                            txt = None
                        
                        if txt != None:
                            # Create Widget
                            wdg = self.addEditorWidget(lang,title,str(filename),editor=editor,code=txt)
                            wdg.setText(txt)
                            QtGui.QApplication.processEvents()
                            wdg.lastText = txt
                            self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
                            wdg.modTime = os.path.getmtime(filename)
                        
    ##                    self.filesystemwatcher.addPath(filename)
    ##                    self.fileModD[filename]=os.path.getmtime(filename)
                        self.updateOutline()
     
                        # Remove Startpage
                        self.removeStart()

        
    #---Editor
    def currentEditor(self):
        return self.ui.sw_main.currentWidget()

    def changeTab(self,tab_ind):
        self.ui.l_statusbar.setText('')

        if tab_ind == -1 and self.ui.tab.count()>0: tab_ind == 0
        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
        if file_id in self.tabD:
            wdg = self.tabD[file_id]
            self.ui.sw_main.setCurrentWidget(wdg)
            self.evnt.editorTabChanged.emit(wdg)
            
            # Show/Hide plugins
            lang = wdg.lang
        else:
            wdg = None
            lang = None

        # Enable Run
        run_enabled=0
        if lang in self.settings['run']:
            run_enabled = lang in self.settings['run']
            
        self.ui.b_run.setEnabled(run_enabled)
        self.armadilloMenu.runAction.setEnabled(run_enabled)
        
        # Disable buttons based on function availability
        btnD = [
            ['indent',self.armadilloMenu.indentAction],
            ['indent',self.ui.b_indent],
            ['unindent',self.ui.b_unindent],
            ['unindent',self.armadilloMenu.unindentAction],
            ['find',self.ui.fr_find],
            ['toggleComment',self.ui.b_comment],
            ['toggleComment',self.armadilloMenu.commentAction],
            ['getText',self.ui.b_save],
            ['toggleWordWrap',self.armadilloMenu.wordwrapAction],
            ['toggleWhitespace',self.armadilloMenu.whitespaceAction],
            ['getText',self.armadilloMenu.statsAction],
            
##            'toggleWordWrap':self.ui.b_wordwrap,
##            'toggleWhitespace':self.ui.b_whitespace,
        ]
        for btn in btnD:
            btn[1].setEnabled(btn[0] in dir(wdg))
        
        try:
            self.armadilloMenu.menuSaveAction.setEnabled('getText' in dir(wdg))
            self.armadilloMenu.menuSaveAsAction.setEnabled('getText' in dir(wdg))
        except:
            pass
        
        # Hide Right side
        pluginRightVisible=0
        if wdg != None:
            pluginRightVisible = wdg.pluginRightVisible
        if pluginRightVisible != self.ui.tab_right.isVisible():
            self.toggleRightPlugin()
        
            # Check for file changes (Disabled for now)
##            self.checkFileChanges()
                
            
    def closeTab(self,tab_ind):
        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
        wdg = self.tabD[file_id]
        ok = 1
        
        # Check Save
        if 'getText' in dir(wdg):
            ok = self.checkSave(wdg)
                
        if ok:
            # Emit close signal
            self.evnt.editorTabClosed.emit(wdg)
            
            self.tabD.pop(file_id)
            # Remove Tab
            self.ui.tab.removeTab(tab_ind)
            # Remove Widget
            self.ui.sw_main.removeWidget(wdg)

            # Add start page if no tabs exist
##            if self.ui.sw_main.count() == 0:
##                self.addStart()

    def editorTextChanged(self):
        # Indicate if text changed
        wdg = self.currentEditor()
        try:
            if wdg.lastText != wdg.getText():
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title+'*')
            else:
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
        except:
            self.ui.l_statusbar.setText('Error: text changed signal')
        # Check for file changes
##        self.checkFileChanges()
    
    def visibleLinesChanged(self,wdg,lines):
        self.evnt.editorVisibleLinesChanged.emit(wdg,lines)
    
    def addEditorWidget(self,lang=None,title='New',filename=None,editor=None,code=''):
        self.fileCount+=1
        sw_ind = self.ui.sw_main.count()
        wdg = None
        
        if filename == None and title=='New': title = 'New '+lang
        
        if editor == None:
            if lang in self.settings['prog_lang']:
                editor = self.settings['prog_lang'][lang]['editor']
            if editor == None:
                if lang == 'webview':
                    editor = 'webview'
                elif lang == 'settings':
                    editor = 'settings'
                else:
                    editor = self.settings['prog_lang']['default']['editor']
                    
                    if lang not in self.editorD[editor]:
                        for e in self.editorD:
                            if lang in self.editorD[e]:
                                editor = e
                                break
        
        # Load Editors
        mod = importlib.import_module("editors."+editor)
        wdg = mod.addEditor(self,lang,filename)

        wdg.filename = filename
        wdg.lastText=''
##        wdg.lastText=code
        wdg.title = title
        wdg.id = self.fileCount
        wdg.lang = lang
        wdg.viewOnly = 0
        wdg.editor = editor
        wdg.pluginRightVisible=0
##        wdg.setText(code)
        if lang=='Start':wdg.editor='Start'
        wdg.modTime = None
        self.tabD[self.fileCount]=wdg
        self.evnt.editorAdded.emit(wdg)

        if 'editorTextChanged' in dir(wdg):
            wdg.evnt.editorChanged.connect(self.editorTextChanged)
        if 'visibleLinesChanged' in dir(wdg):
            wdg.evnt.visibleLinesChanged.connect(self.visibleLinesChanged)
            
##        if 'editingFinished' in  dir(wdg):
##            wdg.evnt.editingFinished.connect(self.editingFinished)
            
        # Insert widget to page
        self.ui.sw_main.insertWidget(sw_ind,wdg)
        self.ui.sw_main.setCurrentIndex(sw_ind)
        
        # Insert Tab on top
        self.ui.tab.insertTab(sw_ind+1,title)
        self.ui.tab.setTabData(sw_ind,self.fileCount)
        self.ui.tab.setCurrentIndex(sw_ind)
        self.ui.tab.setTabToolTip(sw_ind,str(filename))
        
        # Add Icon
        ipth = self.iconPath+'/files/_blank.png'
        icn = QtGui.QIcon(ipth)
        ipth = self.iconPath+'files/'+str(lang)+'.png'
        if os.path.exists(ipth):
            icn = QtGui.QIcon(ipth)
        elif filename != None:
            ext = os.path.splitext(filename)[1][1:]
            if os.path.exists(self.iconPath+'files/'+ext+'.png'):
                icn = QtGui.QIcon(self.iconPath+'files/'+ext+'.png')
        elif os.path.exists(self.editorPath+editor+'/'+editor+'.png'):
            icn = QtGui.QIcon(self.editorPath+editor+'/'+editor+'.png')
        self.ui.tab.setTabIcon(sw_ind,icn)
        wdg.icon = icn

        # Set wordwrap if in settings
        QtGui.QApplication.processEvents()
        if lang in self.settings['prog_lang']:
            if 'wordwrap' in self.settings['prog_lang'][lang]:
                wdg.wordwrapmode = int(self.settings['prog_lang'][lang]['wordwrap'])
                self.editorWordWrap()
        
            # Set Autocomplete Toggle
            if 'autocomplete' in self.settings['prog_lang'][lang]:
                wdg.autocomplete = int(self.settings['prog_lang'][lang]['autocomplete'])
                if 'toggleAutoComplete' in dir(wdg):
                    wdg.toggleAutoComplete()
        
        return wdg

    def checkSave(self,wdg):
        ok = 0
        if wdg.viewOnly:
            ok = 1
        else:
            if 'getText' in dir(wdg):
                try:
##                    if wdg.lastText != unicode(wdg.getText(),'utf-8'):
                    if wdg.lastText != wdg.getText():
                        resp = QtGui.QMessageBox.warning(self,'Save Tab',"Do you want to save the file <b>"+wdg.title+"</b>?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
                        if resp == QtGui.QMessageBox.Yes:
                            self.editorSave()
                            ok =1
                        elif resp == QtGui.QMessageBox.No:
                            ok =1
                    else:
                        ok =1 
                except:
                    ok=1
                    self.ui.l_statusbar.setText('Error: checking save')
            else: # Ignore checksave if no getText
                ok=1
        return ok

    def editorSave(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        
        if wdg.filename != None:
            filename = wdg.filename
        else:
            fileext = ''
            # Don't show extensions for now (not working in Linux)
##            for e in self.settings['extensions']:
##                if self.settings['extensions'][e]==wdg.lang:
##                    fileext+=wdg.lang+' (*.'+e+");;"
            fileext += "All (*.*)"
            
            filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",self.pluginD['filebrowser'].ui.le_root.text(),fileext)
##            print filename
            if filename=='':
                filename=None
            else:
                wdg.filename = os.path.abspath(str(filename))
                wdg.title = os.path.basename(wdg.filename)
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
        if filename != None:
            try:
                txt = wdg.getText()
                f = codecs.open(wdg.filename,'w','utf8')
                f.write(txt)
                f.close()
                wdg.lastText = txt
                wdg.modTime = os.path.getmtime(filename)
                self.ui.l_statusbar.setText('Saved: '+wdg.title)#+' at '+datetime.datetime.now().ctime(),3000)
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
            except:
                QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it.  You may want to copy the text, paste it in another editor to not lose your work.<br><br><b>Error:</b><br>'+str(sys.exc_info()[1]))
                self.ui.l_statusbar.setText('Error Saving: '+filename)
            
            # Save Signal
            self.evnt.editorSaved.emit(wdg)
            
            # If Settings File, reload
            if filename == self.settings_filename:
                self.loadSettings()
            
            
                
    def editorSaveAs(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        fileext = ''
        if wdg.filename != None:
            pth = wdg.filename
        else:
            pth = self.pluginD['filebrowser'].ui.le_root.text()
            
        filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",pth,fileext)
        if filename!='':
            
            ind = self.ui.tab.currentIndex()
            wdg.filename = os.path.abspath(str(filename))
            wdg.title = os.path.basename(wdg.filename)
            self.ui.tab.setTabText(ind,wdg.title)
            self.ui.tab.setTabToolTip(ind,str(filename))
            self.editorSave()
                
    def editorFind(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        if 'find' in dir(wdg):
            txt = self.ui.le_find.text()
            wdg.find(txt)

    def editorRun(self):
        wdg = self.ui.sw_main.currentWidget()
        if wdg.lang in self.settings['run']:
            if self.settings['run'][wdg.lang]['cmd']=='preview':
                self.pluginD['preview'].previewRun(wdg)
                if self.ui.tab_right.isHidden():
                    self.toggleRightPlugin()
            else:
                ok = self.checkSave(wdg)
                filename = str(wdg.filename)
                if ok and filename != 'None':
                    if wdg.lang in self.settings['run']:
                        # Otherwise run in output
                        runD = self.settings['run'][wdg.lang]
                        self.pluginD['output'].newProcess(runD['cmd'],wdg)

    def editorToggleComment(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'toggleComment' in dir(wdg):
            wdg.toggleComment()
            
    def editorToggleWhitespace(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'toggleWhitespace' in dir(wdg):
            wdg.toggleWhitespace()
            
    def editorIndent(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'indent' in dir(wdg):
            wdg.indent()

    def editorUnindent(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'unindent' in dir(wdg):
            wdg.unindent()

    def editorWordWrap(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'toggleWordWrap' in dir(wdg):
            wdg.toggleWordWrap()

    def editorGoto(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        if 'gotoLine' in dir(wdg):
            txt = self.ui.le_goto.text()
            try:
                line = int(str(txt))-1
                wdg.gotoLine(line)
            except:
                pass
    
    def editorPrint(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        
        printer = QtGui.QPrinter()
        pdlg = QtGui.QPrintDialog(printer,self)
        resp = pdlg.exec_()
        if resp:
            
            if 'getText' in dir(wdg):
                txt = wdg.getText()
                te = QtGui.QTextEdit()
                
                te.setFontFamily('Courier')
                te.setFontPointSize(8)
                te.setText(txt)
            elif 'print_' in dir(wdg):
                te = wdg
            try:
                te.print_(printer)

            except:
                QtGui.QMessageBox.warning(self,'Cannot Print','There was an error printing this document')
    
    def editorStats(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        if 'getText' in dir(wdg):
            txt = wdg.getText()
            lines = len(txt.split('\n'))
            words = len(txt.split())
            self.ui.l_statusbar.setText('Lines: %d    Words: %d' %(lines,words))
    
    #---Plugins
    def addPlugin(self,plug):
        curdir = os.path.abspath('.')

        if not os.path.exists(self.pluginPath+plug):
            QtGui.QMessageBox.warning(self,'Plugin Load Failure','The plugin <b>'+plug+'</b> was not found')
        else:
            pmod = importlib.import_module('plugins.'+plug)
            os.chdir(self.pluginPath+plug)
            pluginWidget = pmod.addPlugin(self)
            title = pluginWidget.title
            loc = pluginWidget.location
            icn = QtGui.QIcon()
            if os.path.exists(self.pluginPath+plug+'/icon.png'):
                icn = QtGui.QIcon(self.pluginPath+plug+'/icon.png')
            
            # Check settings for location
            if plug in self.settings['plugins'] and 'location' in self.settings['plugins'][plug]:
                loc = self.settings['plugins'][plug]['location']
            
            tabtext = title
            
            if loc == 'left':
                if self.settings['window']['pluginLeft']['showTabText']!='1': tabtext=''
                ti = self.ui.tab_left.addTab(pluginWidget,icn,tabtext)
                self.ui.tab_left.setTabToolTip(ti,title)
            elif loc=='right':
                if self.settings['window']['pluginRight']['showTabText']!='1': tabtext=''
                ti = self.ui.tab_right.addTab(pluginWidget,icn,tabtext)
                self.ui.tab_right.setTabToolTip(ti,title)
            elif loc == 'bottom':
                if self.settings['window']['pluginBottom']['showTabText']!='1': tabtext=''
                self.ui.sw_bottom.addWidget(pluginWidget)
                self.ui.tabbar_bottom.addTab(icn,tabtext)
            self.pluginD[plug]=pluginWidget
            os.chdir(curdir)




    


    #---   Left Plugins
    def toggleLeftPlugin(self):
        self.ui.fr_left.setVisible(self.ui.fr_left.isHidden())
    
    def nextLeftPlugin(self):
        self.ui.fr_left.setVisible(1)
        i=self.ui.tab_left.currentIndex()
        i+=1
        if i >= self.ui.tab_left.count():
            i=0
        self.ui.tab_left.setCurrentIndex(i)
        
##    def pluginLeftChange(self,ind):
##        if ind==0:
##            self.ui.tab_left.hide()
##            self.ui.fr_left_hidden.show()
##            self.ui.split_bottom.setSizes([26,self.ui.split_left.height()-26])
    
    def updateOutline(self):
        if 'outline' in self.pluginD:
            wdg = self.ui.sw_main.currentWidget()
            if self.ui.fr_left.isHidden():
                self.ui.fr_left.setVisible(1)
            i=self.ui.tab_left.indexOf(self.pluginD['outline'])
            self.ui.tab_left.setCurrentIndex(i)
            if 'getText' in dir(wdg):
                self.pluginD['outline'].updateOutline(wdg)
    
    def viewFileBrowser(self):
        if 'filebrowser' in self.pluginD:
            if self.ui.fr_left.isHidden():
                self.ui.fr_left.setVisible(1)
            i=self.ui.tab_left.indexOf(self.pluginD['filebrowser'])
            self.ui.tab_left.setCurrentIndex(i)
    
    #---   Bottom Plugins
    def pluginBottomChange(self,ind):
        if self.ui.sw_bottom.currentIndex() != 0:
            self.prevPlugin = self.ui.sw_bottom.currentIndex()
        self.ui.sw_bottom.setCurrentIndex(ind)
        self.ui.sw_bottom.setHidden(not ind)
    
    def toggleBottomPlugin(self):
        if self.ui.tabbar_bottom.currentIndex() == 0:
            if self.prevPlugin==0:self.prevPlugin=1
            self.ui.tabbar_bottom.setCurrentIndex(self.prevPlugin)
            if self.ui.fr_bottom.isHidden():
                self.ui.fr_bottom.setHidden(0)
        else:
            self.ui.tabbar_bottom.setCurrentIndex(0)
    
    def nextBottomPlugin(self):
        i=self.ui.tabbar_bottom.currentIndex()
        i+=1
        if i>= self.ui.tabbar_bottom.count():
            i=0
        self.ui.tabbar_bottom.setCurrentIndex(i)
        
    def replaceFocus(self):
        if 'find_replace' in self.pluginD:
            i = self.ui.sw_bottom.indexOf(self.pluginD['find_replace'])
            self.ui.tabbar_bottom.setCurrentIndex(i)
            self.pluginD['find_replace'].ui.le_find.setFocus()
            self.pluginD['find_replace'].ui.le_find.selectAll()

    def viewPythonShell(self):
        if 'py_console' in self.pluginD:
            i = self.ui.sw_bottom.indexOf(self.pluginD['py_console'])
            self.ui.tabbar_bottom.setCurrentIndex(i)
            self.pluginD['py_console'].setFocus()

    def qtHelp(self):
        if 'qt2py' in self.pluginD:
            i=self.ui.sw_bottom.indexOf(self.pluginD['qt2py'])
            self.ui.tabbar_bottom.setCurrentIndex(i)
        self.pluginD['qt2py'].ui.le_help.setFocus()
        self.pluginD['qt2py'].ui.le_help.selectAll()

    #---   Right Plugins
    def toggleRightPlugin(self):
##        if self.ui.tab_right.isVisible():
        if self.ui.tab_right.isVisible() and self.ui.sw_main.isHidden():
            self.toggleRightPluginFull()
        self.ui.tab_right.setVisible(self.ui.tab_right.isHidden())
        self.currentEditor().pluginRightVisible=self.ui.tab_right.isVisible()
        
        if 'leftToggle' in self.settings['window']['pluginRight']:
            if self.settings['window']['pluginRight']['leftToggle']=='1':
                self.ui.fr_left.setVisible(self.ui.tab_right.isHidden())
                
    def toggleRightPluginFull(self):
        if self.ui.tab_right.isVisible():
            self.ui.sw_main.setVisible(self.ui.sw_main.isHidden())

    #---Webview Preview
    def webview_preview(self,html,burl=None):
        openfile = self.isFileOpen('preview')
        if openfile==-1:
            wdg = self.addEditorWidget('webview','Preview','preview')
            wdg.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            wdg.linkClicked.connect(self.urlClicked)
            self.ui.tab.setTabIcon(self.ui.tab.currentIndex(),QtGui.QIcon(self.iconPath+'page_preview.png'))
    
        else:
            self.ui.tab.setCurrentIndex(openfile)
            QtGui.QApplication.processEvents()
            wdg = self.ui.sw_main.currentWidget()
        
        if burl != None:
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(burl)).replace('\\','/')+'/')

        wdg.setText(html,burl)

        wdg.viewOnly = 1
        wdg.modTime = None
        QtGui.QApplication.processEvents()
        self.changeTab(self.ui.tab.currentIndex())
    
    #---Startpage
    def addStart(self,wdg=None):
        pth = 'doc/start.html'
        openfile = self.isFileOpen(pth)
        if openfile==-1:
            wdg = self.addEditorWidget('Start','Start',pth,editor='webview')
        else:
            self.ui.tab.setCurrentIndex(openfile)
            QtGui.QApplication.processEvents()
            wdg = self.ui.sw_main.currentWidget()
        
        f = open(pth,'r')
        txt = f.read()
        f.close()
        if os.name =='nt':
            pfx="file:///"
        else:
            pfx="file://"
        burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/doc/')

        wdg.setText(txt,burl)
        wdg.viewOnly = 1
        wdg.modTime = os.path.getmtime(pth)
        QtGui.QApplication.processEvents()
        self.changeTab(self.ui.tab.currentIndex())
        self.ui.tab.setTabIcon(self.ui.tab.currentIndex(),QtGui.QIcon(self.iconPath+'home.png'))
        wdg.page().mainFrame().evaluateJavaScript("document.getElementById('version').innerHTML=' version "+str(self.version)+"'")
        
        if openfile==-1:
            wdg.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            wdg.linkClicked.connect(self.urlClicked)
        
        # Add Workspaces
        wksp = ''
        icn_wksp = pfx+os.path.abspath('img/workspace.png').replace('\\','/')
        if os.path.exists(self.settingPath+'/workspaces'):
            for w in sorted(os.listdir(self.settingPath+'/workspaces'),key=lambda x: x.lower()):
##                wksp += '<a href="workspace:'+w+'"><span class="workspace"><span class="workspace_title">'+w+'</span><br><table width=100%><tr><td class="blueblob">&nbsp;&nbsp;</td><td width=100%><hr class="workspaceline"><hr class="workspaceline"></td></tr></table></span></a> '
                wksp += '<a href="workspace:'+w+'"><div class="button"><img src="'+icn_wksp+'"> '+w+'</div></a> '
            wdg.page().mainFrame().evaluateJavaScript("document.getElementById('workspaces').innerHTML='"+str(wksp)+"'")
        
        # Add New File Links
        nfiles = ''
        for lang in sorted(self.settings['prog_lang']):
            if lang != 'default' and self.settings['prog_lang'][lang]['fave']:
                icn = None
                if os.path.exists(self.iconPath+'files/'+lang+'.png'):
                    icn = self.iconPath+'files/'+lang+'.png'
                # Set default Icon if language not found
                if icn == None:
                        icn = self.iconPath+'files/_blank.png'

                nfiles += '<a href="new:'+lang+'" title="new '+lang+'"><div class="button"><img src="'+pfx+icn+'" style="height:14px;"> '+lang+'</div></a>'
        wdg.page().mainFrame().evaluateJavaScript("document.getElementById('new_files').innerHTML='"+str(nfiles)+"'")
        
    def removeStart(self):
        # Remove startpage
##        if self.startinit:
            for i in range(self.ui.tab.count()):
                file_id = self.ui.tab.tabData(i).toInt()[0]
                if file_id == 0:
                    self.closeTab(i)
##                    self.startinit=0
                    break
    
    def urlClicked(self,url):
        # Mainly used for startpage urls
        lnk = str(url.toString())
##        print url
        wdg = self.ui.sw_main.currentWidget()
        if lnk.startswith('new:'):
            self.addEditorWidget(lang=lnk.split(':')[1])
            self.removeStart()
        elif lnk.startswith('workspace'):
            w=lnk.split(':')[1]
            if w=='new':
                self.newWorkspace()
                self.addStart(wdg=wdg)
            else:
                self.loadWorkspace(w)
        elif lnk.endswith('start.html'):
            self.addStart(wdg=wdg)
        else:
            wdg.load2(url)
        
    #---Shortcuts
    def findFocus(self):
        if self.ui.fr_toolbar.isHidden():
            self.ui.fr_toolbar.setVisible(1)
        self.ui.le_find.setFocus()
        self.ui.le_find.selectAll()
        
    def gotoFocus(self):
        if self.ui.fr_toolbar.isHidden():
            self.ui.fr_toolbar.setVisible(1)
        self.ui.le_goto.setFocus()
        self.ui.le_goto.selectAll()
        
    def nextTab(self):
        i = self.ui.tab.currentIndex()+1
        if i == self.ui.tab.count():i=0
        self.ui.tab.setCurrentIndex(i)
    
    #---Workspace
    def saveWorkspace(self):
        if self.workspace != None:
            if not os.path.exists(self.settingPath+'/workspaces'):
                os.mkdir(self.settingPath+'/workspaces')
            
            wD={'files':[],'basefolder':None,'lastOpenFile':None}
            ci = self.ui.tab.currentIndex()
            # Save workspace files
            for i in range(self.ui.tab.count()):
                file_id = self.ui.tab.tabData(i).toInt()[0]
                if file_id in self.tabD:
                    wdg = self.tabD[file_id]
                    if wdg.editor != 'Start':
                        wD['files'].append({'filename':wdg.filename,'editor':wdg.editor})
                        if i==ci:
                            wD['lastOpenFile']=wdg.filename
            
            # Save workspace dir
            if 'filebrowser' in self.pluginD:
                wD['basefolder']=self.pluginD['filebrowser'].rootpath
            f = open(self.settingPath+'/workspaces/'+self.workspace,'w')
            f.write(json.dumps(wD))
            f.close()
    
    def loadWorkspace(self,wksp):
        
        self.saveWorkspace()
        ok = self.closeWorkspace(askSave=0,openStart=0)
        
        # Load workspace
        if ok:
            self.workspace=wksp
            f = open(self.settingPath+'/workspaces/'+self.workspace,'r')
            wD = json.loads(f.read())
            f.close()
            
            # Load Files
            for f in wD['files']:
                if f not in [None,'None','']:
                    if type(f) == type({}):
                        self.openFile(f['filename'],editor=f['editor'])
                    else:
                        self.openFile(f)
            
            # Goto lastopen file
            if 'lastOpenFile' in wD:
                for i in range(self.ui.tab.count()):
                    file_id = self.ui.tab.tabData(i).toInt()[0]
                    if file_id in self.tabD:
                        wdg = self.tabD[file_id]
                        if wdg.filename == wD['lastOpenFile']:
                            self.ui.tab.setCurrentIndex(i)
                            break
            
            if 'basefolder' in wD and 'filebrowser' in self.pluginD:
                if wD['basefolder'] != None:
                    self.pluginD['filebrowser'].ui.le_root.setText(wD['basefolder'])
                    self.pluginD['filebrowser'].loadRoot()
            
            self.setWindowTitle('Armadillo | '+wksp)
            
            self.workspaceMenu.saveWact.setDisabled(0)
            self.workspaceMenu.closeWact.setDisabled(0)
            
##            QtGui.QApplication.processEvents()
            self.removeStart()
            
            if self.ui.tab.count() ==1:
                self.changeTab(0)
            
    def newWorkspace(self):
        # New Workspace
        resp,ok = QtGui.QInputDialog.getText(self,'New Workspace','Enter Workspace Name')
        if ok and not resp.isEmpty():
            self.workspace = resp
            self.saveWorkspace()
            self.workspaceMenu.loadMenu()
            self.workspaceMenu.saveWact.setDisabled(0)
            self.workspaceMenu.closeWact.setDisabled(0)
            self.workspaceMenu.deleteWact.setDisabled(0)
    
    def closeWorkspace(self,askSave=0,openStart=0):
        wk_ok = 1
        # Save current workspace
        if self.workspace != None and askSave:
            wk_ok=0
            resp = QtGui.QMessageBox.warning(self,'Save Workspace',"Do you want to save the current workspace <b>"+self.workspace+"</b> first?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
            if resp == QtGui.QMessageBox.Yes:
                self.saveWorkspace()
                wk_ok =1
            elif resp == QtGui.QMessageBox.No:
                wk_ok =1
                
        # Close open files
        fl_ok = 1
        if wk_ok:
            # Check if anything needs saving
            for i in range(self.ui.tab.count()-1,-1,-1):
                file_id = self.ui.tab.tabData(i).toInt()[0]
                wdg = self.tabD[file_id]
                ok = self.checkSave(wdg)
                if not ok:
                    fl_ok = 0
                    break
                self.closeTab(i)
        
##        # Close open files
##        cancelled = 0
##        # Check if anything needs saving
##        for i in range(self.ui.tab.count()-1,-1,-1):
##            file_id = self.ui.tab.tabData(i).toInt()[0]
##            wdg = self.tabD[file_id]
##            ok = self.checkSave(wdg)
##            if not ok:
##                cancelled = 1
##                break
##            self.closeTab(i)
##        ok = not cancelled
##        QtGui.QApplication.processEvents()
        ok=fl_ok*wk_ok
        
        if ok:
            self.workspace=None
            if 'output' in self.pluginD:
                self.pluginD['output'].killAll()
        
        if ok and openStart:
            self.addStart()
        
        return ok

    #---Settings
    def loadSettings(self):
        # Create settings directory
        if not os.path.exists(self.settingPath):
            os.mkdir(self.settingPath)
        
        if not os.path.exists(self.settingPath+'/settings.conf'):
            import shutil
            shutil.copyfile(os.path.abspath(os.path.dirname(__file__))+'/default_settings.conf',self.settingPath+'/settings.conf')

        from plugins.configobj import configobj
        self.settings_filename = self.settingPath+'/settings.conf'
        config = configobj.ConfigObj(os.path.abspath(os.path.dirname(__file__))+'/default_settings.conf')
        try:
            user_config = configobj.ConfigObj(self.settings_filename)
            if type(user_config['editors'])==type([]): # Check editor settings 
                error
            config.merge(user_config)
        except:
            QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<Br><Br>Using default settings<Br><br><i>Compare your settings with the default_settings</i>')
        self.settings = config

        # Configure Settings
        self.settings['run']={}
##        self.settings['run_preview']={}
        for l in self.settings['prog_lang']:
            ok = 1
            #~ self.settings['run_preview'][l]=0
            # Remove default languages if not in user config
            if 'prog_lang' in user_config:
                if l not in user_config['prog_lang']:
                    self.settings['prog_lang'].pop(l)
                    ok = 0
                    
            if ok:
                # Make sure editor in settings
                if not 'editor' in self.settings['prog_lang'][l]:
                    self.settings['prog_lang'][l]['editor']=None
            
                # add run to settings
                if 'run' in self.settings['prog_lang'][l]:
                    self.settings['run'][l]={'cmd':self.settings['prog_lang'][l]['run']}
##                    if 'run_args' in self.settings['prog_lang'][l]:
##                        a = self.settings['prog_lang'][l]['run_args']
##                        self.settings['run'][l]['args']=a
                
##                if 'preview' in self.settings['prog_lang'][l]:
##                    if self.settings['prog_lang'][l]['preview']=='1':
##                        self.settings['run_preview'][l]=1
                
                # Add fave to settings by default
                if 'fave' not in self.settings['prog_lang'][l]:
                    self.settings['prog_lang'][l]['fave']=1
                else:
                    self.settings['prog_lang'][l]['fave']=int(self.settings['prog_lang'][l]['fave'])
                
    
##    def loadSetup(self):
##        # Geometry 
##        if os.path.exists(self.settingPath):
##            # Load window settings
##            if os.path.exists(self.settingPath+'/window'):
##                f = open(self.settingPath+'/window','rb')
##                wingeo = f.read()
##                f.close()
##                self.restoreState(wingeo)
        
    def openSettings(self):
        self.openFile(self.settings_filename)

    def saveSettings(self):
        if self.fullscreen_mode:
            self.toggleFullscreen()
            QtGui.QApplication.processEvents()
        
        # Save Workspace
        if self.workspace != None and int(self.settings['save_workspace_on_close']):
            self.saveWorkspace()

##        # Save Window Geometry
##        f = open(self.settingPath+'/window','wb')
##        f.write(self.saveState())
##        f.close()

    #---FileModify Checker
    def checkFileChanges(self):
##        if self.fileLastCheck < time.time()-5:##        if self.fileLastCheck < time.time()-5:
            chngs = 0
            close_tabs = []
            for i in range(self.ui.tab.count()):
                file_id = self.ui.tab.tabData(i).toInt()[0]
                if file_id in self.tabD:
                    wdg = self.tabD[file_id]
                    if wdg.filename != None and wdg.modTime != None:
                        if not os.path.exists(wdg.filename):
                            resp = QtGui.QMessageBox.warning(self,'File Does not exist',str(wdg.filename)+' does not exist anymore.<br><<br>Do you want to keep the file open?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                            if resp == QtGui.QMessageBox.No:
                                close_tabs.append(i)
                            chngs = 1
                        elif os.path.getmtime(wdg.filename) > wdg.modTime:
                            resp = QtGui.QMessageBox.warning(self,'File Modified',str(wdg.filename)+' has been modified.<br><<br>Do you want to reload it?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                            wdg.modTime = os.path.getmtime(wdg.filename)
                            chngs=1
                            if resp == QtGui.QMessageBox.Yes:
                                QtGui.QApplication.processEvents()
                                f = codecs.open(wdg.filename,'r','utf-8')
                                txt = f.read()
                                f.close()
                                wdg.setText(txt)
            
            if close_tabs != []:
                close_tabs.reverse()
                for i in close_tabs:
                    self.closeTab(i)
            if not chngs:
                QtGui.QMessageBox.warning(self,'No Changes','No external changes to current open files were found')
##            self.fileLastCheck = time.time()

def runui():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app = QtGui.QApplication(sys.argv)
    
    # Setup font
##    fdb = QtGui.QFontDatabase()
##    fdb.addApplicationFont('styles/DejaVuSansMono.ttf')
##    app.setFont(QtGui.QFont('DejaVu Sans Mono',10))
    
    armadilloApp = Armadillo()
    armadilloApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
