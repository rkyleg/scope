from PyQt4 import QtGui, QtCore, QtWebKit
import os

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self,parent):
        QtCore.QObject.__init__(self)
        self.parent = parent
    
    @QtCore.pyqtSlot()
    def closeHome(self):
        pass
    
    @QtCore.pyqtSlot('int')
    def closetab(self,id):
        ok = self.parent.IDE.closeTab(id)
        if ok:
            cid = str(self.parent.IDE.currentEditor().id)
            QtGui.QApplication.processEvents()
            self.parent.webview.page().mainFrame().evaluateJavaScript('closetab('+str(id)+');highlighttab("'+cid+'");')
        return ok
    
    def highlighttab(self,id):
        self.parent.webview.page().mainFrame().evaluateJavaScript('highlightTab("'+id+'");')
    
    @QtCore.pyqtSlot('int')
    def opentab(self,id):
        self.parent.IDE.changeTab(id)

class Home(object):
    def __init__(self,parent):
        self.IDE=parent
    
        # Create home widget
        from plugins.webview import webview
        self.webview=webview.WebView(self.IDE)
    
        self.webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webview.linkClicked.connect(self.homeClicked)

        self.webview.setupInspector()
        self.webview.filename = None

        self.jsObject = jsObject(parent=self)

    
    def toggleHome(self,visible=None):
            self.viewHome()
            self.IDE.ui.sw_main.setCurrentWidget(self.webview)
            
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
    ##                wksp += '<a href="workspace:'+w+'"><span class="workspace"><span class="workspace_title">'+w+'</span><br><table width=100%><tr><td class="blueblob">&nbsp;&nbsp;</td><td width=100%><hr class="workspaceline"><hr class="workspaceline"></td></tr></table></span></a> '
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
            
            if file_txt == '':
                self.webview.page().mainFrame().evaluateJavaScript("document.getElementById('open_files').style.display='none';")
            
            self.webview.page().mainFrame().addToJavaScriptWindowObject('HOME',self.jsObject)
            self.webview.show()
            self.webview.setFocus()
    
    def homeClicked(self,url):
        lnk = str(url.toString()).split('/')[-1]
##        print(lnk)
        if lnk.startswith('opentab:'):
            i=int(lnk.split('opentab:')[1])
            self.IDE.changeTab(i)
        elif lnk.startswith('closetab:'):
            i=int(lnk.split('closetab:')[1])
            self.IDE.closeTab(i)
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
##            self.IDE.openSettings()
            self.IDE.openFile(self.IDE.settings_filename)
        else:
            self.webview.load2(url)
    
    def resize(self):
        g=self.IDE.geometry()
        if self.webview != None:
            self.webview.setGeometry(0,0,g.width(),g.height())
            
            g = self.webview.geometry()
            self.webview.webInspector.setGeometry(0,g.bottom()-300,g.width(),300)
