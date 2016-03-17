# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Wed Mar 16 11:09:50 2016
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
        Form.resize(616, 474)
        Form.setStyleSheet(_fromUtf8("QPushButton {\n"
"    background:rgba(100,100,100,100);\n"
"    color:white;\n"
"    border:0px;\n"
"    border-left:1px solid gray;\n"
"    padding:4px;\n"
"    padding-left:12px;\n"
"    padding-right:12px;\n"
"}\n"
"QPushButton:hover {\n"
"    background:rgba(100,100,100,80);\n"
"}"))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.li_catg = QtGui.QListWidget(Form)
        self.li_catg.setMinimumSize(QtCore.QSize(100, 0))
        self.li_catg.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.li_catg.setFont(font)
        self.li_catg.setStyleSheet(_fromUtf8("QListWidget {\n"
"border-right:1px solid gray;\n"
"}\n"
"QListWidgetItem {\n"
"    margin:0px;\n"
"    padding:20px;\n"
"}"))
        self.li_catg.setFrameShape(QtGui.QFrame.NoFrame)
        self.li_catg.setSpacing(0)
        self.li_catg.setViewMode(QtGui.QListView.ListMode)
        self.li_catg.setObjectName(_fromUtf8("li_catg"))
        item = QtGui.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.li_catg.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.li_catg.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.li_catg.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.li_catg.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.li_catg.addItem(item)
        self.gridLayout.addWidget(self.li_catg, 0, 0, 1, 1)
        self.split_v = QtGui.QSplitter(Form)
        self.split_v.setOrientation(QtCore.Qt.Horizontal)
        self.split_v.setObjectName(_fromUtf8("split_v"))
        self.frame = QtGui.QFrame(self.split_v)
        self.frame.setMinimumSize(QtCore.QSize(200, 0))
        self.frame.setStyleSheet(_fromUtf8("QFrame#frame {\n"
"    border-right:1px solid gray;\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 1, 0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.split_h = QtGui.QSplitter(self.frame)
        self.split_h.setOrientation(QtCore.Qt.Vertical)
        self.split_h.setObjectName(_fromUtf8("split_h"))
        self.fr_plugins = QtGui.QFrame(self.split_h)
        self.fr_plugins.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_plugins.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_plugins.setObjectName(_fromUtf8("fr_plugins"))
        self.gridLayout_2 = QtGui.QGridLayout(self.fr_plugins)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_9 = QtGui.QLabel(self.fr_plugins)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(247, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.b_plugin_file_add = QtGui.QPushButton(self.fr_plugins)
        self.b_plugin_file_add.setObjectName(_fromUtf8("b_plugin_file_add"))
        self.gridLayout_2.addWidget(self.b_plugin_file_add, 0, 2, 1, 1)
        self.b_plugin_url_add = QtGui.QPushButton(self.fr_plugins)
        self.b_plugin_url_add.setObjectName(_fromUtf8("b_plugin_url_add"))
        self.gridLayout_2.addWidget(self.b_plugin_url_add, 0, 3, 1, 1)
        self.tr_plugins = QtGui.QTreeWidget(self.fr_plugins)
        self.tr_plugins.setFrameShape(QtGui.QFrame.NoFrame)
        self.tr_plugins.setIndentation(2)
        self.tr_plugins.setRootIsDecorated(False)
        self.tr_plugins.setObjectName(_fromUtf8("tr_plugins"))
        self.gridLayout_2.addWidget(self.tr_plugins, 1, 0, 1, 4)
        self.fr_json_2 = QtGui.QFrame(self.split_h)
        self.fr_json_2.setStyleSheet(_fromUtf8("QFrame#fr_json_2 {\n"
"    border-top:1px solid gray;\n"
"}"))
        self.fr_json_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_json_2.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_json_2.setObjectName(_fromUtf8("fr_json_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.fr_json_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.l_title = QtGui.QLabel(self.fr_json_2)
        self.l_title.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.l_title.setFont(font)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout_3.addWidget(self.l_title, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)
        self.b_save_json = QtGui.QPushButton(self.fr_json_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_save_json.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_json.setIcon(icon)
        self.b_save_json.setIconSize(QtCore.QSize(12, 12))
        self.b_save_json.setObjectName(_fromUtf8("b_save_json"))
        self.gridLayout_3.addWidget(self.b_save_json, 0, 2, 1, 1)
        self.fr_json = QtGui.QFrame(self.fr_json_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_json.sizePolicy().hasHeightForWidth())
        self.fr_json.setSizePolicy(sizePolicy)
        self.fr_json.setStyleSheet(_fromUtf8("QFrame#fr_json {\n"
"    border-top:1px solid gray;\n"
"}"))
        self.fr_json.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_json.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_json.setObjectName(_fromUtf8("fr_json"))
        self.gridLayout_7 = QtGui.QGridLayout(self.fr_json)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_3.addWidget(self.fr_json, 1, 0, 1, 3)
        self.gridLayout_4.addWidget(self.split_h, 0, 0, 1, 1)
        self.tb_help = QtGui.QTextBrowser(self.split_v)
        self.tb_help.setStyleSheet(_fromUtf8("QTextBrowser {\n"
"    background:transparent;\n"
"}"))
        self.tb_help.setFrameShape(QtGui.QFrame.NoFrame)
        self.tb_help.setObjectName(_fromUtf8("tb_help"))
        self.gridLayout.addWidget(self.split_v, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        __sortingEnabled = self.li_catg.isSortingEnabled()
        self.li_catg.setSortingEnabled(False)
        item = self.li_catg.item(0)
        item.setText(_translate("Form", "General", None))
        item = self.li_catg.item(1)
        item.setText(_translate("Form", "Editors", None))
        item = self.li_catg.item(2)
        item.setText(_translate("Form", "Languages", None))
        item = self.li_catg.item(3)
        item.setText(_translate("Form", "Extensions", None))
        item = self.li_catg.item(4)
        item.setText(_translate("Form", "Plugins", None))
        self.li_catg.setSortingEnabled(__sortingEnabled)
        self.label_9.setText(_translate("Form", " Plugins", None))
        self.b_plugin_file_add.setText(_translate("Form", "Add from File", None))
        self.b_plugin_url_add.setText(_translate("Form", "Add from URL", None))
        self.tr_plugins.headerItem().setText(0, _translate("Form", "Plugin Name", None))
        self.tr_plugins.headerItem().setText(1, _translate("Form", "Enabled", None))
        self.tr_plugins.headerItem().setText(2, _translate("Form", "Description", None))
        self.l_title.setText(_translate("Form", " General Settings", None))
        self.b_save_json.setText(_translate("Form", "save", None))

