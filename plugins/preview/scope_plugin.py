from . import preview

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Preview'
    location = 'right'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        self.widget = preview.Preview(self.parent)
    ##    parent.Events.editorAdded.connect(plugin.addPreview)
        self.parent.Events.editorTabChanged.connect(self.widget.editorTabChanged)
        self.parent.Events.editorTabClosed.connect(self.widget.editorTabClosed)
        self.parent.Events.editorSaved.connect(self.widget.updatePreview)
        return self.widget