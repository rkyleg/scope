# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scope.ui'
#
# Created: Wed Jan  6 01:30:01 2016
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
        Form.resize(938, 488)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/scope.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.gridLayout_8 = QtGui.QGridLayout(Form)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 2)
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
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 1, 0, 0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tab_left = QtGui.QTabWidget(self.fr_left)
        self.tab_left.setObjectName(_fromUtf8("tab_left"))
        self.gridLayout_5.addWidget(self.tab_left, 0, 0, 1, 1)
        self.fr_right = QtGui.QFrame(self.split_left)
        self.fr_right.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_right.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_right.setObjectName(_fromUtf8("fr_right"))
        self.gridLayout_7 = QtGui.QGridLayout(self.fr_right)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setContentsMargins(1, 0, 0, 4)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.fr_bottom = QtGui.QFrame(self.fr_right)
        self.fr_bottom.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_bottom.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_bottom.setObjectName(_fromUtf8("fr_bottom"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.fr_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
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
        self.l_statusbar = QtGui.QLabel(self.fr_right)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_statusbar.sizePolicy().hasHeightForWidth())
        self.l_statusbar.setSizePolicy(sizePolicy)
        self.l_statusbar.setStyleSheet(_fromUtf8("QLabel {\n"
"padding-left:2px;\n"
"padding-top:2px;\n"
"}"))
        self.l_statusbar.setText(_fromUtf8(""))
        self.l_statusbar.setObjectName(_fromUtf8("l_statusbar"))
        self.gridLayout_7.addWidget(self.l_statusbar, 2, 0, 1, 1)
        self.gridLayout_8.addWidget(self.split_left, 1, 1, 1, 1)
        self.fr_leftbar = QtGui.QFrame(Form)
        self.fr_leftbar.setMaximumSize(QtCore.QSize(44, 16777215))
        self.fr_leftbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_leftbar.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_leftbar.setObjectName(_fromUtf8("fr_leftbar"))
        self.verticalLayout = QtGui.QVBoxLayout(self.fr_leftbar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.b_show_tabs = QtGui.QPushButton(self.fr_leftbar)
        self.b_show_tabs.setMinimumSize(QtCore.QSize(0, 50))
        self.b_show_tabs.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/window_switcher.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_show_tabs.setIcon(icon1)
        self.b_show_tabs.setIconSize(QtCore.QSize(32, 32))
        self.b_show_tabs.setCheckable(True)
        self.b_show_tabs.setProperty("class", _fromUtf8(""))
        self.b_show_tabs.setObjectName(_fromUtf8("b_show_tabs"))
        self.verticalLayout.addWidget(self.b_show_tabs)
        self.b_new = QtGui.QPushButton(self.fr_leftbar)
        self.b_new.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/new_file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_new.setIcon(icon2)
        self.b_new.setIconSize(QtCore.QSize(32, 32))
        self.b_new.setObjectName(_fromUtf8("b_new"))
        self.verticalLayout.addWidget(self.b_new)
        self.b_workspaces = QtGui.QPushButton(self.fr_leftbar)
        self.b_workspaces.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/workspace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_workspaces.setIcon(icon3)
        self.b_workspaces.setIconSize(QtCore.QSize(32, 32))
        self.b_workspaces.setObjectName(_fromUtf8("b_workspaces"))
        self.verticalLayout.addWidget(self.b_workspaces)
        self.b_home = QtGui.QPushButton(self.fr_leftbar)
        self.b_home.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_home.setIcon(icon4)
        self.b_home.setIconSize(QtCore.QSize(32, 32))
        self.b_home.setObjectName(_fromUtf8("b_home"))
        self.verticalLayout.addWidget(self.b_home)
        self.b_settings = QtGui.QPushButton(self.fr_leftbar)
        self.b_settings.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_settings.setIcon(icon5)
        self.b_settings.setIconSize(QtCore.QSize(32, 32))
        self.b_settings.setObjectName(_fromUtf8("b_settings"))
        self.verticalLayout.addWidget(self.b_settings)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_8.addWidget(self.fr_leftbar, 1, 0, 1, 1)
        self.fr_topbar = QtGui.QFrame(Form)
        self.fr_topbar.setMinimumSize(QtCore.QSize(0, 34))
        self.fr_topbar.setMaximumSize(QtCore.QSize(16777215, 34))
        self.fr_topbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_topbar.setFrameShadow(QtGui.QFrame.Plain)
        self.fr_topbar.setObjectName(_fromUtf8("fr_topbar"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_topbar)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.fr_topleft = QtGui.QFrame(self.fr_topbar)
        self.fr_topleft.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_topleft.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_topleft.setObjectName(_fromUtf8("fr_topleft"))
        self.gridLayout_3 = QtGui.QGridLayout(self.fr_topleft)
        self.gridLayout_3.setContentsMargins(6, 0, 0, 0)
        self.gridLayout_3.setHorizontalSpacing(2)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.fr_find = QtGui.QFrame(self.fr_topleft)
        self.fr_find.setMaximumSize(QtCore.QSize(250, 16777215))
        self.fr_find.setStyleSheet(_fromUtf8(""))
        self.fr_find.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_find.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_find.setObjectName(_fromUtf8("fr_find"))
        self.gridLayout_4 = QtGui.QGridLayout(self.fr_find)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.fr_find_2 = QtGui.QFrame(self.fr_find)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_find_2.sizePolicy().hasHeightForWidth())
        self.fr_find_2.setSizePolicy(sizePolicy)
        self.fr_find_2.setFrameShape(QtGui.QFrame.NoFrame)
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
"padding-left:4px;"))
        self.le_find.setObjectName(_fromUtf8("le_find"))
        self.gridLayout_9.addWidget(self.le_find, 0, 0, 1, 1)
        self.b_find = QtGui.QPushButton(self.fr_find_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_find.sizePolicy().hasHeightForWidth())
        self.b_find.setSizePolicy(sizePolicy)
        self.b_find.setMaximumSize(QtCore.QSize(28, 16777215))
        self.b_find.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_find.setIcon(icon6)
        self.b_find.setObjectName(_fromUtf8("b_find"))
        self.gridLayout_9.addWidget(self.b_find, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.fr_find_2, 0, 3, 1, 1)
        self.le_goto = QtGui.QLineEdit(self.fr_find)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_goto.sizePolicy().hasHeightForWidth())
        self.le_goto.setSizePolicy(sizePolicy)
        self.le_goto.setMinimumSize(QtCore.QSize(40, 24))
        self.le_goto.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_goto.setStyleSheet(_fromUtf8("padding-left:4px;"))
        self.le_goto.setObjectName(_fromUtf8("le_goto"))
        self.gridLayout_4.addWidget(self.le_goto, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.fr_find, 0, 4, 1, 1)
        self.gridLayout_2.addWidget(self.fr_topleft, 0, 8, 1, 1)
        self.fr_tab = QtGui.QFrame(self.fr_topbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_tab.sizePolicy().hasHeightForWidth())
        self.fr_tab.setSizePolicy(sizePolicy)
        self.fr_tab.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_tab.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_tab.setObjectName(_fromUtf8("fr_tab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.fr_tab)
        self.gridLayout_6.setContentsMargins(0, 0, 2, 0)
        self.gridLayout_6.setHorizontalSpacing(2)
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.l_filename = QtGui.QLabel(self.fr_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_filename.sizePolicy().hasHeightForWidth())
        self.l_filename.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.l_filename.setFont(font)
        self.l_filename.setText(_fromUtf8(""))
        self.l_filename.setObjectName(_fromUtf8("l_filename"))
        self.gridLayout_6.addWidget(self.l_filename, 0, 4, 1, 1)
        self.b_tabicon = QtGui.QPushButton(self.fr_tab)
        self.b_tabicon.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_tabicon.setText(_fromUtf8(""))
        self.b_tabicon.setIconSize(QtCore.QSize(20, 20))
        self.b_tabicon.setObjectName(_fromUtf8("b_tabicon"))
        self.gridLayout_6.addWidget(self.b_tabicon, 0, 3, 1, 1)
        self.l_title_prefix = QtGui.QLabel(self.fr_tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.l_title_prefix.setFont(font)
        self.l_title_prefix.setText(_fromUtf8(""))
        self.l_title_prefix.setObjectName(_fromUtf8("l_title_prefix"))
        self.gridLayout_6.addWidget(self.l_title_prefix, 0, 2, 1, 1)
        self.b_closetab = QtGui.QPushButton(self.fr_tab)
        self.b_closetab.setMaximumSize(QtCore.QSize(26, 16777215))
        self.b_closetab.setObjectName(_fromUtf8("b_closetab"))
        self.gridLayout_6.addWidget(self.b_closetab, 0, 5, 1, 1)
        self.gridLayout_2.addWidget(self.fr_tab, 0, 1, 1, 1)
        self.fr_mainbutton = QtGui.QFrame(self.fr_topbar)
        self.fr_mainbutton.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_mainbutton.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_mainbutton.setObjectName(_fromUtf8("fr_mainbutton"))
        self.gridLayout_10 = QtGui.QGridLayout(self.fr_mainbutton)
        self.gridLayout_10.setMargin(0)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.gridLayout_2.addWidget(self.fr_mainbutton, 0, 0, 1, 1)
        self.fr_toolbar = QtGui.QFrame(self.fr_topbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_toolbar.sizePolicy().hasHeightForWidth())
        self.fr_toolbar.setSizePolicy(sizePolicy)
        self.fr_toolbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_toolbar.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_toolbar.setObjectName(_fromUtf8("fr_toolbar"))
        self.gridLayout = QtGui.QGridLayout(self.fr_toolbar)
        self.gridLayout.setMargin(0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.b_save = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_save.sizePolicy().hasHeightForWidth())
        self.b_save.setSizePolicy(sizePolicy)
        self.b_save.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save.setIcon(icon7)
        self.b_save.setIconSize(QtCore.QSize(18, 18))
        self.b_save.setObjectName(_fromUtf8("b_save"))
        self.gridLayout.addWidget(self.b_save, 0, 4, 1, 1)
        self.b_comment = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_comment.sizePolicy().hasHeightForWidth())
        self.b_comment.setSizePolicy(sizePolicy)
        self.b_comment.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/comment.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_comment.setIcon(icon8)
        self.b_comment.setIconSize(QtCore.QSize(18, 18))
        self.b_comment.setObjectName(_fromUtf8("b_comment"))
        self.gridLayout.addWidget(self.b_comment, 0, 7, 1, 1)
        self.b_unindent = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_unindent.sizePolicy().hasHeightForWidth())
        self.b_unindent.setSizePolicy(sizePolicy)
        self.b_unindent.setText(_fromUtf8(""))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/unindent.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_unindent.setIcon(icon9)
        self.b_unindent.setIconSize(QtCore.QSize(18, 18))
        self.b_unindent.setObjectName(_fromUtf8("b_unindent"))
        self.gridLayout.addWidget(self.b_unindent, 0, 6, 1, 1)
        self.b_color_picker = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_color_picker.sizePolicy().hasHeightForWidth())
        self.b_color_picker.setSizePolicy(sizePolicy)
        self.b_color_picker.setText(_fromUtf8(""))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/color_swatch.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_color_picker.setIcon(icon10)
        self.b_color_picker.setObjectName(_fromUtf8("b_color_picker"))
        self.gridLayout.addWidget(self.b_color_picker, 0, 8, 1, 1)
        self.b_indent = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_indent.sizePolicy().hasHeightForWidth())
        self.b_indent.setSizePolicy(sizePolicy)
        self.b_indent.setText(_fromUtf8(""))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/indent.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_indent.setIcon(icon11)
        self.b_indent.setIconSize(QtCore.QSize(18, 18))
        self.b_indent.setObjectName(_fromUtf8("b_indent"))
        self.gridLayout.addWidget(self.b_indent, 0, 5, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(2, 2, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 10, 1, 1)
        self.b_menu = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_menu.sizePolicy().hasHeightForWidth())
        self.b_menu.setSizePolicy(sizePolicy)
        self.b_menu.setText(_fromUtf8(""))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/menu.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_menu.setIcon(icon12)
        self.b_menu.setIconSize(QtCore.QSize(18, 18))
        self.b_menu.setObjectName(_fromUtf8("b_menu"))
        self.gridLayout.addWidget(self.b_menu, 0, 2, 1, 1)
        self.b_run = QtGui.QPushButton(self.fr_toolbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_run.sizePolicy().hasHeightForWidth())
        self.b_run.setSizePolicy(sizePolicy)
        self.b_run.setText(_fromUtf8(""))
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8("../style/img/run.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_run.setIcon(icon13)
        self.b_run.setIconSize(QtCore.QSize(18, 18))
        self.b_run.setObjectName(_fromUtf8("b_run"))
        self.gridLayout.addWidget(self.b_run, 0, 9, 1, 1)
        self.gridLayout_2.addWidget(self.fr_toolbar, 0, 3, 1, 1)
        self.b_back = QtGui.QPushButton(self.fr_topbar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_back.sizePolicy().hasHeightForWidth())
        self.b_back.setSizePolicy(sizePolicy)
        self.b_back.setObjectName(_fromUtf8("b_back"))
        self.gridLayout_2.addWidget(self.b_back, 0, 9, 1, 1)
        self.gridLayout_8.addWidget(self.fr_topbar, 0, 0, 1, 2)

        self.retranslateUi(Form)
        self.sw_bottom.setCurrentIndex(0)
        QtCore.QObject.connect(self.le_find, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_find.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Scope", None))
        self.b_show_tabs.setToolTip(_translate("Form", "Window Switcher - View Open Files and Workspaces (F1)", None))
        self.b_new.setToolTip(_translate("Form", "New File (Ctrl + N)", None))
        self.b_workspaces.setToolTip(_translate("Form", "Workspaces", None))
        self.b_home.setToolTip(_translate("Form", "Home (F9)", None))
        self.b_settings.setToolTip(_translate("Form", "Settings", None))
        self.fr_find_2.setProperty("class", _translate("Form", "toolbarLineEdit", None))
        self.le_find.setToolTip(_translate("Form", "Find in file (Ctrl + F)", None))
        self.le_find.setPlaceholderText(_translate("Form", "find", None))
        self.le_find.setProperty("class", _translate("Form", "toolbar", None))
        self.b_find.setProperty("class", _translate("Form", "toolbar toolbar-left", None))
        self.le_goto.setToolTip(_translate("Form", "goto (Ctrl + G)", None))
        self.le_goto.setPlaceholderText(_translate("Form", "goto", None))
        self.le_goto.setProperty("class", _translate("Form", "toolbar", None))
        self.b_tabicon.setProperty("class", _translate("Form", "tab_button", None))
        self.b_closetab.setToolTip(_translate("Form", "close file", None))
        self.b_closetab.setProperty("class", _translate("Form", "editor_tab_cls_btn", None))
        self.b_save.setToolTip(_translate("Form", "Save (Ctrl + S)", None))
        self.b_save.setProperty("class", _translate("Form", "toolbar toolbar-big", None))
        self.b_comment.setToolTip(_translate("Form", "Comment/Uncomment (Ctrl+E)", None))
        self.b_comment.setProperty("class", _translate("Form", "toolbar", None))
        self.b_unindent.setToolTip(_translate("Form", "Unindent (Shift + tab)", None))
        self.b_unindent.setProperty("class", _translate("Form", "toolbar", None))
        self.b_color_picker.setToolTip(_translate("Form", "<html><head/><body><p>Insert rgb color</p></body></html>", None))
        self.b_color_picker.setProperty("class", _translate("Form", "toolbar", None))
        self.b_indent.setToolTip(_translate("Form", "Indent (tab)", None))
        self.b_indent.setProperty("class", _translate("Form", "toolbar", None))
        self.b_menu.setToolTip(_translate("Form", "Editor Menu (Ctrl + M)", None))
        self.b_menu.setProperty("class", _translate("Form", "toolbar toolbar-left", None))
        self.b_run.setToolTip(_translate("Form", "Run (F5)", None))
        self.b_run.setProperty("class", _translate("Form", "toolbar toolbar-big", None))
        self.b_back.setToolTip(_translate("Form", "back to last file", None))
        self.b_back.setText(_translate("Form", "back", None))
        self.b_back.setProperty("class", _translate("Form", "toolbar toolbar-left", None))

