import os
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Search in Files'
    location = 'app' # left, bottom, right, app
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        self.btn = self.parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=self.title)
        self.btn.clicked.connect(self.addFindFilesWidget)
        # store widget with button (with addLeftBarButton.  if widget doesn't exist, it calls the getwidget)
        
    def loadWidget(self):
        from . import find_files
        curdir = os.path.abspath('.')
        os.chdir(os.path.dirname(__file__))
        self.widget = find_files.Find_Files(self.parent)
        os.chdir(curdir)
        return self.widget
    
    def addFindFilesWidget(self):
        if self.widget == None:
            self.loadWidget()
            self.parent.addMainWidget(self.widget,self.title,icon=self.btn.icon(),typ='app')
            self.parent.Events.workspaceChanged.connect(self.widget.changeWorkspace)
        self.widget.toggle()
