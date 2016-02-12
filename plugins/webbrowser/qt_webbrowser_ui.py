# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_webbrowser.ui'
#
# Created: Fri Feb 12 17:38:08 2016
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
        Form.resize(708, 426)
        Form.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.fr_top = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_top.sizePolicy().hasHeightForWidth())
        self.fr_top.setSizePolicy(sizePolicy)
        self.fr_top.setMaximumSize(QtCore.QSize(16777215, 26))
        self.fr_top.setStyleSheet(_fromUtf8("QFrame#fr_top {\n"
"    border-bottom:1px solid gray;\n"
"background-color:rgb(50,50,50)\n"
"}\n"
"QPushButton {\n"
"background:transparent;\n"
"border:0px;\n"
"}\n"
"QPushButton:hover {\n"
"background:rgba(70,70,70,150);\n"
"}"))
        self.fr_top.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_top.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_top.setProperty("class", _fromUtf8(""))
        self.fr_top.setObjectName(_fromUtf8("fr_top"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_top)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(2, 0, 2, 0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.b_back = QtGui.QPushButton(self.fr_top)
        self.b_back.setMinimumSize(QtCore.QSize(26, 0))
        self.b_back.setMaximumSize(QtCore.QSize(26, 26))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/tri_left.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_back.setIcon(icon)
        self.b_back.setObjectName(_fromUtf8("b_back"))
        self.gridLayout_2.addWidget(self.b_back, 0, 5, 1, 1)
        self.b_forward = QtGui.QPushButton(self.fr_top)
        self.b_forward.setMinimumSize(QtCore.QSize(26, 0))
        self.b_forward.setMaximumSize(QtCore.QSize(26, 26))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("img/tri_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_forward.setIcon(icon1)
        self.b_forward.setObjectName(_fromUtf8("b_forward"))
        self.gridLayout_2.addWidget(self.b_forward, 0, 6, 1, 1)
        self.b_go = QtGui.QPushButton(self.fr_top)
        self.b_go.setMinimumSize(QtCore.QSize(26, 0))
        self.b_go.setMaximumSize(QtCore.QSize(26, 26))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("img/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_go.setIcon(icon2)
        self.b_go.setObjectName(_fromUtf8("b_go"))
        self.gridLayout_2.addWidget(self.b_go, 0, 3, 2, 1)
        self.b_stop = QtGui.QPushButton(self.fr_top)
        self.b_stop.setMinimumSize(QtCore.QSize(26, 0))
        self.b_stop.setMaximumSize(QtCore.QSize(26, 26))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("img/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_stop.setIcon(icon3)
        self.b_stop.setObjectName(_fromUtf8("b_stop"))
        self.gridLayout_2.addWidget(self.b_stop, 0, 4, 2, 1)
        self.fr_addr = QtGui.QFrame(self.fr_top)
        self.fr_addr.setMinimumSize(QtCore.QSize(0, 22))
        self.fr_addr.setStyleSheet(_fromUtf8("QFrame#fr_addr {\n"
"   border:0px;\n"
"    border-right:1px solid gray;\n"
"}"))
        self.fr_addr.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_addr.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_addr.setObjectName(_fromUtf8("fr_addr"))
        self.gridLayout_3 = QtGui.QGridLayout(self.fr_addr)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.pb_load = QtGui.QProgressBar(self.fr_addr)
        self.pb_load.setMinimumSize(QtCore.QSize(0, 2))
        self.pb_load.setMaximumSize(QtCore.QSize(16777215, 2))
        self.pb_load.setStyleSheet(_fromUtf8("QProgressBar {\n"
"border:0px;\n"
"    background:transparent;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(80,134,175);\n"
"}"))
        self.pb_load.setProperty("value", 0)
        self.pb_load.setTextVisible(False)
        self.pb_load.setObjectName(_fromUtf8("pb_load"))
        self.gridLayout_3.addWidget(self.pb_load, 1, 1, 1, 1)
        self.le_address = QtGui.QLineEdit(self.fr_addr)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_address.sizePolicy().hasHeightForWidth())
        self.le_address.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        self.le_address.setFont(font)
        self.le_address.setStyleSheet(_fromUtf8("QLineEdit {\n"
"background:transparent;\n"
"border:0px;\n"
"color:white;\n"
"}"))
        self.le_address.setObjectName(_fromUtf8("le_address"))
        self.gridLayout_3.addWidget(self.le_address, 0, 1, 1, 1)
        self.b_icon = QtGui.QPushButton(self.fr_addr)
        self.b_icon.setMaximumSize(QtCore.QSize(24, 16777215))
        self.b_icon.setText(_fromUtf8(""))
        self.b_icon.setIconSize(QtCore.QSize(20, 20))
        self.b_icon.setObjectName(_fromUtf8("b_icon"))
        self.gridLayout_3.addWidget(self.b_icon, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.fr_addr, 0, 2, 2, 1)
        self.le_find = QtGui.QLineEdit(self.fr_top)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_find.sizePolicy().hasHeightForWidth())
        self.le_find.setSizePolicy(sizePolicy)
        self.le_find.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_find.setStyleSheet(_fromUtf8("QLineEdit {\n"
"background:transparent;\n"
"border:0px;\n"
"border-left:1px solid gray;\n"
"color:white;\n"
"}"))
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_2.addWidget(self.le_find, 0, 7, 1, 1)
        self.gridLayout.addWidget(self.fr_top, 0, 0, 1, 1)
        self.split_insp = QtGui.QSplitter(Form)
        self.split_insp.setOrientation(QtCore.Qt.Vertical)
        self.split_insp.setObjectName(_fromUtf8("split_insp"))
        self.gridLayout.addWidget(self.split_insp, 1, 0, 1, 1)
        self.l_status = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.l_status.setFont(font)
        self.l_status.setStyleSheet(_fromUtf8("QLineEdit {\n"
"border:0px;\n"
"border-top:1px solid gray;\n"
"background:rgb(50,50,50);\n"
"color:rgb(200,200,200)\n"
"}"))
        self.l_status.setReadOnly(True)
        self.l_status.setObjectName(_fromUtf8("l_status"))
        self.gridLayout.addWidget(self.l_status, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.le_address, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_go.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.b_back.setToolTip(_translate("Form", "back", None))
        self.b_forward.setToolTip(_translate("Form", "forward", None))
        self.b_go.setToolTip(_translate("Form", "reload/go", None))
        self.b_stop.setToolTip(_translate("Form", "stop", None))
        self.le_address.setPlaceholderText(_translate("Form", "url", None))
        self.le_find.setPlaceholderText(_translate("Form", "find", None))

