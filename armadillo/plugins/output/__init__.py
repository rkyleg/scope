import output

def addDock(parent):
    dock = output.Output(parent)
    dock.title = 'Output'
    dock.location = 'bottom'
    return dock