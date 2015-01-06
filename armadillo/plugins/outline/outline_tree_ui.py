# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outline_tree.ui'
#
# Created: Mon Jan  5 23:23:15 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Outline_Tree(object):
    def setupUi(self, Outline_Tree):
        Outline_Tree.setObjectName(_fromUtf8("Outline_Tree"))
        Outline_Tree.resize(196, 308)
        self.gridLayout = QtGui.QGridLayout(Outline_Tree)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.l_title = QtGui.QLabel(Outline_Tree)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_title.setFont(font)
        self.l_title.setStyleSheet(_fromUtf8("    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(48, 85, 100, 255), stop:0.21267 rgba(61, 107, 127, 255), stop:0.831818 rgba(72, 127, 150, 255), stop:1 rgba(104, 166, 175, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-bottom:1px solid gray;\n"
"padding:2px;\n"
"border-top-left-radius:3px;\n"
"border-top-right-radius:3px;"))
        self.l_title.setText(_fromUtf8(""))
        self.l_title.setWordWrap(True)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout.addWidget(self.l_title, 0, 0, 1, 1)
        self.tr_outline = QtGui.QTreeWidget(Outline_Tree)
        self.tr_outline.setStyleSheet(_fromUtf8("QTreeWidget {\n"
"border-bottom-left-radius:5px;\n"
"border-bottom-right-radius:5px;\n"
"show-decoration-selected: 0;\n"
"}"))
        self.tr_outline.setRootIsDecorated(False)
        self.tr_outline.setObjectName(_fromUtf8("tr_outline"))
        self.tr_outline.headerItem().setText(0, _fromUtf8("1"))
        self.tr_outline.header().setVisible(False)
        self.gridLayout.addWidget(self.tr_outline, 1, 0, 1, 1)

        self.retranslateUi(Outline_Tree)
        QtCore.QMetaObject.connectSlotsByName(Outline_Tree)

    def retranslateUi(self, Outline_Tree):
        Outline_Tree.setWindowTitle(_translate("Outline_Tree", "Form", None))

