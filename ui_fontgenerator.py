# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\ui\fontgen.ui'
#
# Created: Wed May 22 17:24:48 2013
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FontGenerator(object):
    def setupUi(self, FontGenerator):
        FontGenerator.setObjectName(_fromUtf8("FontGenerator"))
        FontGenerator.resize(570, 493)
        FontGenerator.setWindowTitle(QtGui.QApplication.translate("FontGenerator", "Font Generator - untitled[*]", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/monokuma-green.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FontGenerator.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(FontGenerator)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnNew = QtGui.QPushButton(FontGenerator)
        self.btnNew.setText(QtGui.QApplication.translate("FontGenerator", "&New", None, QtGui.QApplication.UnicodeUTF8))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/report.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNew.setIcon(icon1)
        self.btnNew.setShortcut(QtGui.QApplication.translate("FontGenerator", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNew.setAutoDefault(False)
        self.btnNew.setObjectName(_fromUtf8("btnNew"))
        self.horizontalLayout_2.addWidget(self.btnNew)
        self.btnSave = QtGui.QPushButton(FontGenerator)
        self.btnSave.setText(QtGui.QApplication.translate("FontGenerator", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/disk.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setShortcut(QtGui.QApplication.translate("FontGenerator", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSave.setAutoDefault(False)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.btnSaveAs = QtGui.QPushButton(FontGenerator)
        self.btnSaveAs.setText(QtGui.QApplication.translate("FontGenerator", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAs.setShortcut(QtGui.QApplication.translate("FontGenerator", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveAs.setAutoDefault(False)
        self.btnSaveAs.setObjectName(_fromUtf8("btnSaveAs"))
        self.horizontalLayout_2.addWidget(self.btnSaveAs)
        self.btnLoad = QtGui.QPushButton(FontGenerator)
        self.btnLoad.setText(QtGui.QApplication.translate("FontGenerator", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLoad.setIcon(icon3)
        self.btnLoad.setShortcut(QtGui.QApplication.translate("FontGenerator", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoad.setAutoDefault(False)
        self.btnLoad.setObjectName(_fromUtf8("btnLoad"))
        self.horizontalLayout_2.addWidget(self.btnLoad)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnGenerateFont = QtGui.QPushButton(FontGenerator)
        self.btnGenerateFont.setText(QtGui.QApplication.translate("FontGenerator", "&Generate", None, QtGui.QApplication.UnicodeUTF8))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/cog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnGenerateFont.setIcon(icon4)
        self.btnGenerateFont.setShortcut(QtGui.QApplication.translate("FontGenerator", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGenerateFont.setAutoDefault(False)
        self.btnGenerateFont.setObjectName(_fromUtf8("btnGenerateFont"))
        self.horizontalLayout_2.addWidget(self.btnGenerateFont)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtGui.QFrame(FontGenerator)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.tabFonts = QtGui.QTabWidget(FontGenerator)
        self.tabFonts.setTabsClosable(False)
        self.tabFonts.setMovable(True)
        self.tabFonts.setObjectName(_fromUtf8("tabFonts"))
        self.verticalLayout.addWidget(self.tabFonts)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnNewTab = QtGui.QPushButton(FontGenerator)
        self.btnNewTab.setText(QtGui.QApplication.translate("FontGenerator", "Add Tab", None, QtGui.QApplication.UnicodeUTF8))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNewTab.setIcon(icon5)
        self.btnNewTab.setAutoDefault(False)
        self.btnNewTab.setObjectName(_fromUtf8("btnNewTab"))
        self.horizontalLayout.addWidget(self.btnNewTab)
        self.btnRemoveTab = QtGui.QPushButton(FontGenerator)
        self.btnRemoveTab.setText(QtGui.QApplication.translate("FontGenerator", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemoveTab.setIcon(icon6)
        self.btnRemoveTab.setAutoDefault(False)
        self.btnRemoveTab.setObjectName(_fromUtf8("btnRemoveTab"))
        self.horizontalLayout.addWidget(self.btnRemoveTab)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(FontGenerator)
        self.groupBox.setTitle(QtGui.QApplication.translate("FontGenerator", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setContentsMargins(-1, 4, -1, 8)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chkGenForGame = QtGui.QCheckBox(self.groupBox)
        self.chkGenForGame.setText(QtGui.QApplication.translate("FontGenerator", "Export to umdimage2", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGenForGame.setChecked(True)
        self.chkGenForGame.setObjectName(_fromUtf8("chkGenForGame"))
        self.verticalLayout_2.addWidget(self.chkGenForGame)
        self.chkGenForEditor = QtGui.QCheckBox(self.groupBox)
        self.chkGenForEditor.setText(QtGui.QApplication.translate("FontGenerator", "Export to editor GFX dir", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGenForEditor.setChecked(True)
        self.chkGenForEditor.setObjectName(_fromUtf8("chkGenForEditor"))
        self.verticalLayout_2.addWidget(self.chkGenForEditor)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.rdoGenFont1 = QtGui.QRadioButton(self.groupBox)
        self.rdoGenFont1.setText(QtGui.QApplication.translate("FontGenerator", "Font 01 (regular text)", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoGenFont1.setChecked(True)
        self.rdoGenFont1.setObjectName(_fromUtf8("rdoGenFont1"))
        self.verticalLayout_3.addWidget(self.rdoGenFont1)
        self.rdoGenFont2 = QtGui.QRadioButton(self.groupBox)
        self.rdoGenFont2.setText(QtGui.QApplication.translate("FontGenerator", "Font 02 (Class Trial minigame text)", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoGenFont2.setChecked(False)
        self.rdoGenFont2.setObjectName(_fromUtf8("rdoGenFont2"))
        self.verticalLayout_3.addWidget(self.rdoGenFont2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("FontGenerator", "Tab Priority", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_6.setContentsMargins(-1, 4, -1, 8)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.rdoLeftToRight = QtGui.QRadioButton(self.groupBox_2)
        self.rdoLeftToRight.setText(QtGui.QApplication.translate("FontGenerator", "Left to right", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoLeftToRight.setChecked(True)
        self.rdoLeftToRight.setObjectName(_fromUtf8("rdoLeftToRight"))
        self.horizontalLayout_6.addWidget(self.rdoLeftToRight)
        self.rdoRightToLeft = QtGui.QRadioButton(self.groupBox_2)
        self.rdoRightToLeft.setText(QtGui.QApplication.translate("FontGenerator", "Right to left", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoRightToLeft.setObjectName(_fromUtf8("rdoRightToLeft"))
        self.horizontalLayout_6.addWidget(self.rdoRightToLeft)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.btnClose = QtGui.QPushButton(FontGenerator)
        self.btnClose.setText(QtGui.QApplication.translate("FontGenerator", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setAutoDefault(False)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_4.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(FontGenerator)
        self.tabFonts.setCurrentIndex(-1)
        QtCore.QObject.connect(self.btnNewTab, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.add_tab)
        QtCore.QObject.connect(self.btnRemoveTab, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.remove_tab)
        QtCore.QObject.connect(self.btnGenerateFont, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.generate_font)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.accept)
        QtCore.QObject.connect(self.chkGenForGame, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.chkGenForEditor, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.rdoGenFont1, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.rdoGenFont2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.rdoLeftToRight, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.rdoRightToLeft, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), FontGenerator.export_changed)
        QtCore.QObject.connect(self.btnNew, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.new_clicked)
        QtCore.QObject.connect(self.btnSave, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.save_clicked)
        QtCore.QObject.connect(self.btnSaveAs, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.save_as_clicked)
        QtCore.QObject.connect(self.btnLoad, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.load_clicked)
        QtCore.QMetaObject.connectSlotsByName(FontGenerator)
        FontGenerator.setTabOrder(self.tabFonts, self.btnNewTab)
        FontGenerator.setTabOrder(self.btnNewTab, self.btnRemoveTab)
        FontGenerator.setTabOrder(self.btnRemoveTab, self.chkGenForGame)
        FontGenerator.setTabOrder(self.chkGenForGame, self.chkGenForEditor)
        FontGenerator.setTabOrder(self.chkGenForEditor, self.rdoGenFont1)
        FontGenerator.setTabOrder(self.rdoGenFont1, self.rdoGenFont2)
        FontGenerator.setTabOrder(self.rdoGenFont2, self.rdoLeftToRight)
        FontGenerator.setTabOrder(self.rdoLeftToRight, self.rdoRightToLeft)
        FontGenerator.setTabOrder(self.rdoRightToLeft, self.btnNew)
        FontGenerator.setTabOrder(self.btnNew, self.btnSave)
        FontGenerator.setTabOrder(self.btnSave, self.btnSaveAs)
        FontGenerator.setTabOrder(self.btnSaveAs, self.btnLoad)
        FontGenerator.setTabOrder(self.btnLoad, self.btnGenerateFont)
        FontGenerator.setTabOrder(self.btnGenerateFont, self.btnClose)

    def retranslateUi(self, FontGenerator):
        pass

import icons_rc
