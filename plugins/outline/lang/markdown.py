
def analyzeLine(line):
    itmText=typ=None
    if line.startswith('#'): # Heading
        h = line.split(' ')[0].count('#')
        head = line.replace('#','')
        itmText = (h-1)*4*' '+head
        if h==1:
            typ='object'
        else:
            typ='function'
    
    return itmText,typ