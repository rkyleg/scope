# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputText.ui'
#
# Created: Mon Jul 20 20:02:50 2015
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
        OutWidget.resize(608, 190)
        self.gridLayout = QtGui.QGridLayout(OutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.fr_cmd = QtGui.QFrame(OutWidget)
        self.fr_cmd.setStyleSheet(_fromUtf8("QFrame#fr_cmd{\n"
"\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"color:white;\n"
"border:0px;\n"
"}"))
        self.fr_cmd.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_cmd.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_cmd.setObjectName(_fromUtf8("fr_cmd"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_cmd)
        self.gridLayout_2.setContentsMargins(4, 1, 4, 1)
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
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
        self.label = QtGui.QLabel(self.fr_cmd)
        self.label.setStyleSheet(_fromUtf8("color:rgb(200,200,200);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.le_args = QtGui.QLineEdit(self.fr_cmd)
        self.le_args.setStyleSheet(_fromUtf8("background:transparent;\n"
"border:0px;\n"
"color:white;"))
        self.le_args.setObjectName(_fromUtf8("le_args"))
        self.gridLayout_2.addWidget(self.le_args, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.fr_cmd, 1, 1, 1, 1)
        self.l_title = QtGui.QLabel(OutWidget)
        self.l_title.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(50, 50, 50, 255), stop:0.831818 rgba(80, 80, 80, 255), stop:1 rgba(100, 100, 100, 255));\n"
"color:white;border-top-right-radius:5px;border-top-left-radius:5px;padding:3px;"))
        self.l_title.setText(_fromUtf8(""))
        self.l_title.setWordWrap(True)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout.addWidget(self.l_title, 0, 0, 1, 2)
        self.frame_2 = QtGui.QFrame(OutWidget)
        self.frame_2.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(94, 94, 94, 255), stop:0.174129 rgba(125, 125, 125, 255), stop:0.890547 rgba(164, 164, 164, 255), stop:1 rgba(188, 188, 188, 255));\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"    width:30px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, stop:0.00995025 rgba(114, 114, 114, 255), stop:0.174129 rgba(145, 145, 145, 255), stop:0.890547 rgba(184, 184, 184, 255), stop:1 rgba(208, 208, 208, 255));\n"
"}"))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.b_stop = QtGui.QPushButton(self.frame_2)
        self.b_stop.setMinimumSize(QtCore.QSize(0, 30))
        self.b_stop.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_stop.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-bottom:1px solid rgb(100,100,100);\n"
"}"))
        self.b_stop.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_stop.setIcon(icon)
        self.b_stop.setObjectName(_fromUtf8("b_stop"))
        self.gridLayout_3.addWidget(self.b_stop, 1, 0, 1, 1)
        self.b_cmd = QtGui.QPushButton(self.frame_2)
        self.b_cmd.setMinimumSize(QtCore.QSize(0, 30))
        self.b_cmd.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_cmd.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("textfield.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_cmd.setIcon(icon1)
        self.b_cmd.setCheckable(True)
        self.b_cmd.setObjectName(_fromUtf8("b_cmd"))
        self.gridLayout_3.addWidget(self.b_cmd, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.b_run = QtGui.QPushButton(self.frame_2)
        self.b_run.setMinimumSize(QtCore.QSize(0, 30))
        self.b_run.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_run.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-bottom:1px solid rgb(100,100,100);\n"
"}"))
        self.b_run.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/tri_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_run.setIcon(icon2)
        self.b_run.setObjectName(_fromUtf8("b_run"))
        self.gridLayout_3.addWidget(self.b_run, 0, 0, 1, 1)
        self.b_save = QtGui.QPushButton(self.frame_2)
        self.b_save.setEnabled(True)
        self.b_save.setMinimumSize(QtCore.QSize(0, 30))
        self.b_save.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_save.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    border-top:1px solid rgb(100,100,100);\n"
"    border-bottom-right-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}"))
        self.b_save.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save.setIcon(icon3)
        self.b_save.setCheckable(True)
        self.b_save.setObjectName(_fromUtf8("b_save"))
        self.gridLayout_3.addWidget(self.b_save, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 0, 3, 1)
        self.tb_out = QtGui.QTextBrowser(OutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeMono"))
        self.tb_out.setFont(font)
        self.tb_out.setStyleSheet(_fromUtf8("QTextBrowser {\n"
"background:rgb(50,50,50);\n"
"color:white;\n"
"}\n"
"a {color:rgb(121,213,255);}"))
        self.tb_out.setFrameShape(QtGui.QFrame.NoFrame)
        self.tb_out.setObjectName(_fromUtf8("tb_out"))
        self.gridLayout.addWidget(self.tb_out, 3, 1, 1, 1)

        self.retranslateUi(OutWidget)
        QtCore.QObject.connect(self.b_cmd, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.fr_cmd.setVisible)
        QtCore.QMetaObject.connectSlotsByName(OutWidget)

    def retranslateUi(self, OutWidget):
        OutWidget.setWindowTitle(_translate("OutWidget", "Form", None))
        self.label_2.setText(_translate("OutWidget", "    Args:", None))
        self.label.setText(_translate("OutWidget", "Command:", None))
        self.b_stop.setToolTip(_translate("OutWidget", "Stop", None))
        self.b_cmd.setToolTip(_translate("OutWidget", "Show/Hide Command", None))
        self.b_run.setToolTip(_translate("OutWidget", "Run", None))
        self.b_save.setToolTip(_translate("OutWidget", "Save output to file", None))
        self.tb_out.setHtml(_translate("OutWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'FreeMono\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"asdfasdf\"><span style=\" text-decoration: underline; color:#0000ff;\">adsfsdfasf</span></a></p></body></html>", None))

