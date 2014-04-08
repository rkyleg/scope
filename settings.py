import os

class Settings(object):
    #---Editors (that are available)
    activeEditors = ['scintilla','ace','ckeditor']#,'monkey']
    
    # Default Editor
    defaultEditor = 'scintilla'
    
    #---Other
    view_folder=0
    save_workspace_on_close=1
    widgetstyle="Plastique" # Set blank to use default OS look
    
    # Enabled Plugins
    activePlugins = ['outline','filebrowser','pycute','qt2py','find_replace','output']
    
    # Run Commands (language:command)
    run = {
        'python':'python',
        'html':'webbrowser',
        'markdown':'markdown',
    }
    
    # Favorite Languages
    favLang = {
        'python':{'editor':'scintilla'},
        'javascript':{'editor':'ace'},
        'html':{'editor':'ace'},
        'css':{'editor':'ace'},
        'text':{'editor':'scintilla'},
        'markdown':{'editor':'ace'},
        'sql':{'editor':'ace'},
        'handlebars':{'editor':'ace'},
        'jade':{'editor':'ace'},
    }
    
    #---Editors
    editors = {
        'scintilla':{
            
        },
        'ace':{
            'theme':'twilight',
            'behavioursEnabled':1,
            'wrapBehavioursEnabled':1,
            'settingJS':'editor.setHighlightSelectedWord(false)'  # Add any additional Ace javascript settings here
        },
        'ckeditor':{
        },
        'webview':{
        },
##        'monkey':{
##        }
    }
    
    #---Plugins
    plugins={ 
        'outline': {
            'dockarea': 'left',
            'title': 'Outline',
        },
        'filebrowser': {
            'dockarea': 'left',
            'title': 'File Browser',
        },
        'pycute':{
            'dockarea': 'bottom',
            'title': 'Python Shell',
        },
        'qt2py':{
           'dockarea': 'bottom',
           'title': 'PyQt Converter',
        },
        'find_replace':{
            'dockarea': 'bottom',
            'title': 'Find / Replace',
        },
        'output':{
            'dockarea': 'bottom',
            'title': 'Output',
        },
    }
    
    #---Extension to language
    ext={
        'py':'python',
        'pyw':'python',
        'js':'javascript',
        'html':'html',
        'htm':'html',
        'css':'css',
        'style':'css',
        'ui':'xml',
        'qml':'javascript',
        'xml':'xml',
        'sh':'bash',
        'sql':'sql',
        'txt':'text',
        'bat':'batch',
        'pref':'json',
        'json':'json',
        'rb':'ruby',
        'php':'php',
        'java':'java',
        'md':'markdown',
        'c':'cpp',
        'h':'cpp',
        'ino':'cpp', # Arduino
        'mky':'monkey',
        'thtml':'handlebars', # Mustache/Handlebars HTML template file
        'jade':'jade',
    }