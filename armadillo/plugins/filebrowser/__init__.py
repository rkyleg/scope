import filebrowser

def addPlugin(parent):
    plugin = filebrowser.DirTree(parent)
    plugin.title = 'File Browser'
    plugin.location = 'left'
    return plugin