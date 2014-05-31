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

class Events(QtCore.QObject):
    editorChanged = QtCore.pyqtSignal(QtGui.QWidget)
        
class WebView(QtWebKit.QWebView):
    def __init__(self,parent=None,baseurl=None):
        QtWebKit.QWebView.__init__(self,parent)
        self.parent = parent
        web_page = WebPage(self)
        #web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)

        self.evnt = Events() # Events
        
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

    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
            self.okedit = 0
                
        if not handled:
            QtWebKit.QWebView.keyPressEvent(self,event)
        QtGui.QApplication.processEvents()
        self.okedit = 1
        self.editorTextChanged()
        
    def editorTextChanged(self):
        self.evnt.editorChanged.emit(self)
        
    def getText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(CKEDITOR.instances.editor1.getData());")
        txt = str(self.editorJS.editorHtml.toUtf8()).decode('utf-8')
        return txt
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        CKEDITOR.instances.editor1.setData(txt)''')
        
    def find(self,txt,*args,**kargs):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)

    def dropEvent(self,event):
        self.parent.dropEvent(event)