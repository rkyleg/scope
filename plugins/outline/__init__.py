from . import outline
from PyQt4 import QtGui, QtCore

title = 'Outline'
location = 'left'

def addPlugin(parent):
    plugin = outline.Outline(parent)
    
    parent.Events.editorAdded.connect(plugin.addOutline)
    parent.Events.editorTabChanged.connect(plugin.editorTabChanged)
    parent.Events.editorTabClosed.connect(plugin.editorTabClosed)
    parent.Events.fileOpened.connect(plugin.updateOutlineToggle)
    
    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_O,parent,plugin.updateOutlineToggle) 
    
##    plugin.title = 'Outline'
##    plugin.location = 'left'    
    return plugin