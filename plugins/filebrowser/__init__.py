from . import filebrowser
from PyQt4 import QtGui, QtCore

title = 'File Browser'
location = 'left'

def addPlugin(parent):
    plugin = filebrowser.FileBrowser(parent)
##    plugin.title = 'File Browser'
##    plugin.location = 'left'
    
    # QtGui.QShortcut(QtCore.Qt.Key_F2,parent,plugin.viewFileBrowser) # View Filebrowser
    
    parent.Events.workspaceOpened.connect(plugin.openWorkspace)
    parent.Events.workspaceChanged.connect(plugin.changeWorkspace)
    
    return plugin