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
        
        if tls.startswith('def '):
            itmText = tls[4:-1]
            typ = 'function'
        elif tls.startswith('class '):
            itmText =tls[6:-1]
            typ = 'object'
        elif tls.startswith('@'):
            itmText =tls.lstrip('-')
            typ = 'decorator'
        elif tls.startswith('#---'):
            itmText =tls[4:].lstrip('-')
            ##if itmText == '': itmText = None
            typ = 'heading'
        
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline