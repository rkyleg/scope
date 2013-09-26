# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find_replace.ui'
#
# Created: Wed Sep 25 23:07:47 2013
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
        Form.resize(536, 141)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.le_find = QtGui.QLineEdit(Form)
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_2.addWidget(self.le_find, 0, 1, 2, 1)
        self.frame = QtGui.QFrame(Form)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.b_find = QtGui.QPushButton(self.frame)
        self.b_find.setObjectName(_fromUtf8("b_find"))
        self.gridLayout.addWidget(self.b_find, 0, 0, 1, 1)
        self.b_replace = QtGui.QPushButton(self.frame)
        self.b_replace.setObjectName(_fromUtf8("b_replace"))
        self.gridLayout.addWidget(self.b_replace, 0, 1, 1, 1)
        self.b_replace_all = QtGui.QPushButton(self.frame)
        self.b_replace_all.setEnabled(False)
        self.b_replace_all.setObjectName(_fromUtf8("b_replace_all"))
        self.gridLayout.addWidget(self.b_replace_all, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(248, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 5)
        self.le_replace = QtGui.QLineEdit(Form)
        self.le_replace.setObjectName(_fromUtf8("le_replace"))
        self.gridLayout_2.addWidget(self.le_replace, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 1)
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 0, 4, 0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ckbx_wo = QtGui.QCheckBox(self.frame_2)
        self.ckbx_wo.setObjectName(_fromUtf8("ckbx_wo"))
        self.gridLayout_3.addWidget(self.ckbx_wo, 1, 0, 1, 1)
        self.ckbx_cs = QtGui.QCheckBox(self.frame_2)
        self.ckbx_cs.setObjectName(_fromUtf8("ckbx_cs"))
        self.gridLayout_3.addWidget(self.ckbx_cs, 0, 0, 1, 1)
        self.ckbx_re = QtGui.QCheckBox(self.frame_2)
        self.ckbx_re.setObjectName(_fromUtf8("ckbx_re"))
        self.gridLayout_3.addWidget(self.ckbx_re, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 0, 2, 3, 1)
        spacerItem2 = QtGui.QSpacerItem(89, 53, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 4, 3, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 2, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.le_find, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_find.click)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.le_find, self.le_replace)
        Form.setTabOrder(self.le_replace, self.b_find)
        Form.setTabOrder(self.b_find, self.b_replace)
        Form.setTabOrder(self.b_replace, self.b_replace_all)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.b_find.setText(_translate("Form", "Find", None))
        self.b_replace.setText(_translate("Form", "Replace", None))
        self.b_replace_all.setText(_translate("Form", "Replace All", None))
        self.label_2.setText(_translate("Form", "Replace With", None))
        self.ckbx_wo.setText(_translate("Form", "Whole Word", None))
        self.ckbx_cs.setText(_translate("Form", "Match Case", None))
        self.ckbx_re.setText(_translate("Form", "Reg Exp", None))
        self.label.setText(_translate("Form", "Search for", None))

