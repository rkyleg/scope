import snippets

def addPlugin(parent):
    plugin = snippets.Snippets(parent)
    plugin.title = 'Snippets'
    plugin.location = 'bottom'
    return plugin