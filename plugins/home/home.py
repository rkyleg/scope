from PyQt4 import QtGui, QtCore, QtWebKit
import os

class Home(object):
    def __init__(self,parent):
        self.IDE=parent
    
        # Create home widget
        from plugins.webview import webview
        self.webview=webview.WebView(self.IDE)
    
        self.webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webview.linkClicked.connect(self.homeClicked)

##        self.webview.setupInspector()
        self.webview.filename = None
        self.webview.contextMenuEvent = self.contextMenuEvent
    
    def toggleHome(self,visible=None):
            self.viewHome()
            self.IDE.ui.sw_main.setCurrentWidget(self.webview)
            
            # Toggle Filebrowser too
            if 'filebrowser' in self.IDE.pluginD:
                self.IDE.pluginD['filebrowser'].toggle()
            
    def viewHome(self):
            cur_itm=0
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            
            f = open(self.IDE.scopePath+'/plugins/home/home.html','r')
            txt=f.read()
            f.close()
            
            # Get Open Files
            file_txt = ''
            
             # Add New File Links
            nfiles = ''
            for lang in sorted(self.IDE.settings['prog_lang']):
                if lang != 'default' and self.IDE.settings['prog_lang'][lang]['fave']:
                    icn = None
                    if os.path.exists(self.IDE.iconPath+'files/'+lang+'.png'):
                        icn = self.IDE.iconPath+'files/'+lang+'.png'
                    # Set default Icon if language not found
                    if icn == None:
                        icn = self.IDE.iconPath+'files/_blank.png'

                    nfiles += '<a href="new:'+lang+'" title="new '+lang+'" class="newfile"><img class="file-icon" src="'+pfx+icn+'""> '+lang+'</a>'
            
            # Grab Editors
            neditors=''
            for e in sorted(self.IDE.editorD):
                ld = self.IDE.editorD[e]
                neditors+='<a href="editor:'+e+'"><div class="newfile"><img src="'+self.IDE.editorPath+'/'+e+'/'+e+'.png'+'" class="file-icon"> ' +e+'</div></a>'
            
            # Add Workspaces
            wksp = ''
            icn_wksp = self.IDE.iconPath+'workspace.png'
            if os.path.exists(self.IDE.settingPath+'/workspaces'):
                for w in sorted(os.listdir(self.IDE.settingPath+'/workspaces'),key=lambda x: x.lower()):
                    wksp += '<a href="workspace:'+w+'"><div class="newfile"><img class="file-icon" src="'+icn_wksp+'"> '+w+'</div></a> '

            cur_wksp = self.IDE.currentWorkspace
            if cur_wksp == None: cur_wksp = ''
            
            # Generate HTML
            g=self.IDE.geometry()
            contentD={
                'files':file_txt,
                'height':g.height()/2,
                'new_files':nfiles,
                'new_editors':neditors,
                'current_item':cur_itm,
                'version':self.IDE.version,
                'workspaces':wksp,
                'workspace':cur_wksp,
            }
            for ky in contentD:
                txt=txt.replace('{{'+ky+'}}',str(contentD[ky]))
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/'))
            self.webview.setText(txt,burl)
            
            # Background Image
            if 'home' in self.IDE.settings['plugins'] and 'backgroundImage' in self.IDE.settings['plugins']['home']:
                if self.IDE.settings['plugins']['home']['backgroundImage'] != '':
                    bkimgtxt = 'document.body.style.backgroundImage = "url(\''+self.IDE.settings['plugins']['home']['backgroundImage']+'\')";'
                    self.webview.page().mainFrame().evaluateJavaScript(bkimgtxt)
            
            self.webview.show()
            self.webview.setFocus()
    
    def homeClicked(self,url):
        lnk = str(url.toString()).split('/')[-1]
        
        if lnk.startswith('home:'):
            self.viewHome()
        elif lnk.startswith('new:'):
            lang = lnk.split('new:')[1]
            self.IDE.addEditorWidget(lang)
        elif lnk.startswith('workspace:'):
            wk = lnk.split('workspace:')[1]
            if wk=='new':
                self.IDE.workspaceNew()
                self.IDE.showHome()
            else:
                self.IDE.workspaceOpen(wk)
        elif lnk.startswith('editor:'):
            e = lnk.split('editor:')[1]
            ld = self.IDE.editorD[e]
            # Show Editor Menu
            lmenu = QtGui.QMenu()
            for l in ld:
                if os.path.exists(self.IDE.iconPath+'/files/'+l.lower()+'.png'):
                    icn = QtGui.QIcon(self.IDE.iconPath+'/files/'+l.lower()+'.png')
                else:
                    icn = QtGui.QIcon(self.IDE.iconPath+'/files/_blank.png')
                a=lmenu.addAction(icn,l)
                a.setData(e)
            
            resp = lmenu.exec_(self.webview.cursor().pos())
            
            if resp != None:
                self.IDE.addEditorWidget(str(resp.text()),editor=e)
        
        elif lnk=='filebrowser':
            self.IDE.openFile()
        elif lnk=='settings':
            self.IDE.openSettings()
        else:
            self.webview.load_help(url)
    
    def resize(self):
        g=self.IDE.geometry()
        if self.webview != None:
            self.webview.setGeometry(0,0,g.width(),g.height())
            
            g = self.webview.geometry()
            self.webview.webInspector.setGeometry(0,g.bottom()-300,g.width(),300)

    def contextMenuEvent(self,event):
        pass