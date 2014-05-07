# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'snippets.ui'
#
# Created: Tue May  6 20:28:42 2014
#      by: PyQt4 UI code generator 4.10.3
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
        Form.resize(519, 135)
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
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.le_search = QtGui.QLineEdit(self.frame)
        self.le_search.setObjectName(_fromUtf8("le_search"))
        self.gridLayout.addWidget(self.le_search, 0, 0, 1, 1)
        self.li_snips = QtGui.QListWidget(self.frame)
        self.li_snips.setObjectName(_fromUtf8("li_snips"))
        self.gridLayout.addWidget(self.li_snips, 1, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(self.split_main)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 68, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.b_save = QtGui.QPushButton(self.frame_2)
        self.b_save.setEnabled(False)
        self.b_save.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_save.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save.setIcon(icon)
        self.b_save.setObjectName(_fromUtf8("b_save"))
        self.gridLayout_2.addWidget(self.b_save, 0, 0, 1, 1)
        self.b_new = QtGui.QPushButton(self.frame_2)
        self.b_new.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_new.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_new.setIcon(icon1)
        self.b_new.setObjectName(_fromUtf8("b_new"))
        self.gridLayout_2.addWidget(self.b_new, 2, 0, 1, 1)
        self.ste_code = Qsci.QsciScintilla(self.frame_2)
        self.ste_code.setToolTip(_fromUtf8(""))
        self.ste_code.setWhatsThis(_fromUtf8(""))
        self.ste_code.setObjectName(_fromUtf8("ste_code"))
        self.gridLayout_2.addWidget(self.ste_code, 0, 1, 4, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.split_main, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Snippets", None))

from PyQt4 import Qsci
