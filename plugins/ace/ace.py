from PyQt4 import QtGui, QtCore, QtWebKit
import os

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self,parent):
        QtCore.QObject.__init__(self)
        self.editorHtml = ''
        self.cliptxt = ''
        self.parent = parent
        self.lines = [0,0]

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
    
    @QtCore.pyqtSlot()
    def visibleLinesChanged(self):
        self.parent.visibleLinesChanged()
    
    @QtCore.pyqtSlot('QString')
    def getLines(self,ltxt):
        lines = str(ltxt).split(',')
        fline = float(lines[0])
        lline = float(lines[1])
        self.lines = [fline,lline]
    
    @QtCore.pyqtSlot('QStringList')
    def getPosition(self,pos):
        # row, column
        self.currentPosition = [int(str(pos[0])),int(str(pos[1]))]
    
    html = QtCore.pyqtProperty(str,fget=insertHtml)
    ctxt = QtCore.pyqtProperty(str,fget=clipHtml)
    
class Events(QtCore.QObject):
    editorChanged = QtCore.pyqtSignal(QtGui.QWidget)
    visibleLinesChanged = QtCore.pyqtSignal(QtGui.QWidget,tuple)
    
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
        self.Events = Events() # Events
        
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
        
        # Default settings
        self.settings = {
            'wrapBehaviours':1,
            'behaviours':1,
            'showPrintMargin':0,
            'fontSize':12,
            'theme':'twighlight',
            'newLineMode':'unix',
            'showWhitespace':'false',
            'fontFamily':'courier,freemono',
            'autocomplete':'true',
            'enableSnippets':'true',
        }
        
        # Load settings
        for ky in self.settings:
            if lang in self.parent.settings['prog_lang'] and ky in self.parent.settings['prog_lang'][lang]:
                self.settings[ky]=self.parent.settings['prog_lang'][lang][ky]
            elif ky in self.parent.settings['editors']['ace']:
                self.settings[ky]=self.parent.settings['editors']['ace'][ky]
        
        # Setup Editor
        js = "editor.getSession().on('change',function (e) {pythonjs.textChanged()});"
        js += "editor.getSession().on('changeScrollTop',function (e) {pythonjs.visibleLinesChanged()});"
        
        self.page().mainFrame().evaluateJavaScript(js)
        
        self.setup()
        
    def setup(self):
        js=''
        
        # Set Javascript settings
        js += 'editor.setTheme("ace/theme/'+self.settings['theme']+'");'
        js += 'editor.setWrapBehavioursEnabled('+['false','true'][self.settings['wrapBehaviours']]+');'
        js += 'editor.setBehavioursEnabled('+['false','true'][self.settings['behaviours']]+');'
        js += 'editor.setShowPrintMargin('+['false','true'][self.settings['showPrintMargin']]+');'
        js += 'editor.setFontSize('+str(self.settings['fontSize'])+');'
        js += 'editor.getSession().getDocument().setNewLineMode("'+str(self.settings['newLineMode'])+'");'
        js += 'editor.setShowInvisibles('+str(self.settings['showWhitespace'])+');'
        js += 'editor.focus();'
        js += 'editor.setOptions({fontFamily:"'+self.settings['fontFamily']+'"});'
        js += 'editor.setOptions({enableBasicAutocompletion: "'+self.settings['autocomplete']+'"});'
        js += 'editor.setOptions({enableSnippets: "'+self.settings['enableSnippets']+'"});'
        self.page().mainFrame().evaluateJavaScript(js)
        
        self.gotoLine(1)

    def editorTextChanged(self):
        self.Events.editorChanged.emit(self)

    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
            self.okedit = 0

        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_C:
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
                
        if not handled:
            QtWebKit.QWebView.keyPressEvent(self,event)
        QtGui.QApplication.processEvents()
        self.okedit = 1
        self.editorTextChanged()

    def contextMenuEvent(self,event):
        menu = QtGui.QMenu('ace menu',self.parent)
        
        # Edit Menu
        menuD=[['Cut','Ctrl+X'],['Copy','Ctrl+C'],['Paste','Ctrl+V'],['Select All','Ctrl+A']]
        for rw in menuD:
            if rw[0] in ['Select All']:
                menu.addSeparator()
            act = QtGui.QAction(rw[0],menu)
            act.setShortcut(QtGui.QKeySequence(rw[1],0))
            menu.addAction(act)
            

        menu.addSeparator()
        # Settings Menu
        smenu = QtGui.QMenu('Ace',menu)
##        tmenu = QtGui.QMenu('theme',smenu)
##        fld = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/src-noconflict/'
##        for f in sorted(os.listdir(fld)):
##            if f.startswith('theme'):
##                a=tmenu.addAction(QtGui.QIcon(),f[6:-3])
##                a.setData('theme')
##        smenu.addMenu(tmenu)
        menu.addMenu(smenu)
        
        # Extra Settings
        smenu.addAction('Jump To Matching')
        act = QtGui.QAction(QtGui.QIcon(),'Behaviours Enabled',menu)
        act.setCheckable(1)
        act.setChecked(self.settings['behaviours'])
        smenu.addAction(act)
        act = QtGui.QAction(QtGui.QIcon(),'Wrap Behaviour Enabled',menu)
        act.setCheckable(1)
        act.setChecked(self.settings['wrapBehaviours'])
        smenu.addAction(act)
        
        smenu.addSeparator()
        smenu.addAction('Settings')
        
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
            elif acttxt == 'Select All':
                self.selectAll()
            elif acttxt == 'Jump To Matching':
                self.jumpToMatching()
            elif acttxt == 'Behaviours Enabled':
                self.toggleBehaviours()
            elif acttxt == 'Wrap Behaviour Enabled':
                self.toggleWrapBehaviours()
            elif acttxt == 'Settings':
                self.page().mainFrame().evaluateJavaScript('editor.execCommand("showSettingsMenu")')
        
    def copy(self):
        js = "pythonjs.getHtml(editor.session.getTextRange(editor.getSelectionRange()));"
        self.page().mainFrame().evaluateJavaScript(js)
        
        clip = QtGui.QApplication.clipboard()
        clip.setText(self.editorJS.editorHtml)
    
    def cut(self):
        # Copy first
        self.copy()
        js = "editor.insert("");"
        self.page().mainFrame().evaluateJavaScript(js)
    
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
    
    def getSelectedText(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getHtml(editor.getSelectedText());")
        txt = str(self.editorJS.editorHtml.toUtf8()).decode('utf-8')
        return txt
    
    def selectAll(self):
        self.page().mainFrame().evaluateJavaScript('editor.selectAll();')
    
    def setText(self,txt):
        self.editorJS.editorHtml = txt#.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.html;
        editor.session.setValue(txt);
        editor.clearSelection();
        editor.moveCursorTo(0,0);
        editor.focus();''')

    def insertText(self,txt):
        self.editorJS.editorHtml = txt#.replace("'","''")
        self.page().mainFrame().evaluateJavaScript(
        '''var txt =  pythonjs.
        html;
        editor.insert(txt);''')

    def toggleWordWrap(self):
        self.wordwrapmode = not self.wordwrapmode
        ww = {0:'true',1:'false'}
        js = "editor.getSession().setUseWrapMode("+ww[self.wordwrapmode]+");"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def toggleComment(self):
        js = "editor.toggleCommentLines();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def toggleWhitespace(self):
        js = "editor.setShowInvisibles(! editor.getShowInvisibles());"
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
    
        self.editorJS.editorHtml = txt#.replace("'","''")
        js='''var txt =  pythonjs.html;
        editor.find(txt,{backwards:false,wrap:true,caseSensitive:'''+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def replace(self,ftxt,rtxt,re=0,cs=0,wo=0):
    
        js = "pythonjs.getHtml(editor.session.getTextRange(editor.getSelectionRange()));"
        self.page().mainFrame().evaluateJavaScript(js)
        
        js = ''
        
        ctxt = self.editorJS.editorHtml
        if unicode(ctxt).lower() == unicode(ftxt).lower():
            self.editorJS.editorHtml = rtxt
            js = "var rtxt =  pythonjs.html;editor.replace(rtxt);"
            self.page().mainFrame().evaluateJavaScript(js)
            QtGui.QApplication.processEvents()
        tre=tcs=two = 'false'
        if re: tre='true'
        if cs: tcs='true'
        if wo: two='true'
        
        self.editorJS.editorHtml = ftxt
        js='''var ftxt =  pythonjs.html;
        editor.find(ftxt,{backwards:false,wrap:true,caseSensitive:'''+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        self.page().mainFrame().evaluateJavaScript(js)

    def replaceAll(self,ftxt,rtxt,re=0,cs=0,wo=0):
        tre=tcs=two = 'false'
        if re: tre='true'
        if cs: tcs='true'
        if wo: two='true'
        self.editorJS.editorHtml = ftxt
        js='var ftxt =  pythonjs.html;'
        js += "editor.find(ftxt,{backwards:false,wrap:true,caseSensitive:"+tcs+",wholeWord:"+two+",regExp:"+tre+"});"
        self.page().mainFrame().evaluateJavaScript(js)
        self.editorJS.editorHtml = rtxt
        js='var rtxt =  pythonjs.html;'
        js += "editor.replaceAll(rtxt);"
        self.page().mainFrame().evaluateJavaScript(js)
        
    def gotoLine(self,line):
        js = "editor.gotoLine("+str(line+1)+");"
        self.page().mainFrame().evaluateJavaScript(js)
        QtGui.QApplication.processEvents()
        self.visibleLinesChanged()
    
    def jumpToMatching(self):
        js = "editor.jumpToMatching();"
        self.page().mainFrame().evaluateJavaScript(js)
    
    def toggleBehaviours(self):
        self.settings['behaviours'] = abs(self.settings['behaviours']-1)
        js = 'editor.setBehavioursEnabled('+['false','true'][self.settings['behaviours']]+');'
        self.page().mainFrame().evaluateJavaScript(js)

    def toggleWrapBehaviours(self):
        self.settings['wrapBehaviours'] = abs(self.settings['wrapBehaviours']-1)
        js = 'editor.setWrapBehavioursEnabled('+['false','true'][self.settings['wrapBehaviours']]+');'
        self.page().mainFrame().evaluateJavaScript(js)
    
    def dropEvent(self,event):
        self.parent.dropEvent(event)
    
    #---Visible Lines
    def getVisibleLines(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getLines(getVisibleLines());")
        line_first = self.editorJS.lines[0]
        line_last = self.editorJS.lines[1]
        return line_first,line_last
    
    def visibleLinesChanged(self):
        self.Events.visibleLinesChanged.emit(self,self.getVisibleLines())
    
    def getCursorPosition(self):
        self.page().mainFrame().evaluateJavaScript("pythonjs.getPosition(getCurrentPosition());")
        return self.editorJS.currentPosition
