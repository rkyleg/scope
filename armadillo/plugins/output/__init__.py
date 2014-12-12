import output

def addDock(parent):
    dock = output.Output(parent)
    parent.evnt.editorTabChanged.connect(dock.editorTabChanged)
    parent.evnt.close.connect(dock.killAll)
    dock.title = 'Output'
    dock.location = 'bottom'
    return dock