# --------------------------------------------------------------------------------
# afide | Another Fantastic IDE
# Copyright 2013 Cole Hagen
#
# afide is licensed under the GNU General Public License (GPL 3)
# --------------------------------------------------------------------------------

import sys, subprocess, json, codecs
from PyQt4 import QtCore, QtGui, QtWebKit
from afide_ui import Ui_MainWindow
import os,shutil,datetime, webbrowser, yaml, subprocess
import plugins.output.output

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
        
        self.iconPath=os.path.abspath(os.path.dirname(__file__))+'/img/'
        
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
        self.ui.toolbar.setObjectName('toolBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.toolbar)
        self.ui.toolbar.addWidget(self.ui.fr_toolbar)
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        
        #--- Setup Tab Toolbar
        self.ui.tabtoolbar = QtGui.QToolBar("editorTabBar",self)
        self.ui.tabtoolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.ui.tabtoolbar.setFloatable(False)
        self.ui.tabtoolbar.setMovable(True)
        self.ui.tabtoolbar.setProperty("class","editorTabBar")
        self.ui.tabtoolbar.setObjectName('editorTabBar')
        self.addToolBar(QtCore.Qt.TopToolBarArea,self.ui.tabtoolbar)
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
        self.ui.b_zen.clicked.connect(self.toggleZen)
        
        self.ui.b_find.clicked.connect(self.editorFind)
        self.ui.le_goto.returnPressed.connect(self.editorGoto)
        
        # Editor Signals
        self.evnt = Events()
        self.tabD={}
        
        # Plugins
        self.pluginDocks = []
        self.setCorner(QtCore.Qt.BottomLeftCorner,QtCore.Qt.LeftDockWidgetArea)
        
        # File Dictionary
        self.fileCount = -1
        
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
            title = self.settings['plugins'][plug]['title']
            if plug == 'pycute': title += ' ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')'
            exec("dplug = self.addPlugin(dwdg,dockareaD[self.settings['plugins']['"+plug+"']['dockarea']],title)")
##            exec('dplug.hide()')
            exec("self.pluginD['"+plug+"'] = dplug")

        os.chdir(curdir)
        
        self.dockstate = self.saveState()
        self.zen = 1

        #--- Add Start
        wdg = self.addEditorWidget('WebView','Start')
        f = open('doc/start.html','r')
        txt = f.read()
        f.close()
        if os.name =='nt':
            pfx="file:///"
        else:
            pfx="file://"
        burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/doc/')
        wdg.setText(txt,burl)
        wdg.viewOnly = 1
        QtGui.QApplication.processEvents()
        self.changeTab(self.ui.tab.currentIndex())

    def closeEvent(self,event):
        # Check if anything needs saving
        for i in range(self.ui.tab.count()):
            file_id = self.ui.tab.tabData(i).toInt()[0]
            wdg = self.tabD[file_id]
            self.checkSave(wdg)

##        QtGui.QMessageBox.warning(self,'check save','check to save'+str(self.ui.tab.count()))

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
    
    def keyPressEvent(self,event):
        handled = 0
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_F:
                self.ui.le_find.setFocus()
                handled = 1
            if event.key() == QtCore.Qt.Key_G:
                self.ui.le_goto.setFocus()
                handled = 1
        if handled:
            event.accept()
            return
        else:
            QtGui.QMainWindow.keyPressEvent(self,event)
    
    def toggleZen(self):
        self.zen = not self.zen
        if self.zen:
            self.restoreState(self.dockstate)
            self.ui.statusbar.show()
        else:
            self.ui.statusbar.hide()
            self.dockstate = self.saveState()
            for plug in self.pluginD:
                self.pluginD[plug].close()

    def openFile(self,filename=None):
        if not filename:
            # Ask for filename if not specified
            filename = QtGui.QFileDialog.getOpenFileName(self,"Select File",""," (*.*)")
            if filename=='':
                filename = None
            else:
                filename = str(filename)
        if filename != None:
            if os.path.isfile(filename):
                opennew = 1
                for i in range(self.ui.tab.count()):
                    file_id = self.ui.tab.tabData(i).toInt()[0]
                    wdg = self.tabD[file_id]
                    if wdg.filename != None and os.path.abspath(wdg.filename) == os.path.abspath(filename):
                        self.ui.tab.setCurrentIndex(i)
                        opennew = 0
                        break
                
                if opennew:
                    lang = None
                    ext = os.path.splitext(str(filename))[1][1:]
                    if ext in self.settings['ext']:
                        lang = self.settings['ext'][ext]
                    
                    title = os.path.basename(filename)
                    if self.settings['view_folder']:
                        title = os.path.split(os.path.dirname(filename))[1]+'/'+title
                    
                    wdg = self.addEditorWidget(lang,title,str(filename))
                    f = codecs.open(filename,'r','utf-8')
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

        if tab_ind == -1 and self.ui.tab.count()>0: tab_ind == 0
        file_id = self.ui.tab.tabData(tab_ind).toInt()[0]
        if file_id in self.tabD:
            wdg = self.tabD[file_id]
            self.ui.sw_main.setCurrentWidget(wdg)
            self.evnt.editorTabChanged.emit(wdg)
            
            # Show/Hide plugins
            lang = wdg.lang
            
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
                            
            if lang in self.settings['lang']:
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
        if wdg.lastText != unicode(wdg.getText(),'utf-8'):
            self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title+'*')
        else:
            self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
            
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
        wdg.viewOnly = 0
        wdg.dockstate = None
        self.tabD[self.fileCount]=wdg
        self.evnt.editorAdded.emit(wdg)
        

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
        
        # Add Icon
        if filename != None:
            ext = os.path.splitext(filename)[1][1:]
            ipth = self.iconPath+'files/'+ext+'.png'
            if os.path.exists(ipth):
                self.ui.tab.setTabIcon(sw_ind,QtGui.QIcon(ipth))
            else:
                ipth = self.iconPath+'/files/_blank.png'
                self.ui.tab.setTabIcon(sw_ind,QtGui.QIcon(ipth))
        
        else:
            # New Files without filename
            ext = [key for key, value in self.settings['ext'].iteritems() if value == lang]
            if type(ext) == type([]) and ext != []:
                ext = ext[0]
            else:
                ext = '_blank'
            ipth = self.iconPath+'files/'+ext+'.png'
            if not os.path.exists(ipth):
                ipth = self.iconPath+'/files/_blank.png'
            self.ui.tab.setTabIcon(sw_ind,QtGui.QIcon(ipth))
        return wdg

    def checkSave(self,wdg):
        ok = 0
        if wdg.viewOnly:
            ok = 1
        else:
            if wdg.lastText != unicode(wdg.getText(),'utf-8'):
                resp = QtGui.QMessageBox.warning(self,'Save Tab',"Do you want to save the file <b>"+wdg.title+"</b>?",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
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
##                f = open(wdg.filename,'w')
                txt = unicode(wdg.getText(),encoding='utf-8')
                f = codecs.open(wdg.filename,'w','utf-8')
                f.write(txt)
                f.close()
                wdg.lastText = txt
                self.ui.statusbar.showMessage('Saved '+filename+' at '+datetime.datetime.now().ctime())
                self.ui.tab.setTabText(self.ui.tab.currentIndex(),wdg.title)
            except:
                QtGui.QMessageBox.warning(self,'Error Saving','There was an error saving this file.  Make sure it is not open elsewhere and you have write access to it.  You may want to copy the text, paste it in another editor to not lose your work.<br><br><b>Error:</b><br>'+str(sys.exc_info()[1]))
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
        if ok and filename != 'None':
            if wdg.lang in self.settings['lang'] and 'run' in self.settings['lang'][wdg.lang]:
                self.pluginD['output'].raise_()
                self.pluginD['output'].wdg.newProcess(self.settings['lang'][wdg.lang]['run'],filename)
##                print self.settings['lang'][wdg.lang]['run']
##                newstream = plugins.output.output.MyStream()
##                exec('procs ='+ self.settings['lang'][wdg.lang]['run'].replace('$file',filename))
                #for line in iter(procs.stdout.readline, ''): print line

                # print stdout
                
##                procs.stdout = newstream
##                procs.stderr = newstream
##                newstream.message.connect(self.pluginD['output'].wdg.on_myStream_message)

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
    def addPlugin(self,wdg,dockarea,title):
        
        dock = QtGui.QDockWidget()
        
        dock.dockWidgetContents = QtGui.QWidget()
        dock.setWidget(dock.dockWidgetContents)
        dock.setWindowTitle(title)
        dock.gridLayout = QtGui.QGridLayout(dock.dockWidgetContents)
        dock.gridLayout.setMargin(0)
        dock.gridLayout.setSpacing(0)
        dock.gridLayout.addWidget(wdg, 0, 0, 1, 1)
        dock.setObjectName(title.replace(' ','_').lower())
        dock.wdg = wdg
        self.addDockWidget(dockarea,dock)
        self.pluginDocks.append(dock)
        
        # Tabify Dock with other widgets in its area
        for idock in self.pluginDocks[:-1]:
            if self.dockWidgetArea(idock) == dockarea:
                self.tabifyDockWidget(idock,dock)
        
        return dock

    #---Settings
    def loadSettings(self):
        self.settings_filename = os.path.abspath(os.path.dirname(__file__))+'/settings.yml'
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
