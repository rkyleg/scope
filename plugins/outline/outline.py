from PyQt4 import QtGui, QtCore
from .outline_ui import Ui_Form
from .outline_tree_ui import Ui_Outline_Tree
import re, os, importlib

class outlineTree(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        curdir=os.path.abspath('.')
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        self.ui = Ui_Outline_Tree()
        self.ui.setupUi(self)
        os.chdir(curdir)
##        self.setHeaderHidden(1)
##        self.setRootIsDecorated(0)
##        self.setStyleSheet("""QTreeWidget {
##            border-bottom-left-radius:5px;
##            border-bottom-right-radius:5px;
##            }""")
        self.setProperty("class","pluginVertical")
        self.parent = parent
        
##        self.ui.fr_find.hide()
        self.ui.l_title.hide()
        self.ui.le_find.textChanged.connect(self.find)
##        self.ui.b_find_close.clicked.connect(self.ui.le_find.clear)

##    def keyPressEvent(self,event):
##        ky = event.key()
##        handled = 0
##        if ky ==QtCore.Qt.Key_F and  (event.modifiers() & QtCore.Qt.ControlModifier):
##            if self.parent.ui.fr_find.isVisible():
##                self.parent.ui.le_find.setText('')
##                self.parent.ui.fr_find.hide()
##            else:
##                self.parent.ui.fr_find.show()
##                self.parent.ui.le_find.setFocus()
##            handled=1
##        if not handled:
##            QtGui.QTreeWidget.keyPressEvent(self,event)

    def find(self):
        trwdg = self.ui.tr_outline
        txt = str(self.ui.le_find.text()).lower()
        for t in range(trwdg.topLevelItemCount()):
            itm = trwdg.topLevelItem(t)
            if txt =='' or txt in str(itm.text(0)).lower():
                itm.setHidden(0)
            else:
                itm.setHidden(1)

class Outline(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ide = parent
        self.wdgD = {}
##        self.treeD = {}
        
        # Create blank page for default
        self.ui.sw_outline.insertWidget(0,QtGui.QWidget())
        
##        QtGui.QShortcut(QtCore.Qt.CTRL+QtCore.Qt.Key_F,self,self.findFocus) # Find
        
##        self.ui.fr_find.hide()
        
        self.outlineLangD = {}
        for lang in os.listdir(os.path.join(os.path.dirname(__file__),'lang')):	
            l = lang.split('.')[0]
            if not l.startswith('_'):
                mod = importlib.import_module('plugins.outline.lang.'+l)
                funcs = dir(mod)

                if 'analyzeLine' in funcs:
                    self.outlineLangD[l]=mod.analyzeLine

        self.alwaysUpdate = self.ide.settings['plugins']['outline']['alwaysUpdate']
        if not self.alwaysUpdate:
            self.ide.Events.editorSaved.connect(self.updateOutline)
            
        # Update location
        if 1:
            self.ide.Events.editorVisibleLinesChanged.connect(self.updateLocation)
        
    def analyzeLine(self,wdg,typ):
        return None,None
        
    def addOutline(self,wdg):
        owdg = outlineTree(parent=self)
        owdg.ui.l_title.setText(wdg.title)
        trwdg = owdg.ui.tr_outline
        sw_ind = self.ui.sw_outline.count()
        self.ui.sw_outline.insertWidget(sw_ind,owdg)
        self.ui.sw_outline.setCurrentIndex(sw_ind)

        self.wdgD[wdg.id] = owdg
##        self.treeD[owdg]=wdg

        if self.alwaysUpdate==1:
            # Add Text Changed Signal
            if 'editorTextChanged' in dir(wdg):
                wdg.Events.editorChanged.connect(self.updateOutline)
        
        if 'gotoLine' in dir(wdg):
            trwdg.itemDoubleClicked.connect(self.goto)
        
        trwdg.contextMenuEvent = self.outlineMenu
        
        self.updateOutline(toggle_view=0)

    def updateOutlineToggle(self):
        self.updateOutline(toggle_view=1)

    def updateOutline(self,wdg=None,toggle_view=0):
        # Get current widget from ide
        wdg = self.ide.currentEditor()
        
        if toggle_view:
            if self.ide.ui.fr_left.isHidden():
                self.ide.ui.fr_left.setVisible(1)
            i=self.ide.ui.tab_left.indexOf(self.ide.pluginD['outline'].widget)
            self.ide.ui.tab_left.setCurrentIndex(i)
        
        if wdg != None:
            trwdg = self.wdgD[wdg.id].ui.tr_outline
            if wdg.lang != 'Text' and wdg.lang in self.outlineLangD and 'getText' in dir(wdg):
                # Select tab if language
    ##            i=self.ide.ui.tab_left.indexOf(self.ide.pluginD['outline'])
    ##            self.ide.ui.tab_left.setCurrentIndex(i)

                trwdg.clear()
                
                # Add Filename
    ##            itm =QtGui.QTreeWidgetItem([wdg.title,'0'])
    ##            trwdg.addTopLevelItem(itm)
    ##            self.format(itm,'filename')
                
##                self.wdgD[wdg.id].ui.b_find_close.click()
                txt = wdg.getText()
##                txtlines = txt.replace('\r\n','\n').replace('\r','\n').split('\n')
                txtlines = txt.splitlines()
                
                txt_outline = self.outlineLangD[wdg.lang](txtlines)
                
                for t in txt_outline:
                    itmText = t[0]
                    typ = t[1]
                    lcnt = t[2]
                    itm =QtGui.QTreeWidgetItem([itmText,str(lcnt)])
                    trwdg.addTopLevelItem(itm)
                    self.format(itm,typ)
                
                # Update Location if possible
                if 'getVisibleLines' in dir(wdg):
                    lines = wdg.getVisibleLines()
                    self.updateLocation(wdg,lines)
    
    def updateLocation(self,wdg,lines):
        if self.ide.settings['visibleLineTracking']:
            trwdg = self.wdgD[wdg.id].ui.tr_outline
            hi=0
    ##        brsh=QtGui.QBrush(QtGui.QColor(195,216,224,150)) # light blue
    ##        brsh=QtGui.QBrush(QtGui.QColor(26,46,56,200)) # dark blue
            brsh=QtGui.QBrush(QtGui.QColor(30,30,30,150)) # gray
            
            for t in xrange(trwdg.topLevelItemCount()-1,-1,-1):
                itm = trwdg.topLevelItem(t)
                line = int(str(itm.text(1)))
                if line>=lines[0] and line<=lines[1]:
                    itm.setBackground(0,brsh)
                    trwdg.scrollToItem(itm,3)
                    hi=1
                elif line<=lines[0] and not hi:
                    itm.setBackground(0,brsh)
                    trwdg.scrollToItem(itm,3)
                    hi=1
                else:
                    itm.setBackground(0,QtGui.QBrush())
            
    def outlineMenu(self,event):
        menu = QtGui.QMenu('file menu')
        trwdg = self.ui.sw_outline.currentWidget()
        menu.addAction(QtGui.QIcon(self.ide.iconPath+'refresh.png'),'Update (Ctrl+O)')
##        menu.addAction(QtGui.QIcon(self.ide.iconPath+'search.png'),'Find')
        act = menu.exec_(trwdg.ui.tr_outline.cursor().pos())
        if act != None:
            acttxt = str(act.text())
            if acttxt=='Update (Ctrl+O)':
                self.updateOutline()
##            elif acttxt == 'Find':
####                trwdg.ui.fr_find.show()
####                trwdg.ui.le_find.setFocus()
##                self.findFocus()
    
    def findFocus(self):
        trwdg = self.ui.sw_outline.currentWidget()
        trwdg.ui.fr_find.show()
        trwdg.ui.le_find.setFocus()
    
    def editorTabChanged(self,wdg):
        if wdg.id in self.wdgD:
            owdg = self.wdgD[wdg.id]
            self.ui.sw_outline.setCurrentWidget(owdg)
        else:
            self.ui.sw_outline.setCurrentIndex(0)
##        self.updateOutline(wdg)

##        self.ui.le_find.clear()
##        self.ui.fr_find.hide()
        
    def editorTabClosed(self,wdg):
        owdg = self.wdgD[wdg.id]
        self.wdgD.pop(wdg.id)
        self.ui.sw_outline.removeWidget(owdg)
        
    def goto(self,itm,col):
        line = int(str(itm.text(1)))
        wdg = self.ide.currentEditor()
        wdg.gotoLine(line)
    
    def format(self,itm,typ):
        # Format the tree widget item
        if typ == 'object':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(52,111,171)))
##            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(46,66,105)))
        elif typ == 'function':
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(101,191,246)))
##            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(52,111,171)))
        elif typ == 'heading':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(180,180,180)))
        elif typ=='filename':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(250,250,250)))
            itm.setBackground(0,QtGui.QBrush(QtGui.QColor(80,80,80)))
        elif typ=='decorator':
            fnt=QtGui.QFont()
##            fnt.setItalic(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(161,225,150)))
##            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(255,170,127)))
##            itm.setBackground(0,QtGui.QBrush(QtGui.QColor(80,80,80)))