from . import qt2py
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'PyQt Converter'
    location = 'bottom'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = qt2py.Qt2Py(self.parent)
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Q,self.parent,self.widget.qtHelp) # Qt Help
        return self.widget