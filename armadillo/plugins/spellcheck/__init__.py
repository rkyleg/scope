from . import spellcheck
from PyQt4 import QtGui, QtCore

def addPlugin(parent):
    plugin = spellcheck.SpellChecker(parent)
    
##    parent.evnt.editorAdded.connect(plugin.addOutline)
##    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
##    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
##    parent.evnt.fileOpened.connect(plugin.updateOutline)
    
##    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_B,parent,plugin.toggle) 
    QtGui.QShortcut(QtCore.Qt.Key_F6,parent,plugin.toggle) 
    
    plugin.title = 'Spellcheck'
    plugin.location = ''
    
    return plugin