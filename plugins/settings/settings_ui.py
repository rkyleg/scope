# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created: Sat Feb 13 16:58:58 2016
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
"    border:1px solid gray;\n"
"    border-top:0px;\n"
"    border-right:0px;\n"
"    padding:4px;\n"
"    padding-left:12px;\n"
"    padding-right:12px;\n"
"    border-bottom-left-radius:3px;\n"
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
        self.b_reload = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_reload.setFont(font)
        self.b_reload.setStyleSheet(_fromUtf8("QPushButton {\n"
"    border:1px solid gray;\n"
"    border-left:0px;\n"
"background:transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background:rgba(100,100,100,80);\n"
"}"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_reload.setIcon(icon)
        self.b_reload.setIconSize(QtCore.QSize(12, 12))
        self.b_reload.setObjectName(_fromUtf8("b_reload"))
        self.gridLayout.addWidget(self.b_reload, 1, 0, 1, 1)
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.sw_main = QtGui.QStackedWidget(self.splitter)
        self.sw_main.setObjectName(_fromUtf8("sw_main"))
        self.pg_gen = QtGui.QWidget()
        self.pg_gen.setObjectName(_fromUtf8("pg_gen"))
        self.gridLayout_8 = QtGui.QGridLayout(self.pg_gen)
        self.gridLayout_8.setMargin(0)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label_7 = QtGui.QLabel(self.pg_gen)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_8.addWidget(self.label_7, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 1, 2, 1, 1)
        self.b_save_gen = QtGui.QPushButton(self.pg_gen)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_save_gen.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_gen.setIcon(icon1)
        self.b_save_gen.setIconSize(QtCore.QSize(12, 12))
        self.b_save_gen.setObjectName(_fromUtf8("b_save_gen"))
        self.gridLayout_8.addWidget(self.b_save_gen, 1, 3, 1, 1)
        self.label_8 = QtGui.QLabel(self.pg_gen)
        self.label_8.setWordWrap(True)
        self.label_8.setMargin(5)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_8.addWidget(self.label_8, 3, 0, 1, 4)
        self.fr_gen_ed = QtGui.QFrame(self.pg_gen)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_gen_ed.sizePolicy().hasHeightForWidth())
        self.fr_gen_ed.setSizePolicy(sizePolicy)
        self.fr_gen_ed.setStyleSheet(_fromUtf8("QFrame#fr_gen_ed {\n"
"    border-top:1px solid gray;\n"
"    border-bottom:1px solid gray;\n"
"}"))
        self.fr_gen_ed.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_gen_ed.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_gen_ed.setObjectName(_fromUtf8("fr_gen_ed"))
        self.gridLayout_7 = QtGui.QGridLayout(self.fr_gen_ed)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_8.addWidget(self.fr_gen_ed, 4, 0, 1, 4)
        self.sw_main.addWidget(self.pg_gen)
        self.pg_editors = QtGui.QWidget()
        self.pg_editors.setObjectName(_fromUtf8("pg_editors"))
        self.gridLayout_6 = QtGui.QGridLayout(self.pg_editors)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.pg_editors)
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_6.addWidget(self.label_6, 0, 0, 1, 1)
        self.b_save_editors = QtGui.QPushButton(self.pg_editors)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_save_editors.setFont(font)
        self.b_save_editors.setIcon(icon1)
        self.b_save_editors.setIconSize(QtCore.QSize(12, 12))
        self.b_save_editors.setObjectName(_fromUtf8("b_save_editors"))
        self.gridLayout_6.addWidget(self.b_save_editors, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.pg_editors)
        self.label_5.setWordWrap(True)
        self.label_5.setMargin(5)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_6.addWidget(self.label_5, 1, 0, 1, 3)
        self.fr_ed_ed = QtGui.QFrame(self.pg_editors)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_ed_ed.sizePolicy().hasHeightForWidth())
        self.fr_ed_ed.setSizePolicy(sizePolicy)
        self.fr_ed_ed.setStyleSheet(_fromUtf8("QFrame#fr_ed_ed {\n"
"    border-top:1px solid gray;\n"
"    border-bottom:1px solid gray;\n"
"}"))
        self.fr_ed_ed.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_ed_ed.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_ed_ed.setObjectName(_fromUtf8("fr_ed_ed"))
        self.gridLayout_5 = QtGui.QGridLayout(self.fr_ed_ed)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_6.addWidget(self.fr_ed_ed, 2, 0, 1, 3)
        self.sw_main.addWidget(self.pg_editors)
        self.pg_lang = QtGui.QWidget()
        self.pg_lang.setObjectName(_fromUtf8("pg_lang"))
        self.gridLayout_4 = QtGui.QGridLayout(self.pg_lang)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 4)
        self.gridLayout_4.setHorizontalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_3 = QtGui.QLabel(self.pg_lang)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 0, 3, 1, 1)
        self.b_save_lang = QtGui.QPushButton(self.pg_lang)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_save_lang.setFont(font)
        self.b_save_lang.setIcon(icon1)
        self.b_save_lang.setIconSize(QtCore.QSize(12, 12))
        self.b_save_lang.setObjectName(_fromUtf8("b_save_lang"))
        self.gridLayout_4.addWidget(self.b_save_lang, 0, 4, 1, 1)
        self.label_4 = QtGui.QLabel(self.pg_lang)
        self.label_4.setWordWrap(True)
        self.label_4.setMargin(5)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 5)
        self.fr_lang_ed = QtGui.QFrame(self.pg_lang)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_lang_ed.sizePolicy().hasHeightForWidth())
        self.fr_lang_ed.setSizePolicy(sizePolicy)
        self.fr_lang_ed.setStyleSheet(_fromUtf8("QFrame#fr_lang_ed {\n"
"    border-top:1px solid gray;\n"
"    border-bottom:1px solid gray;\n"
"}"))
        self.fr_lang_ed.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_lang_ed.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_lang_ed.setObjectName(_fromUtf8("fr_lang_ed"))
        self.gridLayout_3 = QtGui.QGridLayout(self.fr_lang_ed)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_4.addWidget(self.fr_lang_ed, 2, 0, 1, 5)
        self.sw_main.addWidget(self.pg_lang)
        self.pg_ext = QtGui.QWidget()
        self.pg_ext.setObjectName(_fromUtf8("pg_ext"))
        self.gridLayout_2 = QtGui.QGridLayout(self.pg_ext)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.pg_ext)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 2, 1, 1)
        self.b_save_ext = QtGui.QPushButton(self.pg_ext)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.b_save_ext.setFont(font)
        self.b_save_ext.setIcon(icon1)
        self.b_save_ext.setIconSize(QtCore.QSize(12, 12))
        self.b_save_ext.setObjectName(_fromUtf8("b_save_ext"))
        self.gridLayout_2.addWidget(self.b_save_ext, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.pg_ext)
        self.label_2.setMargin(10)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 4)
        self.te_ext = QtGui.QPlainTextEdit(self.pg_ext)
        self.te_ext.setStyleSheet(_fromUtf8("QPlainTextEdit {\n"
"    background:rgb(30,30,30);\n"
"    color:white;\n"
"    border:0px;\n"
"    border-top:1px solid gray;\n"
"    border-bottom:1px solid gray;\n"
"    padding:10px;\n"
"}"))
        self.te_ext.setFrameShape(QtGui.QFrame.NoFrame)
        self.te_ext.setObjectName(_fromUtf8("te_ext"))
        self.gridLayout_2.addWidget(self.te_ext, 2, 0, 1, 4)
        self.sw_main.addWidget(self.pg_ext)
        self.pg_plug = QtGui.QWidget()
        self.pg_plug.setObjectName(_fromUtf8("pg_plug"))
        self.gridLayout_9 = QtGui.QGridLayout(self.pg_plug)
        self.gridLayout_9.setMargin(0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        spacerItem4 = QtGui.QSpacerItem(247, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem4, 0, 2, 1, 1)
        self.b_plugin_file_add = QtGui.QPushButton(self.pg_plug)
        self.b_plugin_file_add.setObjectName(_fromUtf8("b_plugin_file_add"))
        self.gridLayout_9.addWidget(self.b_plugin_file_add, 0, 3, 1, 1)
        self.label_9 = QtGui.QLabel(self.pg_plug)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_9.addWidget(self.label_9, 0, 0, 1, 1)
        self.b_plugin_url_add = QtGui.QPushButton(self.pg_plug)
        self.b_plugin_url_add.setObjectName(_fromUtf8("b_plugin_url_add"))
        self.gridLayout_9.addWidget(self.b_plugin_url_add, 0, 4, 1, 1)
        self.tr_plugins = QtGui.QTreeWidget(self.pg_plug)
        self.tr_plugins.setObjectName(_fromUtf8("tr_plugins"))
        self.gridLayout_9.addWidget(self.tr_plugins, 2, 0, 1, 5)
        self.label_10 = QtGui.QLabel(self.pg_plug)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_9.addWidget(self.label_10, 1, 0, 1, 5)
        self.sw_main.addWidget(self.pg_plug)
        self.textBrowser = QtGui.QTextBrowser(self.splitter)
        self.textBrowser.setStyleSheet(_fromUtf8("QTextBrowser {\n"
"    background:transparent;\n"
"    color:white;\n"
"    border-left:1px solid gray;\n"
"}"))
        self.textBrowser.setFrameShape(QtGui.QFrame.NoFrame)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.splitter, 0, 1, 2, 1)

        self.retranslateUi(Form)
        self.sw_main.setCurrentIndex(4)
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
        self.b_reload.setToolTip(_translate("Form", "reload all settings", None))
        self.b_reload.setText(_translate("Form", "reload", None))
        self.label_7.setText(_translate("Form", " General Settings", None))
        self.b_save_gen.setText(_translate("Form", "save", None))
        self.label_8.setText(_translate("Form", "<html><head/><body><p>The format for these settings are json</p></body></html>", None))
        self.label_6.setText(_translate("Form", " Editors Settings", None))
        self.b_save_editors.setText(_translate("Form", "save", None))
        self.label_5.setText(_translate("Form", "<html><head/><body><p>The format for these settings are json</p><p>Default settings for the editors</p></body></html>", None))
        self.label_3.setText(_translate("Form", " Language Settings", None))
        self.b_save_lang.setText(_translate("Form", "save", None))
        self.label_4.setText(_translate("Form", "<html><head/><body><p>The format for these settings are json</p><p><span style=\" font-weight:600; text-decoration: underline;\">Standard keys are:</span><br/><span style=\" font-weight:600;\">editor</span> - the editor to use for the language<br/><span style=\" font-weight:600;\">run</span> - the command to execute for this language (filepath is appended to the end of the command)<br/><span style=\" font-weight:600;\">fave</span> - set to 0, if you don\'t want this language to show up in the favorites lists<br/><span style=\" font-weight:600;\">theme</span> - for ace editor, this will change the theme<br/><span style=\" font-weight:600;\">wordwrap</span> - 0 for no wordwrap, 1 for wordwrap</p></body></html>", None))
        self.label.setText(_translate("Form", "   File extension to language mapping", None))
        self.b_save_ext.setText(_translate("Form", "save", None))
        self.label_2.setText(_translate("Form", "For list of languages - look at the options for each editor\n"
"Format is:\n"
"extension=language", None))
        self.b_plugin_file_add.setText(_translate("Form", "Add from File", None))
        self.label_9.setText(_translate("Form", " Plugins", None))
        self.b_plugin_url_add.setText(_translate("Form", "Add from URL", None))
        self.tr_plugins.headerItem().setText(0, _translate("Form", "Plugin Name", None))
        self.tr_plugins.headerItem().setText(1, _translate("Form", "Enabled", None))
        self.tr_plugins.headerItem().setText(2, _translate("Form", "Description", None))
        self.label_10.setText(_translate("Form", " A restart may be needed for plugin changes to take affect", None))

