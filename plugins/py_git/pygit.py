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
		self.repo = Repo('../../.git')
		self.ui.lblGitBranch.setText(str(self.repo.head.reference))

