
def analyzeLine(line):
    itmText=typ=None
    if line.startswith('function'):
        itmText =line[9:].rstrip()
        if itmText.endswith('{'): itmText = itmText[:-1]
        typ = 'function'
    elif line.startswith('//---'):
        itmText =line[5:]
        typ = 'heading'
    
    return itmText,typ