from PyQt4 import QtGui, QtCore
import sys, os, re
from .spellcheck_ui import Ui_Form

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
##print os.path.abspath(os.path.dirname(__file__))
##os.environ['PYENCHANT_IGNORE_MISSING_LIB']='True'
import enchant

from PyQt4.QtCore import pyqtSignal

class SpellChecker(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ide = parent
        
##        self.setWindowModality(1)
        
##        self.setWindowOpacity(0.6)
##        self.setStyleSheet("#Form {background:white;}")
##        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.ui.b_cancel.clicked.connect(self.cancel)
        self.ui.b_ok.clicked.connect(self.update)
        
        self.ui.b_undo.clicked.connect(self.undo_word)
        self.ui.b_redo.clicked.connect(self.redo_word)
        
        # Setup Text Editor
        self.ui.te_text.mousePressEvent = self.mousePressEvent2
        self.ui.te_text.contextMenuEvent = self.contextMenuEvent2
        
        self.dict = enchant.Dict("en_US")
        self.highlighter = Highlighter(self.ui.te_text.document())
        self.highlighter.setDict(self.dict)
        
        self.currentEditor=None
        
        self.hide()
    
    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.count = 0
            self.ui.b_ok.setEnabled(0)
            x=self.ide.width()*.05
            y=self.ide.ui.split_left.pos().y()
            w=self.ide.width()*.9
            h=self.ide.ui.split_left.height()*.9
            self.setGeometry(x,y,w,h)
            
            # Get Text
            self.currentEditor=self.ide.currentEditor()
            
            if 'getSelectedText' in dir(self.ide.currentEditor()):
                txt=self.ide.currentEditor().getSelectedText()
                if txt == '':
                    if 'selectAll' in dir(self.ide.currentEditor()):
                        self.ide.currentEditor().selectAll()
                        txt=self.ide.currentEditor().getSelectedText()
                if txt != '':
                    self.ui.te_text.setTextCursor(QtGui.QTextCursor())
                    self.ui.te_text.setPlainText(txt)
    ##                self.currentEditor.setEnabled(0)
                    self.show()
            
    
    def cancel(self):
##        self.currentEditor.setEnabled(1)
        self.hide()
        
    def update(self):
        if self.currentEditor != None:
            self.currentEditor.insertText(self.ui.te_text.toPlainText())
            self.cancel()
    
    def mousePressEvent2(self, event):
        if event.button() == QtCore.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(),
                QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
        QtGui.QPlainTextEdit.mousePressEvent(self.ui.te_text, event)

    def keyPressEvent(self,event):
        # Override tab to spaces
        pass

    def contextMenuEvent2(self, event):
##        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.ui.te_text.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        self.ui.te_text.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        spell_menu = QtGui.QMenu('Spelling Suggestions')
        if self.ui.te_text.textCursor().hasSelection():
            text = unicode(self.ui.te_text.textCursor().selectedText())
            if not self.dict.check(text):
                
                for word in self.dict.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
##                if len(spell_menu.actions()) != 0:
##                    popup_menu.insertSeparator(popup_menu.actions()[0])
##                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)

##        popup_menu.exec_(event.globalPos())
        spell_menu.exec_(event.globalPos())

    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        fmt = QtGui.QTextCharFormat()
        cursor = self.ui.te_text.textCursor()
        fmt.setBackground(QtGui.QColor(184, 215, 255))
        
##        cursor = self.cursorForPosition(event.pos())
        cursor.beginEditBlock()
        
        cursor.removeSelectedText()
        cursor.setCharFormat(fmt)
        cursor.insertText(word)

##        cursor.setCharFormat(fmt)
        cursor.endEditBlock()
        # Update count
        self.count+=1
        self.ui.b_ok.setEnabled(1)
        self.ui.l_count.setText(str(self.count)+' changes')
    
    def undo_word(self):
        self.count -=1
        self.ui.l_count.setText(str(self.count)+' changes')
        if self.count <=0:
            self.ui.b_ok.setEnabled(0)

    def redo_word(self):
        self.count +=1
        self.ui.l_count.setText(str(self.count)+' changes')
        self.ui.b_ok.setEnabled(1)

    def highlighterEnabled(self):
         return self.highlighter.document() is not None

    def setHighlighterEnabled(self, enable):

        if enable != self.highlighterEnabled():
            if enable:
                self.highlighter.setDocument(self.ui.te_text.document())
            else:
                self.highlighter.setDocument(None)

class Highlighter(QtGui.QSyntaxHighlighter):

    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        QtGui.QSyntaxHighlighter.__init__(self, *args)

        self.dict = None

    def setDict(self, dict):
        self.dict = dict

    def highlightBlock(self, text):
        if not self.dict:
            return

        text = unicode(text)

        format = QtGui.QTextCharFormat()
        format.setUnderlineColor(QtCore.Qt.red)
        format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)

        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)


class SpellAction(QtGui.QAction):

    '''
    A special QAction that returns the text in a signal.
    '''

    correct = pyqtSignal(unicode)

    def __init__(self, *args):
        QtGui.QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))