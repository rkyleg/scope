from PyQt4 import QtGui, QtCore
from outline_ui import Ui_Form
import re

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
##        if 'editingFinished' in  dir(wdg):
##            wdg.evnt.editingFinished.connect(self.updateOutline)
            
        if 'gotoLine' in dir(wdg):
            trwdg.itemDoubleClicked.connect(self.goto)

    def updateOutline(self,wdg):
        trwdg = self.wdgD[wdg]
        if wdg.lang != 'Text':
            cnt = -1
            trwdg.clear()
            txt = unicode(wdg.getText())
            txtlines = txt.replace('\r\n','\n').replace('\r','\n').split('\n')
            for t in txtlines:
                cnt += 1
                lcnt = cnt
                typ = None
                itmText = None
                spc = (len(t) -len(t.lstrip()))*' '
                tls = t.lstrip()
                
                #---Python
                if wdg.lang == 'python':
                    if tls.startswith('def '):
                        itmText = tls[4:-1]
                        typ = 'function'
                    elif tls.startswith('class '):
                        itmText =tls[6:-1]
                        typ = 'object'
                    elif tls.startswith('#---'):
                        itmText =tls[4:].lstrip('-')
                        ##if itmText == '': itmText = None
                        typ = 'heading'
                    
                #--- Javascript
                elif wdg.lang == 'javascript':
                    if tls.startswith('function'):
                        itmText =tls[9:].rstrip()
                        if itmText.endswith('{'): itmText = itmText[:-1]
                        typ = 'function'
                    elif tls.startswith('//---'):
                        itmText =tls[5:]
                        typ = 'heading'
##                    elif 'function' in t and not tls.startswith('//'):
##                        itmText =tls
##                    if itmText.endswith('{'): itmText = itmText[:-1]
##                        typ = 'function'                
                #--- CSS
                elif wdg.lang == 'css':
                    if tls.startswith('/*---'):
                        itmText =tls[5:].split('*/')[0]
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
                
                #--- HTML
                elif wdg.lang == 'html':
                    if tls.lower().startswith('<body'):
                        itmText = '<BODY>'
                        typ = 'object'
                    elif tls.lower().startswith('<head'):
                        itmText = '<HEAD>'
                        typ = 'object'
                    elif tls.lower().startswith('<table'):
                        itmText = '<TABLE>'
                        typ = 'object'
                    elif tls.startswith('<!---'):
                        itmText =tls[5:].replace('-->','')
                        typ = 'heading'
                
                #--- Markdown
                elif wdg.lang == 'markdown':
                    if tls.startswith('#'): # Heading
                        h = tls.split(' ')[0].count('#')
                        head = tls.replace('#','')
                        itmText = (h-1)*4*' '+head
                        if h==1:
                            typ='object'
                        else:
                            typ='function'
                
                # Add Outline Item
                if itmText != None:
                    itmText = spc +itmText
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
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(52,111,171)))
        elif typ == 'heading':
            fnt=QtGui.QFont()
            fnt.setBold(1)
            itm.setFont(0,fnt)
            itm.setForeground(0,QtGui.QBrush(QtGui.QColor(120,120,120)))