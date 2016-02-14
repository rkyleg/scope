from . import py_console
import sys

class Plugin(object):
##    title = 'Python Shell ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')'
    title = 'Python Console'
    location = 'bottom'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = py_console.PyConsole(self.parent)
        self.widget.write('# Scope Python Console\n    - only modules included with Scope are available\n    - Ctrl+l to launch popup (outside of Scope) with the default installed Python\n',mode=1)
        self.widget.write('\n')
        return self.widget