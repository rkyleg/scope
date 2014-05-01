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
    
    def load2(self,url):
        # Custom load for handling markdown urls and external
        
        lnk = str(url.toString())
            # Markdown
        if lnk.startswith('file:') and lnk.endswith('.md'):
            filename = str(url.toLocalFile())
            import plugins.mkdown as mkdown
            html = mkdown.generate(filename)
            
            burl = url
##            if burl != None:
##                if os.name =='nt':
##                    pfx="file:///"
##                else:
##                    pfx="file://"
##                burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(burl)).replace('\\','/')+'/')

            self.setText(html,burl)
            
        elif lnk.startswith('http') or lnk.startswith('www'):
            # External links
            import webbrowser
            webbrowser.open(lnk)
        else:
            self.load(url)