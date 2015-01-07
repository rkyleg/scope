# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'armadillo.ui'
#
# Created: Tue Jan  6 17:57:26 2015
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
        Form.resize(676, 333)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/armadillo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout_8 = QtGui.QGridLayout(Form)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setContentsMargins(2, 0, 2, 2)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.split_left = QtGui.QSplitter(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.split_left.sizePolicy().hasHeightForWidth())
        self.split_left.setSizePolicy(sizePolicy)
        self.split_left.setOrientation(QtCore.Qt.Horizontal)
        self.split_left.setObjectName(_fromUtf8("split_left"))
        self.fr_left = QtGui.QFrame(self.split_left)
        self.fr_left.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_left.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_left.setObjectName(_fromUtf8("fr_left"))
        self.gridLayout_5 = QtGui.QGridLayout(self.fr_left)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tab_left = QtGui.QTabWidget(self.fr_left)
        self.tab_left.setObjectName(_fromUtf8("tab_left"))
        self.gridLayout_5.addWidget(self.tab_left, 0, 0, 1, 1)
        self.fr_right = QtGui.QFrame(self.split_left)
        self.fr_right.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_right.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_right.setObjectName(_fromUtf8("fr_right"))
        self.gridLayout_7 = QtGui.QGridLayout(self.fr_right)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.fr_bottom = QtGui.QFrame(self.fr_right)
        self.fr_bottom.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_bottom.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_bottom.setObjectName(_fromUtf8("fr_bottom"))
        self.gridLayout = QtGui.QGridLayout(self.fr_bottom)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_7.addWidget(self.fr_bottom, 1, 0, 1, 1)
        self.split_bottom = QtGui.QSplitter(self.fr_right)
        self.split_bottom.setOrientation(QtCore.Qt.Vertical)
        self.split_bottom.setObjectName(_fromUtf8("split_bottom"))
        self.split_right = QtGui.QSplitter(self.split_bottom)
        self.split_right.setOrientation(QtCore.Qt.Horizontal)
        self.split_right.setObjectName(_fromUtf8("split_right"))
        self.sw_main = QtGui.QStackedWidget(self.split_right)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sw_main.sizePolicy().hasHeightForWidth())
        self.sw_main.setSizePolicy(sizePolicy)
        self.sw_main.setObjectName(_fromUtf8("sw_main"))
        self.tab_right = QtGui.QTabWidget(self.split_right)
        self.tab_right.setObjectName(_fromUtf8("tab_right"))
        self.sw_bottom = QtGui.QStackedWidget(self.split_bottom)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sw_bottom.sizePolicy().hasHeightForWidth())
        self.sw_bottom.setSizePolicy(sizePolicy)
        self.sw_bottom.setObjectName(_fromUtf8("sw_bottom"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.sw_bottom.addWidget(self.page)
        self.gridLayout_7.addWidget(self.split_bottom, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.split_left, 2, 0, 1, 1)
        self.fr_toolbar = QtGui.QFrame(Form)
        self.fr_toolbar.setStyleSheet(_fromUtf8("QPushButton,QToolButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(115, 115, 115, 255), stop:0.154545 rgba(146, 146, 146, 255), stop:0.831818 rgba(174, 174, 174, 255), stop:1 rgba(182, 182, 182, 255));\n"
"    border:0px;\n"
"    padding:3px;\n"
"    padding-left:6px;\n"
"    padding-right:6px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(91, 91, 91, 255), stop:0.154545 rgba(129, 129, 129, 255), stop:0.831818 rgba(154, 154, 154, 255), stop:1 rgba(175, 175, 175, 255));\n"
"}"))
        self.fr_toolbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_toolbar.setFrameShadow(QtGui.QFrame.Plain)
        self.fr_toolbar.setObjectName(_fromUtf8("fr_toolbar"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_toolbar)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setContentsMargins(4, 2, 2, 4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.b_indent = QtGui.QToolButton(self.fr_toolbar)
        self.b_indent.setMinimumSize(QtCore.QSize(32, 0))
        self.b_indent.setMaximumSize(QtCore.QSize(32, 16777215))
        self.b_indent.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-top-left-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}"))
        self.b_indent.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("img/indent.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_indent.setIcon(icon1)
        self.b_indent.setObjectName(_fromUtf8("b_indent"))
        self.gridLayout_2.addWidget(self.b_indent, 0, 8, 1, 1)
        self.b_save = QtGui.QToolButton(self.fr_toolbar)
        self.b_save.setMinimumSize(QtCore.QSize(40, 0))
        self.b_save.setMaximumSize(QtCore.QSize(40, 16777215))
        self.b_save.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"    border-top-right-radius:5px;\n"
"    border-bottom-right-radius:5px;\n"
"}"))
        self.b_save.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save.setIcon(icon2)
        self.b_save.setObjectName(_fromUtf8("b_save"))
        self.gridLayout_2.addWidget(self.b_save, 0, 3, 1, 1)
        self.b_comment = QtGui.QToolButton(self.fr_toolbar)
        self.b_comment.setMinimumSize(QtCore.QSize(32, 0))
        self.b_comment.setMaximumSize(QtCore.QSize(32, 16777215))
        self.b_comment.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"    border-top-right-radius:5px;\n"
"    border-bottom-right-radius:5px;\n"
"}"))
        self.b_comment.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("img/comment.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_comment.setIcon(icon3)
        self.b_comment.setObjectName(_fromUtf8("b_comment"))
        self.gridLayout_2.addWidget(self.b_comment, 0, 10, 1, 1)
        self.b_workspace = QtGui.QPushButton(self.fr_toolbar)
        self.b_workspace.setMinimumSize(QtCore.QSize(40, 25))
        self.b_workspace.setMaximumSize(QtCore.QSize(40, 16777215))
        self.b_workspace.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"}\n"
"QPushButton::menu-indicator {\n"
"     image: url(none.png);\n"
"}"))
        self.b_workspace.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("img/workspace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_workspace.setIcon(icon4)
        self.b_workspace.setObjectName(_fromUtf8("b_workspace"))
        self.gridLayout_2.addWidget(self.b_workspace, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 12, 1, 1)
        self.b_new = QtGui.QPushButton(self.fr_toolbar)
        self.b_new.setMinimumSize(QtCore.QSize(40, 25))
        self.b_new.setMaximumSize(QtCore.QSize(40, 16777215))
        self.b_new.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border-top-left-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}\n"
"QPushButton::menu-indicator {\n"
"     image: url(none.png);\n"
"}"))
        self.b_new.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("img/new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_new.setIcon(icon5)
        self.b_new.setObjectName(_fromUtf8("b_new"))
        self.gridLayout_2.addWidget(self.b_new, 0, 0, 1, 1)
        self.b_unindent = QtGui.QToolButton(self.fr_toolbar)
        self.b_unindent.setMinimumSize(QtCore.QSize(32, 0))
        self.b_unindent.setMaximumSize(QtCore.QSize(32, 16777215))
        self.b_unindent.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"}"))
        self.b_unindent.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8("img/indent_remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_unindent.setIcon(icon6)
        self.b_unindent.setObjectName(_fromUtf8("b_unindent"))
        self.gridLayout_2.addWidget(self.b_unindent, 0, 9, 1, 1)
        self.b_open = QtGui.QToolButton(self.fr_toolbar)
        self.b_open.setMinimumSize(QtCore.QSize(40, 0))
        self.b_open.setMaximumSize(QtCore.QSize(40, 16777215))
        self.b_open.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"}"))
        self.b_open.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8("img/file_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_open.setIcon(icon7)
        self.b_open.setObjectName(_fromUtf8("b_open"))
        self.gridLayout_2.addWidget(self.b_open, 0, 2, 1, 1)
        self.frame = QtGui.QFrame(self.fr_toolbar)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.fr_find = QtGui.QFrame(self.frame)
        self.fr_find.setMinimumSize(QtCore.QSize(150, 0))
        self.fr_find.setMaximumSize(QtCore.QSize(250, 16777215))
        self.fr_find.setStyleSheet(_fromUtf8("border:0px;"))
        self.fr_find.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_find.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_find.setObjectName(_fromUtf8("fr_find"))
        self.gridLayout_4 = QtGui.QGridLayout(self.fr_find)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.fr_find_2 = QtGui.QFrame(self.fr_find)
        self.fr_find_2.setStyleSheet(_fromUtf8("QFrame#fr_find_2 {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-radius:3px;\n"
"}"))
        self.fr_find_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fr_find_2.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_find_2.setObjectName(_fromUtf8("fr_find_2"))
        self.gridLayout_9 = QtGui.QGridLayout(self.fr_find_2)
        self.gridLayout_9.setMargin(0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.le_find = QtGui.QLineEdit(self.fr_find_2)
        self.le_find.setMinimumSize(QtCore.QSize(150, 24))
        self.le_find.setStyleSheet(_fromUtf8("background:transparent;\n"
"border:0px;\n"
"color:white;"))
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_9.addWidget(self.le_find, 0, 0, 1, 1)
        self.b_find = QtGui.QPushButton(self.fr_find_2)
        self.b_find.setMaximumSize(QtCore.QSize(16777215, 25))
        self.b_find.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"border-top-right-radius:3px;\n"
"border-bottom-right-radius:3px;\n"
"}\n"
"QPushButton:hover,QToolButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(91, 91, 91, 255), stop:0.154545 rgba(129, 129, 129, 255), stop:0.831818 rgba(154, 154, 154, 255), stop:1 rgba(175, 175, 175, 255));\n"
"}"))
        self.b_find.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8("img/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_find.setIcon(icon8)
        self.b_find.setObjectName(_fromUtf8("b_find"))
        self.gridLayout_9.addWidget(self.b_find, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.fr_find_2, 0, 3, 1, 1)
        self.le_goto = QtGui.QLineEdit(self.fr_find)
        self.le_goto.setMinimumSize(QtCore.QSize(40, 24))
        self.le_goto.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_goto.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(82, 82, 82, 255), stop:0.0590909 rgba(111, 111, 111, 255), stop:0.922727 rgba(99, 99, 99, 255), stop:1 rgba(151, 151, 151, 255));\n"
"color:white;\n"
"border:0px;\n"
"border-radius:3px;"))
        self.le_goto.setObjectName(_fromUtf8("le_goto"))
        self.gridLayout_4.addWidget(self.le_goto, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.fr_find, 0, 5, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 18, 1, 1)
        self.b_run = QtGui.QToolButton(self.fr_toolbar)
        self.b_run.setMinimumSize(QtCore.QSize(40, 0))
        self.b_run.setMaximumSize(QtCore.QSize(40, 16777215))
        self.b_run.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-top-left-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"    border-top-right-radius:5px;\n"
"    border-bottom-right-radius:5px;\n"
"}"))
        self.b_run.setText(_fromUtf8(""))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8("img/tri_right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_run.setIcon(icon9)
        self.b_run.setObjectName(_fromUtf8("b_run"))
        self.gridLayout_2.addWidget(self.b_run, 0, 13, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 4, 1, 1)
        self.b_settings = QtGui.QToolButton(self.fr_toolbar)
        self.b_settings.setMinimumSize(QtCore.QSize(32, 0))
        self.b_settings.setMaximumSize(QtCore.QSize(32, 16777215))
        self.b_settings.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-left:1px solid rgb(130,130,130);\n"
"    border-top-right-radius:5px;\n"
"    border-bottom-right-radius:5px;\n"
"}"))
        self.b_settings.setText(_fromUtf8(""))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8("img/wrench.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_settings.setIcon(icon10)
        self.b_settings.setObjectName(_fromUtf8("b_settings"))
        self.gridLayout_2.addWidget(self.b_settings, 0, 6, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 7, 1, 1)
        self.b_help = QtGui.QToolButton(self.fr_toolbar)
        self.b_help.setMinimumSize(QtCore.QSize(32, 0))
        self.b_help.setMaximumSize(QtCore.QSize(32, 16777215))
        self.b_help.setStyleSheet(_fromUtf8("QToolButton {\n"
"    border-top-left-radius:5px;\n"
"    border-bottom-left-radius:5px;\n"
"}"))
        self.b_help.setText(_fromUtf8(""))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8("img/home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_help.setIcon(icon11)
        self.b_help.setObjectName(_fromUtf8("b_help"))
        self.gridLayout_2.addWidget(self.b_help, 0, 5, 1, 1)
        self.gridLayout_8.addWidget(self.fr_toolbar, 1, 0, 1, 1)
        self.fr_tabs = QtGui.QFrame(Form)
        self.fr_tabs.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_tabs.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_tabs.setObjectName(_fromUtf8("fr_tabs"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fr_tabs)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(4, 2, 4, 2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.b_main = QtGui.QPushButton(self.fr_tabs)
        self.b_main.setMinimumSize(QtCore.QSize(32, 24))
        self.b_main.setStyleSheet(_fromUtf8("QPushButton::menu-indicator {\n"
"     image: url(none.png);\n"
"}\n"
"QPushButton {\n"
"    border-radius:5px;\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0.00995025 rgba(94, 94, 94, 255), stop:0.174129 rgba(125, 125, 125, 255), stop:0.890547 rgba(164, 164, 164, 255), stop:1 rgba(188, 188, 188, 255));\n"
"}\n"
"QPushButton:hover {\n"
"    border-radius:3px;\n"
"    background-color: qlineargradient(spread:pad, x1:0.98, y1:1, x2:1, y2:0, stop:0 rgba(138, 138, 138, 255), stop:0.0646766 rgba(157, 157, 157, 255), stop:0.935323 rgba(198, 198, 198, 255), stop:1 rgba(231, 231, 231, 255));\n"
"}"))
        self.b_main.setText(_fromUtf8(""))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8("img/menu.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_main.setIcon(icon12)
        self.b_main.setObjectName(_fromUtf8("b_main"))
        self.horizontalLayout.addWidget(self.b_main)
        self.gridLayout_8.addWidget(self.fr_tabs, 0, 0, 1, 1)
        self.l_statusbar = QtGui.QLabel(Form)
        self.l_statusbar.setStyleSheet(_fromUtf8("QLabel {\n"
"padding-left:2px;\n"
"padding-top:2px;\n"
"}"))
        self.l_statusbar.setText(_fromUtf8(""))
        self.l_statusbar.setObjectName(_fromUtf8("l_statusbar"))
        self.gridLayout_8.addWidget(self.l_statusbar, 3, 0, 1, 1)

        self.retranslateUi(Form)
        self.sw_bottom.setCurrentIndex(0)
        QtCore.QObject.connect(self.le_find, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_find.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Armadillo", None))
        self.b_indent.setToolTip(_translate("Form", "Indent", None))
        self.b_save.setToolTip(_translate("Form", "Save", None))
        self.b_comment.setToolTip(_translate("Form", "Comment/Uncomment", None))
        self.b_workspace.setToolTip(_translate("Form", "Workspaces", None))
        self.b_new.setToolTip(_translate("Form", "New", None))
        self.b_unindent.setToolTip(_translate("Form", "Unindent", None))
        self.b_open.setToolTip(_translate("Form", "Open", None))
        self.le_find.setPlaceholderText(_translate("Form", "Find", None))
        self.le_goto.setPlaceholderText(_translate("Form", "goto", None))
        self.le_goto.setProperty("class", _translate("Form", "darklineedit", None))
        self.b_run.setToolTip(_translate("Form", "Run", None))
        self.b_settings.setToolTip(_translate("Form", "Edit Settings", None))
        self.b_help.setToolTip(_translate("Form", "Armadillo start page and help links", None))
        self.b_main.setToolTip(_translate("Form", "Armidillo Menu", None))

