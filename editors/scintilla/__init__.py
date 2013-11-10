import scintilla
from PyQt4 import Qsci

lexD = {'python':Qsci.QsciLexerPython(),
    'javascript':Qsci.QsciLexerJavaScript(),
    'html':Qsci.QsciLexerHTML(),
    'css':Qsci.QsciLexerCSS(),
    'xml':Qsci.QsciLexerXML(),
    'ui':Qsci.QsciLexerXML(),
    'qml':Qsci.QsciLexerJavaScript(),
    'yaml':Qsci.QsciLexerYAML(),
    'bash':Qsci.QsciLexerBash(),
    'batch':Qsci.QsciLexerBatch(),
    'sql':Qsci.QsciLexerSQL(),
    }

def addEditor(parent,lang,filename):
    lex = None
    if lang in lexD:
        lex = lexD[lang]
    else:
        try:
            exec('lex = Qsci.QsciLexer'+lang+'()')
        except:
            pass
            
    editor = scintilla.Sci(parent,lex)
    
    return editor

def getLang():
    lang = []
    for l in sorted(dir(Qsci)):
        if l.startswith('QsciLexer'):
            lex = l[9:]
            if lex != '':
                lang.append(lex)
    return lang
    
##    for l in sorted(lexD.keys()):
##        return l
print getLang()