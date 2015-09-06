import os, subprocess
from PyQt4 import QtGui
    
class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Launch Console'
    location = 'app'
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        def launch_console():
            wksp_pth = ''
            if self.parent.currentWorkspace != None:
                wksp_pth = self.parent.workspaces[self.parent.currentWorkspace]['basefolder']
            else:
                try:
                    wksp_pth = self.parent.settings['plugins']['filebrowser']['defaultPath']
                except:
                    pass
            
            if os.name =='nt':
                if wksp_pth != '': wksp_pth = '/K "cd /d '+wksp_pth.replace('/','\\')+'"'
                
                os.system('start cmd '+wksp_pth)
            else:
                if wksp_pth != '': wksp_pth = '--working-directory='+wksp_pth
                subprocess.Popen(["gnome-terminal",wksp_pth])
##                os.system("gnome-terminal "+wksp_pth)
            
        # Add button 
        btn = self.parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=self.title)
        btn.clicked.connect(launch_console)
        
##    def loadWidget(self):
##        '''Load the widget'''
##        self.widget = None
##        return self.widget