# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt2py.ui'
#
# Created: Sat Feb  8 22:48:26 2014
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
        Form.resize(517, 97)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setContentsMargins(4, 4, 4, 0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame_3 = QtGui.QFrame(Form)
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem = QtGui.QSpacerItem(26, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 3, 1, 1)
        self.label = QtGui.QLabel(self.frame_3)
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
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.frame = QtGui.QFrame(self.frame_3)
        self.frame.setMinimumSize(QtCore.QSize(150, 0))
        self.frame.setStyleSheet(_fromUtf8("QFrame#frame {\n"
"    background-color: qlineargradient(spread:pad, x1:0.826, y1:0.869, x2:0.169, y2:0.267045, stop:0 rgba(48, 48, 48, 255), stop:1 rgba(86, 86, 86, 255));\n"
"border-radius:4px;\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(1)
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.le_help = QtGui.QLineEdit(self.frame)
        self.le_help.setStyleSheet(_fromUtf8("QLineEdit {\n"
"background:transparent;\n"
"color:white;\n"
"border:0px;\n"
"}"))
        self.le_help.setObjectName(_fromUtf8("le_help"))
        self.gridLayout_2.addWidget(self.le_help, 0, 1, 1, 1)
        self.b_help = QtGui.QPushButton(self.frame)
        self.b_help.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_help.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_help.setIcon(icon)
        self.b_help.setObjectName(_fromUtf8("b_help"))
        self.gridLayout_2.addWidget(self.b_help, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setStyleSheet(_fromUtf8("color:white;"))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame, 0, 2, 1, 1)
        self.b_qt_designer = QtGui.QPushButton(self.frame_3)
        self.b_qt_designer.setObjectName(_fromUtf8("b_qt_designer"))
        self.gridLayout_4.addWidget(self.b_qt_designer, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 2)
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.b_open = QtGui.QPushButton(self.frame_2)
        self.b_open.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_open.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/file_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_open.setIcon(icon1)
        self.b_open.setObjectName(_fromUtf8("b_open"))
        self.gridLayout_3.addWidget(self.b_open, 0, 1, 1, 1)
        self.le_path = QtGui.QLineEdit(self.frame_2)
        self.le_path.setObjectName(_fromUtf8("le_path"))
        self.gridLayout_3.addWidget(self.le_path, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 2)
        self.b_convert = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_convert.setFont(font)
        self.b_convert.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0.00995025 rgba(94, 94, 94, 255), stop:0.174129 rgba(125, 125, 125, 255), stop:0.890547 rgba(164, 164, 164, 255), stop:1 rgba(188, 188, 188, 255));\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"    border-radius:5px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0.98, y1:1, x2:1, y2:0, stop:0 rgba(138, 138, 138, 255), stop:0.0646766 rgba(157, 157, 157, 255), stop:0.935323 rgba(198, 198, 198, 255), stop:1 rgba(231, 231, 231, 255));\n"
"}"))
        self.b_convert.setObjectName(_fromUtf8("b_convert"))
        self.gridLayout.addWidget(self.b_convert, 2, 0, 1, 1)
        self.l_result = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_result.sizePolicy().hasHeightForWidth())
        self.l_result.setSizePolicy(sizePolicy)
        self.l_result.setText(_fromUtf8(""))
        self.l_result.setObjectName(_fromUtf8("l_result"))
        self.gridLayout.addWidget(self.l_result, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(196, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.le_help, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_help.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Qt UI to Python Converter", None))
        self.le_help.setPlaceholderText(_translate("Form", "search Qt Help", None))
        self.label_3.setText(_translate("Form", "Q", None))
        self.b_qt_designer.setText(_translate("Form", "Qt Designer", None))
        self.label_2.setText(_translate("Form", "Select .ui (Qt Designer File)", None))
        self.b_convert.setText(_translate("Form", "Convert", None))

