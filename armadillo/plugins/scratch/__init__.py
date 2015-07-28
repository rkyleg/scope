from . import scratch

title = 'Scratchpad'
location = 'bottom'

def addPlugin(parent):
    plugin = scratch.Scratch(parent)
##    plugin.title = 'Scratchpad'
##    plugin.location = 'bottom'
    return plugin