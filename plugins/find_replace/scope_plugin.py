from . import find_replace
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Find / Replace'
    location = 'bottom'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = find_replace.Find_Replace(self.parent)
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_R,self.parent,self.widget.replaceFocus) # Replace
        
        return self.widget