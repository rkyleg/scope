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
            typ = 'object'
        elif tls.startswith('<!---'):
            itmText =tls[5:].replace('-->','')
            typ = 'heading'
    
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline