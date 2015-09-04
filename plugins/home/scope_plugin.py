from . import home
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    location = None
    title = 'Home'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        self.loadWidget()
        
    def loadWidget(self):
        self.widget = home.Home(self.parent)
        self.parent.HomeWidget = self.widget
        icon = QtGui.QIcon(self.parent.iconPath+'home.png')
        self.parent.addMainWidget(self.widget.webview,'Home',icon=icon,typ='app')
        QtGui.QShortcut(QtCore.Qt.Key_F9,self.parent,self.widget.toggleHome) # Show Heads up display
        
        return self.widget