import ckeditor
from PyQt4 import QtGui, QtCore
import os

def addEditor(parent,lang,filename):
    if filename != None:
        if os.name =='nt':
            pfx="file:///"
        else:
            pfx="file://"
        burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(filename)).replace('\\','/')+'/')
    else:
        burl = QtCore.QUrl()
    editor = ckeditor.WebView(parent,baseurl=burl)
    return editor

def getLang():
    return ['html']

def getSettings():
    return {}