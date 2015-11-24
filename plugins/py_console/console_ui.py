# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'console.ui'
#
# Created: Mon Nov 23 22:49:02 2015
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
        Form.resize(580, 272)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../scope/plugins/py_console/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tb_view = QtGui.QTextBrowser(Form)
        self.tb_view.setStyleSheet(_fromUtf8("QTextBrowser {\n"
"    background:rgb(20,20,20);\n"
"    color:white;\n"
"}"))
        self.tb_view.setObjectName(_fromUtf8("tb_view"))
        self.gridLayout_2.addWidget(self.tb_view, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(Form)
        self.frame.setStyleSheet(_fromUtf8("QFrame#frame {\n"
"   background-color:rgb(30,30,30);\n"
"   color:white;\n"
"   border-top:1px solid rgb(60,60,60)\n"
"}\n"
"QLineEdit {\n"
"border:0px;\n"
"color:white;\n"
"background:transparent;\n"
"}\n"
"QLabel {\n"
"    color:rgb(38,90,150);\n"
"font-weight:bold;\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(2, 1, 2, 1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.l_prompt = QtGui.QLabel(self.frame)
        self.l_prompt.setObjectName(_fromUtf8("l_prompt"))
        self.gridLayout.addWidget(self.l_prompt, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Python Console", None))
        self.l_prompt.setText(_translate("Form", ">>>", None))

