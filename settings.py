
class Settings(object):
    #---Language
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
        'CKEditor (HTML)':{
            'editor':'ckeditor',
            'run':'webbrowser'
        },
        'Webview':{
            'editor':'webview',
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
        'ui':{
            'editor':'scintilla',
        },
        'PERL':{
            'editor':'scintilla',
        },
    }
    
    #---Plugins
    plugins={ 
        'outline': 
            'dockarea': 'left',
            'title': 'Outline',
        'filebrowser': 
            'dockarea': 'left',
            'title': 'File Browser',
        'pycute':
            'dockarea': 'bottom',
            'title': 'Python Shell',
        'qt2py':
           'dockarea': 'bottom',
           'title': 'PyQt Converter',
        'find_replace':
            'dockarea': 'bottom',
            'title': 'Find / Replace',
        'output':
            'dockarea': 'bottom',
            'title': 'Output',
    }
    
    #---Extensions
    ext={
        'py': ['Python'],
        'js': ['JavaScript'],
        'html': ['HTML','CkEditor'],
        'htm': ['HTML','CkEditor'],
        'css': ['CSS'],
        'style': ['CSS'],
        'ui': ['UI'],
        'xml': ['XML'],
        'sh': ['Bash'],
        'sql': ['SQL'],
        'txt': 'Text'],
        'bat': ['Batch'],
    }
    
    #---Other
    view_folder=0