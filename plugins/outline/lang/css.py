
def analyzeLine(line):
    itmText=typ=None
    if line.startswith('/*---'):
        itmText =line[5:].split('*/')[0]
        typ = 'heading'
    else:
        g = re.match('.*{',t)
        if g:
            itmText = g.group()[:-1]
            if itmText == '': 
                itmText = txtlines[cnt-1]
                lcnt = cnt-1
            if itmText == '': itmText = None
            if itmText.startswith('.'):
                typ = 'function'
            else:
                typ = 'object'
    
    return itmText,typ