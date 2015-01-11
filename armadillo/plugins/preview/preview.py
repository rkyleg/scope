from PyQt4 import QtGui, QtCore, QtWebKit
from preview_ui import Ui_Form
from editors.webview import webview
import re, os, importlib, subprocess, time

class Preview(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        
        self.wdgD={}
        self.prevD={}
        
    def addPreview(self,wdg):
        
##        if wdg.lang in ['html','markdown']:
        pwdg = webview.WebView(self)
##        if wdg.filename !=None:
##            pwdg.setHtml(wdg.filename)
        pwdg.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        pwdg.linkClicked.connect(self.urlClicked)
        pwdg.lastScrollValue=0
        pwdg.loadFinished.connect(self.load_finished)
        sw_ind = self.ui.sw_prev.count()
        self.ui.sw_prev.insertWidget(sw_ind,pwdg)
        self.ui.sw_prev.setCurrentIndex(sw_ind)

        self.wdgD[wdg] = pwdg
        self.prevD[pwdg]=wdg
            
##            self.previewRun(wdg)
    
    def editorTabChanged(self,wdg):
        if wdg in self.wdgD:
            pwdg = self.wdgD[wdg]
            self.ui.sw_prev.setCurrentWidget(pwdg)
            if self.armadillo.ui.tab_right.isVisible():
                self.previewRun(wdg)
        else:
            self.ui.sw_prev.setCurrentIndex(0)
            
    def previewRun(self,wdg):
        if wdg not in self.wdgD:
            self.addPreview(wdg)
        else:
            pwdg = self.wdgD[wdg]
            pwdg.lastScrollValue = pwdg.page().currentFrame().scrollBarValue(QtCore.Qt.Vertical)

        pwdg = self.wdgD[wdg]

        burl = wdg.filename
        if wdg.filename == None: burl=''
        if burl != None:
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(burl)).replace('\\','/')+'/')

        html = wdg.getText()

        cmd=None
        if 'preview_cmd' in self.armadillo.settings['prog_lang'][wdg.lang]:
            cmd=self.armadillo.settings['prog_lang'][wdg.lang]['preview_cmd']

        if cmd == 'markdown':
            # If markdown generate preview tab
            import plugins.mkdown as mkdown
            html = mkdown.generate(text=html,style='',custom=1)
##                self.armadillo.webview_preview(html,filename)

##            self.armadillo.pluginD['output'].newProcess('markdown',wdg)
        elif cmd != None:
            html = subprocess.check_output(cmd+' '+wdg.filename,shell=True)
        pwdg.setText(html,burl)
##        QtGui.QApplication.processEvents()
##        time.sleep(0.01)
##        pwdg.page().currentFrame().setScrollBarValue(QtCore.Qt.Vertical,sbv)

        
    def editorTabClosed(self,wdg):
        if wdg in self.wdgD:
            pwdg = self.wdgD[wdg]
            self.wdgD.pop(wdg)
            self.ui.sw_prev.removeWidget(pwdg)
    
    def load_finished(self):
        pwdg = self.ui.sw_prev.currentWidget()
        pwdg.page().currentFrame().setScrollBarValue(QtCore.Qt.Vertical,pwdg.lastScrollValue)
    
    def urlClicked(self,url):
        lnk = str(url.toString())
        pwdg = self.ui.sw_prev.currentWidget()
            # Markdown
        if lnk.startswith('file:') and lnk.endswith('.md'):
            filename = str(url.toLocalFile())
            import plugins.mkdown as mkdown
            html = mkdown.generate(filename,custom=1)
            
            burl = url
            pwdg.setText(html,burl)
            
        elif lnk.startswith('http') or lnk.startswith('www'):
            # External links
            import webbrowser
            webbrowser.open(lnk)
        else:
            pwdg.load(url)