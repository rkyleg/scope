from . import output

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Output'
    location = 'bottom'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = output.Output(self.parent)
        self.parent.Events.editorTabChanged.connect(self.widget.editorTabChanged)
        self.parent.Events.editorTabClosed.connect(self.widget.editorTabClosed)
        self.parent.Events.close.connect(self.widget.killAll)
        return self.widget