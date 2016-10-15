import os
from PyQt4 import QtGui, QtCore

class Plugin(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    widget = None  # The widget for the plugin (set at loadWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def loadWidget(self):
        '''Load the widget'''
        self.widget = None  # Set your PyQt widget here if a widget plugin
        return self.widget