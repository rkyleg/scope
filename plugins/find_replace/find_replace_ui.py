# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find_replace.ui'
#
# Created: Sun Sep  4 17:22:12 2016
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
        Form.resize(605, 187)
        Form.setProperty("class", _fromUtf8(""))
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.frame_3 = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_4.setContentsMargins(10, 4, 10, 6)
        self.gridLayout_4.setHorizontalSpacing(4)
        self.gridLayout_4.setVerticalSpacing(6)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.le_find = QtGui.QLineEdit(self.frame_3)
        self.le_find.setMinimumSize(QtCore.QSize(200, 0))
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_4.addWidget(self.le_find, 0, 2, 2, 2)
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 0, 0, 2, 2)
        self.frame_2 = QtGui.QFrame(self.frame_3)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setContentsMargins(4, 0, 4, 0)
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(0)
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
        self.ckbx_whitespace = QtGui.QCheckBox(self.frame_2)
        self.ckbx_whitespace.setObjectName(_fromUtf8("ckbx_whitespace"))
        self.gridLayout_3.addWidget(self.ckbx_whitespace, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 0, 4, 3, 1)
        self.le_replace = QtGui.QLineEdit(self.frame_3)
        self.le_replace.setObjectName(_fromUtf8("le_replace"))
        self.gridLayout_4.addWidget(self.le_replace, 2, 2, 1, 2)
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 2)
        self.frame = QtGui.QFrame(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
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
        self.b_replace_all.setEnabled(True)
        self.b_replace_all.setObjectName(_fromUtf8("b_replace_all"))
        self.gridLayout.addWidget(self.b_replace_all, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 5, 0, 1, 6)
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_4.addItem(spacerItem2, 3, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(2, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 0, 5, 3, 1)
        self.gridLayout_2.addWidget(self.frame_3, 0, 1, 2, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 2, 2, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 0, 2, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.le_find, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_find.click)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.le_find, self.le_replace)
        Form.setTabOrder(self.le_replace, self.b_find)
        Form.setTabOrder(self.b_find, self.b_replace)
        Form.setTabOrder(self.b_replace, self.b_replace_all)
        Form.setTabOrder(self.b_replace_all, self.ckbx_cs)
        Form.setTabOrder(self.ckbx_cs, self.ckbx_wo)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Search for", None))
        self.ckbx_wo.setText(_translate("Form", "Whole Word", None))
        self.ckbx_cs.setText(_translate("Form", "Match Case", None))
        self.ckbx_re.setText(_translate("Form", "Reg Exp", None))
        self.ckbx_whitespace.setToolTip(_translate("Form", "Find \\n, \\t, \\r", None))
        self.ckbx_whitespace.setText(_translate("Form", "Whitespace", None))
        self.label_2.setText(_translate("Form", "Replace With", None))
        self.b_find.setText(_translate("Form", "Find", None))
        self.b_replace.setText(_translate("Form", "Replace", None))
        self.b_replace_all.setText(_translate("Form", "Replace All", None))

