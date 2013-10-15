from PyQt4 import QtGui, QtCore, QtWebKit
import os

# Custom Webpage class
class WebPage(QtWebKit.QWebPage):
    def __init__(self,parent=None,baseurl=None):
        QtWebKit.QWebPage.__init__(self,parent)

    def javaScriptConsoleMessage(self, msg, line, source):
        """
        QWebPage that prints Javascript errors to stderr.
        """
        print('JS ERROR: %s line %d: %s' % (source, line, msg))

class WebView(QtWebKit.QWebView):
    def __init__(self,parent=None,baseurl=None):
        QtWebKit.QWebView.__init__(self,parent)
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)
        self.baseurl = baseurl
    
    def setText(self,txt,baseurl=None):
        if self.baseurl != None:
            baseurl = self.baseurl
        if baseurl == None:
            baseurl=QtCore.QUrl()
        
        self.setHtml(txt,baseurl)
        ##self.setHtml(txt)

    def find(self,txt,**kargs):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)