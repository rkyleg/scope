import scintilla
from PyQt4 import Qsci

# Setup languages
langD = {
    'ui':'QsciLexerXML',
    'qml':'QsciLexerJavaScript',
    'json':'QsciLexerJavaScript',
}

for l in sorted(dir(Qsci)):
    if l.startswith('QsciLexer'):
        lang = l[9:].lower()
        if l != '':
            langD[lang] = l

def addEditor(parent,lang,filename):
    lex = None
##    if lang in langD:
##        lex = langD[lang]
##    else:
    try:
        exec('lex = Qsci.'+langD[lang]+'()')
    except:
        pass
            
    editor = scintilla.Sci(parent,lex)
    
    return editor

def getLang():
    return sorted(langD)
    
def getSettings():
    settingsD = {
        'wordwrap':{'type':'bool'}
    }
    return settingsD