# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\levelInfoWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_infoWidget(object):
    def setupUi(self, infoWidget):
        infoWidget.setObjectName("infoWidget")
        infoWidget.resize(416, 201)
        self.verticalLayout = QtWidgets.QVBoxLayout(infoWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.baseBPMLabel = QtWidgets.QLabel(infoWidget)
        self.baseBPMLabel.setObjectName("baseBPMLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.baseBPMLabel)
        self.baseBPMIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.baseBPMIn.setObjectName("baseBPMIn")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.baseBPMIn)
        self.beatsPerBarLabel = QtWidgets.QLabel(infoWidget)
        self.beatsPerBarLabel.setObjectName("beatsPerBarLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.beatsPerBarLabel)
        self.beatsPerBarIn = QtWidgets.QSpinBox(infoWidget)
        self.beatsPerBarIn.setObjectName("beatsPerBarIn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.beatsPerBarIn)
        self.noteJumpSpeedLabel = QtWidgets.QLabel(infoWidget)
        self.noteJumpSpeedLabel.setObjectName("noteJumpSpeedLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.noteJumpSpeedLabel)
        self.noteJumpSpeedIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.noteJumpSpeedIn.setObjectName("noteJumpSpeedIn")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.noteJumpSpeedIn)
        self.shuffleLabel = QtWidgets.QLabel(infoWidget)
        self.shuffleLabel.setObjectName("shuffleLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.shuffleLabel)
        self.shuffleIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.shuffleIn.setObjectName("shuffleIn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.shuffleIn)
        self.shufflePeriodLabel = QtWidgets.QLabel(infoWidget)
        self.shufflePeriodLabel.setObjectName("shufflePeriodLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.shufflePeriodLabel)
        self.shufflePeriodIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.shufflePeriodIn.setObjectName("shufflePeriodIn")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.shufflePeriodIn)
        self.offsetLabel = QtWidgets.QLabel(infoWidget)
        self.offsetLabel.setObjectName("offsetLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.offsetLabel)
        self.offsetIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.offsetIn.setObjectName("offsetIn")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.offsetIn)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.levelInfoOkBtn = QtWidgets.QPushButton(infoWidget)
        self.levelInfoOkBtn.setObjectName("levelInfoOkBtn")
        self.horizontalLayout.addWidget(self.levelInfoOkBtn)
        self.levelInfoCancelBtn = QtWidgets.QPushButton(infoWidget)
        self.levelInfoCancelBtn.setObjectName("levelInfoCancelBtn")
        self.horizontalLayout.addWidget(self.levelInfoCancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(infoWidget)
        QtCore.QMetaObject.connectSlotsByName(infoWidget)

    def retranslateUi(self, infoWidget):
        _translate = QtCore.QCoreApplication.translate
        infoWidget.setWindowTitle(_translate("infoWidget", "Form"))
        self.baseBPMLabel.setText(_translate("infoWidget", "Base BPM"))
        self.beatsPerBarLabel.setText(_translate("infoWidget", "Beats Per Bar"))
        self.noteJumpSpeedLabel.setText(_translate("infoWidget", "Note Jump Speed"))
        self.shuffleLabel.setText(_translate("infoWidget", "Shuffle"))
        self.shufflePeriodLabel.setText(_translate("infoWidget", "Shuffle Period"))
        self.offsetLabel.setText(_translate("infoWidget", "Offset"))
        self.levelInfoOkBtn.setText(_translate("infoWidget", "OK"))
        self.levelInfoCancelBtn.setText(_translate("infoWidget", "Cancel"))

