from . import spellcheck
from PyQt4 import QtGui, QtCore

title = 'Spellcheck'
location = 'tools'

def addPlugin(parent):
    plugin = spellcheck.SpellChecker(parent)
    
##    parent.evnt.editorAdded.connect(plugin.addOutline)
##    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
##    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
##    parent.evnt.fileOpened.connect(plugin.updateOutline)
    
##    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_B,parent,plugin.toggle) 
##    QtGui.QShortcut(QtCore.Qt.Key_F6,parent,plugin.toggle) 
    
##    plugin.title = 'Spellcheck'
##    plugin.location = ''
    
    # Add button 
##    btn = QtGui.QPushButton()
##    btn.setIcon(QtGui.QIcon('spellcheck.png'))
##    btn.setProperty("class",  "toolbar toolbar-individual")
##    btn.setToolTip('Spellcheck the selected text')
##    layout = parent.ui.fr_toolbar.layout()
##    layout.addWidget(btn,0,layout.columnCount(),QtCore.Qt.AlignLeft,1)
##    btn.clicked.connect(plugin.toggle)
    
    return plugin

##def runPlugin():
##    print 'run spellcheck'