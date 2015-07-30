#!/usr/bin/python
#
# PyConsole is a Python Shell console for Armadillo IDE
# by Cole Hagen
#
# PyConsole is a modified version of pycute4 by Rob Reilink.
# pycute4 source: http://pyqtlive.googlecode.com/hg/pycute4.py
# pycute4 derives from PyCute3.py by gerard vermeulen
# (http://gerard.vermeulen.free.fr/) and was ported for Qt4.
#
# PyConsole has some bug fixes and personalized features for
# the Armadillo IDE

import os, sys
from code import InteractiveInterpreter as Interpreter
from PyQt4 import QtGui,QtCore#, Qsci
from PyQt4.QtCore import Qt

if sys.version_info.major==3:
    from . import highlighter
else:
    import highlighter

class Console(QtGui.QTextEdit):
    
    def __init__(self, parent=None,locals=None, log='',fontSize=10):
        """Constructor.

        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.

        The optional 'log' argument specifies the file in which the
        interpreter session is to be logged.
        
        The optional 'parent' argument specifies the parent widget.
        If no parent widget has been specified, it is possible to
        exit the interpreter by Ctrl-D.
        """

        QtGui.QTextEdit.__init__(self, parent)
        
        self.setProperty("class","pluginHorizontal")
        # Syntax Highlighter
        self.highlighter = highlighter.MyHighlighter(self)

##        # Add sys path if not running from python
##        if not sys.executable.split('.')[-1][:2]=='py':
##            if os.name =='nt':
##                if os.path.exists(r'C:\python27'):
##                    pyflds = ['Lib',r'Lib\site-packages']
##                    for fld in pyflds:
##                        sys.path.append(r'C:\python27\\'+fld)
##            else:
##                if os.path.exists('/usr/lib/python2.7'):
##                    sys.path.append('/usr/lib/python2.7')
##                    sys.path.append('/usr/lib/python2.7/dist-packages')
                    
        if locals==None:
            locals={'self':self,'armadillo':parent}
        self.interpreter = Interpreter(locals)

        # session log
        self.log = log or ''

        # to exit the main interpreter by a Ctrl-D if PyCute has no parent
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None

        self.viewers = []
        class SplitStdErr:
            def __init__(self,*targets):
                self._targets=targets
            def write(self,line):
                for target in self._targets:
                    target.write(line)
                    
        # capture all interactive input/output 
        sys.stdout   = self
        sys.stderr   = SplitStdErr(sys.stderr,self)
        sys.stdin    = self
        # last line + last incomplete lines
        self.line    = ''
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
        
        # user interface setup
        #self.setTextFormat(QtGui.QTextEdit.PlainText)
        self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        #self.setCaption('PyCute -- a Python Shell for PyQt -- '
        #                'http://gerard.vermeulen.free.fr')
        # font
        if os.name == 'posix':
            font = QtGui.QFont("Monospace", fontSize)
        elif os.name == 'nt' or os.name == 'dos':
            font = QtGui.QFont("Courier New", fontSize)
        else:
            print(SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'")
##            raise Exception(SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'")
        font.setFixedPitch(1)
        self.setFont(font)

        # geometry
        height = 40*QtGui.QFontMetrics(font).lineSpacing()
        
        self.setTabStopWidth(QtGui.QFontMetrics(font).width('    ')-1)

        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextBrowserInteraction)

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
            self.write('# Python '+'('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+')<br>')
        else:
            self.write('# Armadillo Python ('+str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)+') Shell <br>#&nbsp;&nbsp;&nbsp;&nbsp;- only modules included with Armadillo are available<br>#&nbsp;&nbsp;&nbsp;&nbsp;- Ctrl+l to launch popup (outside of Armadillo) with the default installed Python<br>')
        
        self.write(sys.ps1)
        self.prompt = sys.ps1
        self.onKeyHook=lambda e: None
        
        self.currentRunPosition = self.textCursor().position()
        
    def clear(self):
        QtGui.QTextEdit.clear(self)
        self.point = 0
        self.line = ''
        self.lines = []
        self.more = 0
        
    def syncViewers(self):
        text=self.toPlainText()
        position=self.textCursor().position()
        for viewer in self.viewers:
            viewer.setText(text)
            viewer.moveCursor(QtGui.QTextCursor.End, 0)
            #viewer.ensureCurorVisible()
            #viewer.textCursor().setPosition(position)
        
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

    def readline(self):
        """
        Simulate stdin, stdout, and stderr.
        """
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QtGui.QTextCursor.End, 0)
        while self.reading:
            QtGui.QApplication.processEvents()
        if len(self.line) == 0:
            return '\n'
        else:
            return unicode(self.line) 
    
    def write(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        # The output of self.append(text) contains to many newline characters,
        # so work around QTextEdit's policy for handling newline characters.
        hack = self.toPlainText()
        hack.append(text)
        self.setText(hack)
        self.moveCursor(QtGui.QTextCursor.End, 0)
        self.syncViewers()
        QtGui.QApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
        
    def writelines(self, text):
        """
        Simulate stdin, stdout, and stderr.
        """
        map(self.write, text)

    def fakeUser(self, lines):
        """
        Simulate a user: lines is a sequence of strings, (Python statements).
        """
        for line in lines:
            self.line = line.rstrip()
            self.write(self.line)
            self.write('\n')
            self.__run()
            
    def __run(self):
        """
        Append the last line to the history list, let the interpreter execute
        the last line(s), and clean up accounting for the interpreter results:
        (1) the interpreter succeeds
        (2) the interpreter fails, finds no errors and wants more line(s)
        (3) the interpreter fails, finds errors and writes them to sys.stderr
        """
        if self.line.strip():    #Non-empty line
            self.history.append(self.line)
            self.pointer = len(self.history)
        else:
            self.line=''
            
        self.lines.append(self.line)
        source = '\n'.join(self.lines)
        self.more = self.interpreter.runsource(source)
        if self.more:
            self.prompt = sys.ps2
            self.indent = self.line[0:len(self.line)-len(self.line.lstrip())]
            if self.line.rstrip():
                if self.line.rstrip()[-1]==':':
                    self.indent+='    '
        else:
            self.prompt = sys.ps1
            self.lines = []
            self.indent=''
        self.write(self.prompt)

        self.__clearLine()
        
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line=''
        self.point = 0
        self.__insertText(self.indent)
        self.currentRunPosition = self.textCursor().position()
        
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """
        
        # Get selection points
        tc = self.textCursor()
        if tc.hasSelection():
            delta_pt = tc.selectionEnd()-tc.selectionStart()
        else:
            delta_pt=0
        
        self.point -= delta_pt
        self.line=self.line[:self.point]+text+self.line[self.point+delta_pt:]
        self.point += len(text)
        self.insertPlainText(text)

    
    def keyPressEvent(self, e):
        """
        Handle user input a key at a time.
        """
        text  = unicode(e.text())
        key   = e.key()
        
        # Copy ahead of disable
        if e.modifiers() & QtCore.Qt.ControlModifier:
            if key == QtCore.Qt.Key_C:  # copy
                clip = QtGui.QApplication.clipboard()
                clip.setText(self.textCursor().selectedText())
        
        # End event if cursor before command position
        if self.currentRunPosition > self.textCursor().position():
            return

        # Paste
        if e.modifiers() & QtCore.Qt.ControlModifier:
            if key == QtCore.Qt.Key_V:  # paste
                self.__insertText(unicode(QtGui.QApplication.clipboard().text()))
                self.syncViewers()
            elif key == QtCore.Qt.Key_L: # launch
                from subprocess import Popen
                try:
                    Popen(["python",os.path.abspath(__file__)])
                except:
                    QtGui.QMessageBox.warning(self,'Error','The Python Shell could not open with your default Python install.  Please make sure you have Python 2.7 (or 2.6) installed and the Python executable is in your system path')
            else:
                QtGui.QTextEdit.keyPressEvent(self,e)
            return
            
        if self.onKeyHook(e):
            return
        
        if len(text):
            ascii = ord(unicode(text))
        else:
            ascii=0

        # Get selection points
        tc = self.textCursor()
        if tc.hasSelection():
            delta_pt = tc.selectionEnd()-tc.selectionStart()
        else:
            delta_pt=1
            
        if len(text) and ascii>=32 and ascii<127:
##            self.point = self.textCursor().positionInBlock()-4
            self.__insertText(text)
            self.syncViewers()
            return

        elif key == Qt.Key_Backspace:
            if self.point:
                self.point -= delta_pt
                self.textCursor().deletePreviousChar()
                self.line=self.line[:self.point]+self.line[self.point+delta_pt:]
        elif key == Qt.Key_Delete:
            self.textCursor().deleteChar()
            if delta_pt>1:
                self.point -= delta_pt
            self.line=self.line[:self.point]+self.line[self.point+delta_pt:]

        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.write('\n')
            if self.reading:
                self.reading = 0
            else:
                self.__run()
        elif key == Qt.Key_Tab:
            self.__insertText('   ')
        elif key == Qt.Key_Left:
            if self.point:
                self.moveCursor(QtGui.QTextCursor.PreviousCharacter, 0)
                self.point -= 1
        elif key == Qt.Key_Right:
            if self.point < len(self.line):
                self.moveCursor(QtGui.QTextCursor.NextCharacter, 0)
                self.point += 1
        elif key == Qt.Key_Home:
            self.moveCursor(QtGui.QTextCursor.StartOfLine, 0)
            for i in range(len(self.prompt)):
                self.moveCursor(QtGui.QTextCursor.NextCharacter, 0)
            self.point = 0
        elif key == Qt.Key_End:
            self.moveCursor(QtGui.QTextCursor.EndOfLine, 0)
            self.point = len(self.line)
        elif key == Qt.Key_Up:
            if len(self.history):
                if self.pointer > 0:
                    self.pointer -= 1
                    self.__recall(self.history[self.pointer])
        elif key == Qt.Key_Down:
            if len(self.history) and self.pointer<len(self.history):
                if self.pointer == len(self.history)-1:
                    self.__recall('')
                    self.pointer += 1
                else:
                    self.pointer += 1
                    self.__recall(self.history[self.pointer])

        else:
            QtGui.QTextEdit.keyPressEvent(self,e)
            
        self.syncViewers()
        
    def __recall(self,text):
        """
        Display the current item from the command history.
        """
        cursor=self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText(self.prompt)
        self.__clearLine()
        self.__insertText(text)

        
    def focusNextPrevChild(self, next):
        """
        Suppress tabbing to the next window in multi-line commands. 
        """
        if next and self.more:
            return 0
        return QtGui.QTextEdit.focusNextPrevChild(self, next)

    def mousePressEvent(self, e):
        QtGui.QTextEdit.mousePressEvent(self,e)
        self.point = self.textCursor().positionInBlock()-4

    def contentsContextMenuEvent(self,ev):
        """
        Suppress the right button context menu.
        """
        return


#---Main
if __name__=='__main__':
    import sys
    app=QtGui.QApplication(sys.argv)
    console=Console()
    console.setStyleSheet('QTextEdit {background:rgb(30,30,30);color:white;}')
    console.resize(600,400)
    console.show()
    app.exec_()