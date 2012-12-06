# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\ui\nonstop.ui'
#
# Created: Wed Dec 05 21:19:58 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Nonstop(object):
    def setupUi(self, Nonstop):
        Nonstop.setObjectName(_fromUtf8("Nonstop"))
        Nonstop.resize(498, 311)
        Nonstop.setMinimumSize(QtCore.QSize(498, 311))
        Nonstop.setMaximumSize(QtCore.QSize(498, 311))
        Nonstop.setWindowTitle(QtGui.QApplication.translate("Nonstop", "Nonstop Debate Viewer", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/monokuma.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Nonstop.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(Nonstop)
        self.buttonBox.setGeometry(QtCore.QRect(339, 280, 151, 31))
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lblPreview = QtGui.QLabel(Nonstop)
        self.lblPreview.setGeometry(QtCore.QRect(9, 9, 480, 272))
        self.lblPreview.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblPreview.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblPreview.setText(_fromUtf8(""))
        self.lblPreview.setObjectName(_fromUtf8("lblPreview"))

        self.retranslateUi(Nonstop)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Nonstop.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Nonstop.reject)
        QtCore.QMetaObject.connectSlotsByName(Nonstop)

    def retranslateUi(self, Nonstop):
        pass

import icons_rc
