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
    def __init__(self,parent=None,baseurl=None):
        QtWebKit.QWebView.__init__(self,parent)
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)

        # Setup Javascript object
        self.editorJS = jsObject()
        self.page().mainFrame().addToJavaScriptWindowObject('pythonjs',self.editorJS)

        ckeditorPath='file:///'+os.path.abspath(os.path.dirname(__file__))+'/ckeditor.js'

        # Default Html
        html = """<!DOCTYPE html>
            <html>
              <head>
                <script type="text/javascript" src=\""""+ckeditorPath+"""\"></script>
              </head>
              <body>
                <form >
                  <textarea id=\"editor1\" name=\"editor1\"></textarea>
                </form>
                <script type="text/javascript">
                  CKEDITOR.replace( 'editor1');
                </script>
              </body>
            </html>
            """

        self.setHtml(html,baseurl)
        QtGui.QApplication.processEvents()
        ckEditorJS = """
            CKEDITOR.on('instanceReady', function(ev) {
            var editor = ev.editor;
            editor.execCommand('maximize');
            });
            """
        web_page.mainFrame().evaluateJavaScript(ckEditorJS)

    def getText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(CKEDITOR.instances.editor1.getData());")
        return self.editorJS.editorHtml
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        CKEDITOR.instances.editor1.setData(txt)''')
        
    
    def find(self,txt):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)