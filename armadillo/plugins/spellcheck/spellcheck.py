from PyQt4 import QtGui, QtCore
import sys, os, re
from .spellcheck_ui import Ui_Form

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import enchant

from PyQt4.Qt import QAction
from PyQt4.Qt import QApplication
from PyQt4.Qt import QEvent
from PyQt4.Qt import QMenu
from PyQt4.Qt import QMouseEvent
from PyQt4.Qt import QPlainTextEdit
from PyQt4.Qt import QSyntaxHighlighter
from PyQt4.Qt import QTextCharFormat
from PyQt4.Qt import QTextCursor
from PyQt4.Qt import Qt
from PyQt4.QtCore import pyqtSignal

class SpellChecker(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        
        self.ui.b_cancel.clicked.connect(self.cancel)
        self.ui.b_ok.clicked.connect(self.update)
        
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
            x=self.armadillo.width()*.05
            y=self.armadillo.ui.split_left.pos().y()
            w=self.armadillo.width()*.9
            h=self.armadillo.ui.split_left.height()*.9
            self.setGeometry(x,y,w,h)
            
            # Get Text
            self.currentEditor=self.armadillo.currentEditor()
            
            txt=self.armadillo.currentEditor().getSelectedText()
            if txt == '':
                txt = self.armadillo.currentEditor().selectAll()
            self.ui.te_text.setPlainText(txt)
##            self.currentEditor.setEnabled(0)
            self.show()
            
    
    def cancel(self):
        self.currentEditor.setEnabled(1)
        self.hide()
        
    def update(self):
        if self.currentEditor != None:
            self.currentEditor.insertText(self.ui.te_text.toPlainText())
            self.cancel()
    
    def mousePressEvent2(self, event):
        if event.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mousePressEvent(self.ui.te_text, event)

    def keyPressEvent(self,event):
        # Override tab to spaces
        pass

    def contextMenuEvent2(self, event):
##        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.ui.te_text.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.ui.te_text.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if self.ui.te_text.textCursor().hasSelection():
            text = unicode(self.ui.te_text.textCursor().selectedText())
            if not self.dict.check(text):
                spell_menu = QMenu('Spelling Suggestions')
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

        cursor = self.ui.te_text.textCursor()
##        cursor = self.cursorForPosition(event.pos())
        cursor.beginEditBlock()

        cursor.removeSelectedText()
        cursor.insertText(word)

        cursor.endEditBlock()
        
    def highlighterEnabled(self):
         return self.highlighter.document() is not None

    def setHighlighterEnabled(self, enable):

        if enable != self.highlighterEnabled():
            if enable:
                self.highlighter.setDocument(self.ui.te_text.document())
            else:
                self.highlighter.setDocument(None)

class Highlighter(QSyntaxHighlighter):

    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

        self.dict = None

    def setDict(self, dict):
        self.dict = dict

    def highlightBlock(self, text):
        if not self.dict:
            return

        text = unicode(text)

        format = QTextCharFormat()
        format.setUnderlineColor(Qt.red)
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)


class SpellAction(QAction):

    '''
    A special QAction that returns the text in a signal.
    '''

    correct = pyqtSignal(unicode)

    def __init__(self, *args):
        QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))