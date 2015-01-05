from PyQt4 import QtGui, QtCore , QtWebKit
from output_ui import Ui_Form
from outputText_ui import Ui_OutWidget
import sys, os, re, webbrowser, time, codecs, datetime

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
            if cmd != 'markdown':
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
                itm.setToolTip(wdg.filename)
                self.ui.li_pages.addItem(itm)
                
    ##            self.ui.sw_pages.setCurrentIndex(sw_ind)
                
                self.wdgD[wdg] = owdg
                self.outD[owdg]=wdg
                
                self.ui.li_pages.setCurrentRow(sw_ind)
                QtGui.QApplication.processEvents()
                owdg.listItem = self.ui.li_pages.item(sw_ind)
                owdg.newProcess(cmd,wdg.filename,args)

    def killAll(self):
        opentxt = ''
        resp = QtGui.QMessageBox.Yes
        for wdg in self.wdgD:
            owdg = self.wdgD[wdg]
            if owdg.process != None:
                opentxt+='<br>'+'&nbsp;'*5+os.path.split(owdg.filename)[1]
                break
                
        if opentxt != '':
            resp=QtGui.QMessageBox.warning(self,'Kill Running Processes','The following output processes are still running:'+opentxt+'<br><br>Do you want to kill all running processes?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                for wdg in self.wdgD:
                    owdg = self.wdgD[wdg]
                    if owdg.process != None:
                        owdg.stopProcess()
        
        # Close all Tabs
        if resp == QtGui.QMessageBox.Yes:
            for wdg in self.wdgD:
##                ind = self.ui.sw_pages.indexOf(owdg)
                owdg = self.wdgD[wdg]
                self.ui.sw_pages.removeWidget(owdg)
            self.ui.li_pages.clear()
            

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
        
        self.ui.b_save.clicked.connect(self.saveFile)
    
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
        txt = "<font color=red>" + str(QtCore.QString(self.process.readAllStandardError()).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))+"</font>"
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
##        curs = self.ui.tb_out.textCursor()
##        curs.movePosition(QtGui.QTextCursor.End,0)
##        self.ui.tb_out.setTextCursor(curs)
##        self.ui.tb_out.append(txt.replace('\n','<br>').replace('<br><br>','<br>'))
        # Append to end without extra line space
        self.ui.tb_out.moveCursor(QtGui.QTextCursor.End)
        self.ui.tb_out.textCursor().insertHtml(txt.replace('\n','<br>'))
        self.ui.tb_out.moveCursor(QtGui.QTextCursor.End)

        
##        self.ui.tb_out.append(txt+QtCore.QString(QtCore.QChar(0x2028)))
       
    def finished(self):
        if self.process != None:
            txt = self.ui.l_title.text()
            self.ui.l_title.setText(txt+'&nbsp;&nbsp;<b>Finished:</b>&nbsp;'+datetime.datetime.now().strftime('%I:%M:%S.%f'))
##            self.appendText('<hr><b>Done</b>&nbsp;&nbsp;'+time.ctime())
        self.process = None
        self.ui.b_run.setEnabled(1)
        self.ui.b_stop.setEnabled(0)
        self.ui.l_title.setStyleSheet('background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(91, 91, 91, 255), stop:0.154545 rgba(129, 129, 129, 255), stop:0.831818 rgba(154, 154, 154, 255), stop:1 rgba(175, 175, 175, 255));color:white;border-top-right-radius:5px;border-top-left-radius:5px;padding:3px;')
        self.ui.tb_out.setStyleSheet('background-color:rgba(240,240,240);border-bottom-left-radius:5px;border-bottom-right-radius:5px;')
    
        # Update list pages
        self.listItem.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
        fnt = self.listItem.font()
        fnt.setItalic(0)
        self.listItem.setFont(fnt)
        
    def newProcess(self,cmd,filename,args=''):
        
        if self.process != None and cmd not in ['webbrowser','markdown']:
            self.stopProcess()
        else:
            self.filename = filename
            if cmd == 'markdown':
                # If markdown generate preview tab
                import plugins.mkdown as mkdown
                html = mkdown.generate(filename,style='',custom=1)
                self.armadillo.webview_preview(html,filename)
                self.ui.tb_out.setPlainText(mkdown.generate(filename))
                self.ui.l_title.setText('<b>&nbsp;'+os.path.split(self.filename)[1])
            else:
                if os.name == 'nt':
                    filename = filename.replace('/','\\')
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
        
        self.ui.l_title.setText('<b>&nbsp;'+os.path.split(self.filename)[1]+'&nbsp;&nbsp;&nbsp;&nbsp;</b><font color=#ccc><b>Started:</b> '+datetime.datetime.now().strftime('%I:%M:%S.%f'))
        self.ui.l_title.setStyleSheet('background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(48, 85, 100, 255), stop:0.21267 rgba(61, 107, 127, 255), stop:0.831818 rgba(72, 127, 150, 255), stop:1 rgba(104, 166, 175, 255));color:white;border-top-right-radius:5px;border-top-left-radius:5px;padding:3px;')
        self.ui.tb_out.setStyleSheet('background-color:white;border-bottom-left-radius:5px;border-bottom-right-radius:5px;')
        self.ui.tb_out.setText('')
        self.listItem.setForeground(QtGui.QBrush(QtGui.QColor(48, 85, 100)))
        fnt = self.listItem.font()
        fnt.setItalic(1)
        self.listItem.setFont(fnt)
        
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
    
    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,"Save Output",self.filename)
        if filename!='':
            txt = self.ui.tb_out.toPlainText()
            txt = str(self.ui.tb_out.toPlainText().toUtf8()).decode('utf-8')
            f = codecs.open(filename,'w','utf8')
            f.write(txt)
            f.close()
