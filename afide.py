# --------------------------------------------------------------------------------
# afide | Another IDE
# Copyright 2013 Cole Hagen
#
# afide is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

import sys, subprocess, json, new
from PyQt4 import QtCore, QtGui, QtWebKit
from afide_ui import Ui_MainWindow
import os,shutil,datetime, webbrowser, yaml, subprocess

class Events(QtCore.QObject):
    editorAdded = QtCore.pyqtSignal(QtGui.QWidget)
    editorTabChanged = QtCore.pyqtSignal(QtGui.QWidget)

class NewMenu(QtGui.QMenu):
    def __init__(self,parent):
        QtGui.QMenu.__init__(self,parent)
        self.parent = parent
        for lang in sorted(parent.settings['lang']):
            self.addAction(lang)
    
        self.triggered.connect(self.newEditor)
    
    def newEditor(self,event):
        ##print event.text()

        self.parent.addEditorWidget(str(event.text()))

class Afide(QtGui.QMainWindow):
    def __init__(self, parent=None):

        # Version
        self.version = '0.2.0'

        # Setup UI
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Style
        QtGui.QApplication.setStyle("Plastique")
        f = open('styles/default.css','r')
        style = f.read()
        f.close()
        self.setStyleSheet(style)
        
        # Settings
        self.loadSettings()
        
        # Screen Size
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        coords= QtGui.QApplication.desktop().screenGeometry(screen).getCoords() 
        dx = 50
        self.setGeometry(coords[0]+dx,coords[1]+dx,(coords[2]-coords[0]-2*dx),(coords[3]-coords[1]-2*dx))
        
        # Toolbutton Toolbar
        self.ui.toolbar = QtGui.QToolBar("toolBar",self)
        self.ui.toolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.toolbar.setFloatable(False)
        self.ui.toolbar.setMovable(True)
        self.ui.toolbar.setProperty("class","toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.toolbar)
        self.ui.toolbar.addWidget(self.ui.fr_toolbar)
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        
        #--- Setup Tab Toolbar
        self.ui.tabtoolbar = QtGui.QToolBar("editorTabBar",self)
        self.ui.tabtoolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.tabtoolbar.setFloatable(False)
        self.ui.tabtoolbar.setMovable(True)
        self.ui.tabtoolbar.setProperty("class","editorTabBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.tabtoolbar)
##        self.ui.tabtoolbar.addWidget(self.ui.fr_toolbar)
        self.ui.tab = QtGui.QTabBar()
        self.ui.tab.setObjectName('editorTabs')
        self.ui.tab.setTabsClosable(True)
        self.ui.tab.setMovable(True)
        self.ui.tab.setProperty("class","editorTabs")
        self.ui.tabtoolbar.addWidget(self.ui.tab)
        self.ui.tab.currentChanged.connect(self.changeTab)
        self.ui.tab.tabCloseRequested.connect(self.closeTab)
        
        self.setAcceptDrops(1)
        
        newmenu = NewMenu(self)
        self.ui.b_new.setMenu(newmenu)
        
        # Signals
        self.ui.b_open.clicked.connect(self.openFile)
        self.ui.b_save.clicked.connect(self.editorSave)

        self.ui.b_indent.clicked.connect(self.editorIndent)
        self.ui.b_unindent.clicked.connect(self.editorUnindent)
        self.ui.b_comment.clicked.connect(self.editorToggleComment)
        
        self.ui.b_run.clicked.connect(self.editorRun)
        self.ui.b_wordwrap.clicked.connect(self.editorWordWrap)
        self.ui.b_settings.clicked.connect(self.openSettings)
        self.ui.b_find.clicked.connect(self.editorFind)
        
        # Editor Signals
        self.evnt = Events()
        self.tabD={}
        
        # Plugins
        self.pluginDocks = []
        self.setCorner(QtCore.Qt.BottomLeftCorner,QtCore.Qt.LeftDockWidgetArea)
        
        # File Dictionary
        self.fileCount = 0
        
        #--- Add Plugins
        dockareaD = {'left':QtCore.Qt.LeftDockWidgetArea,
            'right':QtCore.Qt.RightDockWidgetArea,
            'top':QtCore.Qt.TopDockWidgetArea,
            'bottom':QtCore.Qt.BottomDockWidgetArea
        }
        self.pluginD = {}
        
        curdir = os.path.abspath('.')
        
        for plug in self.settings['plugins']:
            exec('from plugins.'+plug+' import '+plug)
            os.chdir(curdir+'/plugins/'+plug)
            exec('dwdg = '+plug+'.addDock(self)')
            exec("dplug = self.addPlugin(dwdg,dockareaD[self.settings['plugins']['"+plug+"']['dockarea']],self.settings['plugins']['"+plug+"']['title'])")
            exec('dplug.hide()')
            exec("self.pluginD['"+plug+"'] = dplug")

        os.chdir(curdir)

        #--- Add Welcome
        wdg = self.addEditorWidget('WebView','Welcome')
        f = open('doc/start.html','r')
        txt = f.read()
        f.close()
        wdg.setText(txt)
        self.changeTab(self.ui.tab.currentIndex())

    def dropEvent(self,event):
        handled=False
        if event.mimeData().urls():
            for f in event.mimeData().urls():
                self.openFile(str(f.toLocalFile()))
            handled=True

        if not handled:
            QtGui.QWMainWindow.dropEvent(self,event)

    def dragEvent(self,event):
        event.accept()
    
    def dragEnterEvent(self,event):
        event.accept()
    
    def openFile(self,filename=None):
        if not filename:
            # Ask for filename if not specified
            filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",""," (*.*)")
            if filename=='':
                filename = None
            else:
                filename = str(filename)
        if filename != None:
            lang = None
            ext = os.path.splitext(str(filename))[1][1:]
            if ext in self.settings['ext']:
                lang = self.settings['ext'][ext]
                
            wdg = self.addEditorWidget(lang,os.path.basename(filename),str(filename))
            f=open(filename,'r')
            txt = f.read()
            f.close()
            wdg.setText(txt)
            wdg.lastText = txt
            self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)

#---Editor
    def currentWidget(self):
        return self.ui.sw_main.currentWidget()

    def changeTab(self,tab_ind):
        self.ui.statusbar.showMessage('')
        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
        if file_id in self.tabD:
            wdg = self.tabD[file_id]
            self.ui.sw_main.setCurrentWidget(wdg)
            self.evnt.editorTabChanged.emit(wdg)
            
            # Show/Hide plugins
            lang = wdg.lang
            if lang in self.settings['lang']:
                for plug in self.pluginD:
                    if plug in self.settings['lang'][lang]['plugins']:
                        self.pluginD[plug].show()
                    else:
                        self.pluginD[plug].hide()
                    
                self.ui.b_run.setEnabled('run' in self.settings['lang'][lang])
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

    def editorTextChanged(self):
        # Indicate if text changed
        wdg = self.currentWidget()
        self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title+'*')
        
    def addEditorWidget(self,lang=None,title='New',filename=None):
        self.fileCount+=1
        sw_ind = self.ui.sw_main.count()
        wdg = None
        
        if filename == None and title=='New': title = 'New '+lang
        
        if lang in self.settings['lang']:
            editor = self.settings['lang'][lang]['editor']
        else:
            editor = self.settings['lang']['Text']['editor']
        exec("from editors."+editor+" import "+editor)
        exec("wdg = "+editor+".addEditor(self,lang)")

        wdg.filename = filename
        wdg.lastText=''
        wdg.title = title
        wdg.id = self.fileCount
        wdg.lang = lang
        self.evnt.editorAdded.emit(wdg)
        self.tabD[self.fileCount]=wdg

        if 'editorTextChanged' in dir(wdg):
            wdg.evnt.editorChanged.connect(self.editorTextChanged)

        # Insert widget to page
        self.ui.sw_main.insertWidget(sw_ind,wdg)
        self.ui.sw_main.setCurrentIndex(sw_ind)
        
        # Insert Tab on top
        self.ui.tab.insertTab(sw_ind+1,title)
        self.ui.tab.setTabData(sw_ind,self.fileCount)
        self.ui.tab.setCurrentIndex(sw_ind)
        self.ui.tab.setTabToolTip(sw_ind,str(filename))
        
        return wdg

    def checkSave(self,wdg):
        ok = 0
        if wdg.lastText != wdg.getText():
            resp = QtGui.QMessageBox.warning(self,'Save Tab',"Do you want to save the file?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
            if resp == QtGui.QMessageBox.Yes:
                self.editorSave()
                ok =1
            elif resp == QtGui.QMessageBox.No:
                ok =1
        else:
            ok =1 
        return ok

    def editorSave(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        txt = unicode(wdg.getText())
        if wdg.filename != None:
            filename = wdg.filename
        else:
            filename = QtGui.QFileDialog.getSaveFileName(self,"Save Code",""," (*.*)")
            if filename=='':
                filename=None
            else:
                wdg.filename = os.path.abspath(str(filename))
                wdg.title = os.path.basename(wdg.filename)
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
        if filename != None:
            try:
                f = open(wdg.filename,'w')
                f.write(txt)
                f.close()
                wdg.lastText = txt
                self.ui.statusbar.showMessage('Saved '+filename+' at '+datetime.datetime.now().ctime())
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
            except:
                QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it')
                self.ui.statusbar.showMessage('Error Saving: '+filename)
            
            # If Settings File, reload
            if filename == self.settings_filename:
                self.loadSettings()
                
    def editorFind(self):
        wdg = self.ui.sw_main.widget(self.ui.sw_main.currentIndex())
        if 'find' in dir(wdg):
            txt = self.ui.le_find.text()
            wdg.find(txt)

    def editorRun(self):
        wdg = self.ui.sw_main.currentWidget()
        ok = self.checkSave(wdg)
        filename = str(wdg.filename)
        if ok:
            if wdg.lang in self.settings['lang'] and 'run' in self.settings['lang'][wdg.lang]:
                exec(self.settings['lang'][wdg.lang]['run'].replace('$file',filename))

    def editorToggleComment(self):
        wdg = self.ui.sw_main.currentWidget()
        wdg.toggleComment()

    def editorIndent(self):
        wdg = self.ui.sw_main.currentWidget()
        wdg.indent()

    def editorUnindent(self):
        wdg = self.ui.sw_main.currentWidget()
        wdg.unindent()

    def editorWordWrap(self):
        wdg = self.ui.sw_main.currentWidget()
        wdg.toggleWordWrap()

#---Plugins
    def addPlugin(self,wdg,dockarea,title):
        
        dock = QtGui.QDockWidget()
        
        dock.dockWidgetContents = QtGui.QWidget()
        dock.setWidget(dock.dockWidgetContents)
        dock.setWindowTitle(title)
        dock.gridLayout = QtGui.QGridLayout(dock.dockWidgetContents)
        dock.gridLayout.setMargin(0)
        dock.gridLayout.setSpacing(0)
        dock.gridLayout.addWidget(wdg, 0, 0, 1, 1)
        
        self.addDockWidget(dockarea,dock)
        self.pluginDocks.append(dock)
        
        # Tabify Dock with other widgets in its area
        for idock in self.pluginDocks[:-1]:
            if self.dockWidgetArea(idock) == dockarea:
                self.tabifyDockWidget(idock,dock)
        
        return dock

#---Settings
    def loadSettings(self):
        self.settings_filename = os.path.abspath(os.path.dirname(__file__))+'/settings.yaml'
        f = open(self.settings_filename,'r')
        settingstxt = f.read()
        f.close()
        self.settings = yaml.load(settingstxt)
        
    def openSettings(self):
        self.openFile(self.settings_filename)

def runui():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    app = QtGui.QApplication(sys.argv)
    afideApp = Afide()
    afideApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()