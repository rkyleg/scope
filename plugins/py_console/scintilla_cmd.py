from PyQt4 import QtGui,QtCore, Qsci

# Color is a rgb string
styleD = {
    # Python
    'Default':'255,255,255',  #white
    'Comment':'244,255,166', # yellow
    'CommentBlock':'100,100,100',
    
    'ClassName':'255,116,88', # orange

    'FunctionMethodName':'255,201,139',   # orange
    'GlobalClass':'255,177,99', # orange, javascript
    'Tag':'255,177,99', # orange, html
    
    'Decorator':'255,170,127',
    'Keyword':'97,171,205', # light blue
    
    'HighlightedIdentifier':'250,0,0',
    'Identifier':'',
    'Inconsistent':'',
    'NoWarning':'',
    
    'Operator':'166,220,255',  # blue
    
    'Spaces':'',
    'Tabs':'',
    'TabsAfterSpaces':'',
    
    'Number':'255,170,255', # pink
    
    'SingleQuotedString':'125,188,151',
    'DoubleQuotedString':'125,188,151',
    'TripleDoubleQuotedString':'122,159,94',
    'TripleSingleQuotedString':'122,159,94',
    'UnclosedString':'255,94,94', # reddish
    
}

class cmd_widget(Qsci.QsciScintilla):
    def __init__(self,parent=None):
        Qsci.QsciScintilla.__init__(self,parent)

        self.lex = Qsci.QsciLexerPython()
        self.setLexer(self.lex)
        for i in range(5):
            self.setMarginWidth(i,0)
        
        # Set Dark Color
        style_obj = set(styleD.keys()).intersection(dir(self.lex))
        self.setCaretForegroundColor(QtGui.QColor(255,255,255))
        shade=30
        self.setCaretLineBackgroundColor(QtGui.QColor(shade,shade,shade))
        self.lex.setDefaultPaper(QtGui.QColor(shade,shade,shade))
        self.lex.setPaper(QtGui.QColor(shade,shade,shade),self.lex.Default)
        self.setColor(QtGui.QColor(255,255,255))
        self.setMarginsBackgroundColor(QtGui.QColor(60,60,60))
        self.setWhitespaceBackgroundColor(QtGui.QColor(80,80,80))
        self.setFoldMarginColors(QtGui.QColor(200,200,200),QtGui.QColor(90,90,90))
##            self.ui.te_sci.setPaper(QColor(80,80,80))
        self.setMarginsForegroundColor(QtGui.QColor(200,200,200))
##            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETBACK,Qsci.QsciScintilla.STYLE_DEFAULT,QColor(150,150,150))
        
        self.setMatchedBraceBackgroundColor(QtGui.QColor(shade,shade,shade))
        self.setMatchedBraceForegroundColor(QtGui.QColor(170,0,255))
        self.setUnmatchedBraceBackgroundColor(QtGui.QColor(shade,shade,shade))
        
        # Set defaults for all:
        style_obj = set(styleD.keys()).intersection(dir(self.lex))
        style_obj.remove('Default')
        style_obj = set(['Default']).union(sorted(style_obj))
        
        for c in sorted(style_obj,reverse=1):
            clr = styleD[c]
            if clr == '':
                clr = styleD['Default']
            try:
                exec('self.lex.setPaper(QtGui.QColor(30,30,30),self.lex.'+c+')')
                exec('self.lex.setColor(QtGui.QColor('+clr+'),self.lex.'+c+')')
            except:
                print 'no keyword',c
        
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(18)
        self.setStyleSheet('border:0px;')
        
        self.widgetObject = Qsci.QsciScintilla
        self.type = 'qscintilla'
    
    def insert(self,txt):
        self.replaceSelectedText(txt)