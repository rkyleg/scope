from PyQt4 import QtGui, QtCore
from outline_ui import Ui_Form

def addDock(parent):
    dock = Outline(parent)
    parent.evnt.editorAdded.connect(dock.addOutline)
    parent.evnt.editorTabChanged.connect(dock.editorTabChanged)
    return dock

class outlineTree(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        QtGui.QTreeWidget.__init__(self,parent)
        self.setHeaderHidden(1)

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
        for t in txt.split('\n'):
            cnt += 1
            if wdg.lang == 'Python':
                if t.lstrip().startswith('def'):
                    trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([t.lstrip()[4:-1],str(cnt)]))
                elif t.lstrip().startswith('class'):
                    trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([t.lstrip()[6:-1],str(cnt)]))
                if t.lstrip().startswith('#---'):
                    trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([t.lstrip()[4:].lstrip('-'),str(cnt)]))
            elif wdg.lang == 'JavaScript':
                if t.lstrip().startswith('function'):
                    trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([t.lstrip()[9],str(cnt)]))
                elif t.lstrip().startswith('//---'):
                    trwdg.addTopLevelItem(QtGui.QTreeWidgetItem([t.lstrip()[5:],str(cnt)]))
                    
    def editorTabChanged(self,wdg):
        trwdg = self.wdgD[wdg]
        self.ui.sw_outline.setCurrentWidget(trwdg)
    
    def goto(self,itm,col):
        line = int(str(itm.text(1)))
        wdg = self.treeD[self.ui.sw_outline.currentWidget()]
        wdg.gotoLine(line)
