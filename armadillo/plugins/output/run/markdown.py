
def cmd(outputWidget,filename, args=''):
    import plugins.mkdown as mkdown
    html = mkdown.generate(filename)
    outputWidget.webview_preview(html,filename)