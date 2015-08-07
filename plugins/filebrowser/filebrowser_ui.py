# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filebrowser.ui'
#
# Created: Thu Aug  6 21:41:34 2015
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
"border-bottom-left-radius:5px;\n"
"border-bottom-right-radius:5px;\n"
"show-decoration-selected: 0;\n"
"padding-left:4px;\n"
"}\n"
"QTreeWidget::branch {  border-image: url(none.png); }\n"
"\n"
""))
        self.tr_dir.setFrameShape(QtGui.QFrame.NoFrame)
        self.tr_dir.setIndentation(12)
        self.tr_dir.setRootIsDecorated(False)
        self.tr_dir.setExpandsOnDoubleClick(False)
        self.tr_dir.setObjectName(_fromUtf8("tr_dir"))
        self.tr_dir.headerItem().setText(0, _fromUtf8("1"))
        self.tr_dir.header().setVisible(False)
        self.gridLayout.addWidget(self.tr_dir, 1, 0, 1, 2)
        self.frame = QtGui.QFrame(Form)
        self.frame.setStyleSheet(_fromUtf8("QFrame#frame {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(32, 32, 32, 255), stop:0.0590909 rgba(41, 41, 41, 255), stop:0.922727 rgba(59, 59,59, 255), stop:1 rgba(71, 71, 71, 255));\n"
"border-bottom:1px solid rgb(70,70,70);\n"
"border-top-left-radius:3px;\n"
"border-top-right-radius:3px;\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.b_browse = QtGui.QPushButton(self.frame)
        self.b_browse.setMaximumSize(QtCore.QSize(24, 24))
        self.b_browse.setStyleSheet(_fromUtf8("QPushButton {background:transparent;}"))
        self.b_browse.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/file_open2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_browse.setIcon(icon)
        self.b_browse.setIconSize(QtCore.QSize(20, 20))
        self.b_browse.setCheckable(True)
        self.b_browse.setObjectName(_fromUtf8("b_browse"))
        self.gridLayout_2.addWidget(self.b_browse, 0, 0, 1, 1)
        self.le_root = QtGui.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.le_root.setFont(font)
        self.le_root.setStyleSheet(_fromUtf8("background:transparent;\n"
"color:white;\n"
"border:0px;\n"
"padding:2px;"))
        self.le_root.setProperty("class", _fromUtf8(""))
        self.le_root.setObjectName(_fromUtf8("le_root"))
        self.gridLayout_2.addWidget(self.le_root, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "File Browser", None))
        self.tr_dir.setProperty("class", _translate("Form", "pluginVertical", None))
        self.b_browse.setToolTip(_translate("Form", "Browse folders", None))
        self.le_root.setText(_translate("Form", "/", None))
        self.le_root.setPlaceholderText(_translate("Form", "Enter Root Path", None))

