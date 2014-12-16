from PyQt4 import QtGui, QtCore , QtWebKit
from output_ui import Ui_Form
from outputText_ui import Ui_OutWidget
import sys, os, re, webbrowser, time

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class Output(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        
        self.wdgD = {}
        self.outD = {}
        
        self.ui.split_pages.setSizes([200,self.armadillo.width()-200])

    def editorTabChanged(self,wdg):
        if wdg in self.wdgD:
            owdg = self.wdgD[wdg]
            self.ui.li_pages.setCurrentRow(self.ui.sw_pages.indexOf(owdg))
    
    def newProcess(self,cmd,wdg,args=''):
        if cmd == 'webbrowser':
            # If webbrowser - launch in webbrowser
            webbrowser.open(wdg.filename)
        else:
            i = self.armadillo.ui.sw_bottom.indexOf(self.armadillo.pluginD['output'])
            self.armadillo.ui.tabbar_bottom.setCurrentIndex(i)
            if wdg in self.wdgD:
                owdg = self.wdgD[wdg]
                owdg.newProcess(cmd,wdg.filename,args)
                
                self.ui.li_pages.setCurrentRow(self.ui.sw_pages.indexOf(owdg))
                
            else:
                owdg = OutputPage(parent=self,armadillo=self.armadillo)
                sw_ind = self.ui.sw_pages.count()
                self.ui.sw_pages.insertWidget(sw_ind,owdg)
                itm = QtGui.QListWidgetItem(wdg.title)
                itm.setIcon(wdg.icon)
                self.ui.li_pages.addItem(itm)
                
    ##            self.ui.sw_pages.setCurrentIndex(sw_ind)
                
                self.wdgD[wdg] = owdg
                self.outD[owdg]=wdg
                
                self.ui.li_pages.setCurrentRow(sw_ind)
                QtGui.QApplication.processEvents()
                owdg.newProcess(cmd,wdg.filename,args)

    def killAll(self):
        open = 0
        resp = QtGui.QMessageBox.Yes
        for wdg in self.wdgD:
            owdg = self.wdgD[wdg]
            if owdg.process != None:
                open=1
                break
        if open:
            resp=QtGui.QMessageBox.warning(self,'Kill Running Processes','There are still some output processes running.<br><br>Do you want to kill all running processes?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                for wdg in self.wdgD:
                    owdg = self.wdgD[wdg]
                    if owdg.process != None:
                        owdg.stopProcess()
        
        # Close all Tabs
        if resp == QtGui.QMessageBox.Yes:
            for wdg in self.wdgD:
                ind = self.ui.sw_pages.indexOf(owdg)
                self.ui.sw_pages.removeWidget(owdg)
                self.ui.li_pages.takeItem(ind)
            

class OutputPage(QtGui.QWidget):
    def __init__(self,parent=None,armadillo=None):
        QtGui.QWidget.__init__(self,parent)
        curdir = os.path.abspath('.')
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        self.ui = Ui_OutWidget()
        self.ui.setupUi(self)
        os.chdir(curdir)
        self.armadillo = armadillo
        self.parent = parent
        
        self.process = None
        self.ui.fr_cmd.hide()
        
        self.ui.tb_out.setOpenLinks(0)
        self.ui.tb_out.anchorClicked.connect(self.urlClick)
        
        self.ui.b_run.setEnabled(0)
        self.ui.b_stop.setEnabled(0)
        
        self.ui.b_run.clicked.connect(self.startProcess)
        self.ui.b_stop.clicked.connect(self.stopProcess)
    
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
##        QtGui.QApplication.processEvents()
        
    def readErrors(self):
        txt = "<font color=red>" + str(QtCore.QString(self.process.readAllStandardError()).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))+"</font><br>"
        txt = re_file.sub(r"<a href='\g<2>'>\g<2></a>",txt)
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
        self.ui.tb_out.append(txt)#.replace('\n','<br>'))
       
    def finished(self):
        if self.process != None:
            self.appendText('<hr><b>Done</b>&nbsp;&nbsp;'+time.ctime())
        self.process = None
        self.ui.b_run.setEnabled(1)
        self.ui.b_stop.setEnabled(0)
    
    def newProcess(self,cmd,filename,args=''):
        
        if self.process != None and cmd not in ['webbrowser','markdown']:
            self.stopProcess()
        else:
            if cmd == 'markdown':
                # If markdown generate preview tab
                import plugins.mkdown as mkdown
                html = mkdown.generate(filename,custom=1)
                self.armadillo.webview_preview(html,filename)
                self.ui.tb_out.setPlainText(mkdown.generate(filename))
            else:
                if os.name == 'nt':
                    filename = filename.replace('/','\\')
                self.filename = filename
                xcmd = cmd
                if args != '':
                    xcmd += ' '+args
                self.ui.le_cmd.setText(xcmd)
##                self.ui.le_args.setText(str(args))
##                self.args = str(args)
                self.startProcess()
    
    def startProcess(self):
        self.ui.b_run.setEnabled(0)
        self.ui.b_stop.setEnabled(1)
        self.dispError = 1
        
        self.ui.tb_out.setText('<div style="background:rgb(50,50,50);color:white;padding:4px;padding-left:6px;"><b>&nbsp;Start '+self.filename+'</b>&nbsp;&nbsp;'+time.ctime()+'</div><br>')
        self.process = QtCore.QProcess()
        self.process.waitForStarted(5)
        self.process.setReadChannel(QtCore.QProcess.StandardOutput)
        self.process.setWorkingDirectory(os.path.dirname(self.filename))
        
        self.process.readyReadStandardOutput.connect(self.readOutput)
        self.process.readyReadStandardError.connect(self.readErrors)
        self.process.finished.connect(self.finished)
        self.process.error.connect(self.processError)
        
        args = str(self.ui.le_args.text())
        cmd = str(self.ui.le_cmd.text())
        if args != '': args = ' '+args
        
##        self.process.start(cmd,QtCore.QStringList(args.split()+[self.filename]))
##        print cmd+' "'+self.filename+'"'+args
        self.process.start(cmd+' "'+self.filename+'"'+args)
##        self.process.start(cmd+' '+self.filename+args)
    
    def stopProcess(self):
        self.dispError = 0
        self.process.kill()
        self.finished()
    
    def urlClicked(self,url):
        wdg = self.armadillo.ui.sw_main.currentWidget()
        wdg.load2(url)