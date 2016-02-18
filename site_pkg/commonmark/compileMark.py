import os, sys, codecs
import CommonMark

def generate(file=None,text=None,style='',custom=0):
    # Open File
    if file != None:
        f = codecs.open(file,'r','utf-8')
        rawhtml = f.read()
        f.close()
    else:
        rawhtml=text
    # Parse
    html = ''
    txtlines = rawhtml.replace('\r\n','\n').replace('\r','\n').split('\n')
    for t in txtlines:
            # Ignore comments
            html += t+'\n'

    # Get Markdown (Common Mark)
    parser = CommonMark.DocParser()
    renderer = CommonMark.HTMLRenderer()
    md = renderer.render(parser.parse(html))
    
    mhtml=''
    
    # Custom Markdown modifications
    if custom:
        md = md.replace('<li>[ ]','<li class="checkbox"><input type="checkbox" disabled="disabled">')
        md = md.replace('<li>[]','<li class="checkbox"><input type="checkbox" disabled="disabled">')
        md = md.replace('<li>[x]','<li class="checkbox checked"><input type="checkbox" checked="checked" disabled="disabled">')
        md = md.replace('<li>[-]','<li class="cancelled"><input type="checkbox" checked="checked" disabled="disabled">')
        md = md.replace('<li>[f]','<li class="future"><input type="checkbox" disabled="disabled"> FUTURE')
        
        # Custom Style
        style = '''
                h1{border-bottom:2px solid gray;}
                h2,h3,h4,h5,h6,h7 {border-bottom:1px solid gray;}
                li.checkbox,li.cancelled,li.future {list-style-type: none;margin-left:-25px;}
                li.cancelled {text-decoration:line-through;color:gray;}
                li.future {font-style:italic;color:gray;}
                li.checked {color:gray;} 
                pre,code {font-family:Courier New,mono,monospace;font-size:12px;}
                img{max-width:100%;}
        '''+style
        
    # Add Style
    if style != '':
        mhtml += '<style>'+style+'</style>'
    
    mhtml += md

    
    return mhtml

def compile_md(md_file,html_file=None,**kargs):
    if html_file == None:
        html_file = md_file.split('.')[0]+'.html'
    
    mhtml = generate(md_file,**kargs)
    with open(html_file,'w') as f:
        f.write(mhtml)

if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) > 1:
        if sys.argv[1] == '-c':
            md_file = sys.argv[2]
            html_file = None
            if len(sys.argv) > 3:
                html_file = sys.argv[3]
            compile_md(md_file,html_file)
        else:
            generate(sys.argv[1])
