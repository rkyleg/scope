from . import qt2py

def addPlugin(parent):
    plugin = qt2py.Qt2Py(parent)
    plugin.title = 'PyQt Converter'
    plugin.location = 'bottom'
    return plugin