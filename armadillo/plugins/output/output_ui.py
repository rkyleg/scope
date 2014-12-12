# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output.ui'
#
# Created: Thu Dec 11 22:25:16 2014
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
        Form.resize(538, 114)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.split_pages = QtGui.QSplitter(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.split_pages.sizePolicy().hasHeightForWidth())
        self.split_pages.setSizePolicy(sizePolicy)
        self.split_pages.setOrientation(QtCore.Qt.Horizontal)
        self.split_pages.setObjectName(_fromUtf8("split_pages"))
        self.li_pages = QtGui.QListWidget(self.split_pages)
        self.li_pages.setStyleSheet(_fromUtf8("QListWidget#li_pages {\n"
"background:transparent;\n"
"}\n"
"QListWidget::item:selected {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(48, 85, 100, 255), stop:0.21267 rgba(61, 107, 127, 255), stop:0.831818 rgba(72, 127, 150, 255), stop:1 rgba(104, 166, 175, 255));\n"
"color:white;\n"
"border-top-right-radius:5px;\n"
"border-bottom-right-radius:5px;\n"
"}"))
        self.li_pages.setFrameShape(QtGui.QFrame.NoFrame)
        self.li_pages.setObjectName(_fromUtf8("li_pages"))
        self.sw_pages = QtGui.QStackedWidget(self.split_pages)
        self.sw_pages.setObjectName(_fromUtf8("sw_pages"))
        self.gridLayout.addWidget(self.split_pages, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.li_pages, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.sw_pages.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

