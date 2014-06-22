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
        
        if tls.startswith('function'):
            itmText =tls[9:].rstrip()
            if itmText.endswith('{'): itmText = itmText[:-1]
            typ = 'function'
        elif tls.startswith('//---'):
            itmText =tls[5:]
            typ = 'heading'
    
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline