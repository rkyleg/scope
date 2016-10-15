import os
from PyQt4 import QtGui, QtCore
    
class Plugin(object):
    title = 'Edit Settings'
    location = 'app' # left, bottom, right, app
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        from . import settings
        curdir = os.path.abspath('.')
        os.chdir(os.path.dirname(__file__))
        self.widget = settings.Settings_Editor(self.parent)
        self.widget.icon = QtGui.QIcon('icon.png')
        os.chdir(curdir)
        return self.widget
    
    def addSettingsWidget(self):
        if self.widget == None:
            self.loadWidget()
            self.parent.addMainWidget(self.widget,self.title,icon=self.widget.icon,typ='app')
##            self.parent.Events.workspaceChanged.connect(self.widget.changeWorkspace)
        self.toggle()
    
    def toggle(self):
        self.parent.ui.sw_main.setCurrentWidget(self.widget)