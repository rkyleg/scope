# import os, subprocess
from . import py_git


class Settings(object):
    pass


class Plugin(object):
    title = 'Git'
    folder = 'py_git'
    location = 'bottom'
    settings = Settings.__dict__
    widget = None

    def __init__(self, parent=None):
        self.parent = parent

    def load(self):
#       btn = self.parent.addLeftBarButton(QtGui.QIcon('icon.png'), tooltip=self.title)
        pass

    def loadWidget(self):
        self.widget = py_git.PyGit(self.parent, self.title, self.folder)
        return self.widget
