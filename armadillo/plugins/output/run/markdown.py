
def cmd(outputWidget,filename):
    import plugins.mkdown as mkdown
    html = mkdown.generate(filename)
    outputWidget.webview_preview(html,filename)