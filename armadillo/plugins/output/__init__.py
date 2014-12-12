import output

def addDock(parent):
    dock = output.Output(parent)
    parent.evnt.editorTabChanged.connect(dock.editorTabChanged)
    dock.title = 'Output'
    dock.location = 'bottom'
    return dock