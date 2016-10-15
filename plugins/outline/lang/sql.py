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
        
        if tls.startswith('---'):
            itmText =tls[4:].lstrip('-')
            ##if itmText == '': itmText = None
            typ = 'heading'
        
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline