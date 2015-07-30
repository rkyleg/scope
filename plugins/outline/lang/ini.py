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
    
        if tls.lower().startswith('['):
            h = tls.split(' ')[0].count('[')
            head = tls.replace('[','').replace(']','')
            itmText = (h-1)*4*' '+head
            if h==1:
                typ='object'
            else:
                typ='function'
        elif tls.startswith('['):
            itmText =tls[4:].lstrip('-')
            ##if itmText == '': itmText = None
            typ = 'object'
        elif tls.startswith('#---'):
            itmText =tls[4:].lstrip('-')
            ##if itmText == '': itmText = None
            typ = 'heading'
        
        if itmText != None:
            outline.append([itmText,typ,lcnt])
    
    return outline