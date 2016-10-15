from . import snippets

class Plugin(object):
    title = 'Snippets'
    location = 'bottom'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        '''Load the widget'''
        self.widget = snippets.Snippets(self.parent)
        return self.widget