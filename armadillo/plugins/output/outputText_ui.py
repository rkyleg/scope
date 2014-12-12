# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputText.ui'
#
# Created: Thu Dec 11 23:38:39 2014
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

class Ui_OutWidget(object):
    def setupUi(self, OutWidget):
        OutWidget.setObjectName(_fromUtf8("OutWidget"))
        OutWidget.resize(575, 162)
        self.gridLayout = QtGui.QGridLayout(OutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.fr_cmd = QtGui.QFrame(OutWidget)
        self.fr_cmd.setStyleSheet(_fromUtf8("QFrame#fr_cmd{\n"
"\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-radius:3px;\n"
"\n"
"}"))
        self.fr_cmd.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_cmd.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_cmd.setObjectName(_fromUtf8("fr_cmd"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_cmd)
        self.gridLayout_2.setContentsMargins(4, 1, 4, 1)
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.fr_cmd)
        self.label.setStyleSheet(_fromUtf8("color:rgb(200,200,200);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.le_cmd = QtGui.QLineEdit(self.fr_cmd)
        self.le_cmd.setStyleSheet(_fromUtf8("background:transparent;\n"
"border:0px;\n"
"color:white;"))
        self.le_cmd.setText(_fromUtf8(""))
        self.le_cmd.setObjectName(_fromUtf8("le_cmd"))
        self.gridLayout_2.addWidget(self.le_cmd, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.fr_cmd)
        self.label_2.setStyleSheet(_fromUtf8("color:rgb(200,200,200);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.le_args = QtGui.QLineEdit(self.fr_cmd)
        self.le_args.setStyleSheet(_fromUtf8("background:transparent;\n"
"border:0px;\n"
"color:white;"))
        self.le_args.setObjectName(_fromUtf8("le_args"))
        self.gridLayout_2.addWidget(self.le_args, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.fr_cmd, 0, 1, 1, 1)
        self.frame_2 = QtGui.QFrame(OutWidget)
        self.frame_2.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(94, 94, 94, 255), stop:0.174129 rgba(125, 125, 125, 255), stop:0.890547 rgba(164, 164, 164, 255), stop:1 rgba(188, 188, 188, 255));\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(114, 114, 114, 255), stop:0.174129 rgba(145, 145, 145, 255), stop:0.890547 rgba(184, 184, 184, 255), stop:1 rgba(208, 208, 208, 255));\n"
"}"))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setMargin(2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.b_cmd = QtGui.QPushButton(self.frame_2)
        self.b_cmd.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_cmd.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-top:1px solid rgb(100,100,100);\n"
"    border-bottom-right-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}"))
        self.b_cmd.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("textfield.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_cmd.setIcon(icon)
        self.b_cmd.setCheckable(True)
        self.b_cmd.setObjectName(_fromUtf8("b_cmd"))
        self.gridLayout_3.addWidget(self.b_cmd, 2, 0, 1, 1)
        self.b_run = QtGui.QPushButton(self.frame_2)
        self.b_run.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_run.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-bottom:1px solid rgb(100,100,100);\n"
"    border-top-right-radius:5px;\n"
"    border-top-left-radius:5px;\n"
"}"))
        self.b_run.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/tri_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_run.setIcon(icon1)
        self.b_run.setObjectName(_fromUtf8("b_run"))
        self.gridLayout_3.addWidget(self.b_run, 0, 0, 1, 1)
        self.b_stop = QtGui.QPushButton(self.frame_2)
        self.b_stop.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_stop.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_stop.setIcon(icon2)
        self.b_stop.setObjectName(_fromUtf8("b_stop"))
        self.gridLayout_3.addWidget(self.b_stop, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 2, 1)
        self.tb_out = QtGui.QTextBrowser(OutWidget)
        self.tb_out.setFrameShape(QtGui.QFrame.NoFrame)
        self.tb_out.setObjectName(_fromUtf8("tb_out"))
        self.gridLayout.addWidget(self.tb_out, 1, 1, 1, 1)

        self.retranslateUi(OutWidget)
        QtCore.QObject.connect(self.b_cmd, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.fr_cmd.setVisible)
        QtCore.QMetaObject.connectSlotsByName(OutWidget)

    def retranslateUi(self, OutWidget):
        OutWidget.setWindowTitle(_translate("OutWidget", "Form", None))
        self.label.setText(_translate("OutWidget", "Command:", None))
        self.label_2.setText(_translate("OutWidget", "    Args:", None))
        self.b_cmd.setToolTip(_translate("OutWidget", "Show/Hide Command", None))

