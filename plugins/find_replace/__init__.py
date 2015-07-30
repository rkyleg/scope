from . import find_replace
from PyQt4 import QtGui, QtCore

title = 'Find / Replace'
location = 'bottom'

def addPlugin(parent):
    plugin = find_replace.Find_Replace(parent)
##    plugin.title = 'Find / Replace'
##    plugin.location = 'bottom'
    
    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_R,parent,plugin.replaceFocus) # Replace
    
    return plugin