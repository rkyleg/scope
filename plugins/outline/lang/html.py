
def analyzeLine(line):
    itmText=typ=None
    if line.lower().startswith('<body'):
        itmText = '<BODY>'
        typ = 'object'
    elif line.lower().startswith('<head'):
        itmText = '<HEAD>'
        typ = 'object'
    elif line.lower().startswith('<table'):
        itmText = '<TABLE>'
        typ = 'object'
    elif line.startswith('<!---'):
        itmText =line[5:].replace('-->','')
        typ = 'heading'
    
    return itmText,typ