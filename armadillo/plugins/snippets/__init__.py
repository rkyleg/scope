import snippets

def addDock(parent):
    dock = snippets.Snippets(parent)
    dock.title = 'Snippets'
    dock.location = 'bottom'
    return dock