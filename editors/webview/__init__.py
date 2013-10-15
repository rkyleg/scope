import webview
import os
from PyQt4 import QtGui, QtCore

def addEditor(parent,lang,filename):
    baseurl=None
    if filename != None:
        if os.name =='nt':
            pfx="file:///"
        else:
            pfx="file://"
        burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(filename)).replace('\\','/')+'/')
    editor = webview.WebView(parent,baseurl)
    return editor