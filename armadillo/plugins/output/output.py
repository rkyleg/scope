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
    
    def urlClick(self,url):
        pth = str(url.toString())
        try:
            match   = re_loc.match(pth)
            fileName    = match.group(1)
            lineno      = int(match.group(2))
            self.armadillo.openFile(fileName)
            self.armadillo.currentEditor().gotoLine(lineno-1)
        except:
            print('error: could not goto file')
    
    def readOutput(self):
        txt=QtCore.QString(self.process.readAllStandardOutput().replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))
        self.appendText(txt,plaintext=1)
        
    def readErrors(self):
        txt = "<font color=red>" + str(QtCore.QString(self.process.readAllStandardError()).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))+"</font><br>"
        txt = re_file.sub(r"<a href='\g<2>'>\g<2></a><br>",txt)
        self.appendText(txt)

    def processError(self,err):
        if self.dispError:
            errD = {0:'Failed to Start',1:'Crashed',2:'Timedout',3:'Read Error',4:'Write Error',5:'Unknown Error'}
            errtxt = errD[err]
            txt = "<font color=red>QProcess Error: Process "+errtxt+'</font>'
            self.appendText(txt)
            if self.process != None and self.process.state()==0:
                self.finished()
        
    def appendText(self,txt,plaintext=0):
        curs = self.ui.tb_out.textCursor()
        curs.movePosition(QtGui.QTextCursor.End,0)
        self.ui.tb_out.setTextCursor(curs)
        self.ui.tb_out.append(txt.replace('\n','<br>'))
       
    def finished(self):
        if self.process != None:
            self.appendText('<hr><b>Done</b>&nbsp;&nbsp;'+time.ctime())
        self.process = None
    
    def newProcess(self,cmd,filename,args=[]):
        
        if self.process != None and cmd not in ['webbrowser','markdown']:
            self.dispError = 0
            self.process.kill()
            self.finished()
        else:
            if cmd == 'webbrowser':
                # If webbrowser - launch in webbrowser
                webbrowser.open(filename)
            elif cmd == 'markdown':
                # If markdown generate preview tab
                import plugins.mkdown as mkdown
                html = mkdown.generate(filename)
                self.armadillo.webview_preview(html,filename)
            else:
                self.dispError = 1
                i = self.armadillo.ui.sw_bottom.indexOf(self.armadillo.pluginD['output'])
                self.armadillo.ui.tabbar_bottom.setCurrentIndex(i)
                
                self.ui.tb_out.setText('<div style="background:rgb(50,50,50);color:white;padding:4px;padding-left:6px;"><b>&nbsp;Start '+filename+'</b>&nbsp;&nbsp;'+time.ctime()+'</div><br>')
                self.process = QtCore.QProcess()
                self.process.waitForStarted(5)
                self.process.setReadChannel(QtCore.QProcess.StandardOutput)
                self.process.setWorkingDirectory(os.path.dirname(filename))
                
                self.process.readyReadStandardOutput.connect(self.readOutput)
                self.process.readyReadStandardError.connect(self.readErrors)
                self.process.finished.connect(self.finished)
                self.process.error.connect(self.processError)
                
                
                if os.name == 'nt':
                    filename = filename.replace('/','\\')

                self.process.start(cmd,QtCore.QStringList(args+[filename]))

    def urlClicked(self,url):
        wdg = self.armadillo.ui.sw_main.currentWidget()
        wdg.load2(url)