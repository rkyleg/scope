from . import scratch

def addPlugin(parent):
    plugin = scratch.Scratch(parent)
    plugin.title = 'Scratchpad'
    plugin.location = 'bottom'
    return plugin