import ace
from PyQt4 import QtGui, QtCore
import os

def addEditor(parent,lang,filename):
##    if filename != None:
##        if os.name =='nt':
##            pfx="file:///"
##        else:
##            pfx="file://"
##        burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(filename)).replace('\\','/')+'/')
##    else:
##        burl = QtCore.QUrl()
    editor = ace.WebView(parent,lang)
    return editor
    
def getLang():
    '''Get Languages'''
    fld = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/src-noconflict/'
    lexers = []
    for f in sorted(os.listdir(fld)):
        if f.startswith('mode'):
            lexers.append(f[5:-3])
    
    return lexers