from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import Qsci
from PyQt4 import QtGui, QtCore
from scintilla_ui import Ui_Form
import os,sys

lexD = {'Python':Qsci.QsciLexerPython(),
    'JavaScript':Qsci.QsciLexerJavaScript(),
    'HTML':Qsci.QsciLexerHTML(),
    'CSS':Qsci.QsciLexerCSS(),
    'XML':Qsci.QsciLexerXML(),
    }

commentD = {

}

def addEditor(parent,lang):
    lex = None
    if lang in lexD:
        lex = lexD[lang]
    editor = Sci(parent,lex)
    
    return editor

class Events(QtCore.QObject):
    editorChanged = QtCore.pyqtSignal(QtGui.QWidget)

class Sci(QtGui.QWidget):
    def __init__(self,parent,lex):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.te_sci.ARROW_MARKER_NUM = 8

        # Events
        self.evnt = Events()
        self.ui.te_sci.textChanged.connect(self.editorTextChanged)

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
        
        # Indentation
        self.ui.te_sci.setIndentationsUseTabs(0)
        self.ui.te_sci.setAutoIndent(1)
        self.ui.te_sci.setIndentationGuides(1)

        self.ui.te_sci.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)
        self.ui.te_sci.setTabWidth(4)

        # Current line visible with special background color
        self.ui.te_sci.setCaretLineVisible(True)
        self.ui.te_sci.setCaretLineBackgroundColor(QColor("#eeeeee"))
        
        if lex != None:
            lex.setDefaultFont(font)
            self.ui.te_sci.setLexer(lex)
        self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
    
    def setText(self,txt):
        self.ui.te_sci.setText(txt)
    
    def getText(self):
        return self.ui.te_sci.text()

    def find(self,txt):
         self.ui.te_sci.findFirst(txt,0,0,0,1)
    
    def gotoLine(self,line):
        self.ui.te_sci.setCursorPosition(self.ui.te_sci.lines(),0)  # Send to bottom so cursor is at top of page
        self.ui.te_sci.setCursorPosition(line,0)
        #self.ui.te_sci.setSelection(line,0,line,-1)
        self.ui.te_sci.setFocus()
    
    def editorTextChanged(self):
        self.evnt.editorChanged.emit(self)