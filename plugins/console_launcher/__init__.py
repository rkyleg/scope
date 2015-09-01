import os
from PyQt4 import QtGui

title = 'Launch Console'
location = 'app'

def loadPlugin(parent):
    def launch_console():
        wksp_pth = ''
        if parent.currentWorkspace != None:
            wksp_pth = '--working-directory='+parent.workspaces[parent.currentWorkspace]['basefolder']
        
        if os.name =='nt':
            os.system('cmd')
        else:
            os.system("gnome-terminal "+wksp_pth)
        
    # Add button 
    btn = parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=title)
    btn.clicked.connect(launch_console)