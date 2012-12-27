# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\ui\fontgen.ui'
#
# Created: Wed Dec 26 20:28:57 2012
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
        FontGenerator.resize(442, 417)
        FontGenerator.setWindowTitle(QtGui.QApplication.translate("FontGenerator", "Font Generator", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/monokuma-green.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FontGenerator.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(FontGenerator)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(FontGenerator)
        self.pushButton.setText(QtGui.QApplication.translate("FontGenerator", "New Tab", None, QtGui.QApplication.UnicodeUTF8))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(FontGenerator)
        self.pushButton_2.setText(QtGui.QApplication.translate("FontGenerator", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/cross.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabFonts = QtGui.QTabWidget(FontGenerator)
        self.tabFonts.setTabsClosable(False)
        self.tabFonts.setMovable(True)
        self.tabFonts.setObjectName(_fromUtf8("tabFonts"))
        self.verticalLayout.addWidget(self.tabFonts)
        self.comboBox = QtGui.QComboBox(FontGenerator)
        self.comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("FontGenerator", "Font 01 (Normal Text)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("FontGenerator", "Font 02 (Class Trial Minigame Text)", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chkGenForGame = QtGui.QCheckBox(FontGenerator)
        self.chkGenForGame.setText(QtGui.QApplication.translate("FontGenerator", "Export to umdimage2", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGenForGame.setChecked(True)
        self.chkGenForGame.setObjectName(_fromUtf8("chkGenForGame"))
        self.horizontalLayout_2.addWidget(self.chkGenForGame)
        self.chkGenForEditor = QtGui.QCheckBox(FontGenerator)
        self.chkGenForEditor.setText(QtGui.QApplication.translate("FontGenerator", "Export to editor GFX dir", None, QtGui.QApplication.UnicodeUTF8))
        self.chkGenForEditor.setChecked(True)
        self.chkGenForEditor.setObjectName(_fromUtf8("chkGenForEditor"))
        self.horizontalLayout_2.addWidget(self.chkGenForEditor)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_3 = QtGui.QPushButton(FontGenerator)
        self.pushButton_3.setText(QtGui.QApplication.translate("FontGenerator", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(FontGenerator)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FontGenerator)
        self.tabFonts.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FontGenerator.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FontGenerator.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.add_tab)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.remove_tab)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), FontGenerator.generate_font)
        QtCore.QMetaObject.connectSlotsByName(FontGenerator)

    def retranslateUi(self, FontGenerator):
        pass

import icons_rc
