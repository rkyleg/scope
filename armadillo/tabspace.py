import sys, os
from PyQt4 import QtCore, QtGui

class WorkspaceWidget(QtGui.QListWidget):
    def __init__(self,parent=None):
        QtGui.QListWidget.__init__(self)
        

class tab(QtGui.QWidget):
    def __init__(self,file_id,title,filename):
        QtGui.QWidget.__init__(self)
        self.id = file_id
        self.filename = filename
        
        layout = QtGui.QHBoxLayout()
        
        lbl = QtGui.QLabel(title)
        layout.addWidget(lbl)
        
        layout.addWidget(QtGui.QPushButton('x'))
        
        layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.setLayout(layout)


class MainWidget(QtGui.QTabWidget):
    def __init__(self,parent=None):
        QtGui.QTabWidget.__init__(self)
        
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setProperty("class","editorTabs")
        self.setObjectName('editorTabBar')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred))
        
##        self.currentChanged.connect(self.changeTab)
##        self.tabCloseRequested.connect(self.closeTab)
##        self.setExpanding(0)

if __name__ == '__main__':
    # create qt app object
    qtApp = QtGui.QApplication(sys.argv)
    
    # build test of tabwidget
    mw = MainWidget()
    ww = WorkspaceWidget()
    mw.addTab(ww,'workspace 1')
    
    # Add tabs
    t=tab(1,'a file','')
##    t.show()
    itm = QtGui.QListWidgetItem()
    itm.setSizeHint(t.sizeHint())
    ww.addItem(itm)
    ww.setItemWidget(itm,t)
    
    
    # show and start
    mw.show()
    qtApp.exec_()