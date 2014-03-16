import os, sys

try:
    import markdown
except:
    import markdown2 as markdown

#file = r'/media/hdesktop/hmedia/Software/afide/extra/todo.md'

def generate(file):
    # Open File
    f = open(file,'r')
    rawhtml = f.read()
    f.close()
    
    # Parse
    html = ''
    txtlines = rawhtml.replace('\r\n','\n').replace('\r','\n').split('\n')
    for t in txtlines:
        if not t.startswith('> '):
            # Ignore comments
            html += t+'\n'
    
##    html=rawhtml
        
    
    # Get Markdown
    md = markdown.markdown(html)#,extras=['cuddled-lists','wiki-tables'])
    
    # Custom Markdown modifications
    md = md.replace('<li>[ ]','<li class="checkbox"><input type="checkbox" disabled="disabled">')
    md = md.replace('<li>[]','<li class="checkbox"><input type="checkbox" disabled="disabled">')
    md = md.replace('<li>[x]','<li class="checkbox"><input type="checkbox" checked="checked" disabled="disabled">')
    md = md.replace('<li>[-]','<li class="cancelled"><input type="checkbox" checked="checked" disabled="disabled">')
    md = md.replace('<li>[f]','<li class="future"><input type="checkbox" disabled="disabled"> FUTURE')
    
    # Custom Style
    mstyle = '''
            h1{border-bottom:2px solid gray;}
            h2,h3,h4,h5,h6,h7 {border-bottom:1px solid gray;}
            li.checkbox,li.cancelled,li.future {list-style-type: none;margin-left:-25px;}
            li.cancelled {text-decoration:line-through}
            li.future {font-style:italic;color:gray;}
    '''
##    for i in range(2,8):
##        mstyle += 'h'+str(i)+'{margin-left:'+str((i-1)*10)+'px;}'
    mhtml = '<style>'+mstyle+'</style>'
    
    mhtml += md
    
    # Get html path
##    pth = os.path.dirname(file)
##    nm = os.path.basename(file).split('.')[0]
##    fpth = pth+'/'+nm+'.html'
    
    return mhtml
    
##    # Write to file
##    f = open(fpth,'w')
##    f.write(mhtml)
##    f.close()
##
##    import webbrowser
##    webbrowser.open(fpth)

#generate(file)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate(sys.argv[1])