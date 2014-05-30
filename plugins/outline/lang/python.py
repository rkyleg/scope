
def analyzeLine(line):
    itmText=typ=None
    if line.startswith('def '):
        itmText = line[4:-1]
        typ = 'function'
    elif line.startswith('class '):
        itmText =line[6:-1]
        typ = 'object'
    elif line.startswith('#---'):
        itmText =line[4:].lstrip('-')
        ##if itmText == '': itmText = None
        typ = 'heading'
    
    return itmText,typ