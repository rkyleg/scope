import os, subprocess
from PyQt4 import QtGui
    
class Plugin(object):
    title = 'Launch Console'
    location = 'app'
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        def launch_console():
            wksp_pth = None
            if self.parent.currentWorkspace != None:
                wksp_pth = self.parent.workspaces[self.parent.currentWorkspace]['basefolder']
            else:
                try:
                    wksp_pth = self.parent.settings['plugins']['filebrowser']['defaultPath']
                except:
                    pass
            
            if wksp_pth == None: wksp_pth=''
            if wksp_pth == '':
                if self.parent.currentEditor().filename != None:
                    wksp_pth = os.path.dirname(self.parent.currentEditor().filename)
            
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