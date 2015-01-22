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
##        print('JS ERROR: %s line %d: %s' % (source, line, msg))

class WebView(QtWebKit.QWebView):
    def __init__(self,parent=None,baseurl=None):
        QtWebKit.QWebView.__init__(self,parent)
        self.parent = parent
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)
        self.baseurl = baseurl
        
        self.settings().setObjectCacheCapacities(0,0,0) # Make sure images are reloaded
    
    def setText(self,txt,baseurl=None):
        if self.baseurl != None:
            baseurl = self.baseurl
        if baseurl == None:
            baseurl=QtCore.QUrl()
        
        self.setHtml(txt,baseurl)
        ##self.setHtml(txt)

    def find(self,txt,*args,**kargs):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)
    
    def load2(self,url):
        # Custom load for handling markdown urls and external
        
        lnk = str(url.toString())
            # Markdown
        if lnk.startswith('file:') and lnk.endswith('.md'):
            filename = str(url.toLocalFile())
            import plugins.mkdown as mkdown
            html = mkdown.generate(filename,custom=1)
            
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

    def dropEvent(self,event):
        self.parent.dropEvent(event)

    def setupInspector(self):
        page = self.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKit.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtGui.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F12)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())

    def dropEvent(self,event):
        self.parent.dropEvent(event)