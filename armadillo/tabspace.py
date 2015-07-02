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
        self.setStyleSheet("QListWidget{background:transparent;border:0px;}")
        self.setProperty("class",'editor_tab')
        self.setSpacing(2)
        self.clicked.connect(self.select)
##        self.setViewMode(1)
    
    def addEditortab(self,file_id,title,filename):
        etab = editortab(self.ide,file_id,title,filename)
        
        itm = QtGui.QListWidgetItem()
        itm.setSizeHint(etab.sizeHint())
        itm.setToolTip(filename)
##        print etab.sizeHint()
        
        self.addItem(itm)
        etab.item = itm
        self.setItemWidget(itm,etab)
        itm.setSizeHint(etab.sizeHint())
    
    def select(self,m_ind):
        itm = self.itemFromIndex(m_ind)
        wdg = self.itemWidget(itm)
        self.ide.openFile(wdg.filename)
        self.ide.tabspace.toggle(0)
    
    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        cind = self.currentRow()
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return]:
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

##        if event.modifiers() & QtCore.Qt.ControlModifier:
##            if event.key() == QtCore.Qt.Key_C:
##                self.copy()
##                handled = 1
##            elif event.key() == QtCore.Qt.Key_V:
##                self.paste()
##                handled = 1
##            elif event.key() == QtCore.Qt.Key_X:
##                self.copy()
##                self.cut()
##                handled = 1
##            elif event.key() == QtCore.Qt.Key_D:
##                self.copyLinesDown()
##                handled = 1
##            elif event.key() == QtCore.Qt.Key_Delete:
##                self.removeLines()
##                handled = 1
                
        if not handled:
            QtGui.QListWidget.keyPressEvent(self,event)

class editortab(QtGui.QWidget):
    def __init__(self,ide,file_id,title,filename):
        QtGui.QWidget.__init__(self)
        self.id = file_id
        self.filename = filename
        self.ide = ide
        
        # Layout
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        layout.setSpacing(2)
        
        # Icon Button
        icn_btn = QtGui.QPushButton()
        icn_btn.setIcon(QtGui.QIcon(self.ide.getIconPath(filename)))
        icn_btn.setProperty("class",'editor_tab_btn')
        icn_btn.setMaximumWidth(32)
        layout.addWidget(icn_btn)
        
        # File Text
        lbl = QtGui.QLabel(title)
        lbl.setProperty("class",'editor_tab')
        lbl.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred))
        lbl.updateGeometry()
        layout.addWidget(lbl)
        
        # Close Button
        cls_btn = QtGui.QPushButton()
        cls_btn.clicked.connect(self.close)
        cls_btn.setMaximumWidth(32)
        cls_btn.setProperty("class",'editor_tab_cls_btn')
        layout.addWidget(cls_btn)
        
##        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)        self.setLayout(layout)
    
    def close(self):
        li = self.parent().parent()
##        print li, li.indexFromItem(self.item)
        fid = li.ide.isFileOpen(self.filename)
        ok = li.ide.closeTab(fid)
        if ok:
            li.takeItem(li.row(self.item))
            self.ide.tabspace.highlightCurrent()
        else:
            li.ide.tabspace.toggle(1)

class TabSpace(object):
    def __init__(self,parent=None,wtyp='blank'):
        self.tabs = QtGui.QTabWidget(parent)
##        QtGui.QTabWidget.__init__(self)##        self.tabs.setStyleSheet("QTabWidget,QTabBar{background:rgb(61,107,129);}")
        self.tabs.setWindowOpacity(0.9)
        self.tabs.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ide = parent
##        self.wtype = wtyp
        
        # Setup tab widget
        self.tabs.setTabPosition(QtGui.QTabWidget.South)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setProperty("class","editorTabs")
        self.tabs.setObjectName('editorTabBar')
        self.tabs.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
    
        self.tabs.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.tabs.setWindowModality(QtCore.Qt.NonModal)
    
        # Signals
##        self.currentChanged.connect(self.change_workspace)
        self.tabs.tabCloseRequested.connect(self.closeWorkspace)
    
    def addWorkspace(self,name):
        ww = WorkspaceWidget(parent=self.ide)
        self.tabs.addTab(ww,name)
        self.tabs.setCurrentWidget(ww)
        return ww
##        self.currentChanged.connect(self.changeTab)
##        self.tabCloseRequested.connect(self.closeTab)
##        self.setExpanding(0)

    def closeWorkspace(self,ind):
        wksp = self.tabs.widget(ind).title()
##        ok = self.ide.closeWorkspace(wksp)
##        if ok:
##            self.tabs.removeTab(ind)
        self.tabs.removeTab(ind)
    
    def show(self):
        h=300 # default height
        if self.ide != None:
            g=self.ide.geometry()
            
            if h > g.height():
                h = g.height()
            dy = self.ide.ui.fr_topbar.height()
            self.tabs.setGeometry(g.x(),g.y()+dy,g.width(),h)
        else:
            self.tabs.setGeometry(20,20,500,h)
        
        self.tabs.show()
    
    def toggle(self,mode=None):
        if mode == None:
            mode = not self.tabs.isVisible()
            
        if mode:
            self.show()
            if self.tabs.currentWidget() != None:
                self.tabs.currentWidget().setFocus()
                
                self.highlightCurrent()
            
        else:
            self.tabs.hide()
    
    def highlightCurrent(self):
        # Highlight current file
        fid = self.ide.currentEditor().filename
        li = self.tabs.currentWidget()
        for i in range(li.count()):
            litm = li.itemWidget(li.item(i))
            print litm.id,fid
            if litm.filename == fid:
                li.setCurrentRow(i)
                break


if __name__ == '__main__':
    # create qt app object
    qtApp = QtGui.QApplication(sys.argv)
    
    # build test of tabwidget
    mw = TabSpace()
##    ww = WorkspaceWidget()
##    mw.addTab(ww,'workspace 1')
    ww = mw.addWorkspace('workspace 1')    
    # Add tabs
    ww.addEditortab(1,'a file.py','')
    ww.addEditortab(1,'help.md','')
##    t.show()
##    itm = QtGui.QListWidgetItem()
##    itm.setSizeHint(t.sizeHint())
##    ww.addItem(itm)
##    ww.setItemWidget(itm,t)    
    
    # show and start
    mw.show()    qtApp.exec_()