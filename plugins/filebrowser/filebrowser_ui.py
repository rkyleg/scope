# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filebrowser.ui'
#
# Created: Tue Nov 26 23:01:08 2013
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
        self.tr_dir.setStyleSheet(_fromUtf8("QTreeWidget {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(152, 152, 152, 255), stop:0.144279 rgba(169, 169, 169, 255), stop:0.850746 rgba(205, 205, 205, 255), stop:1 rgba(224, 224, 224, 255));\n"
"border-bottom-left-radius:5px;\n"
"border-bottom-right-radius:5px;\n"
"}"))
        self.tr_dir.setFrameShape(QtGui.QFrame.NoFrame)
        self.tr_dir.setIndentation(12)
        self.tr_dir.setRootIsDecorated(False)
        self.tr_dir.setExpandsOnDoubleClick(False)
        self.tr_dir.setObjectName(_fromUtf8("tr_dir"))
        self.tr_dir.headerItem().setText(0, _fromUtf8("1"))
        self.tr_dir.header().setVisible(False)
        self.gridLayout.addWidget(self.tr_dir, 1, 0, 1, 1)
        self.le_root = QtGui.QLineEdit(Form)
        self.le_root.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(29, 29, 29, 255), stop:0.0845771 rgba(54, 54, 54, 255), stop:0.850746 rgba(94, 94, 94, 255), stop:1 rgba(119, 119, 119, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-bottom:1px solid gray;"))
        self.le_root.setObjectName(_fromUtf8("le_root"))
        self.gridLayout.addWidget(self.le_root, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "File Browser", None))
        self.le_root.setText(_translate("Form", "/", None))
        self.le_root.setPlaceholderText(_translate("Form", "Enter Root Path", None))

