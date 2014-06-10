import re

def analyzeLine(txtlines):
    outline = []
    cnt = -1
    for line in txtlines:
        cnt += 1
        lcnt = cnt
        typ = None
        itmText = None
    
        spc = (len(line) -len(line.lstrip()))*' '
        tls = line.lstrip()
    
        if tls.startswith('/*---'):
            itmText =tls[5:].split('*/')[0]
            typ = 'heading'
        elif not tls.startswith('/*'):
            g = re.match('.*{',line)
            if g:
                itmText = g.group()[:-1]
                if itmText == '': 
                    itmText = txtlines[cnt-1]
                    lcnt = cnt-1                if itmText == '': itmText = None
                if itmText != None and itmText.startswith('.'):
                    typ = 'function'
                else:
                    typ = 'object'
    
        if itmText != None:
            outline.append([itmText,typ,lcnt])
    
    return outline