# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outline.ui'
#
# Created: Tue Nov 25 19:17:41 2014
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
        Form.resize(285, 355)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sw_outline = QtGui.QStackedWidget(Form)
        self.sw_outline.setLineWidth(0)
        self.sw_outline.setObjectName(_fromUtf8("sw_outline"))
        self.gridLayout.addWidget(self.sw_outline, 0, 0, 1, 1)
        self.fr_find = QtGui.QFrame(Form)
        self.fr_find.setStyleSheet(_fromUtf8("QFrame#fr_find{\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0.00995025 rgba(34, 34,34, 255), stop:0.174129 rgba(65, 65, 65, 255), stop:0.890547 rgba(104, 104, 104, 255), stop:1 rgba(128, 128, 128, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-radius:3px;\n"
"}"))
        self.fr_find.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_find.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_find.setObjectName(_fromUtf8("fr_find"))
        self.gridLayout_9 = QtGui.QGridLayout(self.fr_find)
        self.gridLayout_9.setMargin(0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.le_find = QtGui.QLineEdit(self.fr_find)
        self.le_find.setMinimumSize(QtCore.QSize(150, 24))
        self.le_find.setStyleSheet(_fromUtf8("background:transparent;\n"
"border:0px;\n"
"color:white;"))
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_9.addWidget(self.le_find, 0, 0, 1, 1)
        self.b_find_close = QtGui.QPushButton(self.fr_find)
        self.b_find_close.setMaximumSize(QtCore.QSize(16777215, 25))
        self.b_find_close.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0.00995025 rgba(34, 34,34, 255), stop:0.174129 rgba(65, 65, 65, 255), stop:0.890547 rgba(104, 104, 104, 255), stop:1 rgba(128, 128, 128, 255));\n"
"border-top-right-radius:3px;\n"
"border-bottom-right-radius:3px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0.98, y1:1, x2:1, y2:0, stop:0 rgba(138, 138, 138, 255), stop:0.0646766 rgba(157, 157, 157, 255), stop:0.935323 rgba(198, 198, 198, 255), stop:1 rgba(231, 231, 231, 255));\n"
"}"))
        self.b_find_close.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/close_hover.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_find_close.setIcon(icon)
        self.b_find_close.setObjectName(_fromUtf8("b_find_close"))
        self.gridLayout_9.addWidget(self.b_find_close, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.fr_find, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.b_find_close, QtCore.SIGNAL(_fromUtf8("clicked()")), self.fr_find.hide)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.le_find.setPlaceholderText(_translate("Form", "Find", None))
        self.b_find_close.setToolTip(_translate("Form", "Hide Find", None))

