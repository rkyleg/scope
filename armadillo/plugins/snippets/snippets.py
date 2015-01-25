from PyQt4 import QtGui, QtCore
from .snippets_ui import Ui_Form
import os

ignore_ext = ['pyc']

class Snippets(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.armadillo = parent
        
        self.snip_fldr = r'E:\snippets\\'
        self.snip_fldr = self.armadillo.settings['plugins']['snippets']['path']
        if self.snip_fldr == '':
            self.snip_fldr = self.armadillo.settingPath+'/snippets'
        
        self.snip_fldr = self.snip_fldr.replace('\\','/')
        if not self.snip_fldr.endswith('/'):
            self.snip_fldr+='/'
        
##        print self.snip_fldr
        if not os.path.exists(self.snip_fldr):
            try:
                os.mkdir(self.snip_fldr)
            except:
                QtGui.QMessageBox.warning(self,'Snippet Directory Error','There was an error creating the snippets folder')
                
        
        self.ui.split_main.setSizes([200,500])
        
        # Signals
        self.ui.cb_ext.currentIndexChanged.connect(self.load_list)
        self.ui.le_search.textChanged.connect(self.search_list)
        self.ui.li_snips.currentItemChanged.connect(self.sel_snip)
        self.ui.li_snips.itemDoubleClicked.connect(self.copy_snip)
        
        self.ui.b_copy.clicked.connect(self.copy_snip)
        self.ui.b_edit.clicked.connect(self.edit_snip)
        self.ui.b_new.clicked.connect(self.new_snip)
        self.ui.b_fldr.clicked.connect(self.open_snip_dir)
        
        self.ui.b_reload.clicked.connect(self.load_ext)
        
        # Startup
        self.load_ext()
##        self.load_list()

    def load_ext(self):
        exts = []
        prev_ext = str(self.ui.cb_ext.currentText())
        if os.path.exists(self.snip_fldr):
            for f in os.listdir(self.snip_fldr):
                ext = f.split('.')[-1].lower()
                if ext not in exts and ext != '':
                    exts.append(ext)
            
            self.ui.cb_ext.clear()
            self.ui.cb_ext.addItem('all')
            ind = 0
            cnt = 0
            for e in exts:
                cnt += 1
                if e == prev_ext: ind = cnt
                self.ui.cb_ext.addItem(e)
            
            self.ui.cb_ext.setCurrentIndex(ind)
    
    def load_list(self):
        filter = str(self.ui.cb_ext.currentText())
        
        self.ui.li_snips.clear()
        if os.path.exists(self.snip_fldr):
            for f in sorted(os.listdir(self.snip_fldr),key=lambda x: x.lower()):
                if os.path.isfile(self.snip_fldr+f):
                    ext = f.split('.')[-1].lower()
                    if (filter == 'all' or filter==ext) and ext not in ignore_ext:
                        itm = QtGui.QListWidgetItem(f)
                        ipth = '/a'
                        if ext in self.armadillo.settings['extensions']:
                            ipth = self.armadillo.iconPath+'files/'+self.armadillo.settings['extensions'][ext]+'.png'
                        if os.path.exists(ipth):
                            icn = QtGui.QIcon(ipth)
                        elif os.path.exists(self.armadillo.iconPath+'files/'+ext+'.png'):
                            icn = QtGui.QIcon(self.armadillo.iconPath+'files/'+ext+'.png')
                        else:
                            icn = QtGui.QIcon(self.armadillo.iconPath+'files/_blank.png')
                        itm.setIcon(icn)
                        self.ui.li_snips.addItem(itm)
                    
            
            self.search_list()

    def search_list(self):
        txt = str(self.ui.le_search.text()).lower()
        for i in range(self.ui.li_snips.count()):
            itm = self.ui.li_snips.item(i)
            if txt in str(itm.text()).lower() or txt == '':
                itm.setHidden(0)
            else:
                itm.setHidden(1)
    
    #---Snippets
    def sel_snip(self):
        itm = self.ui.li_snips.currentItem()
        txt = ''
        if itm != None:
            if os.path.exists(self.snip_fldr+str(itm.text())):
                f = open(self.snip_fldr+str(itm.text()),'r')
                txt = f.read()
                f.close()
            else:
                txt = 'file not found'
        self.ui.te_code.setPlainText(txt)
    
    def new_snip(self):
        resp,ok = QtGui.QInputDialog.getText(self,'New Snippet','Enter the filename for the new snippet (including the extension)')
        if ok and not resp.isEmpty():
            filename = self.snip_fldr+str(resp)
##            print filename
            if os.path.exists(filename):
                QtGui.QMessageBox.warning(self,'Snippet Exists','A snippet with that name already exists')
            else:
                f=open(filename,'w')
                f.write('')
                f.close()
                self.armadillo.openFile(filename)
                self.load_list()
    
    def edit_snip(self):
        itm = self.ui.li_snips.currentItem()
        if itm != None:
            pth=self.snip_fldr+str(itm.text())
            self.armadillo.openFile(pth)
    
    def copy_snip(self):
        clip = QtGui.QApplication.clipboard()
        clip.setText(self.ui.te_code.toPlainText())
    
    def open_snip_dir(self):
        try:
            os.startfile(self.snip_fldr)
        except:
            import subprocess
            subprocess.Popen(['xdg-open', self.snip_fldr])