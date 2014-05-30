
def analyzeLine(line):
    itmText=typ=None
    if line.lower().startswith('['):
        h = line.split(' ')[0].count('[')
        head = line.replace('[','').replace(']','')
        itmText = (h-1)*4*' '+head
        if h==1:
            typ='object'
        else:
            typ='function'
    elif line.startswith('['):
        itmText =line[4:].lstrip('-')
        ##if itmText == '': itmText = None
        typ = 'heading'
    
    return itmText,typ