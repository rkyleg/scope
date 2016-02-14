import os
from PyQt4 import QtGui, QtCore

class Editor(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def getWidget(self, lang, **kargs):
        '''Return the Editor Widget'''

    def getLang(self):
        '''Return a list of strings of the available languages'''
        return []