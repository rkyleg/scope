
class Settings(object):
    #---Editors (that are available)
    editors = ['scintilla','ace','ckeditor']
    # Default Editor
    defaultEditor = 'scintilla'
    
    # Run Commands (language:command)
    run = {
        'python':'python',
        'html':'webbrowser',
    }
    
##    # Favorite New Setup
##    favNew = [
##        {'name':'Python','editor':'scintilla','lang':'python'},
##        {'name':'Javascript','editor':'ace','lang':'javascript'},
##        {'name':'CSS','editor':'ace','lang':'css'},
##        {'name':'HTML','editor':'ace','lang':'html'},
##        {'name':'Text','editor':'scintilla','lang':'text'},
##        
##    ]
    
    # Favorite Languages
    favLang = {
        'python':{'editor':'scintilla'},
        'javascript':{'editor':'ace'},
        'html':{'editor':'ace'},
        'css':{'editor':'ace'},
        'text':{'editor':'scintilla'},
        'markdown':{'editor':'ace'},
    }
    

    
##    #---Favorite Editors
##    favEditors={
##        'Python':{
##            'editor':'scintilla',
##            'run':'python'
##        },
##        'HTML':{
##            'editor':'scintilla',
##            'run':'webbrowser'
##        },
##        'JavaScript':{
##            'editor':'scintilla',
##        },
##        'CSS':{
##            'editor':'scintilla',
##        },
##        'Text':{
##            'editor':'scintilla',
##        },
##        'SQL':{
##            'editor':'scintilla',
##        },
##        'Bash':{
##            'editor':'scintilla',
##            'run':''
##        },
##        'Batch':{
##            'editor':'scintilla',
##        },
##        'UI':{
##            'editor':'scintilla',
##        },
##        'QML':{
##            'editor':'scintilla',
##        },
##        'Perl':{
##            'editor':'scintilla',
##        },
##        'CKEditor':{
##            'editor':'ckeditor',
##            'run':'webbrowser'
##        },
##        'Ace':{
##            'editor':'ace',
##            'run':'webbrowser'
##        },
##        'WebView':{
##            'editor':'webview',
##        },
##    }
    
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
    }
##    ext2={
##        'py': ['Python'],
##        'js': ['JavaScript'],
##        'html': ['HTML','CKEditor'],
##        'htm': ['HTML','CKEditor'],
##        'css': ['CSS'],
##        'style': ['CSS'],
##        'ui': ['UI'],
##        'qml':['QML'],
##        'xml': ['XML'],
##        'sh': ['Bash'],
##        'sql': ['SQL'],
##        'txt': ['Text'],
##        'bat': ['Batch'],
##    }
    
    #---Other
    view_folder=0
    save_workspace_on_close=1