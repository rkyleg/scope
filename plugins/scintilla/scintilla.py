from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import Qsci
from PyQt4 import QtGui, QtCore, Qsci
from .scintilla_ui import Ui_Form
import os,sys, time
from scintilla_style import styleD # scintilla style

##lexD = {'Python':Qsci.QsciLexerPython(),
##    'JavaScript':Qsci.QsciLexerJavaScript(),
##    'HTML':Qsci.QsciLexerHTML(),
##    'CSS':Qsci.QsciLexerCSS(),
##    'XML':Qsci.QsciLexerXML(),
##    'UI':Qsci.QsciLexerXML(),
##    'YAML':Qsci.QsciLexerYAML(),
##    'Bash':Qsci.QsciLexerBash(),
##    'Batch':Qsci.QsciLexerBatch(),
##    'SQL':Qsci.QsciLexerSQL(),
##    }

commentD = {
    'python':'##',
    'javascript':'//',
    'yaml':'##',
    'perl':'##',
    'ruby':'##',
    'php':'#',
    'r':'##',
    'cpp':'//',
    'csharp':'//',
    'java':'//',
    'd':'//',
}

##def addEditor(parent,lang,filename):
##    lex = None
##    if lang in lexD:
##        lex = lexD[lang]
##    editor = Sci(parent,lex)
##    
##    return editor

class Events(QtCore.QObject):
    editorChanged = QtCore.pyqtSignal(QtGui.QWidget)
    visibleLinesChanged = QtCore.pyqtSignal(QtGui.QWidget,tuple)
##    editingFinished = QtCore.pyqtSignal(QtGui.QWidget)

class Sci(QtGui.QWidget):
    def __init__(self,parent,lex,lang=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.te_sci.ARROW_MARKER_NUM = 8
        self.ui.te_sci.setUtf8(True)
        self.ide = parent
        self.okedit = 1
        
        self.lex = lex
        
        # Events
        self.Events = Events()
        self.ui.te_sci.textChanged.connect(self.editorTextChanged)
##        self.ui.te_sci.linesChanged.connect(self.visibleLinesChanged)
        self.ui.te_sci.verticalScrollBar().valueChanged.connect(self.visibleLinesChanged)

        self.ui.te_sci.keyPressEvent = self.keyPressEvent
        self.ui.te_sci.dropEvent = self.dropEvent
        
        # Remove Green border
        self.ui.te_sci.setFrameShape(QtGui.QFrame.NoFrame)
        
        # Default settings
        self.settings = {
##            'wrapBehaviours':1,
##            'behaviours':1,
##            'showPrintMargin':0,
            'fontFamily':'Courier',
##            'fontFamily':'Hack',
##            'fontFamily':'Ubuntu',
            'fontSize':10,
            'theme':'dark',
##            'newLineMode':'unix',
            'showWhitespace':0,
        }
        
        # Load settings
        for ky in self.settings:
            if lang in self.ide.settings['prog_lang'] and ky in self.ide.settings['prog_lang'][lang]:
                self.settings[ky]=self.ide.settings['prog_lang'][lang][ky]
            elif ky in self.ide.settings['editors']['scintilla']:
                self.settings[ky]=self.ide.settings['editors']['scintilla'][ky]
                
        self.setup()
        
    def setup(self):
        # Font
        font = QFont()
##        font.setFamily('Ubuntu Mono')
##        font.setFamily('DejaVu Sans Mono')

        font.setFamily(self.settings['fontFamily'])
        font.setFixedPitch(True)
        
        xfont = self.settings['fontSize']
        
        font.setPointSize(int(xfont))
        self.ui.te_sci.setFont(font)
        self.ui.te_sci.setMarginsFont(font)

        # Margin 0 for line numbers
        fontmetrics = QFontMetrics(font)
##        self.ui.te_sci.setMarginsFont(font)
        self.ui.te_sci.setMarginWidth(0, fontmetrics.width("00000"))
        self.ui.te_sci.setMarginWidth(1, 0)
        self.ui.te_sci.setMarginLineNumbers(0, True)
        self.ui.te_sci.setMarginsBackgroundColor(QColor("#dddddd"))

        # Default to autocomplete
        self.autocompletemode=0
        self.toggleAutoComplete()
        
        self.ui.te_sci.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        
        self.ui.te_sci.setCallTipsStyle(Qsci.QsciScintilla.CallTipsContext)
        self.ui.te_sci.setAnnotationDisplay(Qsci.QsciScintilla.AnnotationBoxed )
        
        # Indentation
        self.ui.te_sci.setIndentationsUseTabs(0)
        self.ui.te_sci.setAutoIndent(1)
        self.ui.te_sci.setIndentationGuides(1)
        self.ui.te_sci.setBackspaceUnindents(1)

        self.ui.te_sci.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)
        self.ui.te_sci.setTabWidth(4)
        
##        self.ui.te_sci.setWrapIndentMode(Qsci.QsciScintilla.WrapIndentIndented)

        # Current line visible with special background color
        self.ui.te_sci.setCaretLineVisible(True)
        self.ui.te_sci.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.ui.te_sci.setEolVisibility(int(self.settings['showWhitespace']))
        
        self.wordwrapmode = 0
        
        if self.lex != None:
            self.lex.setDefaultFont(font)
            self.ui.te_sci.setLexer(self.lex)
        if sys.version_info.major==3:
            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, bytes('Courier','utf-8'))
        else:
##            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, self.settings['fontFamily'])
        
        self.ui.te_sci.setCaretLineBackgroundColor(QColor(105,184,221,30))
        
        # Customize Python lexer
        if self.ide.settings['editors']['scintilla']['theme']=='dark' and type(self.lex) == type(Qsci.QsciLexerPython()):
##            self.ui.te_sci.setCaretLineBackgroundColor(QColor(105,184,221,30))
            self.ui.te_sci.setCaretForegroundColor(QColor(255,255,255))
            
            shade=30
            self.lex.setDefaultPaper(QColor(shade,shade,shade))
            self.lex.setPaper(QColor(shade,shade,shade),self.lex.Default)
            self.ui.te_sci.setColor(QColor(255,255,255))
            
            self.ui.te_sci.setMarginsBackgroundColor(QColor(60,60,60))
            self.ui.te_sci.setWhitespaceBackgroundColor(QColor(80,80,80))
            self.ui.te_sci.setFoldMarginColors(QColor(200,200,200),QColor(90,90,90))
##            self.ui.te_sci.setPaper(QColor(80,80,80))
            self.ui.te_sci.setMarginsForegroundColor(QColor(200,200,200))
##            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETBACK,Qsci.QsciScintilla.STYLE_DEFAULT,QColor(150,150,150))
            
            self.ui.te_sci.setMatchedBraceBackgroundColor(QColor(shade,shade,shade))
            self.ui.te_sci.setMatchedBraceForegroundColor(QColor(170,0,255))
            self.ui.te_sci.setUnmatchedBraceBackgroundColor(QColor(shade,shade,shade))
            
            # Set defaults for all:
            style_obj = set(styleD.keys()).intersection(dir(self.lex))
            style_obj.remove('Default')
            style_obj = set(['Default']).union(sorted(style_obj))
            
            for c in sorted(style_obj,reverse=1):
                clr = styleD[c]
                if clr == '':
##                    clr = '255,255,255'
                    clr = styleD['Default']
##                print c,clr
                try:
                    exec('self.lex.setPaper(QColor(30,30,30),self.lex.'+c+')')
                    exec('self.lex.setColor(QColor('+clr+'),self.lex.'+c+')')
                except:
                    print('no keyword',c)
    
    def keyPressEvent(self,event):
        ky = event.key()
        handled = 0
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
            self.okedit = 0
        
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Space:
                self.ui.te_sci.autoCompleteFromAll()
                handled = 1
            elif event.key() == QtCore.Qt.Key_Delete:
                # Delete line
                self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_LINEDELETE)
                handled = 1
        elif event.modifiers() & QtCore.Qt.AltModifier:
            if event.key() == QtCore.Qt.Key_Down:
                # Move Line Down
                self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_MOVESELECTEDLINESDOWN)
            if event.key() == QtCore.Qt.Key_Up:
                # Move Line Down
                self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_MOVESELECTEDLINESUP)
        
        if not handled:
            Qsci.QsciScintilla.keyPressEvent(self.ui.te_sci,event)
            QtGui.QApplication.processEvents()
    ##        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace]:
    ##            self.editingFinished()
            self.okedit = 1
            self.editorTextChanged()
    
    def setText(self,txt):
        self.ui.te_sci.setText(txt)
##        if self.settings['newLineMode']=='unix':
##            self.ui.te_sci.convertEols(Qsci.QsciScintilla.EolUnix)
    
##    def updateText(self,txt):
##        # Update, but keep current undo
##        self.ui.te_sci.selectAll(select=1)
##        self.ui.te_sci.replaceSelectedText(txt)
    
    def getText(self):
##        if self.settings['newLineMode']=='unix':
##            self.ui.te_sci.convertEols(Qsci.QsciScintilla.EolUnix)
        txt = str(self.ui.te_sci.text().toUtf8()).decode('utf-8')
        return txt
    
    def getSelectedText(self):
        return self.ui.te_sci.selectedText()
    
    def selectAll(self):
        self.ui.te_sci.selectAll()
    
    def insertText(self,txt):
##        self.ui.te_sci.removeSelectedText()
##        self.ui.te_sci.insert(txt)
        self.ui.te_sci.replaceSelectedText(txt)

    def find(self,txt,re=0,cs=0,wo=0):
        return self.ui.te_sci.findFirst(txt,re,cs,wo,1)
    
    def replace(self,ftxt,rtxt,re=0,cs=0,wo=0):
        stxt = str(self.ui.te_sci.selectedText())
        if stxt.lower() == ftxt.lower():
            self.ui.te_sci.replace(rtxt)
        self.ui.te_sci.findFirst(ftxt,re,cs,wo,1)
    
    def replaceAll(self,ftxt,rtxt,re=0,cs=0,wo=0):
        cnt = 0
        r = self.ui.te_sci.findFirst(ftxt,re,cs,wo,0,1,0,0)
        while r:
            cnt +=1
            self.ui.te_sci.replace(rtxt)
            QtGui.QApplication.processEvents()
            r = self.ui.te_sci.findFirst(ftxt,re,cs,wo,0)
        QtGui.QMessageBox.information(self,'Replace All',str(cnt)+' occurrences replaced')
    
    def gotoLine(self,line):
        self.ui.te_sci.setCursorPosition(self.ui.te_sci.lines(),0)  # Send to bottom so cursor is at top of page
        self.ui.te_sci.setCursorPosition(line,0)
        #self.ui.te_sci.setSelection(line,0,line,-1)
        self.ui.te_sci.setFocus()
    
    def editorTextChanged(self):
        if self.okedit:
            self.Events.editorChanged.emit(self)
    
    def getVisibleLines(self):
        line_first = self.ui.te_sci.firstVisibleLine()
        line_last = line_first+self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_LINESONSCREEN)
        return line_first,line_last
    
    def visibleLinesChanged(self):
        self.Events.visibleLinesChanged.emit(self,self.getVisibleLines())
    
##    def editingFinished(self):
##        self.Events.editingFinished.emit(self)
    
    def getCursorPosition(self):
        return self.ui.te_sci.getCursorPosition()
    
    def toggleComment(self):
        lang = self.ide.currentEditor().lang
        if lang in commentD:
            if self.ui.te_sci.getSelection()[0] != -1:
                start = self.ui.te_sci.getSelection()[0]
                stop = self.ui.te_sci.getSelection()[2]
                lines = range(start,stop+1)
                if start == stop: lines = [start]
            else:
                start = stop = self.ui.te_sci.getCursorPosition()[0]
                lines = [start]
            
            # First line text - check if adding comment or removing
            txt1 = str(self.ui.te_sci.text(start)).lstrip()

            self.ui.te_sci.setSelection(start,0,stop,self.ui.te_sci.lineLength(stop)-1)
            ntxt = ''
            self.okedit=0
            for i in lines:
                if txt1.startswith(commentD[lang]): # Remove Comment
                    if str(self.ui.te_sci.text(i)).startswith(commentD[lang]):
                        ntxt += self.ui.te_sci.text(i)[len(commentD[lang]):]
                    else:
                        ntxt += self.ui.te_sci.text(i)
                else: # Add Comment
                    ntxt += commentD[lang]+self.ui.te_sci.text(i)
            self.okedit=1

            self.ui.te_sci.replaceSelectedText(ntxt[:-1])
            self.ui.te_sci.setSelection(start,0,stop,self.ui.te_sci.lineLength(stop)-1)

##            self.ui.te_sci.setSelection(start,0,stop,self.ui.te_sci.lineLength(stop))

    def indent(self):
        if self.ui.te_sci.getSelection()[0] != -1:
            start = self.ui.te_sci.getSelection()[0]
            stop = self.ui.te_sci.getSelection()[2]
            lines = range(start,stop+1)
            if start == stop: lines = [start]
        else:
            start = stop = self.ui.te_sci.getCursorPosition()[0]
            lines = [start]
        self.okedit=0
        for i in lines:
            self.ui.te_sci.indent(i)
        self.okedit=1
        
    def unindent(self):
        self.okedit=0
        if self.ui.te_sci.getSelection()[0] != -1:
            start = self.ui.te_sci.getSelection()[0]
            stop = self.ui.te_sci.getSelection()[2]
            lines = range(start,stop+1)
            if start == stop: lines = [start]
        else:
            start = stop = self.ui.te_sci.getCursorPosition()[0]
            lines = [start]
        for i in lines:
            self.ui.te_sci.unindent(i)
        self.okedit=1
    
    def toggleWordWrap(self):
        self.wordwrapmode = not self.wordwrapmode
        if self.wordwrapmode:
            self.ui.te_sci.setWrapMode(Qsci.QsciScintilla.WrapCharacter)
        else:
            self.ui.te_sci.setWrapMode(Qsci.QsciScintilla.WrapNone)
    
##            txt = self.ui.te_sci.selectedText()
##            print txt
##            ntxt = ''
##            for t in txt.split('\n'):
##                ntxt += commentD[lang]+t+'\n'
##            
##            self.ui.te_sci.replaceSelectedText(ntxt)

    def toggleWhitespace(self):
        v=not self.ui.te_sci.eolVisibility()
        self.ui.te_sci.setEolVisibility(v)
        if v:
            self.ui.te_sci.setWhitespaceVisibility(Qsci.QsciScintilla.WsVisible)
        else:
            self.ui.te_sci.setWhitespaceVisibility(Qsci.QsciScintilla.WsInvisible)
        

    def toggleAutoComplete(self):
        self.autocompletemode = not self.autocompletemode
        if self.autocompletemode:
            # Enabled autocompletion
            self.ui.te_sci.setAutoCompletionFillupsEnabled(1)
            self.ui.te_sci.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
##            self.ui.te_sci.setAutoCompletionThreshold(3)
            self.ui.te_sci.AutoCompletionUseSingle(Qsci.QsciScintilla.AcusExplicit)
        else:
            self.ui.te_sci.setAutoCompletionSource(Qsci.QsciScintilla.AcsNone)
    
    def dropEvent(self,event):
        self.ide.dropEvent(event)
    
    def setFocus(self):
        self.ui.te_sci.setFocus()