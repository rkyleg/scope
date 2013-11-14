from PyQt4 import QtGui, QtCore
from output_ui import Ui_Form
import sys, os, re, webbrowser

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class Output(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
        
        self.process = None

        self.ui.tb_out.setOpenLinks(0)
        self.ui.tb_out.anchorClicked.connect(self.urlClick)
    
    def urlClick(self,url):
        pth = str(url.toString())
        try:
            match   = re_loc.match(pth)
            fileName    = match.group(1)
            lineno      = int(match.group(2))
            self.afide.openFile(fileName)
            self.afide.currentWidget().gotoLine(lineno-1)
        except:
            print('error: could not goto file')
    
    def readOutput(self):
        self.appendText(QtCore.QString(self.process.readAllStandardOutput()))
        
    def readErrors(self):
        txt = "<font color=red>" + str(QtCore.QString(self.process.readAllStandardError()))+"</font><br>"
        txt = re_file.sub(r"<a href='\g<2>'>\g<2></a><br>",txt)
        self.appendText(txt)

    def appendText(self,txt):
        curs = self.ui.tb_out.textCursor()
        curs.movePosition(QtGui.QTextCursor.End,0)
        self.ui.tb_out.setTextCursor(curs)
        self.ui.tb_out.append(txt.replace('\n','<br>'))
       
    def finished(self):
        if self.process != None:
            self.appendText('<hr><b>Done</b>')
        self.process = None
    
    def newProcess(self,cmd,filename):
        
        if self.process != None:
            self.process.kill()
            self.finished()
        else:
            if cmd == 'webbrowser':
                webbrowser.open(filename)
            elif cmd == 'markdown':
                import markdown
                markdown.generate(filename)
            else:
                self.ui.tb_out.setText('<div style="background:rgb(50,50,50);color:white;padding:4px;padding-left:6px;"><b>&nbsp;Start '+filename+'</b></div><br>')
                self.process = QtCore.QProcess()
                self.process.setReadChannel(QtCore.QProcess.StandardOutput)
                self.process.setWorkingDirectory(os.path.dirname(filename))
                self.process.start(cmd,QtCore.QStringList(['-u',filename]))

                self.process.readyReadStandardOutput.connect(self.readOutput)
                self.process.readyReadStandardError.connect(self.readErrors)
                self.process.finished.connect(self.finished)
