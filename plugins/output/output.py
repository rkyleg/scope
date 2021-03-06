from PyQt4 import QtGui, QtCore , QtWebKit
from .output_ui import Ui_Form
from .outputText_ui import Ui_OutWidget
import sys, os, re, webbrowser, time, codecs, datetime

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class Output(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ide = parent
        
        self.wdgD = {}
        
        self.ui.split_pages.setSizes([200,self.ide.width()-200])
        
        self.ui.li_pages.contextMenuEvent = self.listMenuEvent

    def editorTabChanged(self,wdg):
        if wdg.id in self.wdgD:
            owdg = self.wdgD[wdg.id]
            self.ui.li_pages.setCurrentRow(self.ui.sw_pages.indexOf(owdg))
    
    def editorTabClosed(self,wdg):
        if wdg.id in self.wdgD:
            owdg = self.wdgD[wdg.id]
            self.closeOutputWidget(owdg)

    def closeOutputWidget(self,owdg):
        ok=1
        if owdg.status != 'done':
            ok=0
            opentxt=os.path.split(owdg.filename)[1]
            resp=QtGui.QMessageBox.warning(self,'Kill Running Proces','The following output process is still running:'+opentxt+'<br><br>Do you want to kill it?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                owdg.stopProcess()
                ok=1
        if ok:
            self.wdgD.pop(owdg.file_id)
            self.ui.li_pages.takeItem(self.ui.li_pages.row(owdg.listItem))
            self.ui.sw_pages.removeWidget(owdg)
    
    def runProcess(self,cmd,wdg,text='',typ='run',args={},justset=0):
        if cmd == 'webbrowser':
            # If webbrowser - launch in webbrowser
            webbrowser.open(wdg.filename)
        else:
            # Setup the Command
            full_cmd = cmd
            if '{{filename}}' in cmd:
                full_cmd = cmd.replace('{{filename}}',' "'+wdg.filename+'"')
            else:
                if wdg.filename != None:
                    full_cmd = cmd+' "'+wdg.filename+'"'
            if 'new_file' in args:
                full_cmd = full_cmd.replace('{{new_file}}',args['new_file'])
            
            if cmd != 'preview' or justset:
                i = self.ide.ui.sw_bottom.indexOf(self.ide.pluginD['output'].widget)
                self.ide.ui.tabbar_bottom.setCurrentIndex(i)
            if wdg.id in self.wdgD:
                # Process was run
                owdg = self.wdgD[wdg.id]
                self.ui.li_pages.setCurrentRow(self.ui.sw_pages.indexOf(owdg))
                if owdg.process_type != typ:
                    # Update information if process is different
                    if owdg.status != 'done':
                        owdg.stopProcess()
                    owdg.ui.le_cmd.setText(full_cmd)
                    
            else:
                # Create new process
                owdg = OutputPage(parent=self,ide=self.ide,filename=wdg.filename)
                owdg.ui.le_cmd.setText(full_cmd)
                sw_ind = self.ui.sw_pages.count()
                self.ui.sw_pages.insertWidget(sw_ind,owdg)
                itm = QtGui.QListWidgetItem(wdg.title)
                itm.setIcon(wdg.icon)
                if wdg.filename != None:
                    itm.setToolTip(wdg.filename)
                self.ui.li_pages.addItem(itm)

                self.wdgD[wdg.id] = owdg
                owdg.file_id = wdg.id
                owdg.process_type = typ
                
                self.ui.li_pages.setCurrentRow(sw_ind)
                QtGui.QApplication.processEvents()
                owdg.listItem = self.ui.li_pages.item(sw_ind)
            
            owdg.process_type = typ
            
            # Toggle/Run Process
            if cmd=='preview' and not justset:
                owdg.setOutputText(text=text)
                if wdg.filename==None:
                    title = wdg.title
                else:
                    title = os.path.split(wdg.filename)[1]
                owdg.ui.l_title.setText('<b>&nbsp;'+title+'</b>')
            else:
                # Just set the command, don't run
                if justset:
                    owdg.ui.le_cmd.setText(cmd)
                    owdg.ui.b_cmd.setChecked(1)
                    if not owdg.ui.b_stop.isEnabled():
                        owdg.ui.b_run.setEnabled(1)
                else:
                    owdg.toggleProcess()

    def killAll(self):
        opentxt = ''
        resp = QtGui.QMessageBox.Yes
        for wdg.id in self.wdgD:
            owdg = self.wdgD[wdg.id]
            if owdg.status != 'done':
                opentxt+='<br>'+'&nbsp;'*5+os.path.split(owdg.filename)[1]
                break
                
        if opentxt != '':
            resp=QtGui.QMessageBox.warning(self,'Kill Running Processes','The following output processes are still running:'+opentxt+'<br><br>Do you want to kill all running processes?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                for wdg.id in self.wdgD:
                    owdg = self.wdgD[wdg.id]
                    if owdg.status != 'done':
                        owdg.stopProcess()
        
        # Close all Tabs
        if resp == QtGui.QMessageBox.Yes:
            for wdg.id in self.wdgD:
                owdg = self.wdgD[wdg.id]
                self.ui.sw_pages.removeWidget(owdg)
            self.ui.li_pages.clear()
            
    def listMenuEvent(self,event):
        cwdg = self.ui.sw_pages.currentWidget()
        menu = QtGui.QMenu()
        if cwdg.status != 'done':
            menu.addAction(QtGui.QIcon(self.ide.pluginPath+'output/stop.png'),'Stop')
        else:
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'tri_right.png'),'Run')
            menu.addAction(QtGui.QIcon(self.ide.iconPath+'close.png'),'Close')
        
        resp = menu.exec_(event.globalPos())
        if resp != None:
            txt = str(resp.text())
            if txt == 'Close':
                self.closeOutputWidget(cwdg)
            elif txt == 'Stop':
                cwdg.stopProcess()
            elif txt == 'Run':
                cwdg.startProcess()

class OutputPage(QtGui.QWidget):
    def __init__(self,parent=None,ide=None,filename=None):
        QtGui.QWidget.__init__(self,parent)
        curdir = os.path.abspath('.')
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        self.ui = Ui_OutWidget()
        self.ui.setupUi(self)
        os.chdir(curdir)
        self.ide = ide
        self.parent = parent
        self.filename = filename
        
        self.process = None
        self.status = 'done'
        self.process_type = 'run'
        self.ui.fr_cmd.hide()
        self.ui.fr_cmdw.hide()
        
        self.ui.tb_out.setOpenLinks(0)
        self.ui.tb_out.anchorClicked.connect(self.urlClick)
        
        self.ui.b_run.setEnabled(0)
        self.ui.b_stop.setEnabled(0)
        
        self.ui.b_run.clicked.connect(self.startProcess)
        self.ui.b_stop.clicked.connect(self.stopProcess)
        
        self.ui.b_save.clicked.connect(self.saveFile)
        
        self.ui.le_cmdw.returnPressed.connect(self.writeProcess)
    
    def urlClick(self,url):
        pth = str(url.toString())
        try:
            match   = re_loc.match(pth)
            fileName    = match.group(1)
            lineno      = int(match.group(2))
            self.ide.openFile(fileName)
            self.ide.currentEditor().gotoLine(lineno-1)
        except:
            print('error: could not goto file')
    
    def readOutput(self):
        txt=QtCore.QString(self.process.readAllStandardOutput().replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))
        self.appendText(txt,plaintext=1)
        
    def readErrors(self):
        txt = '<font style="color:rgb(255,112,99);">' + str(QtCore.QString(self.process.readAllStandardError()).toUtf8().replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;'))+"</font>"
        txt = re_file.sub(r"<a style=""color:rgb(121,213,255);"" href='\g<2>'>\g<2></a>",txt)
        self.appendText(txt)

    def processError(self,err):
        print('process error',err,self.status,self.process.state())
        if self.dispError:
            errD = {0:'Failed to Start',1:'Crashed',2:'Timedout',3:'Read Error',4:'Write Error',5:'Unknown Error'}
            errtxt = errD[err]
            txt = '<font style="color:rgb(255,112,99);">Error: Process '+errtxt+'</font>'
            if err==0:
                txt += "<br>Check to make sure command is correct:<pre>"+self.actual_command+'</pre>'
            self.appendText(txt)
            if self.status != 'done' and self.process.state()==0:
                self.finished()
            self.status = 'done'
        
    def appendText(self,txt,plaintext=0):
        # Append to end without extra line space
        self.ui.tb_out.moveCursor(QtGui.QTextCursor.End)
        self.ui.tb_out.textCursor().insertHtml(txt.replace('\n','<br>'))
        self.ui.tb_out.moveCursor(QtGui.QTextCursor.End)
       
    def finished(self):
        if self.status != 'done':
            txt = self.ui.l_title.text()
            self.ui.l_title.setText(txt+'&nbsp;&nbsp;<b>Finished:</b>&nbsp;'+datetime.datetime.now().strftime('%I:%M:%S.%f'))
        self.status = 'done'
        self.ui.b_run.setEnabled(1)
        self.ui.b_stop.setEnabled(0)
        self.ui.fr_title.setStyleSheet('QFrame#fr_title {background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(50, 50, 50, 255), stop:0.831818 rgba(80, 80, 80, 255), stop:1 rgba(100, 100, 100, 255));color:white;border:1px solid rgba(130,130,130,200);}')
        self.ui.tb_out.setStyleSheet('QTextBrowser{background-color:rgb(50,50,50);color:white;border-bottom-left-radius:5px;border-bottom-right-radius:5px;} a {color:rgb(121,213,255);}')
    
        # Update list pages
        self.listItem.setForeground(QtGui.QBrush(QtGui.QColor(0,0,0)))
        fnt = self.listItem.font()
        fnt.setItalic(0)
        self.listItem.setFont(fnt)
        
    def toggleProcess(self):
        if self.status != 'done':
            self.stopProcess()
        else:
            self.startProcess()
    
    def setOutputText(self,text):
        self.ui.tb_out.setPlainText(text)
    
    def startProcess(self):
        self.ui.b_run.setEnabled(0)
        self.ui.b_stop.setEnabled(1)
        self.dispError = 1
        
        self.ui.l_title.setText('<b>&nbsp;'+os.path.split(self.filename)[1]+'&nbsp;&nbsp;&nbsp;&nbsp;</b><font color=#ccc><b>Started:</b> '+datetime.datetime.now().strftime('%I:%M:%S.%f'))
        self.ui.fr_title.setStyleSheet('QFrame#fr_title {background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(48, 85, 100, 255), stop:0.21267 rgba(61, 107, 127, 255), stop:0.831818 rgba(72, 127, 150, 255), stop:1 rgba(104, 166, 175, 255));color:white;border:1px solid rgba(130,130,130,200);}')
        self.ui.tb_out.setStyleSheet('background-color:rgb(30,30,30);border-bottom-left-radius:5px;border-bottom-right-radius:5px;')
        self.ui.tb_out.setText('')
        self.listItem.setForeground(QtGui.QBrush(QtGui.QColor(48, 85, 100)))
        fnt = self.listItem.font()
        fnt.setItalic(1)
        self.listItem.setFont(fnt)
        
        self.process = QtCore.QProcess()
        self.process.waitForStarted(100)
        self.process.setReadChannel(QtCore.QProcess.StandardOutput)
        self.process.setWorkingDirectory(os.path.dirname(self.filename))
        
        self.process.readyReadStandardOutput.connect(self.readOutput)
        self.process.readyReadStandardError.connect(self.readErrors)
        self.process.finished.connect(self.finished)
        self.process.error.connect(self.processError)
        
        self.actual_command = str(self.ui.le_cmd.text())
        self.process.start(self.ui.le_cmd.text())
        self.status = 'running'
    
    def stopProcess(self):
        self.dispError = 0
        self.process.kill()
        self.finished()
    
    def writeProcess(self):
        txt = self.ui.le_cmdw.text()+'\n'
##        self.appendText(txt)   # somehow process doesn't work after this
        self.process.write(txt.toLocal8Bit())
        self.ui.le_cmdw.clear()
    
    def saveFile(self):
        if self.filename == None:
            fname = ''
        else:
            fname = os.path.split(self.filename)[-1].split('.')[0]
        fileext = ''
        if os.name =='nt':
            fileext = 'Text (*.txt);;All (*.*)'
        filename = QtGui.QFileDialog.getSaveFileName(self,"Save Output",fname,fileext)
        if filename!='':
            txt = self.ui.tb_out.toPlainText()
            txt = str(self.ui.tb_out.toPlainText().toUtf8()).decode('utf-8')
            f = codecs.open(filename,'w','utf8')
            f.write(txt)
            f.close()