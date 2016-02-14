from . import outline
from PyQt4 import QtGui, QtCore

class Plugin(object):
    title = 'Outline'
    location = 'left'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = outline.Outline(self.parent)
        
        self.parent.Events.editorAdded.connect(self.widget.addOutline)
        self.parent.Events.editorTabChanged.connect(self.widget.editorTabChanged)
        self.parent.Events.editorTabClosed.connect(self.widget.editorTabClosed)
        self.parent.Events.fileOpened.connect(self.widget.updateOutlineToggle)
        
        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_O,self.parent,self.widget.updateOutlineToggle) 
        
    ##    plugin.title = 'Outline'
    ##    plugin.location = 'left'
        
        return self.widget