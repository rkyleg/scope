#!/usr/bin/python
#
# This is PyCute3.py from gerard vermeulen (http://gerard.vermeulen.free.fr/)
# ported to Qt4 and extended to have an external viewer by Rob Reilink
# Source: http://pyqtlive.googlecode.com/hg/pycute4.py
# Slightly modified by Cole Hagen to work with afide
#
# In the future PyCute will get more features of the Idle's Python shell:
# - fontification (syntax coloring)
# - balloon help with documentation strings
# - copy & paste into or out of the shell
#
#
# Did you find a bug in PyCute? Check Idle's behavior before reporting.
#
# There will be always some differences between a GUI shell and the Python
# interpreter running in a terminal (Unix) or DOS box (Windows), e.g:
#
# os.system('dir') or os.system('ls') 
#
# In a terminal or DOS box, the user sees the directory listing followed by
# the return code (0). Why? In this case, stdout of the 'dir' or 'ls' command
# coincides with stdout of the interpreter.
#
# This is not the case with a GUI shell like PyCute or Idle. If the shell has
# been started from a terminal or DOS box, the directory listing will appear
# in the terminal or DOS box and the return code will appear in the GUI shell.
# If the GUI shell has been started by other means, the return code of the
# command will appear in the shell but the other behavior of is undefined
# (under Unix you will see nothing, and under Windows you will see
# a DOS box flashing up).

import os, sys
from code import InteractiveInterpreter as Interpreter
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt

class PyCuteViewer(QtGui.QTextEdit):
	def __init__(self,parent=None,fontSize=12):
		QtGui.QTextEdit.__init__(self, parent)
		self.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
		#self.setCaption('PyCute -- a Python Shell for PyQt -- '
		#				'http://gerard.vermeulen.free.fr')
		# font
		if os.name == 'posix':
			font = QtGui.QFont("Fixed", fontSize)
		elif os.name == 'nt' or os.name == 'dos':
			font = QtGui.QFont("Courier New", fontSize)
		else:
			raise SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'"
		font.setFixedPitch(1)
		self.setFont(font)
		self.setTabStopWidth(QtGui.QFontMetrics(font).width('    ')-1)


class PyCute(QtGui.QTextEdit):

	"""
	PyCute is a Python shell for PyQt.

	Creating, displaying and controlling PyQt widgets from the Python command
	line interpreter is very hard, if not, impossible.  PyCute solves this
	problem by interfacing the Python interpreter to a PyQt widget.

	My use is interpreter driven plotting to QwtPlot instances. Why?
	
	Other popular scientific software packages like SciPy, SciLab, Octave,
	Maple, Mathematica, GnuPlot, ..., also have interpreter driven plotting.  
	It is well adapted to quick & dirty exploration. 

	Of course, PyQt's debugger -- eric -- gives you similar facilities, but
	PyCute is smaller and easier to integrate in applications.
	Eric requires Qt-3.x

	PyCute is based on ideas and code from:
	- Python*/Tools/idle/PyShell.py (Python Software Foundation License)
	- PyQt*/eric/Shell.py (Gnu Public License)
	"""
	
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
		if locals==None:
			locals={'self':self}
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
		sys.stdin	= self
		# last line + last incomplete lines
		self.line	= ''
		self.lines   = []

		# the cursor position in the last line
		self.point   = 0
		# flag: the interpreter needs more input to run the last lines. 
		self.more	= 0
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
		#				'http://gerard.vermeulen.free.fr')
		# font
		if os.name == 'posix':
			font = QtGui.QFont("Monospace", fontSize)
		elif os.name == 'nt' or os.name == 'dos':
			font = QtGui.QFont("Courier New", fontSize)
		else:
			raise SystemExit, "FIXME for 'os2', 'mac', 'ce' or 'riscos'"
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

		self.write(sys.ps1)
		self.prompt = sys.ps1
		self.onKeyHook=lambda e: None
        
	def clear(self):
		QtGui.QTextEdit.clear(self)
		self.write(sys.ps1)
		self.point = 0
		self.line = ''
		self.lines = []
		self.more = 0
		
	def newViewer(self,parent=None,*args,**kwds):
		viewer=PyCuteViewer(parent,*args,**kwds)
		self.viewers.append(viewer)
		self.syncViewers()
		return viewer
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
			return str(self.line) 
	
	def write(self, text):
		"""
		Simulate stdin, stdout, and stderr.
		"""
		# The output of self.append(text) contains to many newline characters,
		# so work around QTextEdit's policy for handling newline characters.
		#print dir(self)
		hack = self.toPlainText()
		hack.append(text)
		self.setText(hack)
		#self.setText(self.text().append(text)) # segmentation fault
		self.moveCursor(QtGui.QTextCursor.End, 0)
		#self.yLast, self.xLast = self.getCursorPosition()
		#sys.stderr.write('Wrote %s\n' % text)
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
					self.indent+='\t'
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
		
	def __insertText(self, text):
		"""
		Insert text at the current cursor position.
		"""
		#y, x = self.getCursorPosition()
		#self.insertAt(text, y, x)
		self.line=self.line[:self.point]+text+self.line[self.point:]
		self.point += len(text)
		#self.setCursorPosition(y, x + text.length())
		self.insertPlainText(text)
	def keyPressEvent(self, e):
		"""
		Handle user input a key at a time.
		"""
		if self.onKeyHook(e):
			return
		
		text  = str(e.text())
		key   = e.key()
		if len(text):
			ascii = ord(str(text))
		else:
			ascii=0

		if len(text) and ascii>=32 and ascii<127:
			self.__insertText(text)
			self.syncViewers()
			return



		if key == Qt.Key_Backspace:
			if self.point:
				self.textCursor().deletePreviousChar()
				self.point -= 1
				self.line=self.line[:self.point]+self.line[self.point+1:]
		elif key == Qt.Key_Delete:
			self.textCursor().deleteChar()
			self.line=self.line[:self.point]+self.line[self.point+1:]

		elif key == Qt.Key_Return or key == Qt.Key_Enter:
			self.write('\n')
			if self.reading:
				self.reading = 0
			else:
				self.__run()
		elif key == Qt.Key_Tab:
			self.__insertText(text)
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
		
		#self.moveCursor(QtGui.QTextCursor.StartOfLine, 0)
		#self.setSelection(self.cursorPosition,-1)
		#fdsafdsa
		cursor.select(QtGui.QTextCursor.LineUnderCursor)

#		self.setSelection(self.yLast, self.xLast,
#						  self.yLast, self.paragraphLength(self.yLast))
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

##	def mousePressEvent(self, e):
##		"""
##		Keep the cursor after the last prompt.
##		"""
##		if e.button() == Qt.LeftButton:
##			self.moveCursor(QtGui.QTextCursor.End, 0)
##		return

	def contentsContextMenuEvent(self,ev):
		"""
		Suppress the right button context menu.
		"""
		return

# Local Variables: ***
# mode: python ***
# End: ***

if __name__=='__main__':
	import sys
	app=QtGui.QApplication(sys.argv)
	pycute=PyCute()
	pycute.resize(600,400)
	pycute.show()

##	newview=pycute.newViewer()
##	newview.resize(600,400)
##	newview.show()
	
	app.exec_()

#---Code to add to afide
def addDock(parent):
    wdg = PyCute(parent)
    return wdg