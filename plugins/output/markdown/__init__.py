import markdown2, os, sys

#file = r'/media/hdesktop/hmedia/Software/afide/extra/todo.md'

def generate(file):
    # Open File
    f = open(file,'r')
    html = f.read()
    f.close()
    
    # Get Markdown
    md = markdown2.markdown(html)
    
    # Custom Markdown modifications
    md = md.replace('<li>[ ]','<li><input type="checkbox" disabled="disabled">')
    md = md.replace('<li>[x]','<li><input type="checkbox" checked="checked" disabled="disabled">')
    
    # Custom Style
    mstyle = '''
            h1{border-bottom:2px solid gray;}
            h2,h3,h4,h5,h6,h7 {border-bottom:1px solid gray;}
    '''
    for i in range(2,8):
        mstyle += 'h'+str(i)+'{margin-left:'+str((i-1)*10)+'px;}'
    mhtml = '<style>'+mstyle+'</style>'
    
    mhtml += md
    
    # Get html path
    pth = os.path.dirname(file)
    nm = os.path.basename(file).split('.')[0]
    fpth = pth+'/'+nm+'.html'
    
    # Write to file
    f = open(fpth,'w')
    f.write(mhtml)
    f.close()

    import webbrowser
    webbrowser.open(fpth)

#generate(file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate(sys.argv[1])