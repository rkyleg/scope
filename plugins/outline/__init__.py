from . import outline
from PyQt4 import QtGui, QtCore

title = 'Outline'
location = 'left'

def addPlugin(parent):
    plugin = outline.Outline(parent)
    
    parent.evnt.editorAdded.connect(plugin.addOutline)
    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
    parent.evnt.fileOpened.connect(plugin.updateOutlineToggle)
    
    # QtGui.QShortcut(QtCore.Qt.Key_F3,parent,plugin.updateOutlineToggle) 
    
##    plugin.title = 'Outline'
##    plugin.location = 'left'
    return plugin