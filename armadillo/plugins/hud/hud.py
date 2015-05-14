from PyQt4 import QtGui, QtCore, QtWebKit
import os

class HUD(object):
    def __init__(self,parent):
        self.armadillo=parent
    
    def toggleHUD(self):
        if self.armadillo.HUDWidget == None:
            # Create hud widget
            from editors.webview import webview
            self.armadillo.HUDWidget=webview.WebView(self.armadillo)
            self.armadillo.HUDWidget.setWindowOpacity(0.6)
            self.armadillo.HUDWidget.setStyleSheet("background:transparent")
            self.armadillo.HUDWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
            self.armadillo.HUDWidget.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            self.armadillo.HUDWidget.linkClicked.connect(self.HUDClicked)

        if self.armadillo.HUDWidget.isVisible():
            self.armadillo.HUDWidget.hide()
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
                file_txt += '<img class="file-icon" src="'+ipth+'"><br>'
                file_txt +=str(self.armadillo.ui.tab.tabText(i))
                file_txt += '</a>'
            
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

                    nfiles += '<a href="new:'+lang+'" title="new '+lang+'" class="newfile"><img class="file-icon" src="'+pfx+icn+'""><br>'+lang+'</a>'
            
            # Generate HTML
            g=self.armadillo.geometry()
            contentD={
                'files':file_txt,
                'height':g.height()/2,
                'new_files':nfiles,
                'current_item':cur_itm
            }
            for ky in contentD:
                txt=txt.replace('{{'+ky+'}}',str(contentD[ky]))
            self.armadillo.HUDWidget.setText(txt)
            
            self.armadillo.HUDWidget.setGeometry(0,0,g.width(),g.height())
            self.armadillo.HUDWidget.show()
            self.armadillo.HUDWidget.setFocus()
    
    def HUDClicked(self,url):
        lnk = str(url.toString())
##        print(lnk)
        if lnk.startswith('opentab:'):
            i=int(lnk.split('opentab:')[1])
            self.armadillo.ui.tab.setCurrentIndex(i)
            self.toggleHUD()
        elif lnk.startswith('new:'):
            lang = lnk.split('new:')[1]
            self.armadillo.addEditorWidget(lang)
            self.toggleHUD()
        
        elif lnk=='close':
            self.toggleHUD()