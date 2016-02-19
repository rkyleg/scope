from PyQt4 import QtGui, QtCore, QtWebKit, QtNetwork
import os, time, sys, json
from qt_webbrowser_ui import Ui_Form

class NetworkAccessManager(QtNetwork.QNetworkAccessManager):
    def __init__(self):
        QtNetwork.QNetworkAccessManager.__init__(self)
        self.connect(self,QtCore.SIGNAL("sslErrors (QNetworkReply *, const QList<QSslError> &)"), self.sslErrorHandler)

    def sslErrorHandler(self, reply, errorList): 
        # Ignore SSL errors
        reply.ignoreSslErrors() 
        print ("SSL error ignored")

class WebBrowser(QtGui.QWidget):
    def __init__(self,parent=None,**kargs):
        QtGui.QWidget.__init__(self,parent)
        curdir = os.path.abspath('.')
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        os.chdir(curdir)
        self.parent = parent
        
        # Add Webview
        self.ui.webView = QtWebKit.QWebView()
        self.ui.split_insp.addWidget(self.ui.webView)
        
        # Setup Settings
        if 'settings' in kargs and kargs['settings'] != {}:
            settings = kargs['settings']
        else:
            # Load Default Settings
            with open('settings.json') as f:
                settings = json.load(f)
        
        # update settings from kargs
        for k in kargs:
            if k in settings:
                settings[k]=kargs[k]

##        self.ui.webView.keyPressEvent = new.instancemethod(self.webview_keyPress,self.ui.webView,self.ui.webView.__class__)
        self.ui.webView.keyPressEvent = self.webview_keyPress
        
        # Address Bar (and signals)
        self.ui.webView.urlChanged.connect(self.update_url)
        self.ui.b_go.clicked.connect(self.go)
        self.ui.webView.loadFinished.connect(self.load_finished)
        self.ui.webView.loadStarted.connect(self.load_started)
        self.ui.webView.loadProgress.connect(self.ui.pb_load.setValue)
        
        self.ui.b_back.clicked.connect(self.ui.webView.back)
        self.ui.b_forward.clicked.connect(self.ui.webView.forward)
        self.ui.b_stop.clicked.connect(self.ui.webView.stop)
        
        self.ui.webView.iconChanged.connect(self.icon_changed)
        self.ui.webView.titleChanged.connect(self.title_changed)
        
        self.ui.le_find.returnPressed.connect(self.find_text)
        
        # Proxy  (Don't use for internal cat sites
        if settings['proxy_path'] != '':
            self.setExternalProxy(settings['proxy_path'],settings['proxy_port'])
        
        if settings['inspector']:
            self.setupInspector()
            self.ui.split_insp.addWidget(self.webInspector)
        
        # Set UserAgent - this makes things not work
        if settings['userAgent'] != '':
            self.user_agent = settings['userAgent'] 
##            self.ui.webView.page().userAgentForUrl = new.instancemethod(self.user_agent_for_url,self.ui.webView.page(),self.ui.webView.page().__class__)
            self.ui.webView.page().userAgentForUrl = self.user_agent_for_url
        
        # Allow flash and java plugins
        if settings['pluginsEnabled']:
            self.ui.webView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
            self.ui.webView.settings().setAttribute(QtWebKit.QWebSettings.JavaEnabled,True)
        if settings['javascriptEnabled']:
            self.ui.webView.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
            self.ui.webView.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows,True)
        self.ui.webView.settings().setIconDatabasePath(os.path.abspath(os.path.expanduser('~')))
        
        if settings['networkManager']:
            self.ui.webView.page().setNetworkAccessManager(NetworkAccessManager())
        
##        if settings['javascriptEnabled']:
##            # Setup Javascript console
##            self.ui.webView.page().javaScriptConsoleMessage = new.instancemethod(self.javascript_console_msg,self.ui.webView.page(),self.ui.webView.page().__class__)
##            self.ui.webView.page().javaScriptConsoleMessage = self.javascript_console_msg
        
        # Override Create new Window
        if settings['createNewWindow']:
            self.ui.webView.hoverLink = ''
##            self.ui.webView.createWindow = new.instancemethod(self.new_window,self.ui.webView,self.ui.webView.__class__)
            self.ui.webView.createWindow = self.new_window
        
        # Setup Statusbar Hover
        if settings['statusbar']:
            QtCore.QObject.connect(self.ui.webView.page(),QtCore.SIGNAL("linkHovered(QString,QString,QString)"),self.link_hover)
        else:
            self.ui.l_status.hide()
        
        self.ui.b_icon.hide()
        
        if 'url' in kargs:
            self.link_clicked(QtCore.QUrl(kargs['url']))
        
        elif settings['loadDefaultHome']:
            self.load_home()
        
    def go(self):
        lnk = self.ui.le_address.text()
        if lnk !='':
            if lnk[:4] =='file' or lnk[0]=='/' or lnk[1]==':':
                if os.name =='nt':
                    url = QtCore.QUrl.fromLocalFile(lnk.replace('file:///',''))
                else:
                    url = QtCore.QUrl.fromLocalFile(lnk.replace('file://',''))
            elif lnk[:4] != 'http' and lnk[:4]!='file':
                lnk = 'http://'+lnk
                self.ui.le_address.setText(lnk)
                url = QtCore.QUrl(lnk)
            else:
                url = QtCore.QUrl(lnk)

            self.ui.webView.load(url)
##            self.ui.webView.setUrl(url)

    def link_clicked(self,url):
        self.ui.le_address.setText(url.toString())
        self.ui.webView.load(url)

    def link_hover(self,lnk,title,textcontent):
        self.ui.l_status.setText(lnk)
        if not lnk.isEmpty():
            self.hoverLink = lnk

    def find_text(self):
        self.ui.webView.findText(self.ui.le_find.text(),QtWebKit.QWebPage.FindWrapsAroundDocument)

    def update_url(self,url):
        if not url.isEmpty():
            self.ui.le_address.setText(url.toString())
            self.hoverLink =''
    
    def load_started(self):
        #self.ui.pb_load.show()
        pass
    
    def load_finished(self,ok):
        if not ok:
            self.ui.webView.setHtml('Page did not load')
        self.ui.pb_load.setValue(0)
    
    def title_changed(self,title):
        if unicode(title) != '':
            self.setWindowTitle(unicode(title))
    
    def icon_changed(self):
##        print 'icon change'
        self.setWindowIcon(self.ui.webView.icon())
        self.ui.b_icon.setIcon(self.ui.webView.icon())
    
    def sslErrorHandler(self, reply, errorList): 
        # Ignore SSL errors
        reply.ignoreSslErrors() 
        print ("SSL error ignored") 
    
    def open(self,link):
        url = QtCore.QUrl(link)
        self.ui.le_address.setText(url.toString())
        self.ui.webView.load(url)
    
    def setExternalProxy(self,proxy_path='',port=8080):
        QtNetwork.QNetworkProxy.setApplicationProxy(QtNetwork.QNetworkProxy(QtNetwork.QNetworkProxy.HttpProxy, proxy_path, port))
    
    def user_agent_for_url(self, url,something):
##        return "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0"    
##        return "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
        return self.user_agent
    
##    def javascript_console_msg(self,webpage, message, lineNumber, sourceID):
##        print 'javascript error'
##        self.ui.l_status.setText('JS ERROR: %s line %d: %s' % (sourceID, lineNumber, message))
##
    def new_window(self,windowtype):
        if windowtype == 0 and self.hoverLink != '':
            nwdg = WebBrowser(url=self.hoverLink)
            nwdg.show()

    #---Webview Setup
    def setupInspector(self):
        page = self.ui.webView.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKit.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtGui.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F12)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())

    def webview_keyPress(self,event):
        handled = False
        if event.modifiers() & QtCore.Qt.ControlModifier:       # Ctrl
            if event.key() == QtCore.Qt.Key_F:                  # F
                # Find
                self.ui.le_find.setFocus()
                self.ui.le_find.selectAll()
                handled = True
            elif event.key() == QtCore.Qt.Key_Plus or event.key() == QtCore.Qt.Key_Equal:
                # Zoom In
                z=self.ui.webView.zoomFactor()
                if round(z,1)==1.0:z=1.0
                self.ui.webView.setZoomFactor(z*1.1)
                handled = True
            elif event.key() == QtCore.Qt.Key_Minus:
                # Zoom Out
                z=self.ui.webView.zoomFactor()
                if round(z,1)==1.0:z=1.0
                if round(z,1)==1.0:z=1.0
                self.ui.webView.setZoomFactor(z*0.9)
                handled = True  
            elif event.key() == QtCore.Qt.Key_0:
                # Clear
                self.ui.webView.setZoomFactor(1.0)
                handled = True  
            
        if handled:
            event.accept()
        else:
            QtWebKit.QWebView.keyPressEvent(self.ui.webView,event)

    def load_home(self):
        # Generate HTML
        html = '''
            <style>
                body{background:rgb(70,70,70);}
                input{
                    background:rgb(50,50,50);
                    color:white;
                    border:0px;
                    border-radius:3px;
                    outline:none;
                    font-size:1.5em;
                    text-align: center;
                }
                input::-webkit-input-placeholder {
                   text-align: center;
                }
            </style>
            <br><br>
            <form method="get" action="https://www.google.com/search" style="text-align:center;">
                <input name="q" type="text" placeholder="search Google">
            </form>
        '''
        self.ui.webView.setHtml(html)

#---Main
if __name__ == '__main__':

    # Start app
    qtApp = QtGui.QApplication(sys.argv)
    web_view = WebBrowser(inspector=1,progressbar=1,addressbar=1)
    web_view.show()
    web_view.load_home()
##    web_view.ui.webView.setHtml(html)
    qtApp.exec_()