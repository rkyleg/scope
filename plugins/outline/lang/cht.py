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
    
        if tls.lower().startswith('h>'):
            itmText = tls[2:].strip()
            typ = 'object'
        elif tls.lower().startswith('c>'):
            itmText = tls[2:].strip()
            typ = 'function'

        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline