from . import find_files
import os
from PyQt4 import QtGui, QtCore

class Plugin(object):
    title = 'Search Files'
    location = 'app'
    widget = None
    
    def __init__(self,parent):
        self.parent = parent
    
    def load(self):
        btn = self.parent.addLeftBarButton(QtGui.QIcon('icon.png'))
        btn.clicked.connect(self.addFindFilesWidget)
        
    def getWidget(self):
        curdir = os.path.abspath('.')
        os.path.chdir(os.path.dirname(__file__))
        self.widget = find_files.Find_Files(self.parent)
        os.path.chdir(curdir)
        return self.widget
    
    def addFindFilesWidget(self):
        if self.widget == None:
            self.getWidget()
        self.parent.addMainWidget(self.widget,'find files',icon=btn.icon())
        self.parent.evnt.workspaceChanged.connect(self.widget.changeWorkspace)
        self.widget.toggle()