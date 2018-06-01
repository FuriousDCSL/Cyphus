 # Cyphus: An editor for Beat Saber song charts
 #    Copyright (C) 2018  Joseph Broderick
 #
 #    This program is free software: you can redistribute it and/or modify
 #    it under the terms of the GNU General Public License as published by
 #    the Free Software Foundation, either version 3 of the License, or
 #    (at your option) any later version.
 #
 #    This program is distributed in the hope that it will be useful,
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #    GNU General Public License for more details.
 #
 #    You should have received a copy of the GNU General Public License
 #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 #

import sys
import json
import math
import os.path
import math
from BSEditor import Editor
from Song import Song

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
    QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
    QButtonGroup, QGridLayout, QAction, QSizePolicy, QFileDialog, QDialog, \
    QGraphicsScene, QGraphicsView, QErrorMessage, QGraphicsScale, QGraphicsItem
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QTransform, QColor, QPainter
from PyQt5.QtCore import QSize,Qt, QRect, QPointF, QTimer, pyqtSignal, pyqtSlot

graphics_dir = 'graphics/'
data_dir = 'data/'


class FileTextDialog(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        topLayout=QHBoxLayout()
        topLayout.setContentsMargins(0,0,0,0)
        self.textIn = QLineEdit()
        self.fileDialogIn = QPushButton('...')
        self.fileDialogIn.setFocusPolicy(Qt.ClickFocus)
        self.fileDialogIn.clicked.connect(self.getFile)
        self.fileDialogIn.setMaximumWidth(20)  #DEBUG need to change this to  dynamic instead of static at some point
        topLayout.addWidget(self.textIn,3)
        topLayout.addWidget(self.fileDialogIn,1)
        self.setLayout(topLayout)

    def getFile(self):
        fileName, filter = QFileDialog.getOpenFileName(self,'Select Level File')
        self.textIn.setText(fileName)

    def setText(self,text):
        self.textIn.setText(text)

def MyDoubleSpinBox(min=-100, max=10000, decimals=4):
    doubleSpinbox = QDoubleSpinBox()
    doubleSpinbox.setRange(min,max)
    doubleSpinbox.setDecimals(decimals)

    return doubleSpinbox


class SongInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.environmentList= [   'DefaultEnvironment',
                            'NiceEnvironment',
                            'BigMirrorEnvironment',
                            'TriangleEnvironment',
                            'TutorialEnvironment']

        topLayout=QVBoxLayout()
        self.setLayout(topLayout)
        formLayout = QFormLayout()
        self.songNameIn = QLineEdit()
        formLayout.addRow(QLabel('Song Name'),self.songNameIn)
        self.songSubtitleIn = QLineEdit()
        formLayout.addRow(QLabel('Song Subtitle'),self.songSubtitleIn)
        self.songArtistIn = QLineEdit()
        formLayout.addRow(QLabel('Song Artist'),self.songArtistIn)
        self.songCharterIn = QLineEdit()
        formLayout.addRow(QLabel('Chart Creator'),self.songCharterIn)
        self.audioOffsetIn = MyDoubleSpinBox()


        formLayout.addRow(QLabel('Audio Offset (s)'),self.audioOffsetIn)
        self.BPMIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Display BPM'),self.BPMIn)
        self.previewStartIn = MyDoubleSpinBox()

        formLayout.addRow(QLabel('Preview Start'),self.previewStartIn)
        self.previewDurationIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Preview Duration'),self.previewDurationIn)
        self.environmentIn = QComboBox()
        for environment in self.environmentList:
            self.environmentIn.addItem(environment)
        formLayout.addRow(QLabel('environment'),self.environmentIn)
        self.audioFileIn = FileTextDialog()
        formLayout.addRow(QLabel('Audio File'),self.audioFileIn)
        self.coverImageIn = FileTextDialog()
        formLayout.addRow(QLabel('Cover Image'),self.coverImageIn)
        self.easyLevelIn = FileTextDialog()
        formLayout.addRow(QLabel('Easy'),self.easyLevelIn)
        self.normalLevelIn = FileTextDialog()
        formLayout.addRow(QLabel('Normal'),self.normalLevelIn)
        self.hardLevelIn = FileTextDialog()
        formLayout.addRow(QLabel('Hard'),self.hardLevelIn)
        self.expertLevelIn = FileTextDialog()
        formLayout.addRow(QLabel('Expert'),self.expertLevelIn)
        self.expertPlusLevelIn = FileTextDialog()
        formLayout.addRow(QLabel('Expert Plus'),self.expertPlusLevelIn)

        confirmButtonLayout = QHBoxLayout()
        self.applyBtn = QPushButton('Apply')
        self.revertBtn = QPushButton('Revert')
        confirmButtonLayout.addWidget(self.applyBtn)
        confirmButtonLayout.addWidget(self.revertBtn)

        topLayout.addLayout(formLayout)
        topLayout.addLayout(confirmButtonLayout)

    def update(self, song):
        self.songNameIn.setText(song.songName)
        self.songSubtitleIn.setText(song.songSubName)
        self.songArtistIn.setText(song.authorName)
        self.songCharterIn.setText(song.chartAuthor)
#        #self.audioOffsetIn.setValue(song.audioOffset)
        self.BPMIn.setValue(song.beatsPerMinute)
        self.previewStartIn.setValue(song.previewStartTime)
        self.previewDurationIn.setValue(song.previewDuration)
        self.coverImageIn.setText(song.coverImagePath)
        # if song.multiAudio:
        #     self.audioFileIn.setText('Multiple Audio Files Present')
        # else:
        self.audioFileIn.setText(song.audioFile)
        if 'Easy' in song.jsonFile:
            self.easyLevelIn.setText(song.jsonFile['Easy'])
        if 'Normal' in song.jsonFile:
            self.normalLevelIn.setText(song.jsonFile['Normal'])
        if 'Hard' in song.jsonFile:
            self.hardLevelIn.setText(song.jsonFile['Hard'])
        if 'Expert' in song.jsonFile:
            self.expertLevelIn.setText(song.jsonFile['Expert'])
        if 'ExpertPlus' in song.jsonFile:
            self.expertPlusLevelIn.setText(song.jsonFile['ExpertPlus'])
        if song.environmentName in self.environmentList:
            self.environmentIn.setCurrentIndex(self.environmentList.index(song.environmentName))
        else:
            self.environmentIn.setCurrentIndex(0)


class NoteDirSelectPanel(QWidget): # need to change h size policy to not stretch
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        noteDirNames = [    'downRight', 'down',     'downLeft',
                            'Right',     'circle',   'left',
                            'upRight',   'up',       'upLeft']
        positions = [(i,j) for i in range(3) for j in range(3)]
        self.btnSize = QSize(40,40)

        self.buttons = {}
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        for position, name in zip (positions, noteDirNames):
            if name =='':
                continue
            self.buttons[name] = QPushButton()
            btnIcon = QIcon()
            btnIcon.addPixmap(QPixmap(graphics_dir+name+".png"), QIcon.Normal, QIcon.Off)
            self.buttons[name].setIconSize(QSize(32,32))
            self.buttons[name].setFixedSize(self.btnSize)
            self.buttons[name].setCheckable(True)
            self.buttons[name].setIcon(btnIcon)
            self.buttons[name].setText("")
            self.buttonGroup.addButton(self.buttons[name])
            layout.addWidget(self.buttons[name], *position)



class NoteTypeSelectPanel(QWidget): # need to change h size policy to not stretch
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        noteDirNames = [    'mine', 'red','blue']
        self.btnSize = QSize(40,40)

        self.buttons = {}
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(True)
        for name in noteDirNames:
            if name =='':
                continue
            self.buttons[name] = QPushButton()
            btnIcon = QIcon()
            btnIcon.addPixmap(QPixmap(graphics_dir+name+".png"), QIcon.Normal, QIcon.Off)
            self.buttons[name].setIconSize(QSize(32,32))
            self.buttons[name].setFixedSize(self.btnSize)
            self.buttons[name].setCheckable(True)
            self.buttons[name].setIcon(btnIcon)
            self.buttons[name].setText("")
            self.buttonGroup.addButton(self.buttons[name])
            layout.addWidget(self.buttons[name])



class NoteInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        topLayout = QVBoxLayout()
        self.setLayout(topLayout)

        noteInfoLayout = QFormLayout()
        self.beatIn = MyDoubleSpinBox()
        self.beatIn.setRange(0,10000)
        noteInfoLayout.addRow(QLabel('Beat'),self.beatIn)
        self.timeIn = MyDoubleSpinBox()
        noteInfoLayout.addRow(QLabel('Time (ms)'),self.timeIn)
        self.positionIn = QSpinBox()
        noteInfoLayout.addRow(QLabel('Position'),self.positionIn)
        self.heightIn = QSpinBox()
        noteInfoLayout.addRow(QLabel('Height'),self.heightIn)
        self.noteTypeIn = NoteTypeSelectPanel()
        noteInfoLayout.addRow(QLabel('Note Type'), self.noteTypeIn)
        self.cutDirIn = NoteDirSelectPanel()
        noteInfoLayout.addRow(QLabel('Cut Direction'), self.cutDirIn)

        confirmButtonLayout = QHBoxLayout()
        self.applyBtn = QPushButton('Apply')
        self.revertBtn = QPushButton('Revert')
        confirmButtonLayout.addWidget(self.applyBtn)
        confirmButtonLayout.addWidget(self.revertBtn)

        topLayout.addLayout(noteInfoLayout)
        topLayout.addLayout(confirmButtonLayout)


class LevelInfoPanel(QWidget):
    levelSelectedSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):
        topLayout=QVBoxLayout()
        self.setLayout(topLayout)
        formLayout = QFormLayout()
        self.levelSelectIn = QComboBox()
        self.levelSelectIn.addItem('Easy')
        self.levelSelectIn.addItem('Normal')
        self.levelSelectIn.addItem('Hard')
        self.levelSelectIn.addItem('Expert')
        self.levelSelectIn.addItem('ExpertPlus')
        self.levelSelectIn.currentIndexChanged.connect(self.levelSelected)
        formLayout.addRow(QLabel('Level Select'),self.levelSelectIn)
        formLayout.addRow(QLabel(''))
        self.baseBPMIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Base BPM'),self.baseBPMIn)
        self.audioOffsetIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Audio Offset (s)'),self.audioOffsetIn)
        self.beatsPerBarIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Beats per Bar'),self.beatsPerBarIn)
        self.noteJumpSpeedIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Note Jump Speed'),self.noteJumpSpeedIn)
        self.shuffleIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Shuffle'),self.shuffleIn)
        self.shufflePeriodIn = MyDoubleSpinBox()
        formLayout.addRow(QLabel('Shuffle Period'),self.shufflePeriodIn)
        self.levelFilePathIn = FileTextDialog()
        formLayout.addRow(QLabel('Level File'),self.levelFilePathIn)

        confirmButtonLayout = QHBoxLayout()
        self.applyBtn = QPushButton('Apply')
        self.revertBtn = QPushButton('Revert')
        confirmButtonLayout.addWidget(self.applyBtn)
        confirmButtonLayout.addWidget(self.revertBtn)

        topLayout.addLayout(formLayout)
        topLayout.addLayout(confirmButtonLayout)

    @pyqtSlot()
    def levelSelected(self):
        self.levelSelectedSignal.emit(self.levelSelectIn.currentText())




# class MyGraphicsView(QGraphicsView):
#     def __init__(self,gs):
#         super().__init__(gs)
#
#     def drawForeground(self,painter,x1,y1,x2,y2):
#         painter.drawLine(x1,y1,x2,y2)





class EditorPanel(QWidget):
    def __init__(self,song):
        super().__init__()

        self.initUI(song)

    def initUI(self,song):

        self.topLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.topLayout)
        self.mainPanel = QSplitter()
        self.levelInfo = LevelInfoPanel()
#        self.levelInfo.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        self.editor = Editor(song)
        self.noteInfo = NoteInfoPanel()

        self.levelInfo.levelSelectedSignal.connect(self.editor.levelSelected)

        self.mainPanel.addWidget(self.levelInfo)
        self.mainPanel.addWidget(self.editor)
        self.mainPanel.addWidget(self.noteInfo)

        self.mainPanel.setStretchFactor(0,1)
        self.mainPanel.setStretchFactor(1,100)
        self.mainPanel.setStretchFactor(2,1)
        self.topLayout.addWidget(self.mainPanel)
        self.updateEditorPanel(song)

    def updateEditorPanel(self, song):
        self.editor.update(song,'Expert')



class CyphusMainWindow(QMainWindow):
    songLoaded= pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.song = Song('c:/github/Cyphus/data/info.json')
        self.song.saved = True
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Cyphus")

        self.statusBar()

        self.resize(1900,1000)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QIcon(graphics_dir+'cyphus.png'))

        self.mainPanel = QTabWidget()

        self.songInfoTab = SongInfoPanel()
        self.editorTab = EditorPanel(self.song)

        self.mainPanel.addTab(self.songInfoTab, 'Song &Info')
        self.mainPanel.addTab(self.editorTab, 'Edi&tor')
        self.mainPanel.setCurrentIndex(1)
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        newAct = QAction('&New',self)
        newAct.setShortcut('Ctrl+N')
        #newAct.triggered.connect(self.newSong)
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.triggered.connect(self.openSong)
        saveAct = QAction('&Save',self)
        saveAct.setShortcut('Ctrl+S')
        saveAsAct= QAction('Save &As...',self)
        saveAct.triggered.connect(self.saveSong)
        saveAsAct.setShortcut('Ctrl+Shit+S')
        settingsAct = QAction('Se&ttings',self)
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.quitApp)
        fileMenu.addAction(newAct)
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAct)
        fileMenu.addAction(saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(settingsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)

        selectMenu = menuBar.addMenu('&Edit')
        undoAct = QAction('&Undo', self)
        undoAct.setShortcut('Ctrl+Z')
        redoAct = QAction('&Redo', self)
        redoAct.setShortcut('Ctrl+Y')
        cutAct = QAction('Cu&t', self)
        cutAct.setShortcut('Ctrl+X')
        copyAct = QAction('&Copy', self)
        copyAct.setShortcut('Ctrl+C')
        pasteAct = QAction('&Paste', self)
        pasteAct.setShortcut('Ctrl+V')
        selectAllAct = QAction('Select &All', self)
        selectAllAct.setShortcut('Ctrl+A')
        selectNoneAct = QAction('Select &None', self)
        selectNoneAct.setShortcut('Ctrl+Shift+A')
        selectMenu.addAction(undoAct)
        selectMenu.addAction(redoAct)
        selectMenu.addSeparator()
        selectMenu.addAction(cutAct)
        selectMenu.addAction(copyAct)
        selectMenu.addAction(pasteAct)
        selectMenu.addSeparator()
        selectMenu.addAction(selectAllAct)
        selectMenu.addAction(selectNoneAct)

        helpMenu = menuBar.addMenu('&Help')
        helpAct = QAction('&Help', self)
        helpAct.setShortcut('F1')
        helpAct.triggered.connect(self.helpDialog)
        aboutAct = QAction('&About', self)
        helpMenu.addAction(helpAct)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAct)


        self.setCentralWidget(self.mainPanel)
        self.show()


    def quitApp(self):
        QApplication.quit()

    def helpDialog(self):
        print("HELP!")

    def openSong(self):
        folderName = QFileDialog.getExistingDirectory(self,'Select Song Folder')
        infoFile = folderName + '/info.json'
        if self.song.saved:
            self.songOpen = Song(infoFile)
            if self.songOpen.valid == True:
                self.song = self.songOpen
                self.songInfoTab.update(self.song)
                self.editorTab.updateEditorPanel(self.song)
            else:
                print('INVALID SONG NOT LOADING')

    def saveSong(self):
        self.song.saveInfoJson('')

def main():

    app = QApplication(sys.argv)

    cyphus = CyphusMainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
