# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'find_files.ui'
#
# Created: Sat Jan  9 01:31:12 2016
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
        Form.resize(568, 341)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tr_results = QtGui.QTreeWidget(self.frame_2)
        self.tr_results.setStyleSheet(_fromUtf8(" QTreeWidget {\n"
"border:0px;\n"
"outline:none;\n"
"}\n"
"QTreeWidget::branch:has-siblings:!adjoins-item {\n"
"     border-image: url(style/img/none.png) 0;\n"
" }\n"
" QTreeWidget::branch:has-siblings:adjoins-item {\n"
"     border-image: url(style/img/none.png) 0;\n"
" }\n"
"\n"
" QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {\n"
"     border-image: url(style/img/none.png) 0;\n"
" }"))
        self.tr_results.setObjectName(_fromUtf8("tr_results"))
        self.gridLayout.addWidget(self.tr_results, 2, 0, 1, 3)
        self.frame_3 = QtGui.QFrame(self.frame_2)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 26))
        self.frame_3.setStyleSheet(_fromUtf8("QFrame#frame_3 {\n"
"background:rgb(40,40,40);\n"
"border-bottom:1px solid rgba(130,130,130,200);\n"
"}\n"
"QLineEdit {\n"
"border:0px;\n"
"border-left:1px solid rgba(130,130,130,200);\n"
"background:transparent;\n"
"}\n"
"QPushButton {\n"
"background:transparent;\n"
"outline:0;\n"
"}\n"
"QPushButton:hover {\n"
"background:rgba(100,100,100,100)\n"
"}"))
        self.frame_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_4.setSpacing(2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 1)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.le_search = QtGui.QLineEdit(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_search.sizePolicy().hasHeightForWidth())
        self.le_search.setSizePolicy(sizePolicy)
        self.le_search.setText(_fromUtf8(""))
        self.le_search.setObjectName(_fromUtf8("le_search"))
        self.gridLayout_4.addWidget(self.le_search, 0, 5, 1, 1)
        self.le_path = QtGui.QLineEdit(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_path.sizePolicy().hasHeightForWidth())
        self.le_path.setSizePolicy(sizePolicy)
        self.le_path.setStyleSheet(_fromUtf8("QLineEdit {\n"
"border-left:0px;\n"
"}"))
        self.le_path.setObjectName(_fromUtf8("le_path"))
        self.gridLayout_4.addWidget(self.le_path, 0, 3, 1, 1)
        self.le_ext = QtGui.QLineEdit(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_ext.sizePolicy().hasHeightForWidth())
        self.le_ext.setSizePolicy(sizePolicy)
        self.le_ext.setText(_fromUtf8(""))
        self.le_ext.setObjectName(_fromUtf8("le_ext"))
        self.gridLayout_4.addWidget(self.le_ext, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(6, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 1, 1, 1)
        self.b_browse = QtGui.QPushButton(self.frame_3)
        self.b_browse.setStyleSheet(_fromUtf8("QPushButton {\n"
"border-left:1px solid rgba(130,130,130,200);\n"
"}"))
        self.b_browse.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/file_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_browse.setIcon(icon)
        self.b_browse.setObjectName(_fromUtf8("b_browse"))
        self.gridLayout_4.addWidget(self.b_browse, 0, 2, 1, 1)
        self.b_browse_2 = QtGui.QPushButton(self.frame_3)
        self.b_browse_2.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/wrench.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_browse_2.setIcon(icon1)
        self.b_browse_2.setCheckable(True)
        self.b_browse_2.setObjectName(_fromUtf8("b_browse_2"))
        self.gridLayout_4.addWidget(self.b_browse_2, 0, 0, 1, 1)
        self.b_search = QtGui.QPushButton(self.frame_3)
        self.b_search.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search.setIcon(icon2)
        self.b_search.setCheckable(True)
        self.b_search.setObjectName(_fromUtf8("b_search"))
        self.gridLayout_4.addWidget(self.b_search, 0, 6, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 0, 0, 1, 3)
        self.frame = QtGui.QFrame(self.frame_2)
        self.frame.setStyleSheet(_fromUtf8("QFrame#frame {\n"
"border-top:1px solid rgba(130,130,130,200);\n"
"}\n"
"QPushButton {\n"
"background:transparent;\n"
"outline:none;\n"
"}\n"
"QPushButton:hover {\n"
"background:rgba(100,100,100,100);\n"
"}"))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.b_search_2 = QtGui.QPushButton(self.frame)
        self.b_search_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_search_2.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/arrow_in.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search_2.setIcon(icon3)
        self.b_search_2.setObjectName(_fromUtf8("b_search_2"))
        self.gridLayout_3.addWidget(self.b_search_2, 0, 2, 1, 1)
        self.l_cur_file = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_cur_file.sizePolicy().hasHeightForWidth())
        self.l_cur_file.setSizePolicy(sizePolicy)
        self.l_cur_file.setStyleSheet(_fromUtf8(""))
        self.l_cur_file.setText(_fromUtf8(""))
        self.l_cur_file.setObjectName(_fromUtf8("l_cur_file"))
        self.gridLayout_3.addWidget(self.l_cur_file, 0, 0, 1, 1)
        self.b_search_3 = QtGui.QPushButton(self.frame)
        self.b_search_3.setMaximumSize(QtCore.QSize(30, 16777215))
        self.b_search_3.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("../../style/img/arrow_out.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search_3.setIcon(icon4)
        self.b_search_3.setObjectName(_fromUtf8("b_search_3"))
        self.gridLayout_3.addWidget(self.b_search_3, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 3, 0, 1, 3)
        self.fr_settings = QtGui.QFrame(self.frame_2)
        self.fr_settings.setFrameShape(QtGui.QFrame.NoFrame)
        self.fr_settings.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_settings.setObjectName(_fromUtf8("fr_settings"))
        self.gridLayout_5 = QtGui.QGridLayout(self.fr_settings)
        self.gridLayout_5.setContentsMargins(-1, 2, 2, 2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.ckbx_case = QtGui.QCheckBox(self.fr_settings)
        self.ckbx_case.setObjectName(_fromUtf8("ckbx_case"))
        self.gridLayout_5.addWidget(self.ckbx_case, 0, 1, 1, 1)
        self.ckbx_reg = QtGui.QCheckBox(self.fr_settings)
        self.ckbx_reg.setObjectName(_fromUtf8("ckbx_reg"))
        self.gridLayout_5.addWidget(self.ckbx_reg, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.fr_settings, 1, 0, 1, 3)
        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.le_search, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_search.click)
        QtCore.QObject.connect(self.b_search_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tr_results.expandAll)
        QtCore.QObject.connect(self.b_search_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tr_results.collapseAll)
        QtCore.QObject.connect(self.le_ext, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_search.click)
        QtCore.QObject.connect(self.le_path, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.b_search.click)
        QtCore.QObject.connect(self.b_browse_2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.fr_settings.setVisible)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.le_path, self.le_ext)
        Form.setTabOrder(self.le_ext, self.le_search)
        Form.setTabOrder(self.le_search, self.b_search)
        Form.setTabOrder(self.b_search, self.tr_results)
        Form.setTabOrder(self.tr_results, self.b_search_2)
        Form.setTabOrder(self.b_search_2, self.b_browse)
        Form.setTabOrder(self.b_browse, self.b_search_3)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.tr_results.setSortingEnabled(True)
        self.tr_results.headerItem().setText(0, _translate("Form", "File", None))
        self.tr_results.headerItem().setText(1, _translate("Form", "Line(s)", None))
        self.tr_results.headerItem().setText(2, _translate("Form", "Path / Code", None))
        self.le_search.setToolTip(_translate("Form", "Search Term", None))
        self.le_search.setPlaceholderText(_translate("Form", "search term", None))
        self.le_path.setToolTip(_translate("Form", "Path to search (recursively)", None))
        self.le_path.setPlaceholderText(_translate("Form", "path", None))
        self.le_ext.setToolTip(_translate("Form", "<html><head/><body><p>Extensions</p><p>   - example: .py</p><p>   - leave blank to search all</p><p>   - multiple are comma separated (.py,.js)</p></body></html>", None))
        self.le_ext.setPlaceholderText(_translate("Form", "extensions", None))
        self.b_browse.setToolTip(_translate("Form", "select a path", None))
        self.b_browse_2.setToolTip(_translate("Form", "search settings", None))
        self.b_search.setToolTip(_translate("Form", "search", None))
        self.b_search_2.setToolTip(_translate("Form", "collapse all", None))
        self.b_search_3.setToolTip(_translate("Form", "expand all", None))
        self.ckbx_case.setText(_translate("Form", "Match case", None))
        self.ckbx_reg.setToolTip(_translate("Form", "Search term is a regular expression (Python format)", None))
        self.ckbx_reg.setText(_translate("Form", "Regular Expression", None))

