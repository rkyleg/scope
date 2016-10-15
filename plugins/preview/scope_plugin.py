from . import preview

class Plugin(object):
    title = 'Preview'
    location = 'right'
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