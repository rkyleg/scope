from PyQt4 import QtGui, QtCore, QtWebKit
import os

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.editorHtml = ''

    @QtCore.pyqtSlot(str)
    def getHtml(self,text):
        self.editorHtml=text

    def insertHtml(self):
        return self.editorHtml

    html = QtCore.pyqtProperty(str,fget=insertHtml)

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
    def __init__(self,parent=None,lang=None):
        QtWebKit.QWebView.__init__(self,parent)
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)
        
        if os.name =='nt':
            pfx="file:///"
        else:
            pfx="file://"
##        url = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/'))
        url = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/editor.html')

        self.setUrl(url)
        QtGui.QApplication.processEvents()
        
        f = open(os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/editor.html','r')
        html = f.read()
        f.close()
        html = html.replace('$mode',lang)
        self.setHtml(html,url)
        
        # Setup Javascript object
        self.editorJS = jsObject()
        self.page().mainFrame().addToJavaScriptWindowObject('pythonjs',self.editorJS)
        
        # Setup Editor
##        js = '''editor.getSession().setMode("ace/mode/'''+lang+'");'
##        self.page().mainFrame().evaluateJavaScript(js)


    def getText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(editor.getValue());")
        return self.editorJS.editorHtml
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        editor.setValue(txt);''')
        
    
    def find(self,txt):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)