# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt2py.ui'
#
# Created: Wed Sep 25 22:33:39 2013
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
        Form.resize(575, 141)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(196, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 4)
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.b_qt_designer = QtGui.QPushButton(Form)
        self.b_qt_designer.setObjectName(_fromUtf8("b_qt_designer"))
        self.gridLayout.addWidget(self.b_qt_designer, 0, 5, 1, 1)
        self.b_convert = QtGui.QPushButton(Form)
        self.b_convert.setObjectName(_fromUtf8("b_convert"))
        self.gridLayout.addWidget(self.b_convert, 4, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.b_open = QtGui.QPushButton(Form)
        self.b_open.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_open.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/file_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_open.setIcon(icon)
        self.b_open.setObjectName(_fromUtf8("b_open"))
        self.gridLayout.addWidget(self.b_open, 2, 0, 1, 1)
        self.le_path = QtGui.QLineEdit(Form)
        self.le_path.setObjectName(_fromUtf8("le_path"))
        self.gridLayout.addWidget(self.le_path, 2, 1, 1, 5)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 5)
        self.l_result = QtGui.QLabel(Form)
        self.l_result.setText(_fromUtf8(""))
        self.l_result.setObjectName(_fromUtf8("l_result"))
        self.gridLayout.addWidget(self.l_result, 4, 2, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Qt UI to Python Converter", None))
        self.b_qt_designer.setText(_translate("Form", "Qt Designer", None))
        self.b_convert.setText(_translate("Form", "Convert", None))
        self.label_2.setText(_translate("Form", "Select .ui (Qt Designer File)", None))

