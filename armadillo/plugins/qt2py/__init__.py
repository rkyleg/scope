from . import qt2py
from PyQt4 import QtGui, QtCore
def addPlugin(parent):
    plugin = qt2py.Qt2Py(parent)
    plugin.title = 'PyQt Converter'
    plugin.location = 'bottom'
    
    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_Q,parent,plugin.qtHelp) # Qt Help
    
    return plugin