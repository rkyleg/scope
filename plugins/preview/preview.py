from PyQt4 import QtGui, QtCore, QtWebKit
from .preview_ui import Ui_Form
from plugins.webview import webview
import re, os, importlib, subprocess, time

class Preview(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ide = parent
        
        self.wdgD={}
        self.prevD={}
        
    def addPreview(self,wdg):
        pwdg = QtGui.QWidget(parent=self)
        
        pwdg.webview = webview.WebView(parent=self.ide)
        layout=QtGui.QGridLayout(pwdg)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        pwdg.setLayout(layout)
        splitter=QtGui.QSplitter(QtCore.Qt.Vertical,self)

        pwdg.layout().addWidget(splitter)
        splitter.addWidget(pwdg.webview)

        pwdg.webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        pwdg.webview.linkClicked.connect(self.urlClicked)
        pwdg.webview.lastScrollValue=0
        pwdg.webview.loadFinished.connect(self.load_finished)
        
        pwdg.webview.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled,True)
        pwdg.webview.settings().setAttribute(QtWebKit.QWebSettings.JavaEnabled,True)
        pwdg.webview.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
        pwdg.webview.settings().setAttribute(QtWebKit.QWebSettings.JavascriptCanOpenWindows,True)
        pwdg.webview.settings().setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled,True)
##        pwdg.webview.settings().setLocalStoragePath(self.ide.settingPath)
##        pwdg.webview.settings().enablePersistentStorage(self.ide.settingPath)
        pwdg.webview.settings().enablePersistentStorage(QtCore.QDir.homePath())
        
        pwdg.webview.setupInspector()
        splitter.addWidget(pwdg.webview.webInspector)
        
        sw_ind = self.ui.sw_prev.count()
        self.ui.sw_prev.insertWidget(sw_ind,pwdg)
        self.ui.sw_prev.setCurrentIndex(sw_ind)

        self.wdgD[wdg] = pwdg
        self.prevD[pwdg]=wdg
    
    def editorTabChanged(self,wdg):
        if wdg in self.wdgD:
            pwdg = self.wdgD[wdg]
            self.ui.sw_prev.setCurrentWidget(pwdg)
##            if self.ide.ui.tab_right.isVisible():
##                self.previewRun(wdg)
        else:
            self.ui.sw_prev.setCurrentIndex(0)
    
    def updatePreview(self,wdg):
        if wdg in self.wdgD:
            if self.wdgD[wdg].isVisible():
                self.previewRun(wdg)
    
    def previewRun(self,wdg,justset=0):
        if wdg not in self.wdgD:
            self.addPreview(wdg)
        else:
            pwdg = self.wdgD[wdg]
            pwdg.webview.lastScrollValue = pwdg.webview.page().currentFrame().scrollBarValue(QtCore.Qt.Vertical)

        pwdg = self.wdgD[wdg]

        burl = wdg.filename
        if wdg.filename == None: burl=''
        if burl != None:
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
##            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(burl)).replace('\\','/')+'/')
            burl = QtCore.QUrl(pfx+os.path.abspath(burl).replace('\\','/'))

        html = wdg.getText()

        cmd=None
##        if 'preview_cmd' in self.ide.settings['prog_lang'][wdg.lang]:
        if 'run' in self.ide.settings['prog_lang'][wdg.lang]:
            pcmd=self.ide.settings['prog_lang'][wdg.lang]['run'].split('preview ')
            if len(pcmd)>1:
                cmd = pcmd[1]

        if cmd == 'markdown':
            # If markdown generate preview tab
            import site_pkg.commonmark as commonmark
            html = commonmark.generate(text=html,style='',custom=0)
##                self.ide.webview_preview(html,filename)

        elif cmd != None:
            if '{{filename}}' in cmd:
                fcmd = cmd.replace('{{filename}}',wdg.filename)
            else:
                fcmd = cmd+' '+wdg.filename
            
            html = subprocess.check_output(fcmd,shell=True)
            
        pwdg.webview.setText(html,burl)
        if html != '':
            self.ide.pluginD['output'].widget.runProcess('preview',wdg,text=html,justset=justset)
            self.ide.prevPlugin=self.ide.ui.sw_bottom.indexOf(self.ide.pluginD['output'].widget)
            
##        QtGui.QApplication.processEvents()
##        time.sleep(0.01)
##        pwdg.page().currentFrame().setScrollBarValue(QtCore.Qt.Vertical,sbv)

        
    def editorTabClosed(self,wdg):
        if wdg in self.wdgD:
            pwdg = self.wdgD[wdg]
            self.wdgD.pop(wdg)
            self.ui.sw_prev.removeWidget(pwdg)
            pwdg.deleteLater()
            del pwdg
    
    def load_finished(self):
        pwdg = self.ui.sw_prev.currentWidget()
        if 'webview' in dir(pwdg):
            pwdg.webview.page().currentFrame().setScrollBarValue(QtCore.Qt.Vertical,pwdg.webview.lastScrollValue)
    
    def urlClicked(self,url):
        lnk = str(url.toString())
        pwdg = self.ui.sw_prev.currentWidget()
            # Markdown
        if lnk.startswith('file:') and lnk.endswith('.md'):
            filename = str(url.toLocalFile())
            import site_pkg.commonmark as commonmark
            html = commonmark.generate(filename,custom=1)
            
            burl = url
            pwdg.webview.setText(html,burl)
            
        elif lnk.startswith('http') or lnk.startswith('www'):
            # External links
            import webbrowser
            webbrowser.open(lnk)
        else:
            pwdg.webview.load_link(url)