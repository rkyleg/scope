from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import Qsci
from PyQt4 import QtGui, QtCore
from scintilla_ui import Ui_Form
import os,sys, time

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
    'yaml':'##'
    
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
##    editingFinished = QtCore.pyqtSignal(QtGui.QWidget)

class Sci(QtGui.QWidget):
    def __init__(self,parent,lex):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.te_sci.ARROW_MARKER_NUM = 8
        self.ui.te_sci.setUtf8(True)
        self.afide = parent
        self.okedit = 1
        
        # Events
        self.evnt = Events()
        self.ui.te_sci.textChanged.connect(self.editorTextChanged)

        self.ui.te_sci.keyPressEvent = self.keyPressEvent
        
        # Font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.ui.te_sci.setFont(font)
        self.ui.te_sci.setMarginsFont(font)

        # Margin 0 for line numbers
        fontmetrics = QFontMetrics(font)
        self.ui.te_sci.setMarginsFont(font)
        self.ui.te_sci.setMarginWidth(0, fontmetrics.width("00000"))
        self.ui.te_sci.setMarginWidth(1, 0)
        self.ui.te_sci.setMarginLineNumbers(0, True)
        self.ui.te_sci.setMarginsBackgroundColor(QColor("#cccccc"))

        # Enabled autocompletion
        self.ui.te_sci.setAutoCompletionFillupsEnabled(1)
        self.ui.te_sci.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.ui.te_sci.setAutoCompletionThreshold(3)

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

        # Current line visible with special background color
        self.ui.te_sci.setCaretLineVisible(True)
        self.ui.te_sci.setCaretLineBackgroundColor(QColor("#eeeeee"))
        
        self.wordwrapmode = 0
        
        if lex != None:
            lex.setDefaultFont(font)
            self.ui.te_sci.setLexer(lex)
        self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
    
    def keyPressEvent(self,event):
        ky = event.key()
        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace,QtCore.Qt.Key_Z,QtCore.Qt.Key_Y]:
            self.okedit = 0
        Qsci.QsciScintilla.keyPressEvent(self.ui.te_sci,event)
        QtGui.QApplication.processEvents()
##        if ky in [QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return,QtCore.Qt.Key_Tab,QtCore.Qt.Key_Backtab,QtCore.Qt.Key_Delete,QtCore.Qt.Key_Backspace]:
##            self.editingFinished()
        self.okedit = 1
        self.editorTextChanged()
    
    def setText(self,txt):
        self.ui.te_sci.setText(txt)
    
##    def updateText(self,txt):
##        # Update, but keep current undo
##        self.ui.te_sci.selectAll(select=1)
##        self.ui.te_sci.replaceSelectedText(txt)
    
    def getText(self):
        txt = str(self.ui.te_sci.text().toUtf8()).decode('utf-8')
        return txt

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
            self.evnt.editorChanged.emit(self)
    
##    def editingFinished(self):
##        self.evnt.editingFinished.emit(self)
    
    def toggleComment(self):
        lang = self.afide.currentWidget().lang
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