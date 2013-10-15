import scintilla
from PyQt4 import Qsci

lexD = {'Python':Qsci.QsciLexerPython(),
    'JavaScript':Qsci.QsciLexerJavaScript(),
    'HTML':Qsci.QsciLexerHTML(),
    'CSS':Qsci.QsciLexerCSS(),
    'XML':Qsci.QsciLexerXML(),
    'UI':Qsci.QsciLexerXML(),
    'YAML':Qsci.QsciLexerYAML(),
    'Bash':Qsci.QsciLexerBash(),
    'Batch':Qsci.QsciLexerBatch(),
    'SQL':Qsci.QsciLexerSQL(),
    }

def addEditor(parent,lang,filename):
    lex = None
    if lang in lexD:
        lex = lexD[lang]
    editor = scintilla.Sci(parent,lex)
    
    return editor