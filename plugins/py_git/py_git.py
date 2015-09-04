# import legit
import sys
import os
import time
import codecs
import datetime
from git import Repo
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QWidget, QFileDialog


class PyGit(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ide = parent
        # self.join = os.path.join
        self.ui = uic.loadUi('git.ui', self)
        # self.ui.setupUi(self)
        # print 'Scope path:' + self.ide.scopePath
        # print 'Current workspace: ' + self.ide.currentWorkspace
        # self.repo = Repo(os.path.dirname(os.path.realpath(self.get_editor_file_name())))
        if self.ide.currentWorkspace is None:
            self.repo = Repo(self.ide.scopePath)
        else:
            self.repo = Repo(self.ide.currentWorkspace)
        self.ui.lblGitBranch.setText(str(self.repo.head.reference))

    def get_editor_file_name(self):
        wdg = self.ide.ui.sw_main.widget(self.ide.ui.sw_main.currentIndex())
        filename = wdg.filename
        return filename
