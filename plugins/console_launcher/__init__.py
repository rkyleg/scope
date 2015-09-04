import os
from PyQt4 import QtGui

title = 'Launch Console'
location = 'app'

def loadPlugin(parent):
    def launch_console():
        wksp_pth = ''
        if parent.currentWorkspace != None:
            wksp_pth = parent.workspaces[parent.currentWorkspace]['basefolder']
        else:
            try:
                wksp_pth = parent.settings['plugins']['filebrowser']['defaultPath']
            except:
                pass
        
        if os.name =='nt':
            if wksp_pth != '': wksp_pth = '/K "cd /d '+wksp_pth.replace('/','\\')+'"'
            os.system('start cmd '+wksp_pth)
        else:
            if wksp_pth != '': wksp_pth = '--working-directory='+wksp_pth
            os.system("gnome-terminal "+wksp_pth)
        
    # Add button 
    btn = parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=title)
    btn.clicked.connect(launch_console)