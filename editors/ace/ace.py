from PyQt4 import QtGui, QtCore, QtWebKit
import os

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self,parent):
        QtCore.QObject.__init__(self)
        self.editorHtml = ''
        self.cliptxt = ''
        self.parent = parent

    @QtCore.pyqtSlot('QString')
    def getHtml(self,text):
        self.editorHtml=text

    def insertHtml(self):
        return self.editorHtml
    
    def clipHtml(self):
        return self.cliptxt

    @QtCore.pyqtSlot()
    def textChanged(self):
        self.parent.editorTextChanged()
    
    html = QtCore.pyqtProperty(str,fget=insertHtml)
    ctxt = QtCore.pyqtProperty(str,fget=clipHtml)

class Events(QtCore.QObject):
    editorChanged = QtCore.pyqtSignal(QtGui.QWidget)
    
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
        self.parent = parent
        self.evnt = Events() # Events
        
        # Initial Variables
        self.wordwrapmode = 1
        
##        fnt=QtGui.QFont()
##        fnt.setFamily('FreeMono')
##        self.setFont(fnt)
        
        # Setup Web Page
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
        QtGui.QApplication.processEvents()
        
        # Setup Javascript object
        self.editorJS = jsObject(parent=self)
        self.page().mainFrame().addToJavaScriptWindowObject('pythonjs',self.editorJS)
        QtGui.QApplication.processEvents()
        
        # Setup Editor
##        js = '''editor.getSession().setMode("ace/mode/'''+lang+'");'
        js = "editor.getSession().on('change',function (e) {pythonjs.textChanged()});"
        if 'theme' in self.parent.settings.editors['ace']:
            js += 'editor.setTheme("ace/theme/'+self.parent.settings.editors['ace']['theme']+'");'
        self.wrapBehaviours = 1
        if 'wrapBehavioursEnabled' in self.parent.settings.editors['ace']:
            js += 'editor.setWrapBehavioursEnabled('+['false','true'][self.parent.settings.editors['ace']['wrapBehavioursEnabled']]+');'
            self.wrapBehaviours = self.parent.settings.editors['ace']['wrapBehavioursEnabled']
        self.behaviours = 1
        if 'behavioursEnabled' in self.parent.settings.editors['ace']:
            js += 'editor.setBehavioursEnabled('+['false','true'][self.parent.settings.editors['ace']['behavioursEnabled']]+');'
            self.behaviours = self.parent.settings.editors['ace']['behavioursEnabled']
        
        self.page().mainFrame().evaluateJavaScript(js)
        
        # Additional Settings
        if 'settingJS' in self.parent.settings.editors['ace']:
            jstxt = self.parent.settings.editors['ace']['settingJS']
            js = ''
            for jt in jstxt.split('\n'):
                txt = jt.strip()
                if not txt.endswith(';'): txt = txt=';'
                js += jstxt
            
            if js != '':
                self.page().mainFrame().evaluateJavaScript(js)
        
        
        self.gotoLine(1)

    def editorTextChanged(self):
        self.evnt.editorChanged.emit(self)

    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
            self.okedit = 0

        if event.modifiers() & QtCore.Qt.ControlModifier:            if event.key() == QtCore.Qt.Key_C:
                self.copy()
                handled = 1
            elif event.key() == QtCore.Qt.Key_V:
                self.paste()
                handled = 1
            elif event.key() == QtCore.Qt.Key_X:
                self.copy()
                self.cut()
                handled = 1
            elif event.key() == QtCore.Qt.Key_D:
                self.copyLinesDown()
                handled = 1
            elif event.key() == QtCore.Qt.Key_Delete:
                self.removeLines()
                handled = 1                
        if not handled:            QtWebKit.QWebView.keyPressEvent(self,event)
        QtGui.QApplication.processEvents()
        self.okedit = 1
        self.editorTextChanged()

    def contextMenuEvent(self,event):
        menu = QtGui.QMenu('ace menu')
        # Edit Menu
##        menu = QtGui.QMenu('edit',menu)
        menu.addAction(QtGui.QIcon(),'Copy')
        menu.addAction(QtGui.QIcon(),'Cut')
        menu.addAction(QtGui.QIcon(),'Paste')
##        menu.addMenu(emenu)
        menu.addSeparator()
        # Settings Menu
        smenu = QtGui.QMenu('settings',menu)
        tmenu = QtGui.QMenu('theme',smenu)
        fld = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/src-noconflict/'
        for f in sorted(os.listdir(fld)):
            if f.startswith('theme'):
                a=tmenu.addAction(QtGui.QIcon(),f[6:-3])
                a.setData('theme')
        smenu.addMenu(tmenu)
        menu.addMenu(smenu)
        # Extra Settings
        
        smenu.addAction('Jump To Matching')
        act = QtGui.QAction(QtGui.QIcon(),'Behaviours Enabled',menu)
        act.setCheckable(1)
        act.setChecked(self.behaviours)
        smenu.addAction(act)
        act = QtGui.QAction(QtGui.QIcon(),'Wrap Behaviour Enabled',menu)
        act.setCheckable(1)
        act.setChecked(self.wrapBehaviours)
        smenu.addAction(act)
        
        for act in menu.actions():  # Set Icon to visible
            act.setIconVisibleInMenu(1)
        
        # Launch Menu
        act = menu.exec_(self.cursor().pos())
        if act != None:
            acttxt = str(act.text())
            actdta = str(act.data().toString())
            if actdta == 'theme':
                js = 'editor.setTheme("ace/theme/'+acttxt+'");'
                self.page().mainFrame().evaluateJavaScript(js)
            elif acttxt == 'Copy':
                self.copy()
            elif acttxt == 'Cut':
                self.cut()
            elif acttxt == 'Paste':
                self.paste()
            elif acttxt == 'Jump To Matching':
                self.jumpToMatching()
            elif acttxt == 'Behaviours Enabled':
                self.toggleBehaviours()
            elif acttxt == 'Wrap Behaviour Enabled':
                self.toggleWrapBehaviours()
        
    def copy(self):
        js = "pythonjs.getHtml(editor.session.getTextRange(editor.getSelectionRange()));"
        self.page().mainFrame().evaluateJavaScript(js)
        
        clip = QtGui.QApplication.clipboard()
        clip.setText(self.editorJS.editorHtml)
    
    def cut(self):
        js = "editor.insert("");"
        self.page().mainFrame().evaluateJavaScript(js)
        print 'cut'
    
    def paste(self):
        clip = QtGui.QApplication.clipboard()
        txt =str(clip.text().toUtf8()).decode('utf-8')
        if txt != '':
            self.editorJS.cliptxt = txt#.replace("'","''")
            self.page().mainFrame().evaluateJavaScript(
            '''var txt =  pythonjs.ctxt;
            editor.insert(txt);''')

    def getText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(editor.getValue());")
        txt = str(self.editorJS.editorHtml.toUtf8()).decode('utf-8')
        return txt
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt#.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        editor.setValue(txt);
        editor.clearSelection();
        editor.moveCursorTo(0,0);
        editor.focus();''')
    
    def toggleWordWrap(self):
        self.wordwrapmode = not self.wordwrapmode
        ww = {0:'true',1:'false'}
        js = "editor.getSession().setUseWrapMode("+ww[self.wordwrapmode]+");"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def toggleComment(self):
        js = "editor.toggleCommentLines();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def indent(self):
        js = "editor.indent();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def unindent(self):
        js = "editor.blockOutdent();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def copyLinesDown(self):
        js = "editor.copyLinesDown();"
        self.page().mainFrame().evaluateJavaScript(js)
        
    def removeLines(self):
        js = "editor.removeLines();"
        self.page().mainFrame().evaluateJavaScript(js)
        
    def find(self,txt,re=0,cs=0,wo=0):
    
        tre=tcs=two = 'false'
        if re: tre='true'
        if cs: tcs='true'
        if wo: two='true'
    
        js = "editor.find('"+txt+"',{backwards:false,wrap:true,caseSensitive:"+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def replace(self,ftxt,rtxt,re=0,cs=0,wo=0):
    
        js = "pythonjs.getHtml(editor.session.getTextRange(editor.getSelectionRange()));"
        self.page().mainFrame().evaluateJavaScript(js)
        
        js = ''
        
        ctxt = self.editorJS.editorHtml
        if unicode(ctxt).lower() == unicode(ftxt).lower():
            js = "editor.replace('"+rtxt+"');"
            self.page().mainFrame().evaluateJavaScript(js)
            QtGui.QApplication.processEvents()
        tre=tcs=two = 'false'
        if re: tre='true'
        if cs: tcs='true'
        if wo: two='true'
    
        js = "editor.find('"+ftxt+"',{backwards:false,wrap:true,caseSensitive:"+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        
        self.page().mainFrame().evaluateJavaScript(js)

    def replaceAll(self,ftxt,rtxt,re=0,cs=0,wo=0):
        tre=tcs=two = 'false'
        if re: tre='true'
        if cs: tcs='true'
        if wo: two='true'
    
        js = "editor.find('"+ftxt+"',{backwards:false,wrap:true,caseSensitive:"+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        js += "editor.replaceAll('"+rtxt+"');"
        self.page().mainFrame().evaluateJavaScript(js)
        
    def gotoLine(self,line):
        js = "editor.gotoLine("+str(line+1)+");"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def jumpToMatching(self):
        js = "editor.jumpToMatching();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def toggleBehaviours(self):
        self.behaviours = abs(self.behaviours-1)
        js = 'editor.setBehavioursEnabled('+['false','true'][self.behaviours]+');'
        print self.behaviours,js
        self.page().mainFrame().evaluateJavaScript(js)

    def toggleWrapBehaviours(self):
        self.wrapBehaviours = abs(self.wrapBehaviours-1)
        js = 'editor.setWrapBehavioursEnabled('+['false','true'][self.wrapBehaviours]+');'
        self.page().mainFrame().evaluateJavaScript(js)
    
    def dropEvent(self,event):
        # Ignore drop event
        pass
        