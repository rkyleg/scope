from PyQt4 import QtGui, QtCore, QtWebKit
import os

class jsObject(QtCore.QObject):
    filePath = ''
    def __init__(self,parent):
        QtCore.QObject.__init__(self)
        self.parent = parent
    
    @QtCore.pyqtSlot()
    def closeHUD(self):
##        print 'close hud'
        self.parent.toggleHUD()

class HUD(object):
    def __init__(self,parent):
        self.armadillo=parent
        self.armadillo.evnt.resized.connect(self.resize)
    
        # Create hud widget
        from editors.webview import webview
        self.webview=webview.WebView(self.armadillo)
        self.webview.setWindowOpacity(0.6)
        self.webview.setStyleSheet("QWebView{background:transparent}")
        self.webview.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    
        self.webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        self.webview.linkClicked.connect(self.HUDClicked)

        self.jsObject = jsObject(parent=self)
    
    def toggleHUD(self):
##        if self.webview == None:


        if self.webview.isVisible():
            self.webview.hide()
        else:
            cur_itm=0
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            
            f = open(self.armadillo.armadilloPath+'/plugins/hud/HUD.html','r')
            txt=f.read()
            f.close()
            
            # Get Open Files
            file_txt = ''
            for i in range(self.armadillo.ui.tab.count()):
                t = int(self.armadillo.ui.tab.tabData(i).toInt()[0])
                wdg = self.armadillo.tabD[t]
                lang = wdg.lang
                filename = str(self.armadillo.ui.tab.tabText(t))
                # Icon
                ipth = self.armadillo.iconPath+'/files/_blank.png'
                fipth = self.armadillo.iconPath+'files/'+str(lang)+'.png'
                if os.path.exists(fipth):
                    ipth = fipth
                elif filename != None:
                    ext = os.path.splitext(filename)[1][1:]
                    if os.path.exists(self.armadillo.iconPath+'files/'+ext+'.png'):
                        ipth = self.armadillo.iconPath+'files/'+ext+'.png'
                elif os.path.exists(self.armadillo.editorPath+editor+'/'+editor+'.png'):
                    ipth = self.armadillo.editorPath+editor+'/'+editor+'.png'

                ipth = pfx+ipth
                
                cls=''
                if i == self.armadillo.ui.tab.currentIndex():
                    cls='current'
                    cur_itm=i
                
                file_txt += '<a href="opentab:'+str(i)+'" class="file '+cls+'" id="'+str(i)+'">'
                file_txt += '<img class="file-icon" src="'+ipth+'"> '
                file_txt +=str(self.armadillo.ui.tab.tabText(i))
##                file_txt += ' <a href="closetab:'+str(i)+'"><img alt="" src="../img/close.png" /></a>'
                file_txt += '</a>'
##                print file_txt
            
             # Add New File Links
            nfiles = ''
            for lang in sorted(self.armadillo.settings['prog_lang']):
                if lang != 'default' and self.armadillo.settings['prog_lang'][lang]['fave']:
                    icn = None
                    if os.path.exists(self.armadillo.iconPath+'files/'+lang+'.png'):
                        icn = self.armadillo.iconPath+'files/'+lang+'.png'
                    # Set default Icon if language not found
                    if icn == None:
                        icn = self.armadillo.iconPath+'files/_blank.png'

                    nfiles += '<a href="new:'+lang+'" title="new '+lang+'" class="newfile"><img class="file-icon" src="'+pfx+icn+'""> '+lang+'</a>'
            
            # Grab Editors
            neditors=''
            for e in sorted(self.armadillo.editorD):
                ld = self.armadillo.editorD[e]
                neditors+='<a href="editor:'+e+'"><div class="newfile"><img src="'+self.armadillo.editorPath+'/'+e+'/'+e+'.png'+'" class="file-icon"> ' +e+'</div></a>'
            
            # Add Workspaces
            wksp = ''
            icn_wksp = pfx+os.path.abspath('img/workspace.png').replace('\\','/')
            if os.path.exists(self.armadillo.settingPath+'/workspaces'):
                for w in sorted(os.listdir(self.armadillo.settingPath+'/workspaces'),key=lambda x: x.lower()):
    ##                wksp += '<a href="workspace:'+w+'"><span class="workspace"><span class="workspace_title">'+w+'</span><br><table width=100%><tr><td class="blueblob">&nbsp;&nbsp;</td><td width=100%><hr class="workspaceline"><hr class="workspaceline"></td></tr></table></span></a> '
                    wksp += '<a href="workspace:'+w+'"><div class="newfile"><img src="'+icn_wksp+'"> '+w+'</div></a> '

            cur_wksp = self.armadillo.workspace
            if cur_wksp == None: cur_wksp = ''
            
            # Generate HTML
            g=self.armadillo.geometry()
            contentD={
                'files':file_txt,
                'height':g.height()/2,
                'new_files':nfiles,
                'new_editors':neditors,
                'current_item':cur_itm,
                'version':self.armadillo.version,
                'workspaces':wksp,
                'workspace':cur_wksp,
            }
            for ky in contentD:
                txt=txt.replace('{{'+ky+'}}',str(contentD[ky]))
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(__file__)).replace('\\','/'))
            self.webview.setText(txt,burl)
            
            if file_txt == '':
                self.webview.page().mainFrame().evaluateJavaScript("document.getElementById('open_files').style.display='none';")
            
            self.webview.page().mainFrame().addToJavaScriptWindowObject('HUD',self.jsObject)
            
            self.webview.setGeometry(0,0,g.width(),g.height())
            self.webview.show()
            self.webview.setFocus()
    
    def HUDClicked(self,url):
        lnk = str(url.toString()).split('/')[-1]
##        print(lnk)
        if lnk.startswith('opentab:'):
            i=int(lnk.split('opentab:')[1])
            self.armadillo.ui.tab.setCurrentIndex(i)
            self.toggleHUD()
        elif lnk.startswith('closetab:'):
            i=int(lnk.split('closetab:')[1])
            self.armadillo.closeTab(i)
        elif lnk.startswith('new:'):
            lang = lnk.split('new:')[1]
            self.armadillo.addEditorWidget(lang)
            self.toggleHUD()
        elif lnk.startswith('workspace:'):
            wk = lnk.split('workspace:')[1]
            if wk=='new':
                self.armadillo.newWorkspace()
##                self.addStart(wdg=wdg)
            else:
                self.armadillo.loadWorkspace(wk)
##            self.toggleHUD()
        elif lnk.startswith('editor:'):
            e = lnk.split('editor:')[1]
            ld = self.armadillo.editorD[e]
            # Show Editor Menu
            lmenu = QtGui.QMenu()
            for l in ld:
                if os.path.exists(self.armadillo.iconPath+'/files/'+l.lower()+'.png'):
                    icn = QtGui.QIcon(self.armadillo.iconPath+'/files/'+l.lower()+'.png')
                else:
                    icn = QtGui.QIcon(self.armadillo.iconPath+'/files/_blank.png')
                a=lmenu.addAction(icn,l)
                a.setData(e)
            
            resp = lmenu.exec_(self.webview.cursor().pos())
            
            if resp != None:
                self.armadillo.addEditorWidget(str(resp.text()),editor=e)
                self.toggleHUD()
        
        elif lnk=='filebrowser':
            self.armadillo.openFile()
##            self.toggleHUD()
        elif lnk=='settings':
            self.armadillo.openSettings()
            
        elif lnk=='close':
            self.toggleHUD()
    
    def resize(self):
        g=self.armadillo.geometry()
        if self.webview != None:
            self.webview.setGeometry(0,0,g.width(),g.height())