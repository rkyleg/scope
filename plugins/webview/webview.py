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

    def find(self,txt,*args,**kargs):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)
    
    def load_link(self,url):
        # Custom load for handling markdown urls and external
        lnk = str(url.toString())
            # Markdown
        if lnk.startswith('file:') and lnk.endswith('.md'):
            filename = str(url.toLocalFile())
            import site_pkg.commonmark as commonmark
            
            html = commonmark.generate(filename,custom=1)
            burl = url
            self.setText(html,burl)
            
        elif lnk.startswith('http') or lnk.startswith('www'):
            # External links
            import webbrowser
            webbrowser.open(lnk)
        else:
            self.load(url)

    def load_help(self,url):
        lnk = str(url.toString())
        if lnk.startswith('http'):
            self.load_link(url)
        else:
            # Read filename html
            filename = str(url.toLocalFile())
            with open(os.path.abspath(filename),'r') as f:
                chtml = f.read()
            
            # Get Main html
            with open(self.parent.scopePath+'/docs/main.html','r') as f:
                mhtml = f.read()
            
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
                            
            ind_fld = pfx+self.parent.scopePath+'/docs/'
            mhtml = mhtml.replace('{{contents}}',chtml).replace('{{fld}}',ind_fld)
            self.setText(mhtml,url)

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