import re

def analyzeLine(txtlines):
    outline = []
    lcnt = -1
    for line in txtlines:
        lcnt += 1
        typ = None
        itmText = None
    
        spc = (len(line) -len(line.lstrip()))*' '
        tls = line.lstrip()
    
        if tls.lower().startswith('<body'):
            itmText = '<BODY>'
            typ = 'object'
        elif tls.lower().startswith('<head'):
            itmText = '<HEAD>'
            typ = 'object'
        elif tls.lower().startswith('<table'):
            itmText = '<TABLE>'
            typ = 'function'
        elif tls.startswith('<!---'):
            itmText =tls[5:].replace('-->','')
            typ = 'heading'
        if tls.startswith('function'):
            itmText =tls[9:].rstrip()
            if itmText.endswith('{'): itmText = itmText[:-1]
            typ = 'function'
    
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline