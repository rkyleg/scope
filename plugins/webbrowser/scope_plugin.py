import os
from PyQt4 import QtGui, QtCore

class Settings(object):
    '''Modifiable settings and their defaults'''
    # attribute=value
    
class Plugin(object):
    title = 'Web Browser'
    location = 'app' # left, bottom, right, app
    settings = Settings.__dict__ # Settings must be a dictionary
    widget = None  # The widget for the plugin (set at getWidget)
    
    def __init__(self,parent=None):
        self.parent = parent
    
    def load(self):
        self.btn = self.parent.addLeftBarButton(QtGui.QIcon('icon.png'),tooltip=self.title)
        self.btn.clicked.connect(self.addWebBrowserWidget)
        # store widget with button (with addLeftBarButton.  if widget doesn't exist, it calls the getwidget)
        
    def loadWidget(self):
        from . import qt_webbrowser
        curdir = os.path.abspath('.')
        os.chdir(os.path.dirname(__file__))
        self.widget = qt_webbrowser.WebBrowser(self.parent)
        os.chdir(curdir)
        return self.widget
    
    def addWebBrowserWidget(self):
        if self.widget == None:
            self.loadWidget()
            ti = self.parent.ui.tab_right.addTab(self.widget,self.btn.icon(),'Web Browser')
            self.parent.ui.tab_right.setTabToolTip(ti,'Web Browser')
            html = "<style>body{background:rgb(70,70,70);}</style>"
            self.widget.ui.webView.setHtml(html)
        else:
            ti = self.parent.ui.tab_right.indexOf(self.widget)
        self.parent.ui.tab_right.setVisible(1)
        self.parent.ui.tab_right.setCurrentIndex(ti)