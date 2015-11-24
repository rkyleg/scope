# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# PyConsole is a Python Shell console for Scope IDE

# VERSION
__version__ = '0.2.1'

import os, sys, re
from code import InteractiveInterpreter as Interpreter
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt
from console_ui import Ui_Form

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class PyConsole(QtGui.QWidget):
    def __init__(self,parent=None,locals=None, log='', fontSize=10, commandWidget=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Setup TextBrowser
        self.ui.tb_view.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.ui.tb_view.keyPressEvent = self.tb_out_keypress

        # Setup Command 
        if not commandWidget:
            try:
                import scintilla_cmd
                commandWidget = scintilla_cmd.cmd_widget()
            except:
                commandWidget = None
        
        if commandWidget:
            # Scintilla Commandline
            self.ui.le_cmd = commandWidget
            
        else:
            # Line Edit
            self.ui.le_cmd = QtGui.QLineEdit()
            self.ui.le_cmd.widgetObject = QtGui.QLineEdit
            self.ui.le_cmd.type = 'qlineedit'
        
        self.ui.frame.layout().addWidget(self.ui.le_cmd,0,2,1,1)
        self.ui.le_cmd.keyPressEvent = self.cmdKeyPress
        
        # font
        if os.name == 'posix':
            font = QtGui.QFont("Monospace", fontSize)
        elif os.name == 'nt' or os.name == 'dos':
            font = QtGui.QFont("Courier New", fontSize)
        else:
            print(SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'")
##            raise Exception(SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'")
        font.setFixedPitch(1)
##        self.setFont(font)
        self.ui.tb_view.setFont(font)
        self.ui.le_cmd.setFont(font)
        self.ui.l_prompt.setFont(font)
        
        # geometry
        height = 40*QtGui.QFontMetrics(font).lineSpacing()
        
        self.ui.tb_view.setTabStopWidth(QtGui.QFontMetrics(font).width('    ')-1)

        # Setup Interpreter
        if locals==None:
            locals={'self':self,'scope':parent}
        self.interpreter = Interpreter(locals)
        
        # Exit with Ctrl+D
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None

##        self.viewers = []
        class SplitStdErr:
            def __init__(self,default_stderr,console_stderr):
##                self._targets=targets
                self.default_stderr = default_stderr
                self.console_stderr = console_stderr
            def write(self,line):
                self.default_stderr.write(line)
                self.console_stderr.write(line,mode=2)
##                for target in self._targets:
##                    target.write(line)
                    
        # capture all interactive input/output 
        sys.stdout   = self
        sys.stderr   = SplitStdErr(sys.stderr,self)
        sys.stdin    = self
        
        # last line + last incomplete lines
        self.lines   = []

        # the cursor position in the last line
        self.point   = 0
        # flag: the interpreter needs more input to run the last lines. 
        self.more    = 0
        # flag: readline() is being used for e.g. raw_input() and input()
        self.reading = 0
        # history
        self.history = []
        self.pointer = 0
        self.indent = ''
        self.prompt = '>>>'
        self.writecount = 0
        
        # interpreter prompt.
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        
        self.write('# Python '+'('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')\n',mode=1)
        
        # Focus to command prompt
        self.ui.le_cmd.setFocus()
    
    def cmdSizeHint(self):
        print 'size hint'
        return QtCore.QSize(20,20)
    
    def enter(self):
        line = unicode(self.ui.le_cmd.text())
        
        if line.strip():
            self.history.append(line)
            self.pointer = len(self.history)
##            self.write(line+'\n',mode=1,prefix=unicode(self.ui.l_prompt.text())+' ')
        else:
            line = ''
        
        # Clear if 2 blank lines in a row
        cmd_reset = 0
        if len(self.lines) > 0:
            if self.lines[-1].rstrip() =='' and line.rstrip()=='':
                self.lines = []
                cmd_reset = 1
        
        if not cmd_reset:
            self.write(line+'\n',mode=1,prefix=unicode(self.ui.l_prompt.text())+' ')
            self.lines.append(line)
            
            if line == 'clear':
                # Clear Text
                self.prompt = '>>>'
                self.ui.tb_view.setText('')
                self.ui.le_cmd.setText('')
                self.lines = []
            
            else:
                source = '\n'.join(self.lines)
                self.more = self.interpreter.runsource(source)

                self.indent=''
                if self.more:
                    self.prompt = sys.ps2
                    self.indent = line[0:len(line)-len(line.lstrip())]
                    if line.rstrip():
                        if line.rstrip()[-1]==':':
                            self.indent+='    '
                            
                else:
                    self.prompt = sys.ps1
                    self.lines = []
                    
                self.setCommandText(self.indent)
        self.ui.l_prompt.setText(self.prompt)
        

    def write(self, text,mode=0,prefix=None):
        # modes
        #  0 = output
        #  1 = input
        #  2 = error
##        hack = self.ui.tb_view.toPlainText()
##        hack.append(text+'\n')
##        self.ui.tb_view.setText(hack)
##        print len(text),len(text.rstrip())

        self.writecount += 1
##        if text.rstrip() or 1:
        self.ui.tb_view.moveCursor(QtGui.QTextCursor.End, 0)
        if mode == 2: # Error
            txt = '<font style="color:rgb(255,112,99);">' + str(QtCore.QString(text).toUtf8()).decode('utf-8').replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</font>"
            txt = re_file.sub(r"<a style=""color:rgb(121,213,255);"" href='\g<2>'>\g<2></a>",txt)
            self.ui.tb_view.insertHtml(txt)
        elif mode == 1: # Input
            txt = '<div style="color:rgb(89,197,254);">'
            if prefix:
                txt += '<span style="color:rgb(38,90,150);">'+prefix.replace('>','&gt;')+'</span>'
            txt +=str(QtCore.QString(text).toUtf8()).decode('utf-8').replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</div>"
            self.ui.tb_view.insertHtml(txt)
        else: # Write
            txt = '<div style="color:rgb(255,255,255);">'+str(QtCore.QString(text).toUtf8()).decode('utf-8').replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</div>"
            self.ui.tb_view.insertHtml(txt)

        self.ui.tb_view.moveCursor(QtGui.QTextCursor.End, 0)
    
    def cmdKeyPress(self,e):
        key   = e.key()
        handled = 0

        if key == Qt.Key_Up:
            # Up
            if len(self.history):
                if self.pointer > 0:
                    self.pointer -= 1
                    self.setCommandText(self.history[self.pointer])
                    handled = 1
        elif key == Qt.Key_Down:
            # Down
            if len(self.history) and self.pointer<len(self.history):
                if self.pointer == len(self.history)-1:
                    self.setCommandText('')
                    self.pointer += 1
                    handled = 1
                else:
                    self.pointer += 1
                    self.setCommandText(self.history[self.pointer])
                    handled = 1
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            # Enter
            if self.reading:
                self.reading = 0
            else:
                self.enter()
            handled = 1
        elif key == Qt.Key_Tab:
            self.__insertText('   ')
        
        # Ctrl
        if e.modifiers() & QtCore.Qt.ControlModifier:
            if key == QtCore.Qt.Key_V:  # paste
                # V
##                txt = QtGui.QApplication.clipboard().text('plain').split(QtCore.QRegExp("[\r\n]"),QtCore.QString.SkipEmptyParts)
                txt = str(QtGui.QApplication.clipboard().text('plain').toUtf8()).decode('utf-8').splitlines()
                if len(txt) > 0:
                    self.ui.le_cmd.insert(txt[0])
                    if len(txt) > 1:
                        self.enter()
                        for t in txt[1:-1]:
                            self.setCommandText(t)
                            self.enter()
                        self.setCommandText(txt[-1])
                    handled = 1
            elif key == QtCore.Qt.Key_L: # launch
                # L
                from subprocess import Popen
                try:
                    if os.name =='nt':
                        Popen(["pythonw",os.path.abspath(__file__)])
                    else:
                        Popen(["python",os.path.abspath(__file__)])
                except:
                    QtGui.QMessageBox.warning(self,'Error','The Python Shell could not open with your default Python install.  Please make sure you have Python 2.7 (or 2.6) installed and the Python executable is in your system path')

        if not handled:
##            QtGui.QLineEdit.keyPressEvent(self.ui.le_cmd,e)
            self.ui.le_cmd.widgetObject.keyPressEvent(self.ui.le_cmd,e)
    
    def setCommandText(self,text):
        self.ui.le_cmd.setText(text)
        if self.ui.le_cmd.type == 'qscintilla':
            self.ui.le_cmd.setCursorPosition(0,len(text))
    
    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.ui.le_cmd.setText('')
        self.ui.l_prompt.setText('?')
##        self.moveCursor(QtGui.QTextCursor.End, 0)
        while self.reading:
            QtGui.QApplication.processEvents()
        line = self.ui.le_cmd.text()
        
        if len(line) == 0:
            return_line = '\n'
        else:
            return_line = str(line)
        self.write('\n')
        return return_line

    def writelines(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        map(self.write, text)

    def flush(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        pass

    def isatty(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        return 1

    #---Output Overrides
    def tb_out_keypress(self,e):
        key   = e.key()
        handled = 0
        
        # Copy ahead of disable
        if e.modifiers() & QtCore.Qt.ControlModifier:
            # Copy
            if key == Qt.Key_C:
                txt = str(self.ui.tb_view.textCursor().selectedText().toUtf8()).replace('\xc2\xa0',' ').decode('utf-8')
##                QtGui.QApplication.clipboard().clear()
                ntxt = []
                for ln in txt.splitlines():
                    t = ln
                    if ln.startswith('>>> ') or ln.startswith('... '):
                        t = ln[4:]
                    ntxt.append(t)
                txt = '\n'.join(ntxt)
                QtGui.QApplication.clipboard().setText(txt)
                handled = 1
        
        if not handled:
            QtGui.QTextEdit.keyPressEvent(self.ui.tb_view,e)

#---Main
if __name__=='__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    console=PyConsole()
##    console.setStyleSheet('QTextEdit {background:rgb(30,30,30);color:white;}')
##    console.resize(600,400)
    console.show()
    sys.exit(app.exec_())