from PyQt4 import QtGui, QtCore, QtWebKit
import os, base64

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
        web_page.setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.setPage(web_page)
        self.baseurl=baseurl
        self.Events = Events() # Events
        
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
##        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
##            self.okedit = 0
        
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_V:
                clip = QtGui.QApplication.clipboard()
                handled = self.paste(clip.mimeData())

        if handled:
            event.accept()
            return
        
        else:
            QtWebKit.QWebView.keyPressEvent(self,event)
        QtGui.QApplication.processEvents()
##        self.okedit = 1
        self.editorTextChanged()
    
    def contextMenuEvent(self):
        pass
    
    def editorTextChanged(self):
        self.Events.editorChanged.emit(self)
        
    def getText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(CKEDITOR.instances.editor1.getData());")
        txt = str(self.editorJS.editorHtml.toUtf8()).decode('utf-8')
        return txt
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        CKEDITOR.instances.editor1.setData(txt)''')
    
    def insertText(self,txt):
        QtGui.QApplication.processEvents()
        self.editorJS.editorHtml = txt.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''CKEDITOR.instances.editor1.focus();
        var txt = pythonjs.html;
        CKEDITOR.instances.editor1.insertHtml(txt)''')
    
    def getSelectedText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(CKEDITOR.instances.editor1.getSelection().getSelectedText());")
        txt = str(self.editorJS.editorHtml.toUtf8()).decode('utf-8')
        return txt
    
    def find(self,txt,*args,**kargs):
        self.findText(txt,QtWebKit.QWebPage.FindWrapsAroundDocument)

    def dropEvent(self,event):
        handled = self.paste(event.mimeData(),drop=1)
        if not handled:
            if self.parent != None:
                self.parent.dropEvent(event)
        else:
            self.editorTextChanged()
    
    #---Paste Convenience Functions
    def paste(self,mimeData,drop=0):
        # View mimedata formats
##        for f in mimeData.formats():
##            print f,mimeData.hasFormat("XML Spreadsheet")
        handled = 0
        if mimeData.hasUrls():
            pth=unicode(mimeData.urls()[0].toString()).split('\n')[0]
            ext = pth.split('.')[-1].lower()
            if not pth.startswith('http'):
                try:
                    pth = os.path.relpath(str(mimeData.urls()[0].toLocalFile()),str(self.baseurl.toLocalFile())).replace('\\','/')
                except:
                    pass
            if ext in ['png','jpg','jpeg','bmp','gif','svg']:
                if drop or pth.startswith('http'):
                    self.insertText(u'<img src="'+pth+'">')
                else:
                    self.pasteImage(mimeData)
                handled=1
        
        elif mimeData.hasText():
            # Spreadsheet
            txt = str(mimeData.text().toUtf8()).decode('utf-8')
            if mimeData.hasFormat("XML Spreadsheet"):
                self.pasteTable(txt)
                handled=1
            else:
                # Ask to paste as table
                if len(txt.split('\n')[0].split('\t')) >1:
                    resp = QtGui.QMessageBox.question(None, 'Paste as Table','Do you want to paste the text as a table?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No,QtGui.QMessageBox.Cancel)
                    if resp == QtGui.QMessageBox.Yes:
                        self.pasteTable(txt)
                        handled=1
                    elif resp == QtGui.QMessageBox.Cancel:
                        handled = 1

        elif mimeData.hasImage():
            self.pasteImage(mimeData)
            handled=1

        return handled
        
    def pasteImage(self,mimeData):
        # Code to insert mimedata image as base64
        if mimeData.hasImage():
            if str(mimeData.imageData().typeName()) == 'QImage':
                # Clipboard Paste
                img = QtGui.QImage(mimeData.imageData())
                ba = QtCore.QByteArray()
                buffer = QtCore.QBuffer(ba)
                buffer.open(QtCore.QIODevice.WriteOnly)
                img.save(buffer,'PNG')

                data = unicode(ba.toBase64())
            
            else:
                data= unicode(mimeData.imageData().toByteArray().toBase64())

        else:
            pth = unicode(mimeData.urls()[0].path())
            if os.name =='nt': pth = pth[1:]
            f = open(pth,'rb')
            data = base64.b64encode(f.read())
            f.close()
        try:
            ext = unicode(mimeData.urls()[0].path()).split('.')[-1].lower()
        except:
            ext='png'

        html = u'<img src="data:image/'+ext+';base64, '+data+'"><br />'
        self.insertText(html)

        self.page().mainFrame().evaluateJavaScript("CKEDITOR.instances.editor1.focus()")
        self.setFocus(1)
    
    def pasteTable(self,text):
        tbltxt = '<table>'
        for tl in text.split('\n'):
            cols = tl.split('\t')
            if cols != ['']:
                tbltxt += '<tr>'
                
                for t in cols:
                    tbltxt += '<td>'+t+'</td>'
                tbltxt += '</tr>'
        
        tbltxt += '</table>'
        self.insertText(tbltxt)
        
#---Main
if __name__=='__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    if os.name =='nt':
        pfx="file:///"
    else:
        pfx="file://"
    burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/')
    editor=WebView(baseurl=burl)
    editor.resize(800,600)
    editor.show()
    app.exec_()