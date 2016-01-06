# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snippets.ui'
#
# Created: Wed Jan  6 03:00:35 2016
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
        Form.resize(573, 163)
        Form.setMinimumSize(QtCore.QSize(0, 20))
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.split_main = QtGui.QSplitter(Form)
        self.split_main.setOrientation(QtCore.Qt.Horizontal)
        self.split_main.setObjectName(_fromUtf8("split_main"))
        self.frame = QtGui.QFrame(self.split_main)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setProperty("class", _fromUtf8(""))
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.le_search = QtGui.QLineEdit(self.frame)
        self.le_search.setObjectName(_fromUtf8("le_search"))
        self.gridLayout.addWidget(self.le_search, 0, 2, 1, 1)
        self.cb_ext = QtGui.QComboBox(self.frame)
        self.cb_ext.setObjectName(_fromUtf8("cb_ext"))
        self.cb_ext.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cb_ext, 0, 1, 1, 1)
        self.b_reload = QtGui.QPushButton(self.frame)
        self.b_reload.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_reload.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"border:0px;\n"
"background:transparent;\n"
"}"))
        self.b_reload.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_reload.setIcon(icon)
        self.b_reload.setObjectName(_fromUtf8("b_reload"))
        self.gridLayout.addWidget(self.b_reload, 0, 0, 1, 1)
        self.li_snips = QtGui.QListWidget(self.frame)
        self.li_snips.setStyleSheet(_fromUtf8("QListWidget {background:transparent;border-top:1px solid rgb(80,80,80);}\n"
"QListWidget::item {\n"
"border-bottom:1px solid rgb(80,80,80);\n"
"}"))
        self.li_snips.setFrameShape(QtGui.QFrame.NoFrame)
        self.li_snips.setProperty("isWrapping", False)
        self.li_snips.setResizeMode(QtGui.QListView.Adjust)
        self.li_snips.setViewMode(QtGui.QListView.ListMode)
        self.li_snips.setObjectName(_fromUtf8("li_snips"))
        self.gridLayout.addWidget(self.li_snips, 1, 0, 1, 4)
        self.frame_2 = QtGui.QFrame(self.split_main)
        self.frame_2.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(94, 94, 94, 255), stop:0.174129 rgba(125, 125, 125, 255), stop:0.890547 rgba(164, 164, 164, 255), stop:1 rgba(188, 188, 188, 255));\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(114, 114, 114, 255), stop:0.174129 rgba(145, 145, 145, 255), stop:0.890547 rgba(184, 184, 184, 255), stop:1 rgba(208, 208, 208, 255));\n"
"}"))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setProperty("class", _fromUtf8(""))
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.te_code = QtGui.QPlainTextEdit(self.frame_2)
        self.te_code.setStyleSheet(_fromUtf8("background:transparent;"))
        self.te_code.setFrameShape(QtGui.QFrame.NoFrame)
        self.te_code.setReadOnly(True)
        self.te_code.setObjectName(_fromUtf8("te_code"))
        self.gridLayout_2.addWidget(self.te_code, 0, 2, 6, 1)
        self.frame_3 = QtGui.QFrame(self.frame_2)
        self.frame_3.setStyleSheet(_fromUtf8("QFrame#frame_3 {\n"
"border-left:1px solid rgba(130,130,130,200);\n"
"border-right:1px solid rgba(130,130,130,200);\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0 rgba(50, 50, 50, 255), stop:0.831818 rgba(80, 80, 80, 255), stop:1 rgba(100, 100, 100, 255));\n"
"}\n"
"QPushButton,QToolButton {\n"
"background:transparent;\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"    width:30px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:1, stop:0 rgba(75, 75, 75, 100), stop:0.154545 rgba(106, 106, 106, 100), stop:0.831818 rgba(134, 134, 134, 100), stop:1 rgba(142, 142, 142, 100));\n"
"}"))
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.b_insert = QtGui.QPushButton(self.frame_3)
        self.b_insert.setMaximumSize(QtCore.QSize(28, 16777215))
        self.b_insert.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-bottom:1px solid rgb(100,100,100);\n"
"    border-top-right-radius:5px;\n"
"    border-top-left-radius:5px;\n"
"}"))
        self.b_insert.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_insert.setIcon(icon1)
        self.b_insert.setObjectName(_fromUtf8("b_insert"))
        self.gridLayout_4.addWidget(self.b_insert, 0, 0, 1, 1)
        self.b_new = QtGui.QPushButton(self.frame_3)
        self.b_new.setMaximumSize(QtCore.QSize(28, 16777215))
        self.b_new.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-top:1px solid rgb(100,100,100);\n"
"}"))
        self.b_new.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_new.setIcon(icon2)
        self.b_new.setObjectName(_fromUtf8("b_new"))
        self.gridLayout_4.addWidget(self.b_new, 2, 0, 1, 1)
        self.b_edit = QtGui.QPushButton(self.frame_3)
        self.b_edit.setMaximumSize(QtCore.QSize(28, 16777215))
        self.b_edit.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_edit.setIcon(icon3)
        self.b_edit.setObjectName(_fromUtf8("b_edit"))
        self.gridLayout_4.addWidget(self.b_edit, 1, 0, 1, 1)
        self.b_fldr = QtGui.QPushButton(self.frame_3)
        self.b_fldr.setMaximumSize(QtCore.QSize(28, 16777215))
        self.b_fldr.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-top:1px solid rgb(100,100,100);\n"
"    border-bottom-right-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}"))
        self.b_fldr.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/folder_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_fldr.setIcon(icon4)
        self.b_fldr.setObjectName(_fromUtf8("b_fldr"))
        self.gridLayout_4.addWidget(self.b_fldr, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_3, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.split_main, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Snippets", None))
        self.split_main.setProperty("class", _translate("Form", "pluginHorizontal", None))
        self.le_search.setPlaceholderText(_translate("Form", "search", None))
        self.cb_ext.setItemText(0, _translate("Form", "All", None))
        self.b_reload.setToolTip(_translate("Form", "reload snippets directory", None))
        self.b_insert.setToolTip(_translate("Form", "insert into current editor", None))
        self.b_new.setToolTip(_translate("Form", "new snippet", None))
        self.b_edit.setToolTip(_translate("Form", "edit snippet", None))
        self.b_fldr.setToolTip(_translate("Form", "open snippet directory", None))

