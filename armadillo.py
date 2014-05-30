# --------------------------------------------------------------------------------
# Armadillo IDE
# Copyright 2013-2014 Cole Hagen
#
# Armadillo is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

# VERSION
__version__ = '0.9.12'

import sys, json, codecs, time
from PyQt4 import QtCore, QtGui, QtWebKit
from armadillo_ui import Ui_MainWindow
import os,shutil,datetime, webbrowser, threading
import plugins.output.output

class Events(QtCore.QObject):
    editorAdded = QtCore.pyqtSignal(QtGui.QWidget)
    editorTabChanged = QtCore.pyqtSignal(QtGui.QWidget)
    
class NewMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        self.setTitle('New')
        self.setIcon(QtGui.QIcon(self.parent.iconPath+'new.png'))
        
        # Add Favorites First
        for lang in sorted(parent.settings['fav_lang']):
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
        self.deleteWact = self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace_delete.png'),'Delete Workspace')

        if os.path.exists(self.parent.settingPath+'/workspaces'):
            self.addSeparator()
            for wsp in sorted(os.listdir(self.parent.settingPath+'/workspaces')):
                self.addAction(QtGui.QIcon(self.parent.iconPath+'workspace.png'),wsp)
                self.deleteWact.setDisabled(0)
    
    def loadWorkspace(self,event):
        if str(event.text()) == 'New Workspace':
            # New Workspace
            resp,ok = QtGui.QInputDialog.getText(self.parent,'Enter Workspace Name','')
            if ok and not resp.isEmpty():
                self.parent.workspace = resp
                self.parent.saveWorkspace()
                self.loadMenu()
                self.saveWact.setDisabled(0)
                self.deleteWact.setDisabled(0)
        elif str(event.text()) == 'Save Workspace':
            self.parent.saveWorkspace()
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

class ArmadilloMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        # New
        self.addMenu(self.parent.newMenu)
        
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
        
        # Workspace
        self.addMenu(self.parent.workspaceMenu)
        
        self.addSeparator()
        
        # Home
        icn = QtGui.QIcon(self.parent.iconPath+'home.png')
        act = self.addAction(icn,'Home',self.parent.addStart)
        
        # Plugins
        plugmenu = self.parent.createPopupMenu()
        plugmenu.setTitle('Plugins')
        plugmenu.setIcon(QtGui.QIcon(self.parent.iconPath+'plugin.png'))
        self.addMenu(plugmenu)
        
        # Settings
        icn = QtGui.QIcon(self.parent.iconPath+'wrench.png')
        act = self.addAction(icn,'Settings',self.parent.openSettings)
        
        self.addSeparator()
        
        # Check for file changes
        icn = QtGui.QIcon()
        act = self.addAction(icn,'File check (changes)',self.parent.checkFileChanges)
        
        # Zen
        icn = QtGui.QIcon(self.parent.iconPath+'zen.png')
        self.zenAction = self.addAction(icn,'Zen Mode (F11)',self.parent.toggleZen)
        
        # Close
        self.addSeparator()
        icn = QtGui.QIcon(self.parent.iconPath+'close.png')
        self.addAction(icn,'Exit',self.parent.close)
        
class Armadillo(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Version
        self.version = __version__

        # Setup UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
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
        
        # Screen Size
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        coords= QtGui.QApplication.desktop().screenGeometry(screen).getCoords() 
        dx = 50
        self.setGeometry(coords[0]+dx,coords[1]+dx,(coords[2]-coords[0]-2*dx),(coords[3]-coords[1]-2*dx))
        
        #--- Setup Tab Toolbar
        self.ui.tabtoolbar = QtGui.QToolBar("editorTabBar",self)
##        self.ui.tabtoolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.tabtoolbar.setFloatable(False)
        self.ui.tabtoolbar.setMovable(False)
        self.ui.tabtoolbar.setProperty("class","editorTabBar")
        self.ui.tabtoolbar.setObjectName('editorTabBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.tabtoolbar)

        # add Main Button to tabbar
        self.ui.tabtoolbar.addWidget(self.ui.b_main)
        
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        
        # Toolbutton Toolbar
        self.ui.toolbar = QtGui.QToolBar("toolBar",self)
##        self.ui.toolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.toolbar.setFloatable(False)
        self.ui.toolbar.setMovable(False)
        self.ui.toolbar.setProperty("class","toolBar")
        self.ui.toolbar.setObjectName('toolBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.toolbar)
        self.ui.toolbar.addWidget(self.ui.fr_toolbar)
        
        # Find Toolbar
        self.ui.findbar = QtGui.QToolBar("findBar",self)
##        self.ui.findbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.findbar.setFloatable(False)
        self.ui.findbar.setMovable(False)
        self.ui.findbar.setProperty("class","findBar")
        self.ui.findbar.setObjectName('findBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.findbar)
        self.ui.findbar.addWidget(self.ui.fr_find)

        # File Tabs
        self.ui.tab = QtGui.QTabBar()
        self.ui.tab.setObjectName('editorTabs')
        self.ui.tab.setTabsClosable(True)
        self.ui.tab.setMovable(True)
        self.ui.tab.setProperty("class","editorTabs")
        self.ui.tab.setObjectName('editorTabBar')
        self.ui.tabtoolbar.addWidget(self.ui.tab)
        self.ui.tab.currentChanged.connect(self.changeTab)
        self.ui.tab.tabCloseRequested.connect(self.closeTab)
        
        self.setAcceptDrops(1)
        
        #--- Signals
        self.ui.b_open.clicked.connect(self.openFile)
        self.ui.b_save.clicked.connect(self.editorSave)

        self.ui.b_indent.clicked.connect(self.editorIndent)
        self.ui.b_unindent.clicked.connect(self.editorUnindent)
        self.ui.b_comment.clicked.connect(self.editorToggleComment)
        
        self.ui.b_run.clicked.connect(self.editorRun)
        self.ui.b_wordwrap.clicked.connect(self.editorWordWrap)
        self.ui.b_settings.clicked.connect(self.openSettings)
        self.ui.b_help.clicked.connect(self.addStart)
        self.ui.b_plugins.clicked.connect(self.showPlugins)
##        self.ui.b_zen.clicked.connect(self.toggleZen)
        
        self.ui.b_find.clicked.connect(self.editorFind)
        self.ui.le_goto.returnPressed.connect(self.editorGoto)
        
        # Editor Signals
        self.evnt = Events()
        self.tabD={}
        
        #--- Shortcuts
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_E,self,self.editorToggleComment) #Toggle Comment
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F,self,self.findFocus) # Find
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_G,self,self.gotoFocus) # Goto
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_N,self,self.ui.b_new.click) # Goto
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_O,self,self.updateOutline) # Update/Show Outline
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Q,self,self.qtHelp) # Qt Help
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_R,self,self.replaceFocus) # Replace
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_S,self,self.editorSave) # Save
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_W,self,self.editorWordWrap) # Toggle Wordwrap
        
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Tab,self,self.nextTab) # Toggle Wordwrap

        QtGui.QShortcut(QtCore.Qt.Key_F1,self,self.addStart) # Add Start Page
        QtGui.QShortcut(QtCore.Qt.Key_F2,self,self.updateOutline) # Update Outline
        QtGui.QShortcut(QtCore.Qt.Key_F5,self,self.editorRun) # Run
        QtGui.QShortcut(QtCore.Qt.Key_F10,self,self.toggleEditorZen) # Editor full screen, but keep tabs
        QtGui.QShortcut(QtCore.Qt.Key_F11,self,self.toggleZen) # Fullscreen Zen
        
        # Plugins
        self.pluginDocks = []
        self.setCorner(QtCore.Qt.BottomLeftCorner,QtCore.Qt.LeftDockWidgetArea)
        
        # File Dictionary
        self.fileCount = -1
        
        #--- Get Editor Languages
        self.editorD = {}
        
        for e in self.settings['editors']:
            exec('import editors.'+e)
            try:
                exec('ld = editors.'+e+'.getLang()')
            except:
                ld = []
            self.editorD[e] = ld

            for l in ld:
                if l not in self.settings['extensions']:
                    self.settings['extensions'][l]=l
            
        #--- Add Plugins
        self.dockareaD = {'left':QtCore.Qt.LeftDockWidgetArea,
            'right':QtCore.Qt.RightDockWidgetArea,
            'top':QtCore.Qt.TopDockWidgetArea,
            'bottom':QtCore.Qt.BottomDockWidgetArea
        }
        self.pluginD = {}
        
        curdir = os.path.abspath('.')
        
        for plug in self.settings['activePlugins']:
            self.addPlugin(plug)

        os.chdir(curdir)
        
        self.dockstate = self.saveState()
        self.zen = 1
        
        #--- Add Start
        self.addStart()
        
        # Load setup
        self.loadSetup()
        
        # Load FileCheck Thread
        self.fileLastCheck = time.time()
        # self.fileModD = {}
        # fmt = threading.Thread(target=self.checkFileChanges,args=(self))
        # fmt.start()

        # New Button Menu
        self.newMenu = NewMenu(self)
        self.ui.b_new.setMenu(self.newMenu)
        
        # Workspace Button Menu
        self.workspaceMenu = WorkspaceMenu(self)
        self.ui.b_workspace.setMenu(self.workspaceMenu)
        
        # add Main Button to tabbar
        self.armadilloMenu = ArmadilloMenu(self)
        self.ui.b_main.setMenu(self.armadilloMenu)
        
        # Plugins Button
##        pluginmenu = self.createPopupMenu()
##        self.ui.b_plugins.setMenu(pluginmenu)
        
        # Open file if in sys arg
        # print "SYS",sys.argv
        if len(sys.argv)>1:
            if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
                self.openFile(sys.argv[1])

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

    def dropEvent(self,event):
        handled=False
        if event.mimeData().urls():
            for f in event.mimeData().urls():
                self.openFile(str(f.toLocalFile()))
            handled=True

        if not handled:
            QtGui.QMainWindow.dropEvent(self,event)

    def dragEvent(self,event):
        event.accept()
    
    def dragEnterEvent(self,event):
        event.accept()
    
    def toggleEditorZen(self):
        self.toggleZen(mode='editor')
    
    def toggleZen(self,mode='full'):
        self.zen = not self.zen
        if self.zen:
            self.restoreState(self.dockstate)
            self.ui.statusbar.show()
            self.ui.findbar.show()
            self.ui.toolbar.show()
            self.ui.tabtoolbar.show()
            self.showNormal()
##            self.setWindowFlags(QtCore.Qt.Window)
##            self.show()
            self.armadilloMenu.zenAction.setIcon(QtGui.QIcon(self.iconPath+'zen.png'))
            self.armadilloMenu.zenAction.setText('Zen mode')
        else:
            self.ui.statusbar.hide()
            self.ui.findbar.hide()
            self.ui.toolbar.hide()
##            self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
##            self.show()
            self.dockstate = self.saveState()
            self.armadilloMenu.zenAction.setIcon(QtGui.QIcon(self.iconPath+'zen_not.png'))
            self.armadilloMenu.zenAction.setText('Exit zen mode')
            for plug in self.pluginD:
                self.pluginD[plug].close()
            
            if mode=='full':
                self.ui.tabtoolbar.hide()
                self.showFullScreen()

    def showPlugins(self):
        menu = self.createPopupMenu()
        menu.exec_(self.cursor().pos())

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
            filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",self.pluginD['filebrowser'].wdg.ui.le_root.text()," (*.*)")
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

                else:
                    ext = os.path.splitext(str(filename))[1][1:]
                    lang = ext

                    if ext in self.settings['extensions']:
                        lang = self.settings['extensions'][ext]

                    title = os.path.basename(filename)
                    if int(self.settings['view_folder']):
                        title = os.path.split(os.path.dirname(filename))[1]+'/'+title
                    elif lang == 'python' and title=='__init__.py':
                        title = os.path.split(os.path.dirname(filename))[1]+'/init'
                    
                    wdg = self.addEditorWidget(lang,title,str(filename),editor=editor)
                    f = codecs.open(filename,'r','utf-8')
                    txt = f.read()
                    f.close()
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
    def currentWidget(self):
        return self.ui.sw_main.currentWidget()

    def changeTab(self,tab_ind):
        self.ui.statusbar.showMessage('')

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
            # Disable hiding of plugins for now - until the state can be saved
##            for plug in self.pluginD:
##                pshow = 0
##                if plug in self.settings['plugins_view']:
##                    pshow = 1
##                else:
##                    if lang in self.settings['lang']:
##                        if plug in self.settings['lang'][lang]['plugins']:
##                            pshow = 1
##                if pshow:
##                    self.pluginD[plug].show()
##                else:
##                    self.pluginD[plug].hide()
        # Enable Run
        if lang in self.settings['run']:
            self.ui.b_run.setEnabled(lang in self.settings['run'])
        else:
            self.ui.b_run.setEnabled(0)
        
        # Disable buttons based on function availability
        btnD = {
            'indent':self.ui.b_indent,
            'unindent':self.ui.b_unindent,
            'find':self.ui.fr_find,
            'toggleComment':self.ui.b_comment,
            'getText':self.ui.b_save,
            'toggleWordWrap':self.ui.b_wordwrap,
        }
        for btn in btnD:
            btnD[btn].setEnabled(btn in dir(wdg))
        
        try:
            self.armadilloMenu.menuSaveAction.setEnabled('getText' in dir(wdg))
            self.armadilloMenu.menuSaveAsAction.setEnabled('getText' in dir(wdg))
        except:
            pass
            
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
        wdg = self.currentWidget()
        try:
##            if wdg.lastText != unicode(wdg.getText(),'utf-8'):
            if wdg.lastText != wdg.getText():
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title+'*')
            else:
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
        except:
            self.ui.statusbar.showMessage('Error: ')
        # Check for file changes
##        self.checkFileChanges()
            
    def addEditorWidget(self,lang=None,title='New',filename=None,editor=None):
        self.fileCount+=1
        sw_ind = self.ui.sw_main.count()
        wdg = None
        
        if filename == None and title=='New': title = 'New '+lang
        
        if editor == None:
            if lang in self.settings['fav_lang']:
                editor = self.settings['fav_lang'][lang]['editor']
            if editor == None:
                if lang == 'webview':
                    editor = 'webview'
                elif lang == 'settings':
                    editor = 'settings'
                else:
                    editor = self.settings['fav_lang']['default']['editor']
                    
                    if lang not in self.editorD[editor]:
                        for e in self.editorD:
                            if lang in self.editorD[e]:
                                editor = e
                                break
                
##        if not editor in self.settings['editors'] and not editor in ['webview','settings']:
##            editor = self.settings['fav_lang']['default']['editor']
            
        exec("import editors."+editor)
        exec("wdg = editors."+editor+".addEditor(self,lang,filename)")

        wdg.filename = filename
        wdg.lastText=''
        wdg.title = title
        wdg.id = self.fileCount
        wdg.lang = lang
        wdg.viewOnly = 0
        wdg.dockstate = None
        wdg.modTime = None
        self.tabD[self.fileCount]=wdg
        self.evnt.editorAdded.emit(wdg)

        if 'editorTextChanged' in dir(wdg):
            wdg.evnt.editorChanged.connect(self.editorTextChanged)
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
##        print 'ipth',ipth
        if os.path.exists(ipth):
            icn = QtGui.QIcon(ipth)
        elif filename != None:
            ext = os.path.splitext(filename)[1][1:]
            if os.path.exists(self.iconPath+'files/'+ext+'.png'):
                icn = QtGui.QIcon(self.iconPath+'files/'+ext+'.png')
        elif os.path.exists(self.editorPath+editor+'/'+editor+'.png'):
            icn = QtGui.QIcon(self.editorPath+editor+'/'+editor+'.png')
        self.ui.tab.setTabIcon(sw_ind,icn)

        # Set wordwrap if in settings
        QtGui.QApplication.processEvents()
        if lang in self.settings['fav_lang']:
            if 'wordwrap' in self.settings['fav_lang'][lang]:
                wdg.wordwrapmode = int(self.settings['fav_lang'][lang]['wordwrap'])
                self.editorWordWrap()
        
            # Set Autocomplete Toggle
            if 'autocomplete' in self.settings['fav_lang'][lang]:
                wdg.autocomplete = int(self.settings['fav_lang'][lang]['autocomplete'])
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
                    self.ui.statusbar.showMessage('Error: checking save')
            else: # Ignore checksave if no getText
                ok=1
        return ok

    def editorSave(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        
        if wdg.filename != None:
            filename = wdg.filename
        else:
            fileext = ''
##            exlist = ''
##            for e in self.settings.ext:
##                if self.settings.ext[e]==wdg.lang:
##                    if exlist != '': exlist += ' '
##                    exlist+='*.'+e
##            if exlist != '':
##                fileext += wdg.lang+" ("+exlist+");;"
            fileext += "All (*.*)"
            
            filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",self.pluginD['filebrowser'].wdg.ui.le_root.text(),fileext)
            if filename=='':
                filename=None
            else:
                wdg.filename = os.path.abspath(str(filename))
                wdg.title = os.path.basename(wdg.filename)
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
        if filename != None:
            try:
##                f = open(wdg.filename,'w')
##            txt = unicode(wdg.getText(),encoding='utf-8')
##            txt = str(wdg.getText().toUtf8()).decode('utf-8')
                txt = wdg.getText()
                f = codecs.open(wdg.filename,'w','utf8')
                f.write(txt)
                f.close()
                wdg.lastText = txt
                wdg.modTime = os.path.getmtime(filename)
                self.ui.statusbar.showMessage('Saved '+wdg.title+' at '+datetime.datetime.now().ctime())
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
            except:
                QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it.  You may want to copy the text, paste it in another editor to not lose your work.<br><br><b>Error:</b><br>'+str(sys.exc_info()[1]))
                self.ui.statusbar.showMessage('Error Saving: '+filename)
            
            # If Settings File, reload
            if filename == self.settings_filename:
                self.loadSettings()
                
    def editorSaveAs(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        fileext = ''
        if wdg.filename != None:
            pth = wdg.filename
        else:
            pth = self.pluginD['filebrowser'].wdg.ui.le_root.text()
            
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
        ok = self.checkSave(wdg)
        filename = str(wdg.filename)
        if ok and filename != 'None':
            if wdg.lang in self.settings['run']:
##                if not self.pluginD['output'].isVisible():
##                    self.pluginD['output'].show()
##                self.pluginD['output'].raise_()
                runD = self.settings['run'][wdg.lang]
                self.pluginD['output'].wdg.newProcess(runD['cmd'],filename,runD['args'])

    def editorToggleComment(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'toggleComment' in dir(wdg):
            wdg.toggleComment()

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
            
    #---Plugins
    def addPlugin(self,plug):
        curdir = os.path.abspath('.')

        if not os.path.exists(self.pluginPath+plug):
            QtGui.QMessageBox.warning(self,'Plugin Load Failure','The plugin <b>'+plug+'</b> was not found')
        else:
            exec('import plugins.'+plug)
            os.chdir(self.pluginPath+plug)
            exec('dwdg = plugins.'+plug+'.addDock(self)')
            if plug in self.settings['plugins']:
                title = self.settings['plugins'][plug]['title']
                dockarea =self.dockareaD[self.settings['plugins'][plug]['dockarea']]
            else:
                # Default info
                title = plug.capitalize()
                dockarea =self.dockareaD['bottom']
            if plug == 'py_console': title += ' ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')'
            dockarea =self.dockareaD[self.settings['plugins'][plug]['dockarea']]
            
            dock = QtGui.QDockWidget()
            
            dock.dockWidgetContents = QtGui.QWidget()
            dock.setWidget(dock.dockWidgetContents)
            dock.setWindowTitle(title)
            dock.gridLayout = QtGui.QGridLayout(dock.dockWidgetContents)
            dock.gridLayout.setMargin(0)
            dock.gridLayout.setSpacing(0)
            dock.gridLayout.addWidget(dwdg, 0, 0, 1, 1)
            dock.setObjectName(title.replace(' ','_').lower())
            dock.wdg = dwdg
            self.addDockWidget(dockarea,dock)
            self.pluginDocks.append(dock)
            
            if os.path.exists(self.pluginPath+plug+'/'+plug+'.png'):
                dock.setWindowIcon(QtGui.QIcon(self.pluginPath+plug+'/'+plug+'.png'))
            
            # Tabify Dock with other widgets in its area
            for idock in self.pluginDocks[:-1]:
                if self.dockWidgetArea(idock) == dockarea:
                    self.tabifyDockWidget(idock,dock)
            
            os.chdir(curdir)
            
            self.pluginD[plug] = dock

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
            config.merge(user_config)
        except:
            QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<Br><Br>Using default settings')
##            self.settings_filename =os.path.abspath(os.path.dirname(__file__))+'/default_settings.conf'
        self.settings = config
        
##        print self.settings
        
        
        # Configure Settings
        self.settings['run']={}
        for l in self.settings['fav_lang']:
            ok = 1
            # Remove default languages if not in user config
            if 'fav_lang' in user_config:
                if l not in user_config['fav_lang']:
                    self.settings['fav_lang'].pop(l)
                    ok = 0
                    
            if ok:
                # Make sure editor in settings
                if not 'editor' in self.settings['fav_lang'][l]:
                    self.settings['fav_lang'][l]['editor']=None
            
                # add run to settings
                if 'run' in self.settings['fav_lang'][l]:
                    self.settings['run'][l]={'cmd':self.settings['fav_lang'][l]['run'],'args':[]}
                    if 'run_args' in self.settings['fav_lang'][l]:
                        a = self.settings['fav_lang'][l]['run_args']
                        if type(a) == type(''):
                            a = [a]
                        self.settings['run'][l]['args']=a
    
    def loadSetup(self):
        # Geometry 
        if os.path.exists(self.settingPath):
            # Load window settings
            if os.path.exists(self.settingPath+'/window'):
                f = open(self.settingPath+'/window','rb')
                wingeo = f.read()
                f.close()
                self.restoreState(wingeo)
        
    def openSettings(self):
        self.openFile(self.settings_filename)

    def saveSettings(self):
        if not self.zen:
            self.toggleZen()
            QtGui.QApplication.processEvents()
        
        # Save Workspace
        if self.workspace != None and int(self.settings['save_workspace_on_close']):
            self.saveWorkspace()

        # Save Window Geometry
        f = open(self.settingPath+'/window','wb')
        f.write(self.saveState())
        f.close()

    #---Shortcuts
    def addStart(self,wdg=None):
        pth = 'doc/start.html'
        
##        if wdg in [None,True,False]:
        openfile = self.isFileOpen(pth)
        if openfile==-1:
            wdg = self.addEditorWidget('webview','Start',pth)
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
        wksp = 'Workspaces: '
        icn_wksp = pfx+os.path.abspath('img/workspace.png').replace('\\','/')
        if os.path.exists(self.settingPath+'/workspaces'):
            for w in sorted(os.listdir(self.settingPath+'/workspaces')):
##                wksp += '<a href="workspace:'+w+'"><span class="workspace"><span class="workspace_title">'+w+'</span><br><table width=100%><tr><td class="blueblob">&nbsp;&nbsp;</td><td width=100%><hr class="workspaceline"><hr class="workspaceline"></td></tr></table></span></a> '
                wksp += '<a href="workspace:'+w+'"><span class="workspace"><img src="'+icn_wksp+'"> '+w+'</span></a> '
            wdg.page().mainFrame().evaluateJavaScript("document.getElementById('workspaces').innerHTML='"+str(wksp)+"'")
        
        # Add New File Links
        nfiles = ''
        for lang in sorted(self.settings['fav_lang']):
            if lang != 'default':
                icn = None
                if os.path.exists(self.iconPath+'files/'+lang+'.png'):
                    icn = self.iconPath+'files/'+lang+'.png'
                # Set default Icon if language not found
                if icn == None:
##                    editor=self.settings['fav_lang'][lang]['editor']
##                    if os.path.exists(self.editorPath+editor+'/'+editor+'.png'):
##                        icn = self.editorPath+editor+'/'+editor+'.png'
##                    else:
                        icn = self.iconPath+'files/_blank.png'

                nfiles += '<a href="new:'+lang+'" title="new '+lang+'"><div class="newfile"><img src="'+pfx+icn+'" style="height:14px;"> '+lang+'</div></a>'
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
            self.loadWorkspace(lnk.split(':')[1])
        elif lnk.endswith('start.html'):
            self.addStart(wdg = wdg)
        else:
            wdg.load2(url)
    
    def findFocus(self):
        if self.ui.findbar.isHidden():
            self.ui.findbar.setVisible(1)
        self.ui.le_find.setFocus()
        self.ui.le_find.selectAll()
        
    def gotoFocus(self):
        if self.ui.findbar.isHidden():
            self.ui.findbar.setVisible(1)
        self.ui.le_goto.setFocus()
        self.ui.le_goto.selectAll()
    
    def replaceFocus(self):
        if not self.pluginD['find_replace'].isVisible():
            self.pluginD['find_replace'].show()
        self.pluginD['find_replace'].raise_()
        self.pluginD['find_replace'].wdg.ui.le_find.setFocus()
        self.pluginD['find_replace'].wdg.ui.le_find.selectAll()
    
    def updateOutline(self):
        wdg = self.ui.sw_main.currentWidget()
        if 'getText' in dir(wdg):
            if not self.pluginD['outline'].isVisible():
                self.pluginD['outline'].show()
            self.pluginD['outline'].raise_()
            self.pluginD['outline'].wdg.updateOutline(wdg)
    
    def qtHelp(self):
        if not self.pluginD['qt2py'].isVisible():
            self.pluginD['qt2py'].show()
        self.pluginD['qt2py'].raise_()
        self.pluginD['qt2py'].wdg.ui.le_help.setFocus()
        self.pluginD['qt2py'].wdg.ui.le_help.selectAll()
    
    def nextTab(self):
        i = self.ui.tab.currentIndex()+1
        if i == self.ui.tab.count():i=0
        self.ui.tab.setCurrentIndex(i)
    
    #--- Workspace
    def saveWorkspace(self):
        if self.workspace != None:
            if not os.path.exists(self.settingPath+'/workspaces'):
                os.mkdir(self.settingPath+'/workspaces')
            
            wD={'files':[],'plugins':[],'basefolder':None}
            # Save workspace files
            for i in range(self.ui.tab.count()):
                file_id = self.ui.tab.tabData(i).toInt()[0]
                if file_id in self.tabD:
                    wdg = self.tabD[file_id]
                    wD['files'].append(wdg.filename)
            # Save workspace plugins
            for plug in self.pluginD:
                if self.pluginD[plug].isVisible():
                    wD['plugins'].append(plug)
            
            # Save workspace dir
            wD['basefolder']=self.pluginD['filebrowser'].wdg.rootpath
            f = open(self.settingPath+'/workspaces/'+self.workspace,'w')
            f.write(json.dumps(wD))
            f.close()
    
    def loadWorkspace(self,wksp):
        ok = 1
        # Save current workspace
        if self.workspace != None:
            ok=0
            resp = QtGui.QMessageBox.warning(self,'Save Workspace',"Do you want to save the current workspace <b>"+self.workspace+"</b> first?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
            if resp == QtGui.QMessageBox.Yes:
                self.saveWorkspace()
                ok =1
            elif resp == QtGui.QMessageBox.No:
                ok =1
                
        # Close open files
        cancelled = 0
        # Check if anything needs saving
        for i in range(self.ui.tab.count()-1,-1,-1):
            file_id = self.ui.tab.tabData(i).toInt()[0]
            wdg = self.tabD[file_id]
            ok = self.checkSave(wdg)
            if not ok:
                cancelled = 1
                break
            self.closeTab(i)
        ok = not cancelled
        QtGui.QApplication.processEvents()
        
        # Load workspace
        if ok:
            self.workspace=wksp
            f = open(self.settingPath+'/workspaces/'+self.workspace,'r')
            wD = json.loads(f.read())
            f.close()
            # Load Files
            for f in wD['files']:
                if f not in [None,'None','']:
                    self.openFile(f)
            
            # Show/Hide Plugins
            for p in self.pluginD:
                self.pluginD[p].close()
            for p in wD['plugins']:
                if p in self.pluginD:
                    self.pluginD[p].setVisible(1)
            
            if 'basefolder' in wD:
                self.pluginD['filebrowser'].wdg.ui.le_root.setText(wD['basefolder'])
                self.pluginD['filebrowser'].wdg.loadRoot()
            
            self.setWindowTitle('Armadillo | '+wksp)
            
            self.workspaceMenu.saveWact.setDisabled(0)
            
##            QtGui.QApplication.processEvents()
            self.removeStart()
    
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
    armadilloApp = Armadillo()
    armadilloApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
