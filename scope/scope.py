# --------------------------------------------------------------------------------
# Scope IDE
#
# developed by lucidlylogicole
#
# Scope is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

# VERSION
__version__ = '0.6.4-dev'

# Make sure qvariant works for Python 2 and 3
import sip
##sip.setapi('QString',1)
sip.setapi('QVariant',1)

import sys, json, codecs, time, importlib, subprocess
from PyQt4 import QtCore, QtGui, QtWebKit
from menus import *
import os,shutil,datetime, webbrowser, threading, sys

class Scope(QtGui.QWidget):
    def __init__(self, parent=None,dev_mode=0):

        # Version
        self.version = __version__
        self.dev_mode = dev_mode   # Development Mode

        # Setup UI
        QtGui.QWidget.__init__(self, parent)
        from scope_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
    def load(self):
        #--- Paths
        rpath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0].replace('\\','/')
        self.iconPath=rpath+'/style/img/'
        self.settingPath = os.path.expanduser('~').replace('\\','/')+'/.scope'
        self.pluginPath = rpath+'/plugins/'
        self.editorPath = rpath+'/plugins/'
        self.scopePath = rpath
        self.currentPath = os.path.expanduser('~')
        if os.name =='nt':
            self.pathPrefix="file:///"
        else:
            self.pathPrefix="file://"
        
        # File Variables
        self.fileOpenD = {} # keep track of open files and associated widgets
        self.fileD = {}     # keep track of all filenames and new files
        self.recentTabs = [] # Keep track of most recent tabs
        self.fileCount = -1
        self.ui.b_closetab.hide()
        self.saveEnabled = 1   # Enable saving to local file
        self.last_editable_file = None # Last file from the editor
        
        # Workspace
        self.currentWorkspace = None
        self.workspaceCount = 0
        self.workspaces = {}
        
        #--- Editor Events
        class Events(QtCore.QObject):
            editorAdded = QtCore.pyqtSignal(QtGui.QWidget)
            editorTabChanged = QtCore.pyqtSignal(QtGui.QWidget)
            editorSaved = QtCore.pyqtSignal(QtGui.QWidget)
            editorBeforeSave = QtCore.pyqtSignal(QtGui.QWidget)
            
            editorVisibleLinesChanged = QtCore.pyqtSignal(QtGui.QWidget,tuple)
            close=QtCore.pyqtSignal()
            editorTabClosed = QtCore.pyqtSignal(QtGui.QWidget)
            fileOpened = QtCore.pyqtSignal(QtGui.QWidget)
            resized = QtCore.pyqtSignal()
            
            settingsLoaded = QtCore.pyqtSignal()
            
            # Workspace Events
            workspaceChanged = QtCore.pyqtSignal(str)
            workspaceOpened = QtCore.pyqtSignal(str)
            workspaceClosed = QtCore.pyqtSignal(str)
            
        self.Events = Events()
        
        # Settings
        self.loadSettings()

        if self.settings['widgetstyle'] != 'None':
            QtGui.QApplication.setStyle(self.settings['widgetstyle'])
        
        self.setAcceptDrops(1)

        # Style
        style_path = self.settings['style']
##        if not os.path.exists(os.path.abspath(style_path)):
##            style_path = 'style/default.css'

        f = open(style_path,'r')
        style = f.read()
        f.close()
        self.setStyleSheet(style)
        self.stylePath = os.path.abspath(style_path)
        
        #--- Window Setup
        
        # Default zen mode
        self.fullscreen_mode = 0
        self.editor_fullmode = 0
        
        # Screen Setup
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        coords= QtGui.QApplication.desktop().screenGeometry(screen).getCoords() 
        if self.settings['window']['openMode']==1:
            # get margins from settings
            dl=self.settings['window']['margin']['left']
            dr=self.settings['window']['margin']['right']
            dt=self.settings['window']['margin']['top']
            db=self.settings['window']['margin']['bottom']
            
            # set up width and height
            ws=coords[2]-coords[0] # screen width
            hs=coords[3]-coords[1] # screen height
            wd = self.settings['window']['size']['width'].strip()
            hd = self.settings['window']['size']['height'].strip()
            if wd.endswith('%'):
                w=float(wd[:-1])/100.0*ws
            else:
                try:
                    w=int(wd.replace('px','').strip())
                except:
                    w=ws
            if hd.endswith('%'):
                h=float(hd[:-1])/100.0*hs
            else:
                try:
                    h=int(hd.replace('px','').strip())
                except:
                    h=hs
            # Set screen size
            self.setGeometry(coords[0]+dl,coords[1]+dt,(w-dl-dr),(h-dt-db))
            QtGui.QApplication.processEvents()
        elif self.settings['window']['openMode']==2:
            # Fullscreen
            self.showMaximized()
            QtGui.QApplication.processEvents()

        self.ui.b_back.hide()

        # Setup plugin views
        # Bottom
        h=self.settings['pluginBottom']['height']
        self.ui.split_bottom.setSizes([self.height()-h,h])
        if self.settings['pluginBottom']['visible']!=1:
            self.ui.sw_bottom.setHidden(1)
        
        # Left
        lw=self.settings['pluginLeft']['width']
        self.ui.split_left.setSizes([lw,self.width()-lw])
        if self.settings['pluginLeft']['visible']!=1:
            self.ui.fr_left.setVisible(0)
        
        # Right
        rw=self.settings['pluginRight']['width']
        if rw.endswith('%'):
            rw = float(rw[:-1])/100*(self.width()-lw)
        else:
            rw=int(rw)
        
        self.ui.split_right.setSizes([self.width()-rw-lw,rw])
        if self.settings['pluginRight']['visible']!=1:
            self.ui.tab_right.setVisible(0)

        # Tab Direction
        tabLocD = {'top':QtGui.QTabWidget.North,'bottom':QtGui.QTabWidget.South,'left':QtGui.QTabWidget.West,'right':QtGui.QTabWidget.East}
        self.ui.tab_left.setTabPosition(tabLocD[self.settings['pluginLeft']['tabPosition']])
        self.ui.tab_right.setTabPosition(tabLocD[self.settings['pluginRight']['tabPosition']])

        #--- Signals
        self.ui.b_closetab.clicked.connect(self.close_tab)
        self.ui.sw_main.currentChanged.connect(self.change_tab)
        self.ui.b_show_tabs.clicked.connect(self.toggleWindowSwitcher)
        self.ui.b_settings.clicked.connect(self.openSettings)
        
        self.ui.b_home.clicked.connect(self.showHome)
        self.ui.b_new.clicked.connect(self.showNewMenu)
        self.ui.b_workspaces.clicked.connect(self.showWorkspaceMenu)
        
        self.ui.b_save.clicked.connect(self.editorSave)

        self.ui.b_indent.clicked.connect(self.editorIndent)
        self.ui.b_unindent.clicked.connect(self.editorUnindent)
        self.ui.b_comment.clicked.connect(self.editorToggleComment)
        self.ui.b_color_picker.clicked.connect(self.colorPicker)

        self.ui.b_run.clicked.connect(self.editorRun)
        
        self.ui.b_find.clicked.connect(self.editorFind)
        self.ui.le_goto.returnPressed.connect(self.editorGoto)

        self.ui.b_back.clicked.connect(self.back_to_editor)
##        self.fileOpenD={}
        
        # Create Window Switcher
        self.createWindowSwitcher()
        
        #--- Key Shortcuts
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_E,self,self.editorToggleComment) #Toggle Comment
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F,self.ui.sw_main,self.findFocus) # Find
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_G,self,self.gotoFocus) # Goto
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_M,self,self.ui.b_menu.click) # New
        QtGui.QShortcut(QtCore.Qt.ALT+QtCore.Qt.Key_F,self,self.ui.b_menu.click) # New
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_N,self,self.ui.b_new.click) # New
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_S,self,self.editorSave) # Save
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_W,self,self.editorWordWrap) # Toggle Wordwrap
        QtGui.QShortcut(QtCore.Qt.ALT+QtCore.Qt.Key_S,self,self.editorStats) # Editor Stats
        
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Tab,self,self.nextTab) # Toggle Wordwrap

        QtGui.QShortcut(QtCore.Qt.Key_F2,self,self.toggleLeftPlugin) # Toggle Left Plugin
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F2,self,self.nextLeftPlugin) # show next left plugin
        
        QtGui.QShortcut(QtCore.Qt.Key_F5,self,self.editorRun) # Run
        QtGui.QShortcut(QtCore.Qt.Key_F7,self,self.toggleRightPluginFull) # Expand Right plugin
        QtGui.QShortcut(QtCore.Qt.Key_F3,self,self.toggleRightPlugin) # Toggle RIght Plugins
        
        QtGui.QShortcut(QtCore.Qt.Key_F4,self,self.toggleBottomPlugin) # Hide Bottom Tab
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F4,self,self.nextBottomPlugin) # Show next bottom tab
        QtGui.QShortcut(QtCore.Qt.Key_F1,self,self.toggleWindowSwitcher) # Show Tabbar
        QtGui.QShortcut(QtCore.Qt.Key_F10,self,self.toggleFullEditor) # Editor full screen, but keep tabs
        QtGui.QShortcut(QtCore.Qt.Key_F11,self,self.toggleFullscreen) # Fullscreen Zen
        
        #--- Load Editors (and languages)
        self.editorD = {}
        self.Editors = {}
        for e in self.settings['activeEditors']:
            try:
                mod = importlib.import_module('plugins.'+e+'.scope_editor')
                self.Editors[e] = mod.Editor(self)
                ld = self.Editors[e].getLang()
            except:
                QtGui.QMessageBox.warning(self,'Failed to Load Editor','The editor, '+e+' failed to load')
                ld = []
            
            if ld != []:
                self.editorD[e] = ld

                for l in ld:
                    if l not in self.settings['extensions']:
                        self.settings['extensions'][l]=l

        #--- Add Menus
        # New Button Menu
        self.newMenu = NewMenu(self)

        # Workspace Button Menu
        self.workspaceMenu = WorkspaceMenu(self)

        # add Main Button to tabbar
        self.editorMenu = EditorMenu(self)
        self.ui.b_menu.setMenu(self.editorMenu)
        
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
        
        # Add Plugins
        self.HomeWidget = None
        self.pluginD = {}
        self.prevPlugin=1
        curdir = os.path.abspath('.')
        for plug in self.settings['activePlugins']:
            if self.dev_mode:
                self.loadPlugin(plug)
                l_time = time.time()
            else:
                try:
                    self.loadPlugin(plug)
                except:
                    QtGui.QMessageBox.warning(self,'Plugin Load Failed','Could not load plugin: '+plug)
        self.ui.l_statusbar.setText('')
        os.chdir(curdir)
        self.ui.tabbar_bottom.setCurrentIndex(0)
        
        #--- Other Setup

        # Open file if in sys arg
        if len(sys.argv)>1:
            if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
                self.openFile(sys.argv[1])
        
        self.setFocus()
        
        # Add Start/Home
        QtGui.QApplication.processEvents()
        self.showHome()
        
        # Setup File Checking
        self.fileCheck_ignore = [] # List of file_ids to ignore checking
        if self.settings['checkFileChanges']:
            self.fileCheckTimer = QtCore.QTimer()
            self.fileCheckTimer.setInterval(1000*self.settings['checkFileChanges'])
            self.fileCheckTimer.timeout.connect(self.checkFileChanges2)
            self.fileCheckTimer.start()

    #---Events
    def closeEvent(self,event):
        cancelled = 0
        # Close all workspaces
        for wksp in self.workspaces.keys():
            ok = self.workspaceClose(wksp)
            if not ok:
                cancelled=1
                break

        if cancelled:
            event.ignore()
        else:
            # Save Settings
            self.saveSettings()
            
            # Other Events
            self.Events.close.emit()

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
    
    def resizeEvent(self,event):
        self.Events.resized.emit()
    
    #---Fullscreen Modes
    def toggleFullEditor(self,fullscreen=0):
        self.editor_fullmode = not self.editor_fullmode
        zen=self.editor_fullmode
        self.ui.l_statusbar.setVisible(not zen)

        self.ui.fr_left.setVisible(not zen)

        if fullscreen == 1 or self.fullscreen_mode:
            self.ui.sw_bottom.setVisible(not zen)
            self.ui.fr_bottom.setVisible(not zen)
            self.ui.fr_topbar.setVisible(not zen)
            self.ui.fr_leftbar.setVisible(not zen)
            
        if zen:
            self.pluginBottomChange(0)
        else:
            self.pluginBottomChange(self.ui.tabbar_bottom.currentIndex())
        
        if self.editor_fullmode:
            self.editorMenu.fullEditorAction.setText('Exit Full Editor Mode')
        else:
            self.editorMenu.fullEditorAction.setText('Full Editor Mode (F10)')
            
    def toggleFullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        if self.fullscreen_mode:
            self.showFullScreen()
            self.editor_fullmode=0
            self.toggleFullEditor(fullscreen=1)
            
            self.editorMenu.fullScreenAction.setText('Exit Full Screen Mode (F11)')
        else:
            self.editorMenu.fullScreenAction.setText('Full Screen (F11)')
            self.showNormal()
            if self.editor_fullmode:
                self.toggleFullEditor(fullscreen=1)
    
    def toggleAppScreen(self):
        if self.currentEditor().type == 'app':
            self.ui.fr_leftbar.setVisible(0)
    
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
            wdg = self.fileOpenD[file_id]
            if wdg.filename != None and os.path.abspath(wdg.filename).lower() == os.path.abspath(filename).lower():
                
                # Check if in current workspace and add tab if not
                wksp_tab = self.WindowSwitcher.tabs.currentWidget()
                if wksp_tab != None:
                    if not file_id in wksp_tab.tabD:
                        self.addWorkspaceEditor(file_id,wdg.title,wdg.filename,wdg.pluginEditor)
                
                # Change tab to the file
                self.changeTab(file_id)
                fileopen = file_id
                break
        return fileopen
    
    def getTitle(self,filename):
        title = os.path.basename(filename)
        if self.settings['window_switcher']['view_folder']:
            title = os.path.split(os.path.dirname(filename))[1]+'/'+title
        elif filename.endswith('.py') and title=='__init__.py':
            title = os.path.split(os.path.dirname(filename))[1]+'/init'
        return title
    
    def setTitle(self,widget):
        w = self.ui.fr_tab.width()
        self.ui.l_filename.setText(widget.title+widget.titleSuffix)
        
        # Show Full Path
        if self.settings['showPath']:
            if widget.type == 'file':

                w = w-70-self.ui.l_filename.fontMetrics().width(widget.title+widget.titleSuffix)
                title = self.ui.l_filename.fontMetrics().elidedText(os.path.split(widget.filename)[0]+'/',0,w)
                self.ui.l_title_prefix.setText(title)
            else:
                self.ui.l_title_prefix.setText('')
    
        # Set Tooltip
        if widget.filename != None:
            self.ui.fr_tab.setToolTip(widget.filename)
        elif widget.type == 'file_new':
            self.ui.fr_tab.setToolTip('New File (unsaved)')
        else:
            self.ui.fr_tab.setToolTip(widget.title)
    
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
        txt = None
        if file_id != None:
            if file_id in self.fileOpenD:
                self.changeTab(file_id)
                
                return 1
            else:
                filename = self.fileD[file_id]['filename']

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
                    return 1
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
                            wdg.tabTitle = self.getTitle(filename)

                            wdg.modTime = os.path.getmtime(filename)
                            wdg.setEnabled(1)
                            self.ui.l_statusbar.setText('')
                            
                            # Update tab text (needed for now after first creation)
                            wdg.titleSuffix=''
                            self.setTitle(wdg)
                            for t in self.fileD[wdg.id]['tabs']:
                                t.setTitle(wdg.tabTitle+wdg.titleSuffix)
                            
                            self.Events.fileOpened.emit(wdg)

        return txt != None

    #---Editor
    def addMainWidget(self,wdg,title,typ='file',**kargs):
        '''Add a widget to the main stackedwidget (where the editors go)'''
        
        # Setup Default Settings
        wdgD = {
            'filename':None,
            'icon':None,
            'lastText':'',
            'lang':None,
            'viewOnly':1,
            'editor':None,
            'pluginRightVisible':0,
            'typ':typ,
        }
        
        for ky in wdgD:
            if ky in kargs:
                wdgD[ky]=kargs[ky]
        
        # Create new widget parameters
        file_id = self.getFileId(wdgD['filename'])
        sw_ind = self.ui.sw_main.count()
        
        wdg.filename = wdgD['filename']
        wdg.lastText=''
        wdg.title = title
        wdg.tabTitle = title
        wdg.titleSuffix = ''
        wdg.id = file_id
        wdg.lang = wdgD['lang']
        wdg.viewOnly = wdgD['viewOnly']
        wdg.pluginEditor = wdgD['editor']
        wdg.pluginRightVisible=wdgD['pluginRightVisible']
        wdg.modTime = None
        wdg.icon = wdgD['icon']
        wdg.type = wdgD['typ']
        
        self.fileOpenD[file_id]=wdg
        
        self.ui.sw_main.insertWidget(sw_ind,wdg)
        self.changeTab(file_id)
        
        return file_id
    
    def addEditorWidget(self,lang=None,title='New',filename=None,editor=None,code=''):
        wdg = None
        typ = 'file'
        
        if filename == None and title=='New': 
            title = 'New '+lang
            typ = 'file_new'
        
        if not editor in self.Editors: # If editor not available - then find one
            editor = None
        
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
        
        kargs = {
            'lang':lang,
            'filename':filename,
        }
        
        # Load Editors
        if editor == 'webview':
            from plugins.webview import webview
            wdg = webview.WebView(self)
        else:
            wdg = self.Editors[editor].getWidget(**kargs)
        
        file_id=self.addMainWidget(wdg,title,filename=filename,viewOnly=0,lang=lang,typ=typ)
        wdg.pluginEditor = editor
        wdg.pluginRightVisible=0

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
        self.Events.editorAdded.emit(wdg)

        if 'editorTextChanged' in dir(wdg):
            wdg.Events.editorChanged.connect(self.editorTextChanged)
        if 'visibleLinesChanged' in dir(wdg) and self.settings['visibleLineTracking']:
            wdg.Events.visibleLinesChanged.connect(self.visibleLinesChanged)

        if self.ui.sw_main.count() ==1:
            self.change_tab(0)

        return wdg

    def currentEditor(self):
        return self.ui.sw_main.currentWidget()
    
    def getEditorWidget(self,file_id):
        if file_id in self.fileOpenD:
            return self.fileOpenD[file_id]
        else:
            return None
    
    def change_tab(self,sw_ind):
        wdg = self.currentEditor()
        if wdg != None:
            file_id = wdg.id
            if file_id != None:
                self.changeTab(file_id)
            else:
                ## MOVE TO changeTab
                self.ui.sw_main.setCurrentIndex(sw_ind)
                self.ui.b_closetab.hide()
                self.setTitle(wdg)
                try:
                    self.ui.b_tabicon.setIcon(wdg.icon)
                except:
                    self.ui.b_tabicon.setIcon(QtGui.QIcon())
                
        else:
            self.ui.b_closetab.hide()

    def changeTab(self,file_id):
        self.ui.l_statusbar.setText('')

        if file_id in self.fileOpenD:
            wdg = self.fileOpenD[file_id]
            self.ui.sw_main.setCurrentWidget(wdg)
            self.Events.editorTabChanged.emit(wdg)
            self.setTitle(wdg)
            if wdg.filename != None:
                self.ui.fr_tab.setToolTip(wdg.filename)
            elif wdg.type == 'file_new':
                self.ui.fr_tab.setToolTip('New File (unsaved)')
            else:
                self.ui.fr_tab.setToolTip(wdg.title)
            try:
                self.ui.b_tabicon.setIcon(wdg.icon)
            except:
                pass
            # Show/Hide plugins
            lang = wdg.lang
            
            self.ui.b_closetab.show()
            self.ui.fr_toolbar.show()
            self.ui.fr_topleft.show()
            self.ui.b_back.hide()
        else:
            wdg = None
            lang = None
            
            self.ui.b_closetab.hide()
            self.ui.l_filename.setText('')

        # Enable Run
        run_enabled=0
        if lang in self.settings['run']:
            run_enabled = lang in self.settings['run']
            
        self.ui.b_run.setEnabled(run_enabled)

        # Disable buttons based on function availability
        btnD = [
            ['indent',self.ui.b_indent],
            ['unindent',self.ui.b_unindent],
            ['find',self.ui.fr_find],
            ['toggleComment',self.ui.b_comment],
            ['getText',self.ui.b_save],
            ['toggleWordWrap',self.editorMenu.wordwrapAction],
            ['toggleWhitespace',self.editorMenu.whitespaceAction],
            ['getText',self.editorMenu.statsAction],
        ]
        for btn in btnD:
            btn[1].setEnabled(btn[0] in dir(wdg))
        
        try:
            self.editorMenu.menuSaveAction.setEnabled('getText' in dir(wdg))
            self.editorMenu.menuSaveAsAction.setEnabled('getText' in dir(wdg))
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
        
            if wdg.viewOnly:
                self.ui.fr_toolbar.hide()
                self.ui.fr_topleft.hide()
                self.ui.b_closetab.hide()
                # Back if current tab
                if self.last_editable_file != None and self.last_editable_file in self.fileOpenD:
                    self.ui.b_back.show()
                
                # Show Full Mode
##                self.editor_fullmode=0
##                self.toggleFullEditor()
                    
            elif wdg.filename != None:
                self.last_editable_file = wdg.id
        
    def close_tab(self):
        if self.currentEditor() != None:
            if len(self.recentTabs) > 1:
                prevtab = self.recentTabs[-2]
            
            file_id = self.currentEditor().id
            self.closeTab(file_id)
            
            if len(self.recentTabs) > 1:
                self.changeTab(prevtab)
    
    def closeTab(self,file_id,remove_from_workspace=1):
        ok = 1
        if file_id >-1 and file_id in self.fileOpenD:
            wdg = self.fileOpenD[file_id]
            filename = wdg.filename
            
            # Check Save
            if 'getText' in dir(wdg):
                ok = self.checkSave(wdg)
                    
            if ok:
                # Emit close signal
                self.Events.editorTabClosed.emit(wdg)
                
                self.fileOpenD.pop(file_id)

                # Remove Widget
                self.ui.sw_main.removeWidget(wdg)
                
                if file_id in self.recentTabs:
                    self.recentTabs.remove(file_id)
                
                wdg.deleteLater()
                del wdg
        
        # Remove from workspace tabs
        if ok and remove_from_workspace:
            for t in self.fileD[file_id]['tabs']:
                t.close(ignoreCheck=1)
                self.fileD[file_id]['tabs'].remove(t)
        
        return ok

    def editorTextChanged(self):
        # Indicate if text changed
        wdg = self.currentEditor()
        try:
            if wdg.lastText != wdg.getText():
                wdg.titleSuffix = '*'
            else:
                wdg.titleSuffix = ''
            self.setTitle(wdg)
        except:
            self.ui.l_statusbar.setText('Error: text changed signal')
        
        # Update tab display title
        if wdg.id != None:
            for t in self.fileD[wdg.id]['tabs']:
                try:
                    t.setTitle(wdg.tabTitle+wdg.titleSuffix)
                except:
                    print('error setting title',wdg.tabTitle+wdg.titleSuffix)
    
        # Check for file changes
##        self.checkFileChanges()
    
    def visibleLinesChanged(self,wdg,lines):
        self.Events.editorVisibleLinesChanged.emit(wdg,lines)

    def checkSave(self,wdg):
        ok = 0
        if wdg.viewOnly:
            ok = 1
        else:
            if 'getText' in dir(wdg):
                try:
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

    def back_to_editor(self):
        if self.last_editable_file != None and self.last_editable_file in self.fileOpenD:
            self.changeTab(self.last_editable_file)
        else:
            self.toggleWindowSwitcher()

    #---Editor Tools
    def editorSave(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        
        if wdg != None:
            
            if wdg.type == 'app':
                # Check if app has save
                if 'appSave' in dir(wdg):
                    wdg.appSave()
            else:
                # File Save
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
                        wdg.tabTitle = self.getTitle(wdg.filename)
                        self.ui.l_filename.setToolTip(wdg.filename)
                        wdg.type = 'file'

                if filename != None:
                    self.Events.editorBeforeSave.emit(wdg)
                    try:
                        txt = wdg.getText()
                        if self.saveEnabled:
                            f = codecs.open(wdg.filename,'w','utf8')
                            f.write(txt)
                            f.close()
                        wdg.lastText = txt
                        wdg.modTime = os.path.getmtime(filename)
                        self.ui.l_statusbar.setText('Saved: '+wdg.title)#+' at '+datetime.datetime.now().ctime(),3000)
                        wdg.titleSuffix = ''
                        self.setTitle(wdg)
                        
                        # Save Signal
                        self.Events.editorSaved.emit(wdg)
                        
                    except:
                        QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it.  You may want to copy the text, paste it in another editor to not lose your work.<br><br><b>Error:</b><br>'+str(sys.exc_info()[1]))
                        self.ui.l_statusbar.setText('Error Saving: '+filename)

##                    # If Settings File, reload
##                    if filename == self.settings_filename:
##                        self.loadSettings()
                
                # Update tabs
                for t in self.fileD[wdg.id]['tabs']:
                    t.setTitle(wdg.tabTitle+wdg.titleSuffix)
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
            
            wdg.filename = os.path.abspath(str(filename))
            wdg.title = os.path.basename(wdg.filename)
            self.ui.l_filename.setText(wdg.title)
            wdg.tabTitle = wdg.title
            self.editorSave()
                
    def editorFind(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        if 'find' in dir(wdg):
            txt = self.ui.le_find.text()
            wdg.find(txt)

    def editorRun(self,wdg=None):
        if wdg == None or isinstance(wdg,bool):
            wdg = self.ui.sw_main.currentWidget()
        if wdg.lang in self.settings['run']:
            if self.settings['run'][wdg.lang]['cmd'].startswith('preview'):
                if 'preview' in self.pluginD:
                    self.pluginD['preview'].widget.previewRun(wdg)
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
                        self.pluginD['output'].widget.runProcess(runD['cmd'],wdg)

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
            lines = len(txt.splitlines())
            words = len(txt.split())
            if 'getCursorPosition' in dir(wdg):
                row,col = wdg.getCursorPosition()
                self.ui.l_statusbar.setText('Row: %d    Column: %d    Lines: %d    Words: %d    ' %(row+1,col,lines,words))
            else:
                self.ui.l_statusbar.setText('Lines: %d    Words: %d    ' %(lines,words))
    
    def colorPicker(self):
        dclr = [255,255,255,255]
        dclr = [255,255,255,255]
        # Check for selected text
        if 'getSelectedText' in dir(self.currentEditor()):
            txt=self.currentEditor().getSelectedText()
            # Check for rgb color
            sel_clrs = txt.split(',')
            if len(sel_clrs) >2:
                try:
                    sclr=[]
                    for c in sel_clrs:
                        sclr.append(int(str(c)))
                    if len(sel_clrs) == 3: sclr.append(255)
                    dclr = sclr
                except:
                    print('invalid color',sel_clrs)
        
        clrdlg = QtGui.QColorDialog(self)
        clr=clrdlg.getColor(QtGui.QColor(dclr[0],dclr[1],dclr[2],dclr[3]),self,'Select color',QtGui.QColorDialog.ShowAlphaChannel)
        if clr.isValid():
            r,g,b,a = clr.getRgb()
            atxt=apfx=''
            if a < 255:
                atxt=',%0.2g' %(a/255.0)
            txt = '%d,%d,%d%s' %(r,g,b,atxt)
            if 'insertText' in dir(self.currentEditor()):
                self.currentEditor().insertText(txt)
            self.currentEditor().setFocus()

    #---Left Toolbar
    def showNewMenu(self):
        # Show menu to the right of the toolbar
        s = self.ui.b_new.size()
        bpos = self.ui.b_new.mapToGlobal(QtCore.QPoint(s.width(),0))
        self.newMenu.exec_(bpos)

    def showWorkspaceMenu(self):
        # Show menu to the right of the toolbar
        s = self.ui.b_workspaces.size()
        bpos = self.ui.b_workspaces.mapToGlobal(QtCore.QPoint(s.width(),0))
        self.workspaceMenu.exec_(bpos)

    def addLeftBarButton(self,icon,tooltip='',click_function=None):
        '''Add a button on the left toolbar'''
        btn = QtGui.QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QtCore.QSize(32,32))
        btn.setToolTip(tooltip)
        layout = self.ui.fr_leftbar.layout()
        layout.insertWidget(layout.count()-1,btn)
        
        if click_function != None:
            btn.clicked.connect(click_function)
        
        return btn

    #---Plugins
    def loadPlugin(self,plug):
        curdir = os.path.abspath('.')

        if not os.path.exists(self.pluginPath+plug):
            QtGui.QMessageBox.warning(self,'Plugin Load Failure','The plugin <b>'+plug+'</b> was not found')
        else:
            
            pmod = importlib.import_module('plugins.'+plug+'.scope_plugin')
            Plugin = pmod.Plugin(self)
            
            os.chdir(self.pluginPath+plug)
        
            if 'load' in dir(Plugin):
                Plugin.load()
        
            title = Plugin.title
            loc = Plugin.location
            icn = QtGui.QIcon()
            if os.path.exists(self.pluginPath+plug+'/icon.png'):
                icn = QtGui.QIcon(self.pluginPath+plug+'/icon.png')

            # Check settings for location
            if plug in self.settings['plugins'] and 'location' in self.settings['plugins'][plug]:
                loc = self.settings['plugins'][plug]['location']
            
            if loc in ['left','right','bottom'] and Plugin.widget == None:
                pluginWidget = Plugin.loadWidget()
                
            tabtext = title
            
            if loc == 'left':
                if not self.settings['pluginLeft']['showTabText']: tabtext=''
                ti = self.ui.tab_left.addTab(pluginWidget,icn,tabtext)
                self.ui.tab_left.setTabToolTip(ti,title)
            elif loc=='right':
                if not self.settings['pluginRight']['showTabText']: tabtext=''
                ti = self.ui.tab_right.addTab(pluginWidget,icn,tabtext)
                self.ui.tab_right.setTabToolTip(ti,title)
            elif loc == 'bottom':
                if not self.settings['pluginBottom']['showTabText']: tabtext=''
                self.ui.sw_bottom.addWidget(pluginWidget)
                ti=self.ui.tabbar_bottom.addTab(icn,tabtext)
                self.ui.tabbar_bottom.setTabToolTip(ti,title)

            self.pluginD[plug]=Plugin
            os.chdir(curdir)

    def installPlugin(self,plugin_name,plugin_pkg):
        plug_path = os.path.join(self.pluginPath,plugin_name)
        if not os.path.exists(plug_path):
            os.mkdir(plug_path)
        import zipfile
        
        if plugin_pkg.startswith('http'):
            import requests, StringIO
            r = requests.get(plugin_pkg)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
        else:
            z = zipfile.ZipFile(plugin_pkg,'r')
        
        # Ignore root directory in zip
        root = z.namelist()[0].split('/')[0]+'/'
        for zfile in z.namelist():
            npth = str(zfile).replace(root,'')
            if npth != '':
##                print npth,'   ',os.path.join(plug_path,npth)
                if npth.endswith('/'):
                    if not os.path.exists(os.path.join(plug_path,npth)):
                        os.mkdir(os.path.join(plug_path,npth))
                else:
                    data = z.read(zfile)
                    myfile = open(os.path.join(plug_path,npth), "wb")
                    myfile.write(data)
                    myfile.close()
            
        z.close()

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
        
        if 'leftToggle' in self.settings['pluginRight']:
            if self.settings['pluginRight']['leftToggle']:
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
            wdg.pic = QtGui.QPixmap(self.iconPath+'page_preview.png')
            wdg.icon = QtGui.QIcon(wdg.pic)
            self.ui.b_tabicon.setIcon(wdg.icon)
    
        else:
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
    
    def showHome(self):
        if self.HomeWidget != None:
            self.HomeWidget.toggleHome()
    
    def toggleWindowSwitcher(self):
        self.WindowSwitcher.toggle()
    
    def createWindowSwitcher(self):
        import window_switcher
        self.WindowSwitcher = window_switcher.WindowSwitcher(parent=self)
    
    #---Shortcuts
    def findFocus(self):
        if self.ui.fr_topbar.isHidden():
            self.ui.fr_topbar.setVisible(1)
        self.ui.le_find.setFocus()
        self.ui.le_find.selectAll()
        
    def gotoFocus(self):
        if self.ui.fr_topbar.isHidden():
            self.ui.fr_topbar.setVisible(1)
        self.ui.le_goto.setFocus()
        self.ui.le_goto.selectAll()
        
    def nextTab(self):
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
                # Save workspace files
                if wksp in self.workspaces:
                    li_wdg = self.workspaces[wksp]['widget']
                    for i in range(li_wdg.count()):
                        itm = li_wdg.itemWidget(li_wdg.item(i))
                        file_id = itm.id
                        
                        if file_id in self.fileOpenD:
                            wdg = self.fileOpenD[file_id]
                            editor = wdg.pluginEditor
                        else:
                            editor = itm.pluginEditor
                        if itm.filename != None:
                            wD['files'].append({'filename':itm.filename,'editor':editor})

                    if self.currentEditor() != None and not self.currentEditor().viewOnly:
                        wD['lastOpenFile']=self.currentEditor().filename
                
                    # Save workspace dir
                    wD['basefolder']=self.workspaces[wksp]['basefolder']
                f = open(self.settingPath+'/workspaces/'+wksp,'w')
                f.write(json.dumps(wD))
                f.close()
    
    def workspaceOpen(self,wksp,show_tabs=1):
        # Load workspace
        if wksp in self.workspaces: # and wksp != None:
            self.Events.workspaceChanged.emit(wksp)
            self.WindowSwitcher.show()
            self.WindowSwitcher.tabs.setCurrentWidget(self.workspaces[wksp]['widget'])
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

            # Add workspace to window switcher
            wD['widget'] = self.WindowSwitcher.addWorkspace(wksp)
            wD['type'] = wtype
            
            # Load Files
            last_file = None
            for f in wD['files']:
                if f not in [None,'None','']:
                    if type(f) == type({}):
                        fid = self.getFileId(f['filename'])
                        self.addWorkspaceEditor(fid,self.getTitle(f['filename']),f['filename'],f['editor'])
                        last_file =f['filename']

            # Goto lastopen file
            if 'lastOpenFile' in wD:
                last_file = wD['lastOpenFile']

            if last_file != None:
                self.openFile(last_file)
            
            # Current Directory
            self.currentPath = wD['basefolder']
            
            self.workspaceMenu.saveWact.setDisabled(0)
            self.workspaceMenu.renameWact.setDisabled(0)
            self.workspaceMenu.closeWact.setDisabled(0)
            
            if show_tabs:
                self.toggleWindowSwitcher()

            self.Events.workspaceOpened.emit(wksp)
    
    def addWorkspaceEditor(self,file_id,title,filename,editor=''):
        if self.currentWorkspace == None:
            self.workspaceOpen(None,show_tabs=0)
        tab = self.WindowSwitcher.tabs.currentWidget().addEditortab(file_id,title,filename,editor)
        if not tab in self.fileD[file_id]['tabs']:
            self.fileD[file_id]['tabs'].append(tab)
    
    def workspaceNew(self):
        # New Workspace
        resp,ok = QtGui.QInputDialog.getText(self,'New Workspace','<b>Enter Workspace Name</b><br><font style="color:#bbb">(leave blank for a temporary workspace)</font>')
        if ok:
            if resp.isEmpty():
                self.workspaceOpen(None,show_tabs=1)
            else:
                self.workspaceSave(str(resp))
                self.workspaceOpen(str(resp))
                
                self.workspaceMenu.loadMenu()
    
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
                        self.workspaceClose(owskp)
                    npth = self.settingPath+'/workspaces/'+str(resp)
                    os.rename(pth,npth)
                    self.workspaceMenu.loadMenu()
                    self.workspaceOpen(str(resp))
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
                    if len(self.fileD[fid]['tabs']) < 2:
                        fl_ok = self.closeTab(fid,remove_from_workspace=0)
                        if not fl_ok:
                            break
                
        # Close open files
        if wk_ok:
            pass
            # Check if anything needs saving and if not in other workspace
        
        ok=fl_ok*wk_ok
        
        if ok:
            self.Events.workspaceClosed.emit(wksp)
            self.workspaces.pop(str(wksp))
            if len(self.workspaces) == 0:
                self.workspaceMenu.saveWact.setDisabled(1)
                self.workspaceMenu.closeWact.setDisabled(1)
            
        return ok

    #---Settings
    def loadSettings(self):
        # Create settings directory
        if not os.path.exists(self.settingPath):
            os.mkdir(self.settingPath)
        
        if not os.path.exists(self.settingPath+'/scope.json'):
            import shutil
            shutil.copyfile(os.path.abspath(os.path.dirname(__file__))+'/default_settings.json',self.settingPath+'/scope.json')
        
##        from site_pkg.configobj import configobj
        self.settings_filename = self.settingPath+'/scope.json'
        dflt_path = os.path.abspath(os.path.abspath(os.path.dirname(__file__))+'/default_settings.json')
        
        # Default Settings
        with open(dflt_path,'r') as setf:
            config = json.load(setf)
        
        mysettings={}
        try:
            with open(self.settings_filename,'r') as setf:
                mysettings = json.load(setf)
        except:
            err = str(sys.exc_info()[1])
            QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<br><br>Using default settings<br><br><i>Compare your settings with the scope/default_settings.json</i><br><br><b>Error:</b>'+err)
        
        self.settings = config.copy()
        self.settings.update(mysettings)
        
##        try:
##            user_config = configobj.ConfigObj(self.settings_filename,unrepr=True,_inspec=True,list_values=False)
##            if type(user_config['editors'])==type([]): # Check editor settings 
##                error
##            config.merge(user_config)
##        except:
##            QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<br><br>Using default settings<br><br><i>Compare your settings with the default_settings</i>')
##            user_config = None
        
##        print dflt_path
##        config = configobj.ConfigObj(dflt_path,unrepr=True,_inspec=True,list_values=False)
##        try:
##            user_config = configobj.ConfigObj(self.settings_filename,unrepr=True,_inspec=True,list_values=False)
##            if type(user_config['editors'])==type([]): # Check editor settings 
##                error
##            config.merge(user_config)
##        except:
##            QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<br><br>Using default settings<br><br><i>Compare your settings with the default_settings</i>')
##            user_config = None
##        self.settings = config

        # Setup Webview stylesheet
        wsettings = QtWebKit.QWebSettings.globalSettings()
        wsettings.setUserStyleSheetUrl(QtCore.QUrl('file://'+self.scopePath+'/style/webview.css'))

        # Configure Settings
        self.settings['run']={}
        for l in self.settings['prog_lang']:
            ok = 1
            #~ self.settings['run_preview'][l]=0
            # Remove default languages if not in user config
            
            if 'prog_lang' in self.settings:
                if l not in self.settings['prog_lang']:
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
        
        self.settings['checkFileChanges'] = int(self.settings['checkFileChanges'])
        
        self.Events.settingsLoaded.emit()
    
    def openSettings(self):
        self.pluginD['settings'].addSettingsWidget()
##        menu = QtGui.QMenu(self.ui.b_settings)
##        menu.addAction('Edit Settings')
####        menu.addAction('Plugins')
##        s = self.ui.b_settings.size()
##        bpos = self.ui.b_settings.mapToGlobal(QtCore.QPoint(s.width(),0))
##        act = menu.exec_(bpos)
##        if act != None:
##            acttxt = str(act.text())
##            if acttxt == 'Edit Settings':
##                self.openFile(self.settings_filename)

    def saveSettings(self):
        if self.fullscreen_mode:
            self.toggleFullscreen()
            QtGui.QApplication.processEvents()
        
        # Save Workspace
        if self.currentWorkspace != None and self.settings['save_workspace_on_close']:
            self.workspaceSave()

    #---FileModify Checker
    def checkFileChanges2(self):
        self.checkFileChanges(nothing_message=0)
        #
    def checkFileChanges(self,nothing_message=1):
            chngs = 0
            close_tabs = []
            for file_id in self.fileOpenD:
                wdg = self.fileOpenD[file_id]
                if wdg.filename != None and wdg.modTime != None:
                    if not os.path.exists(wdg.filename) and file_id not in self.fileCheck_ignore:
                        resp = QtGui.QMessageBox.warning(self,'File Does not exist',str(wdg.filename)+' does not exist anymore.<br><<br>Do you want to keep the file open?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
                        if resp == QtGui.QMessageBox.No:
                            close_tabs.append(file_id)
                        else:
                            self.fileCheck_ignore.append(file_id)
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
            if not chngs and nothing_message:
                QtGui.QMessageBox.warning(self,'No Changes','No external changes to current open files were found')

    #---Other Functions
    def openFileExternal(self,path=None,program=None):
        '''Open the path external to Scope with the OS default'''

        if path == None:
            wdg = self.currentEditor()
            if wdg != None:
                path = wdg.filename
        
        if path != None:
            if os.name=='nt':path = path.replace('/','\\')
            dpth = os.path.dirname(path)
            if os.path.isdir(path) and program != None:
                # Use specified file browser
                subprocess.Popen([program,path],cwd=dpth)
            else:
                # use default filebrowser
                curdir = os.path.abspath('.')
                os.chdir(os.path.dirname(path))
                if os.name == 'nt':
    ##                        subprocess.Popen(path,shell=True,cwd=dpth)
                    os.startfile(path)
                elif os.name=='posix':
                    subprocess.Popen(['xdg-open', path],cwd=dpth)
                elif os.name=='mac':
                    subprocess.Popen(['open', path],cwd=dpth)
                os.chdir(curdir)

def runui(dev_mode=0):
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app = QtGui.QApplication(sys.argv)

    scopeApp = Scope(dev_mode=dev_mode)
    os.chdir('../')
    scopeApp.load()
    scopeApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    sys.path.append(os.path.abspath('../'))
    runui(dev_mode=1)