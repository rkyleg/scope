import qt2py

def addDock(parent):
    dock = qt2py.Qt2Py(parent)
    dock.title = 'PyQt Converter'
    dock.location = 'bottom'
    return dock