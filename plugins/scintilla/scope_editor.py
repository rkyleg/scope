from . import scintilla
from PyQt4 import Qsci

class Settings(object):
    '''Modifiable settings and their defaults'''
    
class Editor(object):
    title = 'Plugin Title'
    location = 'app' # left, bottom, right, app
    settings = Settings.__dict__
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def getWidget(self, lang, **kargs):
        lex = None

        try:
            exec('lex = Qsci.'+self.langD[lang]+'()')
        except:
            pass
                
        editor = scintilla.Sci(self.parent,lex,lang)
        
        return editor

    def getLang(self):
        # Setup languages
        self.langD = {
            'ui':'QsciLexerXML',
            'qml':'QsciLexerJavaScript',
            'json':'QsciLexerJavaScript',
        }

        for l in sorted(dir(Qsci)):
            if l.startswith('QsciLexer'):
                lang = l[9:].lower()
                if l != '':
                    self.langD[lang] = l
                    
        return sorted(self.langD)