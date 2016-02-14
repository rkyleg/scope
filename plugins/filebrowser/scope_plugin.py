from . import filebrowser
from PyQt4 import QtGui, QtCore

class Plugin(object):
    title = 'File Browser'
    location = 'left'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = filebrowser.FileBrowser(self.parent)

        self.parent.Events.workspaceOpened.connect(self.widget.openWorkspace)
        self.parent.Events.workspaceChanged.connect(self.widget.changeWorkspace)
        return self.widget