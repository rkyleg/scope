import os

def get_themes():
    # Get Theme list
    fld = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/src-noconflict/'
    themes = []
    for f in sorted(os.listdir(fld)):
        if f.startswith('theme'):
            themes.append(f[6:-3])
    return themes


class Settings(object):
    '''Modifiable settings and their defaults'''
    wordwrap = {'type':'bool'}
    behavioursEnabled = {'type':'bool','tooltip':'autocomplete quotation marks, parenthesis, and brackets'}
    wrapBehavioursEnabled = {'type':'bool','tooltip':'use automatic wrapping after certain characters like brackets'}
    theme = {'type':'list','options':get_themes()}

class Editor(object):
    title = 'Plugin Title'
    settings = Settings.__dict__
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        '''Called when loading the plugin'''
        
    def getWidget(self, lang, **kargs):
        '''Return the Editor Widget'''
        from . import ace
        editor = ace.WebView(self.parent,lang)
        return editor
        
    def getLang(self):
        '''Get Languages'''
        fld = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+'/src-noconflict/'
        lexers = []
        for f in sorted(os.listdir(fld)):
            if f.startswith('mode'):
                lexers.append(f[5:-3])
        
        return lexers
