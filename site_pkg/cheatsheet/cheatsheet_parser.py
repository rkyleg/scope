import os,sys, collections
import codecs, traceback

def parse(filename):
    
    document = collections.OrderedDict()
    
    cur_header = None  # Current Header
    cur_command = None # Current Command
    cur_object = None  # Current Object
    
    with open(filename,'r') as file:
        for line in file:
            if line.startswith('h>'):
                # Header
                hdr = line[2:].strip()
                document[hdr] = collections.OrderedDict()
                cur_header = hdr
                cur_command = None
                cur_object = None
            elif line.startswith('c>'):
                # Command
                cmd = line[2:].strip()
                document[cur_header][cmd]=collections.OrderedDict()
                cur_command = document[cur_header][cmd]
                cur_object = None
            elif line.startswith('d>'):
                # Command Description
                dsc = line[2:].strip()
                cur_command['description'] = dsc
                cur_object = 'd>'
            elif line.startswith('e>'):
                # Examples
                ex = line[2:].strip()
                if 'examples' not in cur_command:
                    cur_command['examples'] = []
                cur_command['examples'].append(ex)
                cur_object = 'e>'
            elif line.startswith('o>'):
                # Options
                op = line[2:].strip()
                if 'options' not in cur_command:
                    cur_command['options']=collections.OrderedDict()
                cur_command['options'][op]=''
                cur_option = op
                cur_object = 'o>'
            elif line.startswith('od>'):
                # Option Description
                opdesc = line[3:].strip()
                cur_command['options'][op]=opdesc
                cur_object = 'od>'
            elif line.startswith('title>'):
                document['title'] = line[6:].strip()
            elif cur_object != None:
                # Command has not closed
                if cur_object == 'd>':
                    # Append to description
                    cur_command['description'] += '\n'+line.rstrip()
                elif cur_object == 'e>':
                    # Append to examples
                    cur_command['examples'][-1] += '\n'+line.rstrip()
                elif cur_object == 'od>':
                    # Append to examples
                    cur_command['options'][cur_option] += '\n'+line.rstrip()
    
    # Cleanup Whitespace
    for hdr in document:
        if hdr != 'title':
            for cmd in document[hdr]:
                if 'description' in document[hdr][cmd]:
                    document[hdr][cmd]['description'] = document[hdr][cmd]['description'].rstrip()
                if 'examples' in document[hdr][cmd]:
                    for e in range(len(document[hdr][cmd]['examples'])):
                        document[hdr][cmd]['examples'][e] = document[hdr][cmd]['examples'][e].rstrip()
    
    return document

def toHtml(document):
    import pystache
    docD = {'sections':[]}
    
    if 'title' in document:
        docD['title'] = document['title']
    
    for hdr in document:
        if hdr != 'title':
            secD = {'title':hdr,'commands':[]}
            for cmd in document[hdr]:
                cmdD = {'cmd':cmd}
                if 'description' in document[hdr][cmd]:
                    cmdD['desc'] = document[hdr][cmd]['description'].replace('\n','<br>').replace('  ',' &nbsp;')
                secD['commands'].append(cmdD)
                if 'examples' in document[hdr][cmd]:
                    cmdD['examples'] = document[hdr][cmd]['examples']
                if 'options' in document[hdr][cmd]:
                    cmdD['options']= [] 
                    for op in document[hdr][cmd]['options']:
                        cmdD['options'].append({'opt':op,'desc':document[hdr][cmd]['options'][op]})
            docD['sections'].append(secD)
    
    
    txt = codecs.open(os.path.join(os.path.dirname(__file__),'cheatsheet.thtml'),'r','utf-8').read()
    u_renderer = pystache.Renderer(string_encoding='utf8')
    html = u_renderer.render(txt,docD)
    return html

if len(sys.argv) > 1:
    import pprint
    flnm = sys.argv[1]
    
    mode='text'
    if 'html' in sys.argv:
        mode = 'html'
    
    result = ''
    
    try:
        if mode == 'text':
            result = parse(flnm)
        elif mode == 'html':
            result = toHtml(parse(flnm))
    ##        print(toHtml(parse(flnm)))
            #.replace('\n','<br>').replace(' ',' &nbsp;')
    except:
##        print('Error parsing file: %s' %'a')
        result = traceback.format_exc()
    
    
    # Compile
    if 'compile' in sys.argv:
        new_file = sys.argv[-1]
        with codecs.open(new_file,'w','utf-8') as file:
            file.write(result)
    else:
        print(result)