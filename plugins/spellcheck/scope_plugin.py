from . import spellcheck
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Spellcheck'
    location = None
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        self.loadWidget()
        # Add button 
        btn = QtGui.QPushButton()
        btn.setIcon(QtGui.QIcon('icon.png'))
        btn.setProperty("class",  "toolbar toolbar-individual")
        btn.setToolTip('Spellcheck the selected text')
        layout = self.parent.ui.fr_toolbar.layout()
        layout.addWidget(btn,0,layout.columnCount(),QtCore.Qt.AlignLeft,1)
        btn.clicked.connect(self.widget.toggle)
        
    def loadWidget(self):
        self.widget = spellcheck.SpellChecker(self.parent)

        return self.widget