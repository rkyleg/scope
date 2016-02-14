import os
from PyQt4 import QtGui, QtCore

##class Settings(object):
##    '''Modifiable settings and their defaults'''
##    # attribute=value
    
class Plugin(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
##    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        '''Load the widget'''
        self.widget = None
        return self.widget