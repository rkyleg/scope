from . import filebrowser
from PyQt4 import QtGui, QtCore

def addPlugin(parent):
    plugin = filebrowser.FileBrowser(parent)
    plugin.title = 'File Browser'
    plugin.location = 'left'
    
    # QtGui.QShortcut(QtCore.Qt.Key_F2,parent,plugin.viewFileBrowser) # View Filebrowser
    
    parent.evnt.workspaceOpened.connect(plugin.openWorkspace)
    parent.evnt.workspaceChanged.connect(plugin.changeWorkspace)
    
    return plugin