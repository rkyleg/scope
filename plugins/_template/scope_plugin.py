import os
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''

class Plugin(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    widget = None
    settings = Settings.__dict__
    # or
    settings = {}
    
    def __init__(self,parent):
        self.parent = parent
    
    def load(self):
        '''Called on when loading the plugin'''
        
    def getWidget(self):
        '''Return a Widget'''
    
