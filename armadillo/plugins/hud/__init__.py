from . import hud
from PyQt4 import QtGui, QtCore

def addPlugin(parent):
    plugin = hud.HUD(parent)
    plugin.title = 'HUD'
    plugin.location = None
    
    parent.HUDWidget = plugin
    plugin.webview.id = None
    parent.ui.sw_main.addWidget(plugin.webview)
    parent.ui.sw_main.setCurrentIndex(0)
    
    QtGui.QShortcut(QtCore.Qt.Key_F9,parent,plugin.toggleHUD) # Show Heads up display
    
    return plugin