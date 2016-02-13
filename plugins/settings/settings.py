import os,sys,fnmatch
from PyQt4 import QtGui, QtCore, Qsci
from settings_ui import Ui_Form
import re, json
from collections import OrderedDict


class Settings_Editor(QtGui.QWidget):
    def __init__(self,parent=None,pth=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.IDE = parent
        
        # Add Ace editor
        import plugins.ace.ace
        self.ui.te_lang = plugins.ace.ace.WebView(self.IDE,lang='json')
        self.ui.fr_lang_ed.layout().addWidget(self.ui.te_lang)
        
        self.ui.te_editor = plugins.ace.ace.WebView(self.IDE,lang='json')
        self.ui.fr_ed_ed.layout().addWidget(self.ui.te_editor)

        self.ui.te_gen = plugins.ace.ace.WebView(self.IDE,lang='json')
        self.ui.fr_gen_ed.layout().addWidget(self.ui.te_gen)

##        import plugins.scintilla.scintilla
##        wv = plugins.scintilla.scintilla.Sci(self.IDE,Qsci.QsciLexerJavaScript(),lang='json')
        
##        self.ui.fr_lang_ed.layout().addWidget(self.ui.te_lang)
        
        # Load Settings
        self.load_settings()
        
        # Signals
        self.ui.li_catg.currentRowChanged.connect(self.catg_change)
        self.ui.b_save_ext.clicked.connect(self.save_ext)
        self.ui.b_save_lang.clicked.connect(self.save_lang)
        self.ui.b_save_editors.clicked.connect(self.save_editors)
        self.ui.b_save_gen.clicked.connect(self.save_general)
        self.ui.b_reload.clicked.connect(self.reload_settings)
    
        self.ui.li_catg.setCurrentRow(0)
    
    def reload_settings(self):
        resp = QtGui.QMessageBox.warning(self.IDE,'Reload Settings','Do you want to reload the settings?<br><br>Any unsaved settings will be lost.',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if resp == QtGui.QMessageBox.Yes:
            self.load_settings()
    
    def load_settings(self):
        setD = self.getSettingsCopy()
        
        # General
        genD = OrderedDict()
        for ky in setD:
            if ky not in ['editors','prog_lang','plugins','extensions','activePlugins','activeEditors']:
                genD[ky] = setD[ky]
        txt = json.dumps(genD,indent=4)
        self.ui.te_gen.setText(txt)
        
        # Editors
        txt = json.dumps(setD['editors'],indent=4)
        self.ui.te_editor.setText(txt)
        
        # Languages
        txt = json.dumps(setD['prog_lang'],indent=4)
        self.ui.te_lang.setText(txt)
        
        # Extensions
        txt = ''
        for ext in setD['extensions']:
            if txt != '': txt += '\n'
            txt += ext+'='+setD['extensions'][ext]
        self.ui.te_ext.setPlainText(txt)
    
    def getSettingsCopy(self):
        

##        from site_pkg.configobj import configobj
##        self.settings_filename = self.IDE.settingPath+'/scope.json'
        dflt_path = os.path.abspath(self.IDE.scopePath+'/scope/default_settings.json')
        
        # Default Settings
        with open(dflt_path,'r') as setf:
            defaultSettings = json.load(setf,object_pairs_hook=OrderedDict)
        
        mysettings={}
        if os.path.exists(self.IDE.settings_filename):
            try:
                with open(self.IDE.settings_filename,'r') as setf:
                    mysettings = json.load(setf)
            except:
                err = str(sys.exc_info()[1])
                QtGui.QMessageBox.warning(self,'Settings Load Failed','There is something wrong with the settings file and it failed to load.<br><br>Using default settings<br><br><i>Compare your settings with the scope/default_settings.json</i><br><br><b>Error:</b>'+err)
        
        defaultSettings.update(mysettings)
        
        return defaultSettings
    
    def saveSettings(self,settings):
        with open(self.IDE.settingPath+'/scope.json','w') as f:
            json.dump(settings,f,indent=4)
        
        self.IDE.ui.l_statusbar.setText('Saved: Settings')
        self.IDE.loadSettings()
    
    def appSave(self):
        ind = self.ui.sw_main.currentIndex()
        if ind == 0:
            self.save_general()
        elif ind == 1:
            self.save_editors()
        elif ind == 2:
            self.save_lang()
        elif ind == 3:
            self.save_ext()
    
    def catg_change(self,ind):
        self.ui.sw_main.setCurrentIndex(ind)
        
##        setD = self.getSettingsCopy()
##        
##        if ind == 3: # Extensions
##            txt = ''
##            for ext in setD['extensions']:
##                if txt != '': txt += '\n'
##                txt += ext+'='+setD['extensions'][ext]
##            
##            self.ui.te_ext.setPlainText(txt)
##        elif ind == 2: # Languages
##            txt = json.dumps(setD['prog_lang'],indent=4)
##            self.ui.te_lang.setText(txt)
    
    def save_ext(self):
        txt = str(self.ui.te_ext.toPlainText())
        extD = OrderedDict()
        for rw in txt.splitlines():
            if rw.strip() != '':
                exts = rw.split('=')
                if len(exts) > 1:
                    extD[exts[0].strip()] = exts[1].strip()
        
        newSettings = self.getSettingsCopy()
        newSettings['extensions'] = extD
        self.saveSettings(newSettings)
    
    def save_lang(self):
        try:
            langD = json.loads(str(self.ui.te_lang.getText()))
        except:
            QtGui.QMessageBox.warning(self.IDE,'Error Saving Language Settings','Error:<br>'+str(sys.exc_info()[1]))
        newSettings = self.getSettingsCopy()
        newSettings['prog_lang'] = langD
        self.saveSettings(newSettings)
    
    def save_editors(self):
        try:
            editorD = json.loads(str(self.ui.te_editor.getText()))
        except:
            QtGui.QMessageBox.warning(self.IDE,'Error Saving Editors Settings','Error:<br>'+str(sys.exc_info()[1]))
        newSettings = self.getSettingsCopy()
        newSettings['editors'] = editorD
        self.saveSettings(newSettings)
    
    def save_general(self):
        try:
            genD = json.loads(str(self.ui.te_gen.getText()))
        except:
            QtGui.QMessageBox.warning(self.IDE,'Error Saving General Settings','Error:<br>'+str(sys.exc_info()[1]))
        newSettings = self.getSettingsCopy()
        for ky in genD:
            newSettings[ky] = genD[ky]
        self.saveSettings(newSettings)