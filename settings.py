
class Settings(object):
    #---Editors
    editors={
        'Python':{
            'editor':'scintilla',
            'run':'python'
        },
        'HTML':{
            'editor':'scintilla',
            'run':'webbrowser'
        },
        'JavaScript':{
            'editor':'scintilla',
        },
        'CSS':{
            'editor':'scintilla',
        },
        'Text':{
            'editor':'scintilla',
        },
        'SQL':{
            'editor':'scintilla',
        },
        'Bash':{
            'editor':'scintilla',
            'run':''
        },
        'Batch':{
            'editor':'scintilla',
        },
        'UI':{
            'editor':'scintilla',
        },
        'Perl':{
            'editor':'scintilla',
        },
        'CKEditor':{
            'editor':'ckeditor',
            'run':'webbrowser'
        },
        'WebView':{
            'editor':'webview',
        },
##        'Monkey':{
##            'editor':'monkey',
##        },
        
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
    
    #---Extensions
    ext={
        'py': ['Python'],
        'js': ['JavaScript'],
        'html': ['HTML','CKEditor'],
        'htm': ['HTML','CKEditor'],
        'css': ['CSS'],
        'style': ['CSS'],
        'ui': ['UI'],
        'xml': ['XML'],
        'sh': ['Bash'],
        'sql': ['SQL'],
        'txt': ['Text'],
        'bat': ['Batch'],
    }
    
    #---Other
    view_folder=0
    save_workspace_on_close=1