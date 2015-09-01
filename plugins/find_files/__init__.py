from . import find_files
from PyQt4 import QtGui, QtCore
import os

title = 'Search Files'
location = 'app'
plugin = None

def loadPlugin(parent):
    def addFindFilesWidget():
        
        if plugin == None:
            global plugin
            curdir = os.path.abspath('.')
            os.chdir(os.path.dirname(__file__))
            plugin = find_files.Find_Files(parent)
            os.chdir(curdir)
            parent.addMainWidget(plugin,'find files',icon=btn.icon())
            parent.evnt.workspaceChanged.connect(plugin.changeWorkspace)
            
        plugin.toggle()
        
    # Add button 
    btn = parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=title)
##    btn.setIcon(QtGui.QIcon('icon.png'))
##    btn.setProperty("class",  "toolbar toolbar-individual")
##    btn.setToolTip('Spellcheck the selected text')
##    layout = parent.ui.fr_leftbar.layout()
##    layout.insertWidget(layout.count()-1,btn)
    btn.clicked.connect(addFindFilesWidget)

def addPlugin(parent,**kargs):
    plugin = find_files.Find_Files(parent)
    return plugin 
    
    
##        if plugin == None:
##            global plugin
##            plugin = find_files.Find_Files(parent)

##    plugin = find_files.Find_Files(parent)
##    plugin.id = None
##    plugin.title = 'Find Files'
##    plugin.icon = QtGui.QIcon('icon.png')


    # Tool Menu Code
##    parent.ui.sw_main.addWidget(plugin)
##    parent.evnt.workspaceChanged.connect(plugin.changeWorkspace)
##    lay = parent.ui.fr_leftbar.layout()
##    lay.insertWidget(lay.count()-1,QtGui.QPushButton('ff'))
    
    
    
##    parent.evnt.editorAdded.connect(plugin.addOutline)
##    parent.evnt.editorTabChanged.connect(plugin.editorTabChanged)
##    parent.evnt.editorTabClosed.connect(plugin.editorTabClosed)
##    parent.evnt.fileOpened.connect(plugin.updateOutline)
    
##    QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_B,parent,plugin.toggle) 
##    QtGui.QShortcut(QtCore.Qt.Key_F6,parent,plugin.toggle) 
    
##    plugin.title = 'Spellcheck'
##    plugin.location = ''
##    
##    # Add button 
##    # Add button 
##    btn = QtGui.QPushButton()
##    btn.setIcon(QtGui.QIcon('icon.png'))
##    btn.setProperty("class",  "toolbar toolbar-individual")
##    btn.setToolTip('Spellcheck the selected text')
##    layout = parent.ui.fr_leftbar.layout()
##    layout.insertWidget(layout.count()-1,btn)
##    btn.clicked.connect(addFindFilesWidget)
##    btn.clicked.connect(plugin.toggle)
    
##    return plugin
