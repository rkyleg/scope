import os
from PyQt4 import QtGui, QtCore
from . import ckeditor

class Settings(object):
    '''Modifiable settings and their defaults'''
    
class Editor(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    settings = Settings.__dict__
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def getWidget(self, lang, **kargs):
        filename = kargs['filename']
        if filename != None:
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(filename)).replace('\\','/')+'/')
        else:
            burl = QtCore.QUrl()
        editor = ckeditor.WebView(self.parent,baseurl=burl)
        return editor

    def getLang(self):
        '''Return a list of strings of the available languages'''
        return ['html']