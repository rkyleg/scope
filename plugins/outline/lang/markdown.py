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
        
        if tls.startswith('#'): # Heading
            h = tls.split(' ')[0].count('#')
            head = tls.replace('#','')
            itmText = (h-1)*4*' '+head
            if h==1:
                typ='object'
            else:
                typ='function'
    
        if itmText != None:
            outline.append([spc+itmText,typ,lcnt])
    
    return outline