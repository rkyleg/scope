# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spellcheck.ui'
#
# Created: Thu Jul 30 01:27:24 2015
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
        Form.resize(579, 352)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.fr_main = QtGui.QFrame(Form)
        self.fr_main.setStyleSheet(_fromUtf8("QFrame#fr_main {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"border-radius:8px;\n"
"}"))
        self.fr_main.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_main.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_main.setObjectName(_fromUtf8("fr_main"))
        self.gridLayout_4 = QtGui.QGridLayout(self.fr_main)
        self.gridLayout_4.setMargin(6)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.te_text = QtGui.QPlainTextEdit(self.fr_main)
        self.te_text.setReadOnly(True)
        self.te_text.setObjectName(_fromUtf8("te_text"))
        self.gridLayout_4.addWidget(self.te_text, 2, 0, 1, 4)
        self.frame = QtGui.QFrame(self.fr_main)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(313, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.b_cancel = QtGui.QPushButton(self.frame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/close_hover.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_cancel.setIcon(icon)
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.gridLayout.addWidget(self.b_cancel, 0, 2, 1, 1)
        self.b_ok = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_ok.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/checkmark.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_ok.setIcon(icon1)
        self.b_ok.setObjectName(_fromUtf8("b_ok"))
        self.gridLayout.addWidget(self.b_ok, 0, 3, 1, 1)
        self.l_count = QtGui.QLabel(self.frame)
        self.l_count.setStyleSheet(_fromUtf8("color: rgb(184, 215, 255);"))
        self.l_count.setObjectName(_fromUtf8("l_count"))
        self.gridLayout.addWidget(self.l_count, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 3, 0, 1, 4)
        self.frame_2 = QtGui.QFrame(self.fr_main)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setContentsMargins(4, 0, 4, 0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(_fromUtf8("color: rgb(250, 255, 187);"))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 5, 1, 1)
        self.b_redo = QtGui.QPushButton(self.frame_2)
        self.b_redo.setMaximumSize(QtCore.QSize(26, 24))
        self.b_redo.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/redo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_redo.setIcon(icon2)
        self.b_redo.setObjectName(_fromUtf8("b_redo"))
        self.gridLayout_3.addWidget(self.b_redo, 0, 3, 1, 1)
        self.b_undo = QtGui.QPushButton(self.frame_2)
        self.b_undo.setMaximumSize(QtCore.QSize(26, 24))
        self.b_undo.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/undo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_undo.setIcon(icon3)
        self.b_undo.setObjectName(_fromUtf8("b_undo"))
        self.gridLayout_3.addWidget(self.b_undo, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("color:white;"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 4, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 1, 0, 1, 4)
        self.gridLayout_2.addWidget(self.fr_main, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.b_undo, QtCore.SIGNAL(_fromUtf8("clicked()")), self.te_text.undo)
        QtCore.QObject.connect(self.b_redo, QtCore.SIGNAL(_fromUtf8("clicked()")), self.te_text.redo)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.b_cancel.setText(_translate("Form", "cancel", None))
        self.b_ok.setText(_translate("Form", "apply changes", None))
        self.l_count.setText(_translate("Form", "0 changes", None))
        self.label_2.setText(_translate("Form", "Right click on word for spelling suggestions", None))
        self.b_redo.setToolTip(_translate("Form", "redo", None))
        self.b_undo.setToolTip(_translate("Form", "undo", None))
        self.label.setText(_translate("Form", "Spellcheck", None))

