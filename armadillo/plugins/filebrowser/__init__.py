import filebrowser

def addDock(parent):
    dock = filebrowser.DirTree(parent)
    dock.title = 'File Browser'
    dock.location = 'left'
    return dock