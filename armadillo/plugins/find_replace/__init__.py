import find_replace

def addDock(parent):
    dock = find_replace.Find_Replace(parent)
    dock.title = 'Find / Replace'
    dock.location = 'bottom'
    return dock