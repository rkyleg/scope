from PyQt4 import QtGui, QtCore , QtWebKit
from output_ui import Ui_Form
import sys, os, re, webbrowser, time

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class Output(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        
        self.process = None

        self.ui.tb_out.setOpenLinks(0)
        self.ui.tb_out.anchorClicked.connect(self.urlClick)
    
        # Get Command dictionary
        self.runD = {}
        for runs in os.listdir(os.path.join(os.path.dirname(__file__),'run')):
            r = runs.split('.')[0]
            exec('import run.'+r)
            exec('funcs=dir(run.'+r+')')
            if 'cmd' in funcs:
##                print 'self.outlineLangD["'+l+'"]=lang.'+l+'.analyzeLine'
                exec('self.runD["'+r+'"]=run.'+r+'.cmd')
    
    def urlClick(self,url):
        pth = str(url.toString())
        try:
            match   = re_loc.match(pth)
            fileName    = match.group(1)
            lineno      = int(match.group(2))
            self.armadillo.openFile(fileName)
            self.armadillo.currentWidget().gotoLine(lineno-1)
        except:
            print('error: could not goto file')
    
    def readOutput(self):
        self.appendText(QtCore.QString(self.process.readAllStandardOutput().replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;')),plaintext=1)
        
    def readErrors(self):
        txt = "<font color=red>" + str(QtCore.QString(self.process.readAllStandardError()).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))+"</font><br>"
        txt = re_file.sub(r"<a href='\g<2>'>\g<2></a><br>",txt)
        self.appendText(txt)

    def appendText(self,txt,plaintext=0):
        curs = self.ui.tb_out.textCursor()
        curs.movePosition(QtGui.QTextCursor.End,0)
        self.ui.tb_out.setTextCursor(curs)
        self.ui.tb_out.append(txt.replace('\n','<br>'))
##        if plaintext:
##            txt = '<pre>'+txt+'</pre>'
##        else:
##            txt = txt.replace('\n','<br>')
##        curs.insertHtml(txt)
       
    def finished(self):
        if self.process != None:
            self.appendText('<hr><b>Done</b>&nbsp;&nbsp;'+time.ctime())
        self.process = None
    
    def newProcess(self,cmd,filename,args=[]):
        
        if self.process != None and cmd not in ['webbrowser','markdown']:
            self.process.kill()
            self.finished()
        else:
            if cmd == 'webbrowser':
                webbrowser.open(filename)
            elif cmd in self.runD:
                self.runD[cmd](self,filename)
            else:
            
                if not self.armadillo.pluginD['output'].isVisible():
                    self.armadillo.pluginD['output'].show()
                self.armadillo.pluginD['output'].raise_()
                
                self.ui.tb_out.setText('<div style="background:rgb(50,50,50);color:white;padding:4px;padding-left:6px;"><b>&nbsp;Start '+filename+'</b>&nbsp;&nbsp;'+time.ctime()+'</div><br>')
                self.process = QtCore.QProcess()
                self.process.setReadChannel(QtCore.QProcess.StandardOutput)
                self.process.setWorkingDirectory(os.path.dirname(filename))
##                self.process.start(cmd,QtCore.QStringList(['-u',filename]))
                self.process.start(cmd,QtCore.QStringList(args+[filename]))

                self.process.readyReadStandardOutput.connect(self.readOutput)
                self.process.readyReadStandardError.connect(self.readErrors)
                self.process.finished.connect(self.finished)

    def webview_preview(self,html,burl=None):
        openfile = self.armadillo.isFileOpen('preview')
        if openfile==-1:
            wdg = self.armadillo.addEditorWidget('webview','Preview','preview')
            wdg.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            wdg.linkClicked.connect(self.urlClicked)
            self.armadillo.ui.tab.setTabIcon(self.armadillo.ui.tab.currentIndex(),QtGui.QIcon(self.armadillo.iconPath+'page_preview.png'))
    
        else:
            self.armadillo.ui.tab.setCurrentIndex(openfile)
            QtGui.QApplication.processEvents()
            wdg = self.armadillo.ui.sw_main.currentWidget()
        
        if burl != None:
            if os.name =='nt':
                pfx="file:///"
            else:
                pfx="file://"
            burl = QtCore.QUrl(pfx+os.path.abspath(os.path.dirname(burl)).replace('\\','/')+'/')

        wdg.setText(html,burl)

        wdg.viewOnly = 1
        wdg.modTime = None
        QtGui.QApplication.processEvents()
        self.armadillo.changeTab(self.armadillo.ui.tab.currentIndex())
        
    def urlClicked(self,url):
        wdg = self.armadillo.ui.sw_main.currentWidget()
        wdg.load2(url)
##        lnk = str(url.toString())
##        wdg = self.armadillo.ui.sw_main.currentWidget()
##        if lnk.startswith('file:') and lnk.endswith('.md'):
##            filename = str(url.path())
##            import plugins.mkdown as mkdown
##            html = mkdown.generate(filename)
##            self.webview_preview(html,filename)
##        else:
##            wdg.load(url)