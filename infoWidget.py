# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\infoWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_infoWidget(object):
    def setupUi(self, infoWidget):
        infoWidget.setObjectName("infoWidget")
        infoWidget.resize(416, 541)
        self.verticalLayout = QtWidgets.QVBoxLayout(infoWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.songTitleLabel = QtWidgets.QLabel(infoWidget)
        self.songTitleLabel.setObjectName("songTitleLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.songTitleLabel)
        self.songTitleIn = QtWidgets.QLineEdit(infoWidget)
        self.songTitleIn.setObjectName("songTitleIn")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.songTitleIn)
        self.songSubtitleLabel = QtWidgets.QLabel(infoWidget)
        self.songSubtitleLabel.setObjectName("songSubtitleLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.songSubtitleLabel)
        self.songSubtitleIn = QtWidgets.QLineEdit(infoWidget)
        self.songSubtitleIn.setObjectName("songSubtitleIn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.songSubtitleIn)
        self.songArtistLabel = QtWidgets.QLabel(infoWidget)
        self.songArtistLabel.setObjectName("songArtistLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.songArtistLabel)
        self.songArtistIn = QtWidgets.QLineEdit(infoWidget)
        self.songArtistIn.setObjectName("songArtistIn")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.songArtistIn)
        self.chartCreatorLabel = QtWidgets.QLabel(infoWidget)
        self.chartCreatorLabel.setObjectName("chartCreatorLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.chartCreatorLabel)
        self.chartCreatorIn = QtWidgets.QLineEdit(infoWidget)
        self.chartCreatorIn.setObjectName("chartCreatorIn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chartCreatorIn)
        self.songAudioOffsetLabel = QtWidgets.QLabel(infoWidget)
        self.songAudioOffsetLabel.setObjectName("songAudioOffsetLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.songAudioOffsetLabel)
        self.songAudioOffsetIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.songAudioOffsetIn.setObjectName("songAudioOffsetIn")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.songAudioOffsetIn)
        self.songBPMLabel = QtWidgets.QLabel(infoWidget)
        self.songBPMLabel.setObjectName("songBPMLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.songBPMLabel)
        self.songBPMIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.songBPMIn.setObjectName("songBPMIn")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.songBPMIn)
        self.previewStartLabel = QtWidgets.QLabel(infoWidget)
        self.previewStartLabel.setObjectName("previewStartLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.previewStartLabel)
        self.previewStartIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.previewStartIn.setObjectName("previewStartIn")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.previewStartIn)
        self.previewDurLabel = QtWidgets.QLabel(infoWidget)
        self.previewDurLabel.setObjectName("previewDurLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.previewDurLabel)
        self.previewDurIn = QtWidgets.QDoubleSpinBox(infoWidget)
        self.previewDurIn.setObjectName("previewDurIn")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.previewDurIn)
        self.enviromentLabel = QtWidgets.QLabel(infoWidget)
        self.enviromentLabel.setObjectName("enviromentLabel")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.enviromentLabel)
        self.enviromentIn = QtWidgets.QComboBox(infoWidget)
        self.enviromentIn.setObjectName("enviromentIn")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.enviromentIn)
        self.audioFileLabel = QtWidgets.QLabel(infoWidget)
        self.audioFileLabel.setObjectName("audioFileLabel")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.audioFileLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.audioFileTextIn = QtWidgets.QLineEdit(infoWidget)
        self.audioFileTextIn.setObjectName("audioFileTextIn")
        self.horizontalLayout_3.addWidget(self.audioFileTextIn)
        self.audioFileSelectBtn = QtWidgets.QPushButton(infoWidget)
        self.audioFileSelectBtn.setObjectName("audioFileSelectBtn")
        self.horizontalLayout_3.addWidget(self.audioFileSelectBtn)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.coverLabel = QtWidgets.QLabel(infoWidget)
        self.coverLabel.setObjectName("coverLabel")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.coverLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.coverTextIn = QtWidgets.QLineEdit(infoWidget)
        self.coverTextIn.setObjectName("coverTextIn")
        self.horizontalLayout_2.addWidget(self.coverTextIn)
        self.coverSelectBtm = QtWidgets.QPushButton(infoWidget)
        self.coverSelectBtm.setObjectName("coverSelectBtm")
        self.horizontalLayout_2.addWidget(self.coverSelectBtm)
        self.formLayout.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.levelJsonLabel = QtWidgets.QLabel(infoWidget)
        self.levelJsonLabel.setObjectName("levelJsonLabel")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.levelJsonLabel)
        self.levelEasyLabel = QtWidgets.QLabel(infoWidget)
        self.levelEasyLabel.setObjectName("levelEasyLabel")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.levelEasyLabel)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.levelEasyTextIn = QtWidgets.QLineEdit(infoWidget)
        self.levelEasyTextIn.setObjectName("levelEasyTextIn")
        self.horizontalLayout_5.addWidget(self.levelEasyTextIn)
        self.levelEasySelectBtn = QtWidgets.QPushButton(infoWidget)
        self.levelEasySelectBtn.setObjectName("levelEasySelectBtn")
        self.horizontalLayout_5.addWidget(self.levelEasySelectBtn)
        self.formLayout.setLayout(13, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.levelNormalLabel = QtWidgets.QLabel(infoWidget)
        self.levelNormalLabel.setObjectName("levelNormalLabel")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.levelNormalLabel)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.levelNormalTextIn = QtWidgets.QLineEdit(infoWidget)
        self.levelNormalTextIn.setObjectName("levelNormalTextIn")
        self.horizontalLayout_4.addWidget(self.levelNormalTextIn)
        self.levelNormalSelectBtn = QtWidgets.QPushButton(infoWidget)
        self.levelNormalSelectBtn.setObjectName("levelNormalSelectBtn")
        self.horizontalLayout_4.addWidget(self.levelNormalSelectBtn)
        self.formLayout.setLayout(14, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.levelHardLabel = QtWidgets.QLabel(infoWidget)
        self.levelHardLabel.setObjectName("levelHardLabel")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.levelHardLabel)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.levelHardTextIn = QtWidgets.QLineEdit(infoWidget)
        self.levelHardTextIn.setObjectName("levelHardTextIn")
        self.horizontalLayout_6.addWidget(self.levelHardTextIn)
        self.levelHardSelectBtm = QtWidgets.QPushButton(infoWidget)
        self.levelHardSelectBtm.setObjectName("levelHardSelectBtm")
        self.horizontalLayout_6.addWidget(self.levelHardSelectBtm)
        self.formLayout.setLayout(15, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.levelExpertLabel = QtWidgets.QLabel(infoWidget)
        self.levelExpertLabel.setObjectName("levelExpertLabel")
        self.formLayout.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.levelExpertLabel)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.levelExpertTextIn = QtWidgets.QLineEdit(infoWidget)
        self.levelExpertTextIn.setObjectName("levelExpertTextIn")
        self.horizontalLayout_7.addWidget(self.levelExpertTextIn)
        self.levelExpertSelectBtn = QtWidgets.QPushButton(infoWidget)
        self.levelExpertSelectBtn.setObjectName("levelExpertSelectBtn")
        self.horizontalLayout_7.addWidget(self.levelExpertSelectBtn)
        self.formLayout.setLayout(16, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)
        self.levelExpertPlusLabel = QtWidgets.QLabel(infoWidget)
        self.levelExpertPlusLabel.setObjectName("levelExpertPlusLabel")
        self.formLayout.setWidget(17, QtWidgets.QFormLayout.LabelRole, self.levelExpertPlusLabel)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.levelExpertPlusTextIn = QtWidgets.QLineEdit(infoWidget)
        self.levelExpertPlusTextIn.setObjectName("levelExpertPlusTextIn")
        self.horizontalLayout_8.addWidget(self.levelExpertPlusTextIn)
        self.levelExpertPlusSelectBtn = QtWidgets.QPushButton(infoWidget)
        self.levelExpertPlusSelectBtn.setObjectName("levelExpertPlusSelectBtn")
        self.horizontalLayout_8.addWidget(self.levelExpertPlusSelectBtn)
        self.formLayout.setLayout(17, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_8)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(11, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.levelJSONDescptionLabel = QtWidgets.QLabel(infoWidget)
        self.levelJSONDescptionLabel.setObjectName("levelJSONDescptionLabel")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.levelJSONDescptionLabel)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.infoOkBtn = QtWidgets.QPushButton(infoWidget)
        self.infoOkBtn.setObjectName("infoOkBtn")
        self.horizontalLayout.addWidget(self.infoOkBtn)
        self.infoCancelBtn = QtWidgets.QPushButton(infoWidget)
        self.infoCancelBtn.setObjectName("infoCancelBtn")
        self.horizontalLayout.addWidget(self.infoCancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(infoWidget)
        QtCore.QMetaObject.connectSlotsByName(infoWidget)

    def retranslateUi(self, infoWidget):
        _translate = QtCore.QCoreApplication.translate
        infoWidget.setWindowTitle(_translate("infoWidget", "Form"))
        self.songTitleLabel.setText(_translate("infoWidget", "Song Name"))
        self.songSubtitleLabel.setText(_translate("infoWidget", "Song Subtitle"))
        self.songArtistLabel.setText(_translate("infoWidget", "Song Artist Name"))
        self.chartCreatorLabel.setText(_translate("infoWidget", "Chart Creator"))
        self.songAudioOffsetLabel.setText(_translate("infoWidget", "Song Auido Offset"))
        self.songBPMLabel.setText(_translate("infoWidget", "Song BPM"))
        self.previewStartLabel.setText(_translate("infoWidget", "Preview Start Time"))
        self.previewDurLabel.setText(_translate("infoWidget", "Preview Duration"))
        self.enviromentLabel.setText(_translate("infoWidget", "Enviroment"))
        self.audioFileLabel.setText(_translate("infoWidget", "Audio File"))
        self.audioFileSelectBtn.setText(_translate("infoWidget", "Select File"))
        self.coverLabel.setText(_translate("infoWidget", "Cover Image Path"))
        self.coverSelectBtm.setText(_translate("infoWidget", "Select File"))
        self.levelJsonLabel.setText(_translate("infoWidget", "Level JSON Files"))
        self.levelEasyLabel.setText(_translate("infoWidget", "Easy"))
        self.levelEasySelectBtn.setText(_translate("infoWidget", "Select File"))
        self.levelNormalLabel.setText(_translate("infoWidget", "Normal"))
        self.levelNormalSelectBtn.setText(_translate("infoWidget", "Select File"))
        self.levelHardLabel.setText(_translate("infoWidget", "Hard"))
        self.levelHardSelectBtm.setText(_translate("infoWidget", "Select File"))
        self.levelExpertLabel.setText(_translate("infoWidget", "Expert"))
        self.levelExpertSelectBtn.setText(_translate("infoWidget", "Select File"))
        self.levelExpertPlusLabel.setText(_translate("infoWidget", "Expert Plus"))
        self.levelExpertPlusSelectBtn.setText(_translate("infoWidget", "Select File"))
        self.levelJSONDescptionLabel.setText(_translate("infoWidget", "Choose Files for each existing level"))
        self.infoOkBtn.setText(_translate("infoWidget", "OK"))
        self.infoCancelBtn.setText(_translate("infoWidget", "Cancel"))
