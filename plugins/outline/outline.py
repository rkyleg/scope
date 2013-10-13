from PyQt4 import QtGui, QtCore
from outline_ui import Ui_Form
import re

def addDock(parent):
    dock = Outline(parent)
    parent.evnt.editorAdded.connect(dock.addOutline)
    parent.evnt.editorTabChanged.connect(dock.editorTabChanged)
    return dock

class outlineTree(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        QtGui.QTreeWidget.__init__(self,parent)
        self.setHeaderHidden(1)
        self.setRootIsDecorated(0)

class Outline(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.afide = parent
        self.wdgD = {}
        self.treeD = {}

    def addOutline(self,wdg):
        trwdg = outlineTree()
        sw_ind = self.ui.sw_outline.count()
        self.ui.sw_outline.insertWidget(sw_ind,trwdg)
        self.ui.sw_outline.setCurrentIndex(sw_ind)
        
        ##trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([wdg.title]))
        
        self.wdgD[wdg] = trwdg
        self.treeD[trwdg]=wdg
        
        # Add Text Changed Signal
        if 'editorTextChanged' in dir(wdg):
            wdg.evnt.editorChanged.connect(self.updateOutline)
        
            if 'gotoLine' in dir(wdg):
                trwdg.itemDoubleClicked.connect(self.goto)

    def updateOutline(self,wdg):
        trwdg = self.wdgD[wdg]
        cnt = -1
        trwdg.clear()
        txt = unicode(wdg.getText())
        txtlines = txt.split('\n')
        for t in txtlines:
            cnt += 1
            lcnt = cnt
            typ = None
            itmText = None
            spc = (len(t) -len(t.lstrip()))*' '
            
            #---Python
            if wdg.lang == 'Python':
                if t.lstrip().startswith('def '):
                    itmText = t.lstrip()[4:-1]
                    typ = 'function'
                elif t.lstrip().startswith('class '):
                    itmText =t.lstrip()[6:-1]
                    typ = 'object'
                elif t.lstrip().startswith('#---'):
                    itmText =t.lstrip()[4:].lstrip('-')
                    typ = 'heading'
                if itmText != None:
                    itmText = spc +itmText
                
            #--- Javascript
            elif wdg.lang == 'JavaScript':
                if t.lstrip().startswith('function'):
                    itmText =t.lstrip()[9]
                    typ = 'function'
                elif t.lstrip().startswith('//---'):
                    itmText =t.lstrip()[5:]
                    typ = 'heading'
            
            #--- CSS
            elif wdg.lang == 'CSS':
                if t.lstrip().startswith('/*---'):
                    itmText =t.lstrip()[5:].split('*/')[0]
                    typ = 'heading'
                else:
                    g = re.match('.*{',t)
                    if g:
                        itmText = g.group()[:-1]
                        if itmText == '': 
                            itmText = txtlines[cnt-1]
                            lcnt = cnt-1
                        if itmText == '': itmText = None
                        if itmText.startswith('.'):
                            typ = 'function'
                        else:
                            typ = 'object'
                        
            # Add Outline Item
            if itmText != None:
                itm =QtGui.QTreeWidgetItem([itmText,str(lcnt)])
                trwdg.addTopLevelItem(itm)
                self.format(itm,typ)
                    
    def editorTabChanged(self,wdg):
        trwdg = self.wdgD[wdg]
        self.ui.sw_outline.setCurrentWidget(trwdg)
    
    def goto(self,itm,col):
        line = int(str(itm.text(1)))
        wdg = self.treeD[self.ui.sw_outline.currentWidget()]
        wdg.gotoLine(line)
       
    
    def format(self,itm,typ):
        # Format the tree widget item
        if typ == 'object':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(46,66,105)))
        elif typ == 'function':
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(62,121,181)))
        elif typ == 'heading':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(181,181,181)))