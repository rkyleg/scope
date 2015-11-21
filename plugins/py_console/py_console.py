#!/usr/bin/python
#
# PyConsole is a Python Shell console for Scope IDE

import os, sys, re
from code import InteractiveInterpreter as Interpreter
from PyQt4 import QtGui,QtCore, Qsci
from PyQt4.QtCore import Qt

from scintilla_style import styleD # scintilla style

##if sys.version_info.major==3:
##    from . import highlighter
##else:
##    import highlighter

from console_ui import Ui_Form

re_file     = re.compile('(\s*)(File "(.*))\n')
re_loc = re.compile('File "([^"]*)", line (\d+)')

class PyConsole(QtGui.QWidget):
    def __init__(self,parent=None,locals=None, log='',fontSize=10):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #--- Signals
##        self.ui.le_cmd.returnPressed.connect(self.enter)
        self.ui.le_cmd.keyPressEvent = self.cmdKeyPress
##        self.ui.sci_cmd.keyPressEvent = self.cmdKeyPress
        
        # Setup TextBrowser
##        self.highlighter = highlighter.MyHighlighter(self.ui.tb_view)
##        self.highlighter = highlighter.MyHighlighter(self.ui.le_cmd)
        self.ui.tb_view.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        
        
        
        # Setup Command 
##        self.ui.te_cmd.sizeHint = self.cmdSizeHint
        self.lex = Qsci.QsciLexerPython()
        self.ui.le_cmd.setLexer(self.lex)
        for i in range(5):
            self.ui.le_cmd.setMarginWidth(i,0)
        
        # Set Dark Color
        style_obj = set(styleD.keys()).intersection(dir(self.lex))
        self.ui.le_cmd.setCaretForegroundColor(QtGui.QColor(255,255,255))
        shade=30
        self.ui.le_cmd.setCaretLineBackgroundColor(QtGui.QColor(shade,shade,shade))
        self.lex.setDefaultPaper(QtGui.QColor(shade,shade,shade))
        self.lex.setPaper(QtGui.QColor(shade,shade,shade),self.lex.Default)
        self.ui.le_cmd.setColor(QtGui.QColor(255,255,255))
        self.ui.le_cmd.setMarginsBackgroundColor(QtGui.QColor(60,60,60))
        self.ui.le_cmd.setWhitespaceBackgroundColor(QtGui.QColor(80,80,80))
        self.ui.le_cmd.setFoldMarginColors(QtGui.QColor(200,200,200),QtGui.QColor(90,90,90))
##            self.ui.te_sci.setPaper(QColor(80,80,80))
        self.ui.le_cmd.setMarginsForegroundColor(QtGui.QColor(200,200,200))
##            self.ui.te_sci.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETBACK,Qsci.QsciScintilla.STYLE_DEFAULT,QColor(150,150,150))
        
        self.ui.le_cmd.setMatchedBraceBackgroundColor(QtGui.QColor(shade,shade,shade))
        self.ui.le_cmd.setMatchedBraceForegroundColor(QtGui.QColor(170,0,255))
        self.ui.le_cmd.setUnmatchedBraceBackgroundColor(QtGui.QColor(shade,shade,shade))
        
        # Set defaults for all:
        style_obj = set(styleD.keys()).intersection(dir(self.lex))
        style_obj.remove('Default')
        style_obj = set(['Default']).union(sorted(style_obj))
        
        for c in sorted(style_obj,reverse=1):
            clr = styleD[c]
            if clr == '':
##                    clr = '255,255,255'
                clr = styleD['Default']
##                print c,clr
            try:
                exec('self.lex.setPaper(QtGui.QColor(30,30,30),self.lex.'+c+')')
                exec('self.lex.setColor(QtGui.QColor('+clr+'),self.lex.'+c+')')
            except:
                print 'no keyword',c
        
        
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

##        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextBrowserInteraction)

        
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
        
        if __name__ =='__main__':
            self.write('# Python '+'('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')\n',mode=1)
        else:
            self.write('# Scope Python ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+') Shell\n    - only modules included with Scope are available\n    - Ctrl+l to launch popup (outside of Scope) with the default installed Python\n',mode=1)
        
        # Focus to command prompt
        self.ui.le_cmd.setFocus()
    
    def cmdSizeHint(self):
        print 'size hint'
        return QtCore.QSize(20,20)
    
    def enter(self):
##        print 'enter'
        line = unicode(self.ui.le_cmd.text())
        
        if line.strip():
            self.history.append(line)
            self.pointer = len(self.history)
            self.write(unicode(self.ui.l_prompt.text())+' '+line+'\n',mode=1)
        else:
            line = ''

        self.lines.append(line)
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
            
##        print 'indent',len(self.indent)
        self.setCommandText(self.indent)
        self.ui.l_prompt.setText(self.prompt)
        

    def write(self, text,mode=0):
        # modes
        #  0 = output
        #  1 = input
        #  2 = error
##        hack = self.ui.tb_view.toPlainText()
##        hack.append(text+'\n')
##        self.ui.tb_view.setText(hack)
##        print len(text),len(text.rstrip())
        self.writecount += 1
        if text.rstrip() or 1:
            self.ui.tb_view.moveCursor(QtGui.QTextCursor.End, 0)
##            self.ui.tb_view.insertPlainText(text.rstrip()+'\n')
            if mode == 2: # Error
                txt = '<font style="color:rgb(255,112,99);">' + str(QtCore.QString(text)).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</font>"
                txt = re_file.sub(r"<a style=""color:rgb(121,213,255);"" href='\g<2>'>\g<2></a>",txt)
##                text = '<div style="color:red">'+text.replace('\n','<br>').replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;')+'</div>'
                self.ui.tb_view.insertHtml(txt)
            elif mode == 1: # Input
                txt = '<div style="color:rgb(89,197,254);">'+str(QtCore.QString(text)).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</div>"
                self.ui.tb_view.insertHtml(txt)
            else: # Write
                txt = '<div style="color:rgb(255,255,255);">'+str(QtCore.QString(text)).replace('<','&lt;').replace('>','&gt;').replace('  ','&nbsp;&nbsp;').replace('\n','<br>')+"</div>"
                self.ui.tb_view.insertHtml(txt)
##            self.ui.tb_view.insertPlainText(text)
    ##        self.ui.tb_view.insertHtml(text.replace('\n','<br>')+'<br>')
            self.ui.tb_view.moveCursor(QtGui.QTextCursor.End, 0)
    
    def cmdKeyPress(self,e):
        key   = e.key()
        handled = 0
##        print key
        # Copy ahead of disable
##        if e.modifiers() & QtCore.Qt.ControlModifier:
##            pass
        if key == Qt.Key_Up:
            if len(self.history):
                if self.pointer > 0:
                    self.pointer -= 1
                    self.setCommandText(self.history[self.pointer])
                    handled = 1
        elif key == Qt.Key_Down:
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
##            print 'enter'
            self.enter()
            handled = 1
        elif key == Qt.Key_Tab:
            self.__insertText('   ')
        if key == QtCore.Qt.Key_V:  # paste
            txt = unicode(QtGui.QApplication.clipboard().text()).splitlines()
            if len(txt) > 1:
                for t in txt[:-1]:
##                    self.write(t)
                    self.setCommandText(t)
                    self.enter()
            self.setCommandText(txt[-1])
            handled = 1
                    
        
        if not handled:
##            QtGui.QLineEdit.keyPressEvent(self.ui.le_cmd,e)
            Qsci.QsciScintilla.keyPressEvent(self.ui.le_cmd,e)
    
    def setCommandText(self,text):
        self.ui.le_cmd.setText(text)
        self.ui.le_cmd.setCursorPosition(0,len(text))
    
    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.ui.le_cmd.setText('')
##        self.moveCursor(QtGui.QTextCursor.End, 0)
        while self.reading:
            QtGui.QApplication.processEvents()
        line = self.ui.le_cmd.text()
        if len(line) == 0:
            return '\n'
        else:
            return unicode(line) 

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


#---Main
if __name__=='__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    console=PyConsole()
    console.setStyleSheet('QTextEdit {background:rgb(30,30,30);color:white;}')
    console.resize(600,400)
    console.show()
    app.exec_()