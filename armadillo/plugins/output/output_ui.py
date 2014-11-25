# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output.ui'
#
# Created: Mon Nov 24 20:12:55 2014
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
        Form.resize(538, 107)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tb_out = QtGui.QTextBrowser(Form)
        self.tb_out.setFrameShape(QtGui.QFrame.NoFrame)
        self.tb_out.setFrameShadow(QtGui.QFrame.Plain)
        self.tb_out.setLineWidth(0)
        self.tb_out.setOpenExternalLinks(False)
        self.tb_out.setObjectName(_fromUtf8("tb_out"))
        self.gridLayout.addWidget(self.tb_out, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

