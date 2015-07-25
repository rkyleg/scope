# --------------------------------------------------------------------------------
# Armadillo IDE
# Copyright 2013-2015 Cole Hagen
#
# Armadillo is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

# VERSION
__version__ = '1.10.1-dev'

# Make sure qvariant works for Pyxthon 2 and 3
import sip
##sip.setapi('QString',1)
sip.setapi('QVariant',1)

import sys, json, codecs, time, importlib
from PyQt4 import QtCore, QtGui, QtWebKit
from armadillo_ui import Ui_Form
from menus import *
import os,shutil,datetime, webbrowser, threading

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
        self.armadilloPath = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
        self.currentPath = os.path.expanduser('~')
        
        # File Variables
        self.fileOpenD = {} # keep track of open files and associated widgets
        self.fileD = {}     # keep track of all filenames and new files
        self.recentTabs = [] # Keep track of most recent tabs
        self.fileCount = -1
        self.ui.b_closetab.hide()
        
        # Workspace
        self.currentWorkspace = None
        self.workspaceCount = 0
        self.workspaces = {}
        
        # Settings
        self.loadSettings()

        if self.settings['widgetstyle'] != 'None':
            QtGui.QApplication.setStyle(self.settings['widgetstyle'])
        
        self.setAcceptDrops(1)
        
##        # Filesystem watercher - NOT USED CAUSE TO MANY SIGNALS FIRE OFF
##        self.startinit = 1
        self.fileLastCheck = time.time()
##        self.filesystemwatcher = QtCore.QFileSystemWatcher(self)
##        self.filesystemwatcher.fileChanged.connect(self.file_changed)

##        import thread
##        thread = thread.start_new_thread(self.checkFileChanges, (self,))
        
        
        # Style
        style_path = self.settings['style']
        if not os.path.exists(style_path):
            style_path = 'styles/default.css'
        f = open(style_path,'r')
        style = f.read()
        f.close()
        self.setStyleSheet(style)
        self.stylePath = os.path.abspath(style_path)
        
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

        #--- Editor Tabs
##        self.ui.tab = QtGui.QTabBar()
##        self.ui.tab.setObjectName('editorTabs')
##        self.ui.tab.setTabsClosable(True)
##        self.ui.tab.setMovable(True)
##        self.ui.tab.setProperty("class","editorTabs")
##        self.ui.tab.setObjectName('editorTabBar')
##        self.ui.tab.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
##        self.ui.fr_tabs.layout().addWidget(self.ui.tab)
##        self.ui.tab.currentChanged.connect(self.changeTab)
##        self.ui.tab.tabCloseRequested.connect(self.closeTab)
##        self.ui.tab.setExpanding(0)
##        self.ui.tab.mousePressEvent=self.tabMousePressEvent
##        self.ui.fr_tabs.hide()

        
        #--- Hide toolbar buttons for now
##        self.ui.b_save.hide()
        self.ui.b_new.hide()
        
        #--- Signals
        self.ui.b_closetab.clicked.connect(self.close_tab)
        self.ui.sw_main.currentChanged.connect(self.change_tab)
        self.ui.b_show_tabs.clicked.connect(self.showTabspace)
##        self.ui.b_open.clicked.connect(self.openFile)
        self.ui.b_save.clicked.connect(self.editorSave)

        self.ui.b_indent.clicked.connect(self.editorIndent)
        self.ui.b_unindent.clicked.connect(self.editorUnindent)
        self.ui.b_comment.clicked.connect(self.editorToggleComment)
        self.ui.b_color_picker.clicked.connect(self.colorPicker)

        self.ui.b_run.clicked.connect(self.editorRun)
##        self.ui.b_wordwrap.clicked.connect(self.editorWordWrap)
##        self.ui.b_settings.clicked.connect(self.openSettings)
##        self.ui.b_help.clicked.connect(self.addStart)
        
        self.ui.b_find.clicked.connect(self.editorFind)
        self.ui.le_goto.returnPressed.connect(self.editorGoto)

        #--- Editor Events
        class Events(QtCore.QObject):
            editorAdded = QtCore.pyqtSignal(QtGui.QWidget)
            editorTabChanged = QtCore.pyqtSignal(QtGui.QWidget)
            editorSaved = QtCore.pyqtSignal(QtGui.QWidget)
            editorVisibleLinesChanged = QtCore.pyqtSignal(QtGui.QWidget,tuple)
            close=QtCore.pyqtSignal()
            editorTabClosed = QtCore.pyqtSignal(QtGui.QWidget)
            fileOpened = QtCore.pyqtSignal(QtGui.QWidget)
            resized = QtCore.pyqtSignal()
            
            # Workspace Events
            workspaceChanged = QtCore.pyqtSignal(str)
            workspaceOpened = QtCore.pyqtSignal(str)
            workspaceClosed = QtCore.pyqtSignal(str)
        self.evnt = Events()
##        self.fileOpenD={}
        
        # Create Tabspace
        self.createTabspace()
        
        #--- Key Shortcuts
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_E,self,self.editorToggleComment) #Toggle Comment
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F,self,self.findFocus) # Find
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_G,self,self.gotoFocus) # Goto
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_M,self,self.ui.b_main.click) # New
        QtGui.QShortcut(QtCore.Qt.ALT+QtCore.Qt.Key_F,self,self.ui.b_main.click) # New
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_N,self,self.ui.b_new.click) # New
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_S,self,self.editorSave) # Save
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_W,self,self.editorWordWrap) # Toggle Wordwrap
        
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Tab,self,self.nextTab) # Toggle Wordwrap

        QtGui.QShortcut(QtCore.Qt.Key_F2,self,self.toggleLeftPlugin) # Toggle Left Plugin
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F2,self,self.nextLeftPlugin) # show next left plugin
        
        QtGui.QShortcut(QtCore.Qt.Key_F5,self,self.editorRun) # Run
        QtGui.QShortcut(QtCore.Qt.Key_F7,self,self.toggleRightPluginFull) # Expand Right plugin
        QtGui.QShortcut(QtCore.Qt.Key_F3,self,self.toggleRightPlugin) # Toggle RIght Plugins
        
        QtGui.QShortcut(QtCore.Qt.Key_F4,self,self.toggleBottomPlugin) # Hide Bottom Tab
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F4,self,self.nextBottomPlugin) # Show next bottom tab
        QtGui.QShortcut(QtCore.Qt.Key_F1,self,self.showTabspace) # Show Tabbar
        QtGui.QShortcut(QtCore.Qt.Key_F10,self,self.toggleFullEditor) # Editor full screen, but keep tabs
        QtGui.QShortcut(QtCore.Qt.Key_F11,self,self.toggleFullscreen) # Fullscreen Zen
        
##        # File Dictionary
##        self.fileCount = -1
        
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
        self.ui.tabbar_bottom = QtGui.QTabBar()
        self.ui.fr_bottom.layout().addWidget(self.ui.tabbar_bottom)
        self.ui.tabbar_bottom.currentChanged.connect(self.pluginBottomChange)
        self.ui.tabbar_bottom.setShape(1)
        self.ui.tabbar_bottom.setExpanding(0)
        # Add down arrow
        self.ui.tabbar_bottom.addTab(QtGui.QIcon(self.iconPath+'tri_down.png'),'')
        self.ui.tabbar_bottom.setTabToolTip(0,'Hide bottom plugins')
        
        # Add button
##        plugin_add_btn = QtGui.QPushButton('Add')
##        self.ui.fr_bottom.layout().addItem(QtGui.QSpacerItem(1,1,QtGui.QSizePolicy.Expanding))
##        self.ui.fr_bottom.layout().addWidget(plugin_add_btn)
##        plugin_add_btn.setMenu(self.addPluginMenu)
        
##        self.ui.b_toggle_find.toggle()
##        self.ui.fr_find.hide()
        self.ui.b_toggle_find.hide()
        
        # Add Plugins
        self.HomeWidget = None
        self.pluginD = {}
        self.prevPlugin=1
        curdir = os.path.abspath('.')
        for plug in self.settings['activePlugins']:
##            try:
                self.addPlugin(plug)
##            except:
##                QtGui.QMessageBox.warning(self,'Plugin Load Failed','Could not load plugin: '+plug)
        os.chdir(curdir)
        self.ui.tabbar_bottom.setCurrentIndex(0)
        
        # Add Menu Plugins
##        self.addPluginMenu = QtGui.QMenu()
##        for plug in self.settings['otherPlugins']:
##            self.addPluginMenu.addAction()
        
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
##        self.ui.b_workspace.setMenu(self.workspaceMenu)
        
        # add Main Button to tabbar
        self.armadilloMenu = ArmadilloMenu(self)
        self.ui.b_main.setMenu(self.armadilloMenu)
        
##        # Load custom setup
##        self.loadSetup()
        

##        self.addStart()
        
        # Open file if in sys arg
        # print "SYS",sys.argv
        if len(sys.argv)>1:
            if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
                self.openFile(sys.argv[1])
        
        self.setFocus()
        
        # Add Start/Home
        QtGui.QApplication.processEvents()
        self.showHome()
##        self.HomeWidget.toggleHome(0)
        
        # Add blank workspace
##        self.workspaceOpen(None)

        
    #---Events
    def closeEvent(self,event):
        cancelled = 0
        # Close all workspaces
        for wksp in self.workspaces.keys():
            ok = self.workspaceClose(wksp)
            if not ok:
                cancelled=1
                break
        
        # Check if anything needs saving
##        for file_id in self.fileOpenD:
####            file_id = self.ui.tab.tabData(i).toInt()[0]
##            wdg = self.fileOpenD[file_id]
##            ok = self.checkSave(wdg)
##            if not ok:
##                cancelled = 1
##                break

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
##                self.HomeWidget.toggleHome(0)
            handled=True

        if not handled:
            QtGui.QWidget.dropEvent(self,event)

    def dragEvent(self,event):
        event.accept()
    
    def dragEnterEvent(self,event):
        event.accept()
    
    def resizeEvent(self,event):
        self.evnt.resized.emit()
    
##    def tabMousePressEvent(self,event):
####        print event.button(),event.button() == QtCore.Qt.MidButton
##        if event.button() == QtCore.Qt.MidButton:
##            i = self.ui.tab.tabAt(event.pos())
##            self.closeTab(i)
##        else:
##            QtGui.QTabBar.mousePressEvent(self.ui.tab, event)
    
    #---Fullscreen Modes
    def toggleFullEditor(self):
        self.editor_fullmode = not self.editor_fullmode
        zen=self.editor_fullmode
        self.ui.l_statusbar.setVisible(not zen)
        self.ui.fr_topbar.setVisible(not zen)
        self.ui.fr_left.setVisible(not zen)
        self.ui.sw_bottom.setVisible(not zen)
        self.ui.fr_bottom.setVisible(not zen)
##        self.ui.fr_tabs.setVisible(not self.fullscreen_mode)
##        if zen:
##            self.ui.tab_right.setVisible(not zen)
            
        if zen:
            self.pluginBottomChange(0)
        else:
            self.pluginBottomChange(self.ui.tabbar_bottom.currentIndex())
##            self.ui.fr_tabs.setVisible(1)
        
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
    def getFileId(self,filename):
        file_id = None
        if filename == None:
            pass
        elif os.name =='nt': # Check lower path name for windows
            for f in self.fileD:
                if self.fileD[f]['filename'] != None and os.path.abspath(self.fileD[f]['filename']).lower() == os.path.abspath(filename).lower():
                    file_id = f
        else:
            for f in self.fileD:
                if self.fileD[f]['filename'] != None and os.path.abspath(self.fileD[f]['filename']) == os.path.abspath(filename):
                    file_id = f
        
        if file_id == None:
            self.fileCount += 1
            file_id = self.fileCount
            self.fileD[file_id]={'filename':filename,'tabs':[],'editor':None}
        
        return file_id
                
    def isFileOpen(self,filename):
        # Check if file open and return tab index
        fileopen = -1
        for file_id in self.fileOpenD:
##            file_id = self.ui.tab.tabData(i).toInt()[0]
            wdg = self.fileOpenD[file_id]
            if wdg.filename != None and os.path.abspath(wdg.filename).lower() == os.path.abspath(filename).lower():
                self.changeTab(file_id)
                fileopen = file_id
##                self.ui.tab.setCurrentIndex(i)
##                fileopen = i
##                self.ui.tab.setTabEnabled(i,1)
                break
        return fileopen
    
    def getTitle(self,filename):
        title = os.path.basename(filename)
        if int(self.settings['view_folder']):
            title = os.path.split(os.path.dirname(filename))[1]+'/'+title
        elif filename.endswith('.py') and title=='__init__.py':
            title = os.path.split(os.path.dirname(filename))[1]+'/init'
        return title
    
    def getIconPath(self,filename):
        ext = os.path.splitext(str(filename))[1][1:]
        lang = ext

        if ext in self.settings['extensions']:
            lang = self.settings['extensions'][ext]
        ipth = self.iconPath+'files/_blank.png'
        fipth = self.iconPath+'files/'+str(lang)+'.png'
        if os.path.exists(fipth):
            ipth = fipth
        elif filename != None:
            ext = os.path.splitext(filename)[1][1:]
            if os.path.exists(self.iconPath+'files/'+ext+'.png'):
                ipth = self.iconPath+'files/'+ext+'.png'
        
        return ipth
    
    def openFile(self,filename=None,editor=None,file_id=None):
        if file_id != None:
            if file_id in self.fileOpenD:
                self.changeTab(file_id)
                return
            else:
                filename = self.fileD[file_id]['filename']
##        print 'open',filename
        if not filename:
            # Ask for filename if not specified
            filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",self.currentPath," (*.*)")
            if filename=='':
                filename = None
            else:
                filename = str(filename)
        if filename != None:
            if os.path.isfile(filename):
                filename = filename.replace('\\','/')
                # Check if file already open
                file_open = self.isFileOpen(filename)
                if file_open !=-1:
                    self.changeTab(file_open)
##                    self.ui.sw_main.setCurrentIndex(file_open)
##                    self.ui.tab.setTabEnabled(file_open,1)
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
                        title = self.getTitle(filename)
##                        title = os.path.basename(filename)
##                        if int(self.settings['view_folder']):
##                            title = os.path.split(os.path.dirname(filename))[1]+'/'+title
##                        elif lang == 'python' and title=='__init__.py':
##                            title = os.path.split(os.path.dirname(filename))[1]+'/init'
                        
                        try:
                            f = codecs.open(filename,'r','utf-8')
                            txt = f.read()
                            f.close()
                            
                        except:
                            QtGui.QMessageBox.warning(self,'Error Opening File','The following file could not be read.  Make sure it is ascii or utf-8 encoded<br><br>'+filename)
                            txt = None
                        
                        if txt != None:
                            # Create Widget
                            wdg = self.addEditorWidget(lang,title,str(filename),editor=editor) #,code=txt)
                            wdg.setEnabled(0)
                            self.ui.l_statusbar.setText('Loading...'+os.path.basename(filename))
                            QtGui.QApplication.processEvents()
                            wdg.setText(txt)
                            wdg.lastText = txt
                            wdg.displayTitle = wdg.title
##                            self.ui.tab.setTabText(self.ui.sw_main.indexOf(wdg),wdg.title)
                            self.ui.l_filename.setText(wdg.title)
                            wdg.modTime = os.path.getmtime(filename)
                            wdg.setEnabled(1)
                            self.ui.l_statusbar.setText('')
                            
                            # Remove Startpage
##                            self.removeStart()
                            
                            # Update tab text
                            for t in self.fileD[wdg.id]['tabs']:
                                t.setTitle(wdg.displayTitle)
                            
                            self.evnt.fileOpened.emit(wdg)
                            
                            # Add to workspace tab
##                if not filename in self.workspaces[self.currentWorkspace]['filelist']:
##                    print 'add to workspace'
##                    self.tabspace.tabs.currentWidget().addEditortab(wdg.id,wdg.title,wdg.filename)
                            
##                        if self.ui.tab.count() ==1:
##                            self.changeTab(0)
                            
                # Close Home if visible
##                if self.HUDWidget != None and self.HUDWidget.webview.isVisible():
##                    self.HUDWidget.webview.hide()
    ##                    self.filesystemwatcher.addPath(filename)
    ##                    self.fileModD[filename]=os.path.getmtime(filename)
##                        self.updateOutline()
     


    #---Editor
    def addEditorWidget(self,lang=None,title='New',filename=None,editor=None,code=''):
        file_id = self.getFileId(filename)
        sw_ind = self.ui.sw_main.count()
        wdg = None
        
        if filename == None and title=='New': 
            title = 'New '+lang
            
        
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
        wdg.displayTitle = title
        wdg.id = file_id
        wdg.lang = lang
        wdg.viewOnly = 0
        wdg.editor = editor
        wdg.pluginRightVisible=0
##        wdg.setText(code)
        if lang=='Start':wdg.editor='Start'
        wdg.modTime = None
        self.fileOpenD[file_id]=wdg
        
        # MOVED to end
##        self.evnt.editorAdded.emit(wdg)
##
##        if 'editorTextChanged' in dir(wdg):
##            wdg.evnt.editorChanged.connect(self.editorTextChanged)
##        if 'visibleLinesChanged' in dir(wdg):
##            wdg.evnt.visibleLinesChanged.connect(self.visibleLinesChanged)
##            
####        if 'editingFinished' in  dir(wdg):
####            wdg.evnt.editingFinished.connect(self.editingFinished)
            
        # Insert widget to page
        self.ui.sw_main.insertWidget(sw_ind,wdg)
        self.ui.sw_main.setCurrentIndex(sw_ind)
        
        # Insert Tab on top
##        self.ui.tab.insertTab(sw_ind+1,title)
##        self.ui.tab.setTabData(sw_ind,self.fileCount)
##        self.ui.tab.setCurrentIndex(sw_ind)
##        self.ui.tab.setTabToolTip(sw_ind,str(filename))

        
        # Add Icon
        ipth = self.iconPath+'/files/_blank.png'
        icn = QtGui.QPixmap(ipth)
        ipth = self.iconPath+'files/'+str(lang)+'.png'
        if os.path.exists(ipth):
            icn = QtGui.QPixmap(ipth)
        elif filename != None:
            ext = os.path.splitext(filename)[1][1:]
            if os.path.exists(self.iconPath+'files/'+ext+'.png'):
                icn = QtGui.QPixmap(self.iconPath+'files/'+ext+'.png')
        elif os.path.exists(self.editorPath+editor+'/'+editor+'.png'):
            icn = QtGui.QPixmap(self.editorPath+editor+'/'+editor+'.png')
        self.ui.b_tabicon.setIcon(QtGui.QIcon(icn))
        wdg.icon = QtGui.QIcon(icn)
        wdg.pic = icn
        # Insert tab in workspace
        self.addWorkspaceEditor(wdg.id,wdg.title,wdg.filename)

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
        
        # Emit Signals
        self.evnt.editorAdded.emit(wdg)

        if 'editorTextChanged' in dir(wdg):
            wdg.evnt.editorChanged.connect(self.editorTextChanged)
        if 'visibleLinesChanged' in dir(wdg):
            wdg.evnt.visibleLinesChanged.connect(self.visibleLinesChanged)
##      
        if self.ui.sw_main.count() ==1:
            self.change_tab(0)

        return wdg

    def currentEditor(self):
        return self.ui.sw_main.currentWidget()

    def change_tab(self,sw_ind):
        if self.currentEditor() != None:
            file_id = self.currentEditor().id
            if file_id != None:
                self.changeTab(file_id)
            else:
                self.ui.sw_main.setCurrentIndex(sw_ind)
                self.ui.b_closetab.hide()
                try:
                    self.ui.l_filename.setText(self.ui.sw_main.widget(sw_ind).title)
                except:
                    self.ui.l_filename.setText('')
                try:
                    self.ui.b_tabicon.setIcon(self.ui.sw_main.widget(sw_ind).icon)
                except:
                    self.ui.b_tabicon.setIcon(QtGui.QIcon())
        else:
            self.ui.b_closetab.hide()

    def changeTab(self,file_id):
        self.ui.l_statusbar.setText('')
    
##        if tab_ind == -1 and self.ui.tab.count()>0: tab_ind == 0
##        if sys.version_info.major==3:
##            file_id = self.ui.tab.tabData(tab_ind)  # Python3 compatible code
##        else:
##        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
##        print 'change tab',file_id,file_id in self.fileOpenD
        if file_id in self.fileOpenD:
            wdg = self.fileOpenD[file_id]
            self.ui.sw_main.setCurrentWidget(wdg)
            self.evnt.editorTabChanged.emit(wdg)
            self.ui.l_filename.setText(wdg.displayTitle)
            if wdg.filename != None:
                self.ui.fr_tab.setToolTip(wdg.filename)
##                self.ui.l_filename.setToolTip(wdg.filename)
            else:
##                self.ui.l_filename.setToolTip('New File (unsaved)')
                self.ui.fr_tab.setToolTip('New File (unsaved)')
            try:
                self.ui.b_tabicon.setIcon(wdg.icon)
            except:
##                print('error loading icon: '+wdg.title)
                pass
            # Show/Hide plugins
            lang = wdg.lang
            
            self.ui.b_closetab.show()
        else:
            wdg = None
            lang = None
            
            self.ui.b_closetab.hide()
            self.ui.l_filename.setText(wdg.title)

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
            
            # Update recent tabs list
            if wdg.id in self.recentTabs:
                self.recentTabs.remove(wdg.id)
            self.recentTabs.append(wdg.id)
        
            # Check for file changes (Disabled for now)
##            self.checkFileChanges()
                
    def close_tab(self):
        if self.currentEditor() != None:
            if len(self.recentTabs) > 1:
                prevtab = self.recentTabs[-2]
            
            file_id = self.currentEditor().id
            self.closeTab(file_id)
            
            if len(self.recentTabs) > 1:
                self.changeTab(prevtab)
    
    def closeTab(self,file_id,remove_from_workspace=1):
##        if sys.version_info.major==3:
##            file_id = self.ui.tab.tabData(tab_ind)
##        else:
##        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
##        print 'close',file_id
        ok = 1
        if file_id >-1 and file_id in self.fileOpenD:
            wdg = self.fileOpenD[file_id]
            filename = wdg.filename
            
            # Check Save
            if 'getText' in dir(wdg):
                ok = self.checkSave(wdg)
                    
            if ok:
                # Emit close signal
                self.evnt.editorTabClosed.emit(wdg)
                
                self.fileOpenD.pop(file_id)
                # Remove Tab
    ##            self.ui.tab.removeTab(tab_ind)
                # Remove Widget
                self.ui.sw_main.removeWidget(wdg)
                
                if file_id in self.recentTabs:
                    self.recentTabs.remove(file_id)
                    
                # Remove from workspace tabs
                if remove_from_workspace:
                    for t in self.fileD[file_id]['tabs']:
                        t.close(ignoreCheck=1)
                        self.fileD[file_id]['tabs'].remove(t)
                
                del wdg
                # Add start page if no tabs exist
    ##            if self.ui.sw_main.count() == 0:
    ##                self.addStart()
        return ok

    def editorTextChanged(self):
        # Indicate if text changed
        wdg = self.currentEditor()
        try:
            if wdg.lastText != wdg.getText():
##                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title+'*')
                
                wdg.displayTitle=wdg.title+'*'
            else:
##                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
                wdg.displayTitle=wdg.title
            self.ui.l_filename.setText(wdg.displayTitle)
        except:
            self.ui.l_statusbar.setText('Error: text changed signal')
        
        # Update tab display title
        if wdg.id != None:
            for t in self.fileD[wdg.id]['tabs']:
                t.setTitle(wdg.displayTitle)
    
        # Check for file changes
##        self.checkFileChanges()
    
    def visibleLinesChanged(self,wdg,lines):
        self.evnt.editorVisibleLinesChanged.emit(wdg,lines)

    def checkSave(self,wdg):
        ok = 0
        if wdg.viewOnly:
            ok = 1
        else:
            if 'getText' in dir(wdg):
                try:
##                    if wdg.lastText != unicode(wdg.getText(),'utf-8'):
                    if wdg.lastText != wdg.getText():
                        resp = QtGui.QMessageBox.warning(self,'Save File',"Do you want to save the file <b>"+wdg.title+"</b>?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
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

    #---Editor Tools
    def editorSave(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        
        if wdg != None:
            if wdg.filename != None:
                filename = wdg.filename
            else:
                fileext = ''
                # Don't show extensions for now (not working in Linux)
                if os.name =='nt':
                    for e in self.settings['extensions']:
                        if self.settings['extensions'][e]==wdg.lang:
                            fileext+=wdg.lang+' (*.'+e+");;"
                fileext += "All (*.*)"
                
                filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",self.currentPath,fileext)
                if filename=='':
                    filename=None
                else:
                    wdg.filename = os.path.abspath(str(filename))
                    wdg.title = os.path.basename(wdg.filename)
    ##                ind = self.ui.tab.currentIndex()
    ##                self.ui.tab.setTabText(ind,wdg.title)
    ##                self.ui.tab.setTabToolTip(ind,wdg.filename)
                    self.ui.l_filename.setText(wdg.title)
                    wdg.displayTitle = wdg.title
                    self.ui.l_filename.setToolTip(wdg.filename)

            if filename != None:
                try:
                    txt = wdg.getText()
                    f = codecs.open(wdg.filename,'w','utf8')
                    f.write(txt)
                    f.close()
                    wdg.lastText = txt
                    wdg.modTime = os.path.getmtime(filename)
                    self.ui.l_statusbar.setText('Saved: '+wdg.title)#+' at '+datetime.datetime.now().ctime(),3000)
    ##                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
                    self.ui.l_filename.setText(wdg.title)
                    wdg.displayTitle = wdg.title
                    self.ui.l_filename.setToolTip(wdg.filename)
                except:
                    QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it.  You may want to copy the text, paste it in another editor to not lose your work.<br><br><b>Error:</b><br>'+str(sys.exc_info()[1]))
                    self.ui.l_statusbar.setText('Error Saving: '+filename)
                
                # Save Signal
                self.evnt.editorSaved.emit(wdg)
                
                # If Settings File, reload
                if filename == self.settings_filename:
                    self.loadSettings()
            
            # Update tabs
            for t in self.fileD[wdg.id]['tabs']:
                t.setTitle(wdg.title)
                t.item.setToolTip(wdg.filename)
            
    def editorSaveAs(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        fileext = ''
        if wdg.filename != None:
            pth = wdg.filename
        else:
            pth = self.currentPath
        
        if os.name =='nt':
            for e in self.settings['extensions']:
                if self.settings['extensions'][e]==wdg.lang:
                    fileext+=wdg.lang+' (*.'+e+");;"
        fileext += "All (*.*)"
        
        filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",pth,fileext)
        if filename!='':
            
##            ind = self.ui.tab.currentIndex()
            wdg.filename = os.path.abspath(str(filename))
            wdg.title = os.path.basename(wdg.filename)
            self.ui.l_filename.setText(wdg.title)
            wdg.displayTitle = wdg.title
##            self.ui.tab.setTabText(ind,wdg.title)
##            self.ui.tab.setTabToolTip(ind,str(filename))
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
                if 'preview' in self.pluginD:
                    self.pluginD['preview'].previewRun(wdg)
                    if self.ui.tab_right.isHidden():
                        self.toggleRightPlugin()
                else:
                    QtGui.QMessageBox.warning(self,'No Preview Plugin','The Preview plugin is not available.<br><br>Please add it to the activePlugins settings')
            else:
                ok = self.checkSave(wdg)
                filename = str(wdg.filename)
                if ok and filename != 'None':
                    if wdg.lang in self.settings['run']:
                        # Otherwise run in output
                        runD = self.settings['run'][wdg.lang]
                        self.pluginD['output'].runProcess(runD['cmd'],wdg)

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
    
    def colorPicker(self):
        clrdlg = QtGui.QColorDialog(self)
        clr=clrdlg.getColor(QtGui.QColor(255,255,255),self,'Select color',QtGui.QColorDialog.ShowAlphaChannel)
        if clr.isValid():
            r,g,b,a = clr.getRgb()
            atxt=apfx=''
            if a < 255:
                atxt=',%0.2g' %(a/255.0)
                apfx='a'
            txt = 'rgb%s(%d,%d,%d%s)' %(apfx,r,g,b,atxt)
            if 'insertText' in dir(self.currentEditor()):
                self.currentEditor().insertText(txt)

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
                ti=self.ui.tabbar_bottom.addTab(icn,tabtext)
                self.ui.tabbar_bottom.setTabToolTip(ti,title)
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

    #---   Right Plugins
    def toggleRightPlugin(self):
        if self.ui.tab_right.isVisible() and self.ui.sw_main.isHidden():
            self.toggleRightPluginFull()
        self.ui.tab_right.setVisible(self.ui.tab_right.isHidden())
        if self.currentEditor() != None:
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
##            wdg.linkClicked.connect(self.urlClicked)
##            self.ui.tab.setTabIcon(self.ui.tab.currentIndex(),QtGui.QIcon(self.iconPath+'page_preview.png'))
            wdg.pic = QtGui.QPixmap(self.iconPath+'page_preview.png')
            wdg.icon = QtGui.QIcon(wdg.pic)
            self.ui.b_tabicon.setIcon(wdg.icon)
    
        else:
##            self.ui.tab.setCurrentIndex(openfile)
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
##        QtGui.QApplication.processEvents()
##        self.changeTab(self.ui.tab.currentIndex())
    
    def showHome(self):
        if self.HomeWidget != None:
            self.HomeWidget.toggleHome()
    
    def showTabspace(self):
##        # Add tabs
##        self.tabworkspace.addEditortab(1,'a file.py','')
##        self.tabworkspace.addEditortab(1,'help.md','')
        
        self.tabspace.toggle()
    
    def createTabspace(self):
        import tabspace
        self.tabspace = tabspace.TabSpace(parent=self)
##        self.tabworkspace = self.tabspace.addWorkspace('workspace 1')
##        self.tabspace.addWorkspace('workspace 2')
    
    #---Shortcuts
    def findFocus(self):
        if self.ui.fr_topbar.isHidden():
            self.ui.fr_topbar.setVisible(1)
        if self.ui.fr_find.isHidden():
            self.ui.b_toggle_find.toggle()
        self.ui.le_find.setFocus()
        self.ui.le_find.selectAll()
        
    def gotoFocus(self):
        if self.ui.fr_topbar.isHidden():
            self.ui.fr_topbar.setVisible(1)
        if self.ui.fr_find.isHidden():
            self.ui.b_toggle_find.toggle()
        self.ui.le_goto.setFocus()
        self.ui.le_goto.selectAll()
        
    def nextTab(self):
        
##        i = self.ui.sw_main.indexOf(self.recentTabs[1])
        
        i = self.ui.sw_main.currentIndex()+1
        if i == self.ui.sw_main.count():i=0
        self.ui.sw_main.setCurrentIndex(i)
    
    #---Workspace
    def workspaceSave(self,wksp=None):
        
        if wksp == None:
            wksp = self.currentWorkspace
        # Save the current Workspace
        if wksp != None:
            if wksp not in self.workspaces or self.workspaces[wksp]['type'] != 'blank':
                if not os.path.exists(self.settingPath+'/workspaces'):
                    os.mkdir(self.settingPath+'/workspaces')
                
                wD={'files':[],'basefolder':None,'lastOpenFile':None}
    ##            ci = self.ui.tab.currentIndex()
                # Save workspace files
                if wksp in self.workspaces:
                    li_wdg = self.workspaces[wksp]['widget']
                    for i in range(li_wdg.count()):
                        itm = li_wdg.itemWidget(li_wdg.item(i))
                        file_id = itm.id
        ##                file_id = self.ui.tab.tabData(i).toInt()[0]
        ##                if file_id in self.fileOpenD:
                        
                        if file_id in self.fileOpenD:
                            wdg = self.fileOpenD[file_id]
                            editor = wdg.editor
                        else:
                            editor = itm.editor
                        if itm.filename != None:
                            wD['files'].append({'filename':itm.filename,'editor':editor})
        ##                    if i==ci:
                    if self.currentEditor() != None:
                        wD['lastOpenFile']=self.currentEditor().filename
                
                    # Save workspace dir
                    wD['basefolder']=self.workspaces[wksp]['basefolder']
                f = open(self.settingPath+'/workspaces/'+wksp,'w')
                f.write(json.dumps(wD))
                f.close()
    
    def workspaceOpen(self,wksp,show_tabs=1):
##        self.workspaceSave()
##        ok = self.deactivateWorkspace(self.currentWorkspace)
##        ok = self.workspaceClose(askSave=0)
##        ok=1
        
        # Load workspace
        if wksp in self.workspaces: # and wksp != None:
            self.evnt.workspaceChanged.emit(wksp)
        else:
            self.workspaceCount +=1
            
            wtype = 'workspace'
            # Create Blank Workspace
            if wksp == None:
                wtype='blank'
                wksp = 'workspace '+str(self.workspaceCount)
                self.workspaces[wksp]={'files':[],'basefolder':None,'lastOpenFile':None}
            else:
                # Open existing workspace settings
                f = open(self.settingPath+'/workspaces/'+wksp,'r')
                wD = json.loads(f.read())
                f.close()
                self.workspaces[wksp]=wD.copy()
            
            self.currentWorkspace=wksp
            wD = self.workspaces[wksp]
##            self.workspaces[wksp]['filelist']=[]
            
            # Add workspace to tabspace
            wD['widget'] = self.tabspace.addWorkspace(wksp)
            wD['type'] = wtype
            
            
            # Load Files
            last_file = None
            for f in wD['files']:
                if f not in [None,'None','']:
                    if type(f) == type({}):
##                        self.openFile(f['filename'],editor=f['editor'])
##                        self.workspaces[wksp]['filelist'].append(f['filename'])
##                        fid = self.isFileOpen(f['filename'])
##                        if fid == -1:
##                            fid = None
                        fid = self.getFileId(f['filename'])
                        self.addWorkspaceEditor(fid,self.getTitle(f['filename']),f['filename'],f['editor'])
                        last_file =f['filename']
##                    else:
##                        self.openFile(f)

            # Goto lastopen file
            if 'lastOpenFile' in wD:
                last_file = wD['lastOpenFile']
##                for file_id in self.fileOpenD:
####                    file_id = self.ui.tab.tabData(i).toInt()[0]
####                    if file_id in self.fileOpenD:
##                        wdg = self.fileOpenD[file_id]
##                        if wdg.filename == wD['lastOpenFile']:
##                            self.changeTab(file_id)
##                            last_file =f['filename']
##                            break
            if last_file != None:
                self.openFile(last_file)
            
##            if 'basefolder' in wD and wD['basefolder'] != None:
##                if 'filebrowser' in self.pluginD:
##                    self.pluginD['filebrowser'].ui.le_root.setText(wD['basefolder'])
##                    self.pluginD['filebrowser'].loadRoot()
            
            
            
            self.workspaceMenu.saveWact.setDisabled(0)
            self.workspaceMenu.renameWact.setDisabled(0)
            self.workspaceMenu.closeWact.setDisabled(0)
            
            if show_tabs:
                self.showTabspace()
            
            
            self.evnt.workspaceOpened.emit(wksp)
        
##            self.workspaces[wksp]={}
            
##            QtGui.QApplication.processEvents()
##            self.removeStart()
            
##            if self.ui.sw_main.count() ==1:
##                self.changeTab(0)
    
    def addWorkspaceEditor(self,file_id,title,filename,editor=''):
        if self.currentWorkspace == None:
            self.workspaceOpen(None,show_tabs=0)
        tab = self.tabspace.tabs.currentWidget().addEditortab(file_id,title,filename,editor)
        if not tab in self.fileD[file_id]['tabs']:
            self.fileD[file_id]['tabs'].append(tab)
    
    def workspaceNew(self):
        # New Workspace
        resp,ok = QtGui.QInputDialog.getText(self,'New Workspace','Enter Workspace Name')
        if ok and not resp.isEmpty():
##            self.currentWorkspace = resp
##            self.workspaceSave(str(resp))
            self.workspaceSave(str(resp))
            self.workspaceOpen(str(resp))
##            self.workspaceSave(str(resp))
##            self.workspaceMenu.loadMenu()
##            self.workspaceMenu.saveWact.setDisabled(0)
##            self.workspaceMenu.closeWact.setDisabled(0)
    
##    def activateWorkspace(self,workspace):
##        print 'activate workspace'
##    
##    def deactivateWorkspace(self,workspace):
##        if self.currentWorkspace != None:
##            print 'deactivate workspace'
####            for i in range(self.ui.tab.count()):
####                file_id = self.ui.tab.tabData(i).toInt()[0]
####                self.ui.tab.setTabEnabled(i,False)
##        
##        
##        return 1
    
    def workspaceRename(self,wksp=None):
        if os.path.exists(self.settingPath+'/workspaces'):
            if wksp == None:
                resp,ok = QtGui.QInputDialog.getItem(self,'Rename Workspace','Select the workspace to rename',QtCore.QStringList(sorted(os.listdir(self.settingPath+'/workspaces'))),editable=0)
                if ok: wksp = str(resp)
            if wksp != None:
                owskp=wksp
                pth = self.settingPath+'/workspaces/'+owskp
                resp,ok = QtGui.QInputDialog.getText(self,'Rename Workspace','Enter Workspace Name',QtGui.QLineEdit.Normal,str(owskp))
                if ok and not resp.isEmpty():
                    # save and close workspace if open
                    if owskp in self.workspaces:
##                        self.parent.workspaceSave(owskp)
                        self.workspaceClose(owskp)
                    npth = self.settingPath+'/workspaces/'+str(resp)
                    os.rename(pth,npth)
                    self.loadMenu()
                    self.workspaceOpen(str(resp))
##                        if owskp == self.parent.workspace:
##                            self.parent.workspace=str(resp)
        else:
            QtGui.QMessageBox.warning(self,'No Workspaces','There are no workspaces to rename')
    
    def workspaceClose(self,wksp=None,askSave=0,openStart=0):
        wk_ok = 1
        
        if wksp == None:
            wksp = self.currentWorkspace
        
        # Save current workspace
        fl_ok = 1
        if wksp != None:
            self.workspaceSave()
            
            # Close 
            wksp_tabs = self.workspaces[wksp]['widget'].tabD.keys()
            for fid in wksp_tabs[:]:
                if fid in self.fileOpenD.keys():
##                    print 'close',fid,self.fileD[fid]['tabs']
                    if len(self.fileD[fid]['tabs']) < 2:
                        fl_ok = self.closeTab(fid,remove_from_workspace=0)
##                        print 'ok',fl_ok
                        if not fl_ok:
                            break
            
##        if wksp != None and askSave:
##            wk_ok=0
##            resp = QtGui.QMessageBox.warning(self,'Save Workspace',"Do you want to save the current workspace <b>"+self.currentWorkspace+"</b> first?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
##            if resp == QtGui.QMessageBox.Yes:
##                self.workspaceSave()
##                wk_ok =1
##            elif resp == QtGui.QMessageBox.No:
##                wk_ok =1
                
        # Close open files
        
        if wk_ok:
            pass
            # Check if anything needs saving and if not in other workspace
##            for file_id in self.fileOpenD.keys():
##                file_id = self.ui.tab.tabData(i).toInt()[0]
##                self.closeTab(file_id)
        
        ok=fl_ok*wk_ok
        
        if ok:
            self.evnt.workspaceClosed.emit(wksp)
##            self.currentWorkspace=None
            self.workspaces.pop(str(wksp))

            self.workspaceMenu.saveWact.setDisabled(1)
            self.workspaceMenu.closeWact.setDisabled(1)
        
##        if ok and openStart and self.ui.sw_main.count()==0:
####            self.addStart()
####            print self.HUDWidget
##            if self.HUDWidget != None:
##                self.HUDWidget.toggleHUD()
        
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
        if self.currentWorkspace != None and int(self.settings['save_workspace_on_close']):
            self.workspaceSave()

##        # Save Window Geometry
##        f = open(self.settingPath+'/window','wb')
##        f.write(self.saveState())
##        f.close()

    #---FileModify Checker
    def checkFileChanges(self):
##        while 1:
##        if self.fileLastCheck < time.time()-5:##        if self.fileLastCheck < time.time()-5:
            chngs = 0
            close_tabs = []
            for file_id in self.fileOpenD:
##                file_id = self.ui.tab.tabData(i).toInt()[0]
##                if file_id in self.fileOpenD:
                wdg = self.fileOpenD[file_id]
                if wdg.filename != None and wdg.modTime != None:
                    if not os.path.exists(wdg.filename):
                        resp = QtGui.QMessageBox.warning(self,'File Does not exist',str(wdg.filename)+' does not exist anymore.<br><<br>Do you want to keep the file open?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        if resp == QtGui.QMessageBox.No:
                            close_tabs.append(file_id)
                        chngs = 1
                    elif os.path.getmtime(wdg.filename) > wdg.modTime:
                        resp = QtGui.QMessageBox.warning(self,'File Modified',str(wdg.filename)+' has been modified.<br><<br>Do you want to reload it?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        
                        chngs=1
                        if resp == QtGui.QMessageBox.Yes:
                            QtGui.QApplication.processEvents()
                            f = codecs.open(wdg.filename,'r','utf-8')
                            txt = f.read()
                            f.close()
                            wdg.setText(txt)
                            wdg.modTime = os.path.getmtime(wdg.filename)
            
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
