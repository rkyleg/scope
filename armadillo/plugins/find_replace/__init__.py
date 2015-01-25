from . import find_replace

def addPlugin(parent):
    plugin = find_replace.Find_Replace(parent)
    plugin.title = 'Find / Replace'
    plugin.location = 'bottom'
    return plugin