from PyQt4 import QtGui, QtCore
from outline_ui import Ui_Form
import re, os, importlib

class outlineTree(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        QtGui.QTreeWidget.__init__(self,parent)
        self.setHeaderHidden(1)
        self.setRootIsDecorated(0)
        self.setStyleSheet("""QTreeWidget {
            border-bottom-left-radius:5px;
            border-bottom-right-radius:5px;
            }""")
        self.setProperty("class","pluginVertical")
        self.parent = parent

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
        
class Outline(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        self.wdgD = {}
        self.treeD = {}
        
        self.ui.fr_find.hide()
        
        self.outlineLangD = {}
        for lang in os.listdir(os.path.join(os.path.dirname(__file__),'lang')):
            l = lang.split('.')[0]
            mod = importlib.import_module('plugins.outline.lang.'+l)
            funcs = dir(mod)
##            exec('import lang.'+l)
##            exec('funcs=dir(lang.'+l+')')
            if 'analyzeLine' in funcs:
                self.outlineLangD[l]=mod.analyzeLine
##                exec('self.outlineLangD["'+l+'"]=lang.'+l+'.analyzeLine')

        self.alwaysUpdate = int(self.armadillo.settings['plugins']['outline']['alwaysUpdate'])
        if self.alwaysUpdate==0:
            self.armadillo.evnt.editorSaved.connect(self.updateOutline)
            
        # Update location
        if 1:
            self.armadillo.evnt.editorVisibleLinesChanged.connect(self.updateLocation)
        
        self.ui.le_find.textChanged.connect(self.find)
        self.ui.b_find_close.clicked.connect(self.ui.le_find.clear)
        
    def analyzeLine(self,wdg,typ):
        return None,None
        
    def addOutline(self,wdg):
        trwdg = outlineTree(parent=self)
        sw_ind = self.ui.sw_outline.count()
        self.ui.sw_outline.insertWidget(sw_ind,trwdg)
        self.ui.sw_outline.setCurrentIndex(sw_ind)

        self.wdgD[wdg] = trwdg
        self.treeD[trwdg]=wdg

        if self.alwaysUpdate==1:
            # Add Text Changed Signal
            if 'editorTextChanged' in dir(wdg):
                wdg.evnt.editorChanged.connect(self.updateOutline)
        
        if 'gotoLine' in dir(wdg):
            trwdg.itemDoubleClicked.connect(self.goto)
        
        trwdg.contextMenuEvent = self.outlineMenu

    def updateOutline(self,wdg):
        trwdg = self.wdgD[wdg]
        if wdg.lang != 'Text' and wdg.lang in self.outlineLangD:
            trwdg.clear()
            self.ui.le_find.setText('')
            txt = unicode(wdg.getText())
            txtlines = txt.replace('\r\n','\n').replace('\r','\n').split('\n')
            
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
        trwdg = self.wdgD[wdg]
        hi=0
        brsh=QtGui.QBrush(QtGui.QColor(195,216,224,150))
        for t in range(trwdg.topLevelItemCount()-1,-1,-1):
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
        menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'refresh.png'),'Update (F3)')
        menu.addAction(QtGui.QIcon(self.armadillo.iconPath+'search.png'),'Find')
        act = menu.exec_(trwdg.cursor().pos())
        if act != None:
            acttxt = str(act.text())
            if acttxt=='Update (F4)':
                self.updateOutline(self.armadillo.currentWidget())
            elif acttxt == 'Find':
                self.ui.fr_find.show()
                self.ui.le_find.setFocus()
        
    def editorTabChanged(self,wdg):
        trwdg = self.wdgD[wdg]
        self.ui.sw_outline.setCurrentWidget(trwdg)
        self.updateOutline(wdg)
        self.ui.le_find.clear()
        self.ui.fr_find.hide()
    
    def goto(self,itm,col):
        line = int(str(itm.text(1)))
        wdg = self.treeD[self.ui.sw_outline.currentWidget()]
        wdg.gotoLine(line)
       
    def find(self):
        trwdg = self.ui.sw_outline.currentWidget()
        txt = str(self.ui.le_find.text()).lower()
        for t in range(trwdg.topLevelItemCount()):
            itm = trwdg.topLevelItem(t)
            if txt =='' or txt in str(itm.text(0)).lower():
                itm.setHidden(0)
            else:
                itm.setHidden(1)
    
    def format(self,itm,typ):
        # Format the tree widget item
        if typ == 'object':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(46,66,105)))
        elif typ == 'function':
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(52,111,171)))
        elif typ == 'heading':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(120,120,120)))