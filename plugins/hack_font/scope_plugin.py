import os
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''

class Plugin(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    widget = None
    settings = Settings.__dict__
    
    def __init__(self,parent):
        self.parent = parent
    
    def load(self):
        '''Called on when loading the plugin'''
        fdb = QtGui.QFontDatabase()
        fdb.addApplicationFont('../../style/Hack-Regular.ttf')
        fdb.addApplicationFont('../../style/Hack-Bold.ttf')
        fdb.addApplicationFont('../../style/Hack-RegularOblique.ttf')
        fdb.addApplicationFont('../../style/Hack-Oblique.ttf')
        
    def getWidget(self):
        '''Return a Widget'''
    
