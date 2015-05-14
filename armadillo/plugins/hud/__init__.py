from . import hud
from PyQt4 import QtGui, QtCore

def addPlugin(parent):
    plugin = hud.HUD(parent)
    plugin.title = 'HUD'
    plugin.location = None
    
    parent.HUDWidget = plugin
    
    QtGui.QShortcut(QtCore.Qt.Key_F1,parent,plugin.toggleHUD) # Show Heads up display
    
    return plugin