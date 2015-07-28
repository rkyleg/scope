from . import home
from PyQt4 import QtGui, QtCore

location = None
title = 'Home'

def addPlugin(parent):
    plugin = home.Home(parent)
##    plugin.title = 'Home'
##    plugin.location = None
    
    parent.HomeWidget = plugin
    plugin.webview.id = None
    plugin.webview.title = 'Home'
    plugin.webview.icon = QtGui.QIcon(parent.iconPath+'home.png')
    parent.ui.sw_main.addWidget(plugin.webview)
    parent.ui.sw_main.setCurrentIndex(0)
    
    QtGui.QShortcut(QtCore.Qt.Key_F9,parent,plugin.toggleHome) # Show Heads up display
    
    return plugin