from . import scratch

class Plugin(object):
    title = 'Scratchpad'
    location = 'bottom'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        '''Load the widget'''
        self.widget = scratch.Scratch(self.parent)
        return self.widget