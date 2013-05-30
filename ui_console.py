# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\ui\console.ui'
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

class Ui_Console(object):
    def setupUi(self, Console):
        Console.setObjectName(_fromUtf8("Console"))
        Console.resize(552, 333)
        Console.setWindowTitle(QtGui.QApplication.translate("Console", "Console", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/monokuma-green.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Console.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Console)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtConsole = XLoggerWidget(Console)
        self.txtConsole.setObjectName(_fromUtf8("txtConsole"))
        self.verticalLayout.addWidget(self.txtConsole)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Console)
        self.label.setText(QtGui.QApplication.translate("Console", " Logging Level ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cboLevels = QtGui.QComboBox(Console)
        self.cboLevels.setObjectName(_fromUtf8("cboLevels"))
        self.horizontalLayout.addWidget(self.cboLevels)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(Console)
        self.pushButton.setText(QtGui.QApplication.translate("Console", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Console)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.txtConsole.clear)
        QtCore.QObject.connect(self.cboLevels, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), Console.updateLogLevel)
        QtCore.QMetaObject.connectSlotsByName(Console)

    def retranslateUi(self, Console):
        pass

from projexui.xloggerwidget import XLoggerWidget
import icons_rc
