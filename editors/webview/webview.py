from PyQt4 import QtGui, QtCore, QtWebKit
import os

def addEditor(parent,lang):
    editor = WebView(parent)
    return editor

# Custom Webpage class
class WebPage(QtWebKit.QWebPage):
    def __init__(self,parent=None):
        QtWebKit.QWebPage.__init__(self,parent)

    def javaScriptConsoleMessage(self, msg, line, source):
        """
        QWebPage that prints Javascript errors to stderr.
        """
        print('JS ERROR: %s line %d: %s' % (source, line, msg))

class WebView(QtWebKit.QWebView):
    def __init__(self,parent=None):
        QtWebKit.QWebView.__init__(self,parent)
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)
    
    def setText(self,txt):
        baseurl=QtCore.QUrl(os.path.abspath(os.path.dirname(__file__)+'../../../'))
        self.setHtml(txt,baseurl)
        ##self.setHtml(txt)

    def find(self,txt,**kargs):
        self.findText(txt)