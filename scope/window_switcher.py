import sys, os
from PyQt4 import QtCore, QtGui

class WorkspaceWidget(QtGui.QListWidget):
    def __init__(self,parent=None):
        QtGui.QListWidget.__init__(self)
        self.ide = parent
        self.setFlow(0)
        self.setWrapping(1)
        self.setResizeMode(1)
        self.setDragDropMode(4) # internalmove
        self.setDragEnabled(1) # enable drag drop
##        self.setStyleSheet("QListWidget{background:transparent;border:0px;margin:4px;}")
        self.setProperty("class",'editor_tab')
        self.setSpacing(0)
        self.clicked.connect(self.select)
        self.tabD = {}
##        self.setViewMode(1)
    
    def addEditortab(self,file_id,title,filename,editor=''):
        if not file_id in self.tabD:
            etab = editortab(self.ide,file_id,title,filename,editor)
            itm = QtGui.QListWidgetItem()
            itm.setSizeHint(etab.sizeHint())
            if filename != None:
                itm.setToolTip(filename)
            
            self.addItem(itm)
            etab.item = itm
            self.setItemWidget(itm,etab)
            itm.setSizeHint(etab.sizeHint())
            self.tabD[file_id]=etab
            tab = etab
        else:
            tab = self.tabD[file_id]
            
        return tab
    
    def mousePressEvent(self, event):
        handled = 0
        ind = self.indexAt(event.pos())
        btn = event.button()
        if btn == 1: #left
            handled = 0
        elif btn == 4: # middle
            itm = self.itemFromIndex(ind)
            wdg = self.itemWidget(itm)
            wdg.close()
            handled = 1
        elif btn == 2: # right
            self.rightclick(event)
            handled = 1
        
        if not handled:
            QtGui.QListWidget.mousePressEvent(self,event)
    
    def select(self,m_ind,hide_tabs=1):
        itm = self.itemFromIndex(m_ind)
        wdg = self.itemWidget(itm)
        file_id=wdg.id

        ok = self.ide.openFile(file_id=file_id)
        if not ok:
            resp = QtGui.QMessageBox.warning(self,'File not Found','This file no longer exists or there was an error opening it<br><br>Do you want to remove the tab?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                wdg.close(ignoreCheck=1)
            self.ide.WindowSwitcher.toggle(1)
        else:
            if hide_tabs:
                self.ide.WindowSwitcher.toggle(0)
    
    def rightclick(self,event):
        ind = self.indexAt(event.pos())
        itm = self.itemFromIndex(ind)
        current_ind = self.currentIndex()
        if itm != None:
            wdg = self.itemWidget(itm)
        
            # Right Click Menu
            menu = QtGui.QMenu()
            
            icn = QtGui.QIcon(self.ide.iconPath+'tri_right.png')
            menu.addAction(icn,'Run')
            
            icn = QtGui.QIcon(self.ide.iconPath+'file_go.png')
            menu.addAction(icn,'Open (external)')
            
            icn = QtGui.QIcon(self.ide.iconPath+'close_blue.png')
            menu.addAction(icn,'Close')
            
            act = menu.exec_(self.cursor().pos())
            if act != None:
                acttxt = str(act.text())
                
                if acttxt == 'Close':
                    wdg.close()
                elif acttxt == 'Run':
                    #TODO: If file not open
                    if wdg.id not in self.ide.fileOpenD:
                        self.select(ind)
                    self.ide.editorRun(self.ide.fileOpenD[wdg.id])
                    if current_ind != None:
                        self.select(current_ind)
                elif acttxt == 'Open (external)':
                    self.ide.WindowSwitcher.toggle(0)
                    self.ide.openFileExternal(wdg.filename)
    
    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        cind = self.currentRow()
        tind = self.ide.WindowSwitcher.tabs.currentIndex() # Current workspace tab
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if ky == QtCore.Qt.Key_Left:
                # Change workspaces
                tind -=1
                if tind <0:
                    tind = self.ide.WindowSwitcher.tabs.count()-1
                self.ide.WindowSwitcher.tabs.setCurrentIndex(tind)
                self.ide.WindowSwitcher.tabs.currentWidget().setFocus()
                handled = 1
            elif ky == QtCore.Qt.Key_Right:
                tind +=1
                if tind >= self.ide.WindowSwitcher.tabs.count():
                    tind = 0
                self.ide.WindowSwitcher.tabs.setCurrentIndex(tind)
                self.ide.WindowSwitcher.tabs.currentWidget().setFocus()

                handled = 1
        elif ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return]:
            handled = 1
            self.select(self.currentIndex())
        elif ky == QtCore.Qt.Key_Right:
            cind +=1
            if cind >= self.count():
                cind = 0
            self.setCurrentRow(cind)
            handled = 1
        elif ky == QtCore.Qt.Key_Left:
            cind -=1
            if cind < 0:
                cind = self.count()-1
            self.setCurrentRow(cind)
            handled = 1
                
        if not handled:
            QtGui.QListWidget.keyPressEvent(self,event)

##    def tabMousePressEvent(self,event):
####        print event.button(),event.button() == QtCore.Qt.MidButton
##        if event.button() == QtCore.Qt.MidButton:
##            i = self.ui.tab.tabAt(event.pos())
##            self.closeTab(i)
##        else:
##            QtGui.QTabBar.mousePressEvent(self.ui.tab, event)


class editortab(QtGui.QWidget):
    def __init__(self,ide,file_id,title,filename,editor=''):
        QtGui.QWidget.__init__(self)
        self.id = file_id
        self.filename = filename
        self.ide = ide
        self.pluginEditor = ''
        
        # Layout
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(4,2,2,2)
        layout.setSpacing(4)
        
        if file_id in self.ide.fileOpenD:
            wdg = self.ide.fileOpenD[file_id]
            img = wdg.pic
        else:
            img = QtGui.QPixmap(self.ide.getIconPath(filename))
        img2 = img.scaledToHeight(20,QtCore.Qt.SmoothTransformation)
        icn_lbl = QtGui.QLabel()
        icn_lbl.setPixmap(img2)
        layout.addWidget(icn_lbl)
        
        # File Text
        lbl = QtGui.QLabel(title)
        lbl.setProperty("class",'editor_tab')
        lbl.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred))
        lbl.updateGeometry()
        layout.addWidget(lbl)
        self.titleLabel = lbl
        
        # Close Button
        cls_btn = QtGui.QPushButton()
        cls_btn.clicked.connect(self.close)
        cls_btn.setMaximumWidth(22)
        cls_btn.setProperty("class",'editor_tab_cls_btn')
        layout.addWidget(cls_btn)
        self.closeButton = cls_btn
        
##        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.setLayout(layout)
    
    def setTitle(self,title):
        self.titleLabel.setText(title)
        self.item.setSizeHint(self.sizeHint())
    
    def close(self,ignoreCheck=0):
        li = self.parent().parent()

        if ignoreCheck:
            ok =1
        else:
            ok = li.ide.closeTab(self.id,remove_from_workspace=1)
        if ok:
            li.takeItem(li.row(self.item))
            if self.id in li.tabD:
                li.tabD.pop(self.id)
            li.ide.WindowSwitcher.highlightCurrent()
        else:
            li.ide.WindowSwitcher.toggle(1)


class WindowSwitcher(object):
    def __init__(self,parent=None,wtyp='blank'):
        self.tabs = QtGui.QTabWidget(parent)

        self.tabs.setStyleSheet("""
            QTabWidget,QTabBar{
                background:rgba(40,40,40);
            }
            QTabWidget::tab-bar {
                alignment: left;
            }

            /* Style the tab using the tab sub-control. Note that
                it reads QTabBar _not_ QTabWidget */
            QTabBar::tab {
                background: transparent;
                border:0px;
                border-right: 1px solid rgb(80,80,80);
                min-width: 8ex;
                padding: 4px;
                color:#BBBBBB
            }
            QTabBar::tab:hover {
                color:white;
            }

            QTabBar::tab:selected {
                background: rgb(50,50,50);
                color:white;

            }""")
##        self.tabs.setWindowOpacity(0.9)
##        self.tabs.setStyleSheet("background:transparent;")
        
        # Make translucent if not windows
##        if os.name !='nt':
##            self.tabs.setAttribute(QtCore.Qt.WA_TranslucentBackground,1)
        
##        self.tabs.setAttribute(QtCore.Qt.WA_NoSystemBackground,1)
##        self.tabs.setAttribute(QtCore.Qt.WA_DeleteOnClose, 1);
        

        self.ide = parent
        
        # Setup tab widget
        self.tabs.setTabPosition(QtGui.QTabWidget.South)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setProperty("class","editorTabs")
        self.tabs.setObjectName('editorTabBar')
        self.tabs.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
    
        self.tabs.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
##        self.tabs.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
##        self.tabs.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
##        self.tabs.setWindowFlags(QtCore.Qt.SplashScreen)
        self.tabs.setWindowModality(QtCore.Qt.NonModal)
    
        # Signals
        self.tabs.currentChanged.connect(self.changeWorkspace)
        self.tabs.tabCloseRequested.connect(self.closeWorkspaceTab)
        
        self.tabs.keyPressEvent = self.tabKeyPress
        self.tabs.closeEvent = self.closeDialog
        
        # sign up for events
        self.ide.Events.workspaceClosed.connect(self.closeWorkspace)
    
    def tabKeyPress(self,event):
        handled = 0
        ky = event.key()
        if ky == QtCore.Qt.Key_F1:
            self.toggle(0)
            handled = 1
            
        if not handled:
            QtGui.QTabWidget.keyPressEvent(self.tabs,event)
    
    def closeDialog(self,event):
        self.ide.ui.b_show_tabs.setChecked(0)
    
    def addWorkspace(self,name):
        ww = WorkspaceWidget(parent=self.ide)
        self.tabs.addTab(ww,QtGui.QIcon(self.ide.iconPath+'workspace.png'),name)
        self.tabs.setCurrentWidget(ww)
        return ww

    def changeWorkspace(self,ind):
        if ind == -1:
            self.ide.currentWorkspace = None
        else:
            self.ide.currentWorkspace = str(self.tabs.tabText(ind))
            # set current file to current file in workspace
            wwdg = self.tabs.widget(ind)
            if wwdg.currentRow() >-1:
                wwdg.select(wwdg.currentIndex(),hide_tabs=0)
            
            self.ide.Events.workspaceChanged.emit(self.ide.currentWorkspace)
            self.ide.setWindowTitle('Scope | '+self.ide.currentWorkspace)

    def closeWorkspaceTab(self,ind):
        wksp = str(self.tabs.tabText(ind))
        ok = self.ide.workspaceClose(wksp)
    
    def closeWorkspace(self,wksp):
        for i in range(self.tabs.count()):
            if str(self.tabs.tabText(i)) == wksp:
                self.tabs.removeTab(i)
                break
        
        if self.tabs.count()==0:
            self.tabs.hide()
            self.ide.ui.b_show_tabs.setChecked(0)
    
    def show(self):
        h=self.ide.settings['window_switcher']['height'] # default height
        if self.ide != None:
            g=self.ide.geometry()
            
            if h > g.height():
                h = g.height()
            dy = self.ide.ui.fr_topbar.height()
            tlw = self.ide.ui.fr_leftbar.width()  # Left toolbar width
            self.tabs.setGeometry(g.x()+tlw,g.y()+dy,g.width()-tlw,h)
        else:
            self.tabs.setGeometry(20,20,500,h)
        
        self.tabs.show()
    
    def toggle(self,mode=None,ignore_button=0):
        if mode == None:
            mode = not self.tabs.isVisible()
            
        if mode:
            self.show()
            if self.tabs.currentWidget() != None:
                self.tabs.currentWidget().setFocus()
                self.highlightCurrent()
        else:
            self.tabs.hide()
        
        # Check button
        if not ignore_button:
            self.ide.ui.b_show_tabs.setChecked(mode)

    def highlightCurrent(self):
        # Highlight current file
        if self.ide.currentEditor() != None:
            fid = self.ide.currentEditor().id
            li = self.tabs.currentWidget()
            if li != None:
                for i in range(li.count()):
                    litm = li.itemWidget(li.item(i))
                    if litm.id == fid:
                        li.setCurrentRow(i)
                        break

