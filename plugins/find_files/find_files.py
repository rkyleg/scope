import os,sys,fnmatch
from PyQt4 import QtGui, QtCore
from find_in_files_ui import Ui_Form
    
class Find_Files(QtGui.QWidget):
    def __init__(self,parent=None,pth=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.IDE = parent
        
        # Set Default Path
        if pth == None:
            pth = os.path.expanduser('~')
        self.ui.le_path.setText(pth)
        
        # Signals
        self.ui.b_search.clicked.connect(self.search_click)
        self.ui.b_browse.clicked.connect(self.browse)
        self.ui.tr_results.itemDoubleClicked.connect(self.itmDClick)
        
        self.ui.tr_results.resizeColumnToContents(1)
        self.ui.tr_results.sortByColumn(0,0)
    
    def search_click(self):
        if self.ui.b_search.isChecked():
##            self.ui.b_search.setIcon(QtGui.QIcon('../img/stop.png'))
            self.search()
    
    def search(self):
        pth = str(self.ui.le_path.text())
        ext = tuple(str(self.ui.le_ext.text()).split(','))
        stxt = str(self.ui.le_search.text())
        
        self.ui.tr_results.clear()
        
##        if stxt == '':
##            QtGui.QMessageBox.warning(self,'No Search Term','Please enter a search term')
            
        if not os.path.exists(pth):
            QtGui.QMessageBox.warning(self,'Invalid Path','The path is invalid<br><br>'+pth)
        else:
            for root, dirnames, filenames in os.walk(pth):
##                for filename in fnmatch.filter(filenames, ext):
                self.ui.l_cur_file.setText(root)
                QtGui.QApplication.processEvents()
                if not self.ui.b_search.isChecked(): break
                
                for filename in filenames:
                    filepath = os.path.join(root,filename)
                    self.ui.l_cur_file.setText(filepath)
                    QtGui.QApplication.processEvents()
                    if not self.ui.b_search.isChecked(): break
                    
                    # Search in file
                    if filename.endswith(ext):

                        itm = None
                        
                        if stxt in filename:
                            itm = self.addFileItem(filepath)
                        
                        # Check in file
                        cnt = 0
                        line_cnt = 0
                        try:
                            with open(filepath, 'r') as searchfile:
                                for line in searchfile:
                                    cnt +=1
                                    if stxt in line:
                                        line_cnt +=1
                                        if itm == None: itm = self.addFileItem(filepath)
##                                        l = str(cnt),line.replace('\n','').replace('\r','').lstrip()
                                        l = line.replace('\n','').replace('\r','')
                                        litm = QtGui.QTreeWidgetItem(['',str(cnt),l])
                                        for i in range(3):
                                            litm.setBackground(i,QtGui.QBrush(QtGui.QColor(30,30,30)))
                                        litm.setForeground(2,QtGui.QBrush(QtGui.QColor(255,255,255)))
                                        litm.setForeground(1,QtGui.QBrush(QtGui.QColor(150,150,150)))
                                        litm.setTextAlignment(1,2)
                                        itm.addChild(litm)
    ##                                    print line
                                    if not self.ui.b_search.isChecked(): break
                        except:
                            print('ERROR opening: '+filepath)
                        
                        if itm != None:
                            itm.setText(1,str(line_cnt))

        self.ui.l_cur_file.setText('')
        self.ui.b_search.setChecked(0)
        
        self.ui.tr_results.resizeColumnToContents(0)
        self.ui.tr_results.resizeColumnToContents(2)
    
    def addFileItem(self,filename,lines = 0):
        pth,f = os.path.split(filename)
        itm = QtGui.QTreeWidgetItem([f,str(lines),pth])
        
        # Set icon
        if self.IDE != None:
            ext = f.split('.')[-1]
            if ext in ['png','jpg','jpeg','gif','bmp','ico']:
                ipth = filename
            elif ext in self.IDE.settings['extensions']:
                ext = self.IDE.settings['extensions'][ext]
                ipth = self.IDE.iconPath+'files/'+ext+'.png'
            else:
                ipth = self.IDE.iconPath+'files/_blank.png'
            
            itm.setIcon(0,QtGui.QIcon(ipth))

##        for i in range(3):
##            itm.setBackground(i,QtGui.QBrush(QtGui.QColor(37,65,78)))
##            itm.setForeground(i,QtGui.QBrush(QtGui.QColor(255,255,255)))
        self.ui.tr_results.addTopLevelItem(itm)
        
        return itm
    
    def browse(self):
##        print self.ui.le_path.text()
        npth = QtGui.QFileDialog.getExistingDirectory(self,'Select directory to search',self.ui.le_path.text())
        if not npth.isEmpty(): self.ui.le_path.setText(npth)
    
    #---IDE Functions
    def itmDClick(self,itm,col):
        if self.IDE != None:
            if itm.parent() != None:
                pth = os.path.join(str(itm.parent().text(2)),str(itm.parent().text(0)))
                ok = self.IDE.openFile(pth)
##                print 'ok',ok,'goto',int(str(itm.text(1)))-1
                if ok: 
                    self.IDE.currentEditor().gotoLine(int(str(itm.text(1)))-1)
            elif col > 0:
                pth = os.path.join(str(itm.text(2)),str(itm.text(0)))
                self.IDE.openFile(pth)
    
    def toggle(self):
        self.IDE.ui.sw_main.setCurrentWidget(self)

def runui():
    app = QtGui.QApplication(sys.argv)
    appui = Find_Files(pth = os.path.expanduser('~'))
    appui.ui.le_ext.setText('.py')
    appui.ui.le_search.setText('outline')
    appui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runui()
