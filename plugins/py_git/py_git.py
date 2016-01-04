# import legit
import sys
import os
import time
import codecs
import datetime
import git
from git import Repo
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QWidget, QFileDialog


class PyGit(QtGui.QWidget):

    def __init__(self, parent=None):
        """
        :type parent: Scope

        """
        QtGui.QWidget.__init__(self, parent)
        self.ide = parent

        self.title = title
        self.folder = folder
        # self.join = os.path.join
        self.ui = uic.loadUi('git.ui', self)
        # print 'Scope path:' + self.ide.scopePath
        # print 'Current workspace: ' + self.ide.currentWorkspace
        # self.repo = Repo(os.path.dirname(os.path.realpath(self.get_editor_file_name())))
        # print self.ide.scopePath
        # print self.ide.currentWorkspace
        # print self.ide.pluginPath+self.folder
        if self.ide.currentWorkspace is None:
            self.repo = Repo(self.ide.scopePath)
        else:
            self.repo = Repo(self.ide.currentWorkspace)

        print self.repo.active_branch
        self.ui.lblBranchText.setText(str(self.repo.head.reference))
        self.ui.lblWorkingDirText.setText(self.repo.working_dir)
        if self.repo.is_dirty():
            self.ui.lblStatusText.setText('Dirty')
        else:
            self.ui.lblStatusText.setText('Clean')
        # print self.ide.Events
        #--- Add left toolbar button
        btn = self.ide.addLeftBarButton(QtGui.QIcon('Icon.png'),tooltip=self.title)
        
        #--- Signals
        self.ui.btnGitStatus.clicked.connect(self.get_status)
        self.ui.btnUpdateWorkingDir.clicked.connect(self.working_dir)

    def get_editor_file_name(self):
        wdg = self.ide.ui.sw_main.widget(self.ide.ui.sw_main.currentIndex())
        filename = wdg.filename
        return filename


    def commit(self):
        pass
    
    def push(self):
        pass
    
    def pull(self):
        pass

    def get_status(self):
        print "status button clicked"
        self.ui.lblStatusText.setText('....')
        if self.repo.is_dirty():
            self.ui.lblStatusText.setText('Dirty')
        else:
            self.ui.lblStatusText.setText('Clean')
    def working_dir(self):
        file = self.ide.currentEditor().filename
        print file
        dir = git.repo.fun.find_git_dir(file)
        print dir
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.lblWorkingDirText.setText(file)

