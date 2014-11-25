import py_console, sys

#---Code to add to afide
def addDock(parent):
    wdg = py_console.Console(parent)
    wdg.title = 'Python Shell ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')'
    wdg.location = 'bottom'
    return wdg