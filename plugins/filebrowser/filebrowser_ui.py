# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filebrowser.ui'
#
# Created: Mon Nov 25 20:41:59 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(231, 434)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tr_dir = QtGui.QTreeWidget(Form)
        self.tr_dir.setIndentation(12)
        self.tr_dir.setRootIsDecorated(False)
        self.tr_dir.setExpandsOnDoubleClick(False)
        self.tr_dir.setObjectName(_fromUtf8("tr_dir"))
        self.tr_dir.headerItem().setText(0, _fromUtf8("1"))
        self.tr_dir.header().setVisible(False)
        self.gridLayout.addWidget(self.tr_dir, 1, 0, 1, 1)
        self.le_root = QtGui.QLineEdit(Form)
        self.le_root.setObjectName(_fromUtf8("le_root"))
        self.gridLayout.addWidget(self.le_root, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "File Browser", None))
        self.le_root.setText(_translate("Form", "/", None))
        self.le_root.setPlaceholderText(_translate("Form", "Enter Root Path", None))

