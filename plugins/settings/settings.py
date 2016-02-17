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
        self.ui.te_json = plugins.ace.ace.WebView(self.IDE,lang='json')
        self.ui.fr_json.layout().addWidget(self.ui.te_json)

##        import plugins.scintilla.scintilla
##        wv = plugins.scintilla.scintilla.Sci(self.IDE,Qsci.QsciLexerJavaScript(),lang='json')
        
##        self.ui.fr_lang_ed.layout().addWidget(self.ui.te_lang)
        
        # Setup Plugins file
        if not os.path.exists(os.path.join(self.IDE.settingPath,'plugins.json')):
            import shutil
            shutil.copyfile(os.path.abspath(os.path.dirname(__file__))+'/plugins.json',os.path.join(self.IDE.settingPath,'plugins.json'))
        
        self.ui.split_v.setSizes([self.IDE.width()/2,self.IDE.width()/2])
        self.ui.split_h.setSizes([self.IDE.height()/2,self.IDE.height()/2])
        
        self.ui.fr_plugins.hide()
        
        # Signals
        self.ui.li_catg.currentRowChanged.connect(self.catg_change)
        self.ui.b_save_json.clicked.connect(self.save_json)

        self.ui.tr_plugins.itemDoubleClicked.connect(self.plugin_dclick)
        self.ui.b_plugin_file_add.clicked.connect(self.plugin_add_file)
        self.ui.b_plugin_url_add.clicked.connect(self.plugin_add_url)
        
        self.ui.tr_plugins.itemSelectionChanged.connect(self.plugin_select)
        
        self.ui.li_catg.setCurrentRow(0)
    
    def getSettingsCopy(self):
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
    
##    def appSave(self):
##        ind = self.ui.li_catg.currentIndex()
##        if ind == 0:
##            self.save_general()
##        elif ind == 1:
##            self.save_editors()
##        elif ind == 2:
##            self.save_lang()
##        elif ind == 3:
##            self.save_ext()
    
    def catg_change(self,ind):
        
        setD = self.getSettingsCopy()
        
        h=''
        if ind == 4: # Plugins
##            self.ui.sw_main.setCurrentIndex(1)
            with open(self.IDE.pluginPath+'/settings/docs/plugins.html','r') as f:
                h = f.read()
            self.load_plugins()
            
            self.ui.fr_plugins.show()
            txt = ''
            title = 'Plugin'
            self.ui.fr_json.setEnabled(0)
        else:
##            self.ui.sw_main.setCurrentIndex(0)
            
            self.ui.fr_plugins.hide()
            
            if ind == 0: # General
                title = 'General'
                with open(self.IDE.pluginPath+'/settings/docs/general.html','r') as f:
                    h = f.read()
                
                genD = OrderedDict()
                for ky in setD:
                    if ky not in ['editors','prog_lang','plugins','extensions','activePlugins']:
                        genD[ky] = setD[ky]
                txt = json.dumps(genD,indent=4)
                
            elif ind == 1: # Editors
                title = 'Editors'
                with open(self.IDE.pluginPath+'/settings/docs/editors.html','r') as f:
                    h = f.read()
                
                txt = json.dumps(setD['editors'],indent=4)
            elif ind == 2: # Languages
                title = 'Programing Languages'
                with open(self.IDE.pluginPath+'/settings/docs/languages.html','r') as f:
                    h = f.read()
                
                txt = json.dumps(setD['prog_lang'],indent=4)
            elif ind == 3: # Extensions
                title = 'Extensions'
                with open(self.IDE.pluginPath+'/settings/docs/extensions.html','r') as f:
                    h = f.read()
                
                txt = json.dumps(setD['extensions'],indent=4)
            
        self.ui.te_json.setText(txt)
    
        self.ui.l_title.setText(' '+title+' Settings')
        self.ui.tb_help.setHtml(h)
        
    def save_json(self):
        ind = self.ui.li_catg.currentRow()
        newSettings = self.getSettingsCopy()
        
        ok = 0
        
        # Get current settings
        try:
            jsonD = json.loads(str(self.ui.te_json.getText()),object_pairs_hook=OrderedDict)
            ok = 1
        except:
            QtGui.QMessageBox.warning(self.IDE,'Error Saving General Settings','Error:<br>'+str(sys.exc_info()[1]))
        
        if ok:
            if ind == 0: # General
                for ky in jsonD:
                    newSettings[ky] = jsonD[ky]
            elif ind == 1: # Editors
                newSettings['editors'] = jsonD
            elif ind == 2: # Languages
                newSettings['prog_lang']  = jsonD
            elif ind == 3: # Extensions
                newSettings['extensions'] = jsonD
            elif ind == 4: # Plugins
                itm = self.ui.tr_plugins.currentItem()
                if itm != None:
                    plug = str(itm.plug)
                    newSettings['plugins'][plug]=jsonD
                    
            self.saveSettings(newSettings)
    
    #---Plugins
    def load_plugins(self):
        # Plugins
        with open(os.path.join(self.IDE.settingPath,'plugins.json'),'r') as f:
            pluginD = json.load(f)
        
        self.ui.tr_plugins.clear()
        for plug in sorted(pluginD.keys()):
            if not plug in ['settings']:
                enbl=''
                if plug in self.IDE.pluginD:
                    enbl = 'Y'
                itm = QtGui.QTreeWidgetItem([pluginD[plug]['title'],enbl,pluginD[plug]['desc']])
                itm.plug = plug
                self.ui.tr_plugins.addTopLevelItem(itm)
        self.ui.tr_plugins.resizeColumnToContents(0)
        self.ui.tr_plugins.resizeColumnToContents(1)

    def plugin_dclick(self,itm,col):
        if col == 1:
            newSettings = self.getSettingsCopy()
            plug = str(itm.plug)
            if str(itm.text(col)) == 'Y':
                itm.setText(col,'')
                newSettings['activePlugins'].remove(plug)
            else:
                itm.setText(col,'Y')
                newSettings['activePlugins'].append(plug)
                
                if not plug in self.IDE.pluginD:
                    self.IDE.loadPlugin(plug)
                
            self.saveSettings(newSettings)
    
    def plugin_select(self):
        itm = self.ui.tr_plugins.currentItem()
        if itm != None:
            plug = str(itm.plug)
            self.ui.fr_json.setEnabled(1)
            
            # Main settings
            scopeSettings = self.getSettingsCopy()
            
            # Load Settings
            with open(os.path.join(self.IDE.pluginPath,plug+'/plugin.json'),'r') as f:
                plugD = json.load(f,object_pairs_hook=OrderedDict)
            
            pD = OrderedDict()
            for ky in plugD['settings']:
                pD[ky] = plugD['settings'][ky]
            
                if plug in scopeSettings['plugins']:
                    if ky in scopeSettings['plugins'][plug]:
                        pD[ky] = scopeSettings['plugins'][plug][ky]
            
            self.ui.te_json.setText(json.dumps(pD,indent=4))
            self.ui.l_title.setText(itm.text(0)+' Plugin Settings')
    
    def plugin_add_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Select Plugin Zip File",self.IDE.currentPath," (*.zip)")
        if not filename.isEmpty():
            self.installPlugin(str(filename))

    def plugin_add_url(self):
        resp,ok = QtGui.QInputDialog.getText(self,'Add Plugin','Paste the url to the plugin zip file')
        if ok:
            self.installPlugin(str(resp))

    def installPlugin(self,plugin_pkg):

        import zipfile
        
        if plugin_pkg.startswith('http'):
            import requests, StringIO
            r = requests.get(plugin_pkg)
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
        else:
            z = zipfile.ZipFile(plugin_pkg,'r')
        
        # Ignore root directory in zip
        root = z.namelist()[0].split('/')[0]+'/'
        
        # Get Plugin Info
        plugD = json.loads(z.read(root+'plugin.json'))
        
        plugin_name = plugD['folder_name']
        
        # Check Plugin Name
        plug_path = os.path.join(self.IDE.pluginPath,plugin_name)
        
        ok = 0
        if not os.path.exists(plug_path):
            os.mkdir(plug_path)
            ok = 1
        else:
            resp = QtGui.QMessageBox.warning(self.IDE,'Plugin Exists','This plugin already exists. Do you want to overwrite the current plugin?',QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
            if resp == QtGui.QMessageBox.Yes:
                ok = 1
        
        if ok:
            for zfile in z.namelist():
                npth = str(zfile).replace(root,'')
                if npth != '':
                    if npth.endswith('/'):
                        if not os.path.exists(os.path.join(plug_path,npth)):
                            os.mkdir(os.path.join(plug_path,npth))
                    else:
                        data = z.read(zfile)
                        myfile = open(os.path.join(plug_path,npth), "wb")
                        myfile.write(data)
                        myfile.close()
        
        z.close()
        
        # Add to plugins.json file
        if ok:
            with open(os.path.join(self.IDE.settingPath,'plugins.json'),'r') as f:
                pluginD = json.load(f)
            
            pluginD[plugin_name]={'title':plugD['title'],'desc':plugD['desc'],'version':plugD['version']}
            with open(os.path.join(self.IDE.settingPath,'plugins.json'),'w') as f:
                json.dump(pluginD,f,indent=4)
                
            self.load_plugins()