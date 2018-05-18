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


from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
    QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
    QButtonGroup, QGridLayout, QAction, QSizePolicy, QFileDialog, QDialog, \
    QGraphicsScene, QGraphicsView, QErrorMessage, QGraphicsScale
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QTransform
from PyQt5.QtCore import QSize,Qt, QRect

graphics_dir = "graphics/"

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
        print(fileName)
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
        self.audioOffsetIn.setValue(song.audioOffset)
        self.BPMIn.setValue(song.beatsPerMinute)
        self.previewStartIn.setValue(song.previewStartTime)
        self.previewDurationIn.setValue(song.previewDuration)
        self.coverImageIn.setText(song.coverImagePath)
        if song.multiAudio:
            self.audioFileIn.setText('Multiple Audio Files Present')
        else:
            self.audioFileIn.setText(song.audioPath)
        self.easyLevelIn.setText(song.jsonFile['Easy'])
        self.normalLevelIn.setText(song.jsonFile['Normal'])
        self.hardLevelIn.setText(song.jsonFile['Hard'])
        self.expertLevelIn.setText(song.jsonFile['Expert'])
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
            self.buttons[name].clicked.connect(self.btnClicked)
            self.buttonGroup.addButton(self.buttons[name])
            layout.addWidget(self.buttons[name], *position)


    def btnClicked(self):
        sender = self.sender()
        print(sender.accessibleName())

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
            self.buttons[name].clicked.connect(self.btnClicked)
            self.buttonGroup.addButton(self.buttons[name])
            layout.addWidget(self.buttons[name])


    def btnClicked(self):
        sender = self.sender()
        print(sender.accessibleName())

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
        self.levelSelectIn.addItem('Expert Plus')
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

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.spectrogramDisplay = False
        self.notewidth=40;

        self.initUI()

    def initUI(self):
        self.editorTheme = self.getTheme()
        self.topLayout=QVBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)


        self.setLayout(self.topLayout)
        self.gs = QGraphicsScene()
        self.gv = QGraphicsView(self.gs)
        self.drawBG()
        if self.spectrogramDisplay:
            self.drawSpectrogram()
        self.drawGrid()

        self.topLayout.addWidget(self.gv)

    def drawSpectrogram(self):
        self.bgImage = self.gs.addPixmap(QPixmap(graphics_dir+'spectrogram.png'))
        scaleBG = QTransform()
        scaleBG.scale(1,2)
        self.bgImage.setTransform(scaleBG)


    def drawBG(self):
        self.gs.setBackgroundBrush(self.editorTheme['BG'])
        self.bgrect = self.gs.addRect(0,0,1000,10000,QPen(Qt.black),self.editorTheme['BG'])


    def drawGrid(self):
        for measure in range(int(10000/160)):
            self.gs.addLine(1,measure*160,159,measure*160,self.editorTheme['GridMeasure'])
            self.gs.addLine(1,measure*160+40,159,measure*160+40,self.editorTheme['Grid4'])
            self.gs.addLine(1,measure*160+80,159,measure*160+80,self.editorTheme['Grid4'])
            self.gs.addLine(1,measure*160+120,159,measure*160+120,self.editorTheme['Grid4'])
            self.gs.addLine(1,measure*160+20,159,measure*160+20,self.editorTheme['Grid8'])
            self.gs.addLine(1,measure*160+60,159,measure*160+60,self.editorTheme['Grid8'])
            self.gs.addLine(1,measure*160+100,159,measure*160+100,self.editorTheme['Grid8'])
            self.gs.addLine(1,measure*160+140,159,measure*160+140,self.editorTheme['Grid8'])
        self.gs.addLine(0,0,0,10000,self.editorTheme['GridLayer1Vert'])
        self.gs.addLine(40,0,40,10000,self.editorTheme['GridLayer1Vert'])
        self.gs.addLine(80,0,80,10000,self.editorTheme['GridLayer1Vert'])
        self.gs.addLine(120,0,120,10000,self.editorTheme['GridLayer1Vert'])
        self.gs.addLine(160,0,160,10000,self.editorTheme['GridLayer1Vert'])

    def getTheme(self):
        return {    'BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridLayer1Vert': QPen(Qt.white,Qt.SolidLine),
                    'GridLayer1BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridLayer2Vert': QPen(Qt.white,Qt.SolidLine),
                    'GridLayer2BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridLayer3Vert': QPen(Qt.white,Qt.SolidLine),
                    'GridLayer3BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridObs': QPen(Qt.blue,Qt.SolidLine),
                    'GridObsBG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridEventVert': QPen(Qt.red,Qt.SolidLine),
                    'GridEventBG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridMeasure': QPen(Qt.red,Qt.SolidLine),
                    'Grid4': QPen(QBrush(Qt.white),1,Qt.DashLine),
                    'Grid8': QPen(QBrush(Qt.blue),1,Qt.DotLine),
                    'Grid12': QPen(Qt.red,Qt.SolidLine),
                    'Grid16': QPen(Qt.red,Qt.SolidLine),
                    'Grid24': QPen(Qt.red,Qt.SolidLine),
                    'Grid32': QPen(Qt.red,Qt.SolidLine),
                    'Grid48': QPen(Qt.red,Qt.SolidLine),
                    'Grid64': QPen(Qt.red,Qt.SolidLine),
                    'Grid192': QPen(Qt.red,Qt.SolidLine),

                    }

class EditorPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.topLayout = QHBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.topLayout)
        self.mainPanel = QSplitter()
        self.levelInfo = LevelInfoPanel()
#        self.levelInfo.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.editor = Editor()
        self.noteInfo = NoteInfoPanel()


        self.mainPanel.addWidget(self.levelInfo)
        self.mainPanel.addWidget(self.editor)
        self.mainPanel.addWidget(self.noteInfo)

        self.mainPanel.setStretchFactor(0,1)
        self.mainPanel.setStretchFactor(1,100)
        self.mainPanel.setStretchFactor(2,1)
        self.topLayout.addWidget(self.mainPanel)

class Song():
    def __init__(self, infoFile):
        self.saved = True
        self.valid = False

        self.loadInfoJson(infoFile)

    def loadInfoJson(self, infoFile):
        self.infoJson ={}
        if infoFile != '':
            print(infoFile)
            try:
                with open (infoFile,'r') as info:
                    self.infoJson = json.load(info)
            except (FileNotFoundError):
                print('info.json not found')
                fileError = QDialog()
                fileErrorLayout = QVBoxLayout()
                fileError.setLayout(fileErrorLayout)
                fileErrorOKBtn = QPushButton('OK')
                fileErrorOKBtn.clicked.connect(fileError.close)
                fileErrorLayout.addWidget(QLabel('info.json not found.'))
                fileErrorLayout.addWidget(fileErrorOKBtn)
                fileError.exec_()
                return
            except (json.decoder.JSONDecodeError):
                print('info.json invalid')
                fileError = QDialog()
                fileErrorLayout = QVBoxLayout()
                fileError.setLayout(fileErrorLayout)
                fileErrorOKBtn = QPushButton('OK')
                fileErrorOKBtn.clicked.connect(fileError.close)
                fileErrorLayout.addWidget(QLabel('info.json Invalid'))
                fileErrorLayout.addWidget(fileErrorOKBtn)
                fileError.exec_()
                return
        if 'songName' in self.infoJson:
            self.songName = self.infoJson['songName']
        else:
            print('Warning: Song name missing')
            self.songName = ''
        if 'songSubName' in self.infoJson:
            self.songSubName = self.infoJson['songSubName']
        else:
            print('Warning: Song  subname missing')
            self.songSubName = ''
        if 'authorName' in self.infoJson:
            self.authorName = self.infoJson['authorName']
        else:
            print('Warning: Song authorName missing')
            self.authorName = ''
        if 'chartAuthor' in self.infoJson:
            self.chartAuthor = self.infoJson['chartAuthor']
        else:
            print('Warning: Song chartAuthor missing')
            self.chartAuthor = ''
        if 'beatsPerMinute' in self.infoJson:
            self.beatsPerMinute = self.infoJson['beatsPerMinute']
        else:
            print('Warning: Song beatsPerMinute missing')
            self.beatsPerMinute = 0.0
        if 'previewStartTime' in self.infoJson:
            self.previewStartTime = self.infoJson['previewStartTime']
        else:
            print('Warning: Song previewStartTime missing')
            self.previewStartTime = 0.0
        if 'previewDuration' in self.infoJson:
            self.previewDuration = self.infoJson['previewDuration']
        else:
            print('Warning: Song previewDuration missing')
            self.previewDuration = 0.0
        if 'coverImagePath' in self.infoJson:
            self.coverImagePath = self.infoJson['coverImagePath']
        else:
            print('Warning: Song coverImagePath missing')
            self.coverImagePath = ''
        if 'environmentName' in self.infoJson:
            self.environmentName = self.infoJson['environmentName']
        else:
            print('Warning: Song environmentName missing')
            self.environmentName = 'DefaultEnvironment'
        if 'offset' in self.infoJson:
            self.audioOffset = self.infoJson['offset']
        else:
            print('Warning: Song Offset missing')
            self.audioOffset = 0.0
        self.jsonFile={}
        self.audioFile={}
        self.levelRank={}
        self.levelExists={}
        if 'difficultyLevels' in self.infoJson:
            for difficulty in self.infoJson['difficultyLevels']:
                self.jsonFile[difficulty['difficulty']]=difficulty['jsonPath']
                self.audioFile[difficulty['difficulty']]=difficulty['audioPath']
                self.levelRank[difficulty['difficulty']]=difficulty['difficultyRank']
                self.levelExists[difficulty['difficulty']]=True

        if 'Easy' not in self.jsonFile.keys():
            self.jsonFile['Easy']=''
            self.audioFile['Easy']=''
            self.levelRank['Easy']=0
            self.levelExists['Easy'] = False
        if 'Normal' not in self.jsonFile.keys():
            self.jsonFile['Normal']=''
            self.audioFile['Normal']=''
            self.levelRank['Normal']=0
            self.levelExists['Normal'] = False
        if 'Hard' not in self.jsonFile.keys():
            self.jsonFile['Hard']=''
            self.audioFile['Hard']=''
            self.levelRank['Hard']=0
            self.levelExists['Hard'] = False
        if 'Expert' not in self.jsonFile.keys():
            self.jsonFile['Expert']=''
            self.audioFile['Expert']=''
            self.levelRank['Expert']=0
            self.levelExists['Expert'] = False
        if 'ExpertPlus' not in self.jsonFile.keys():
            self.jsonFile['ExpertPlus']=''
            self.audioFile['ExpertPlus']=''
            self.levelRank['ExpertPlus']=0
            self.levelExists['ExpertPlus'] = False

        uniqueAudioFiles = []
        for difficulty, audioFile in self.audioFile.items():
            if audioFile not in uniqueAudioFiles and audioFile!='':
                uniqueAudioFiles.append(audioFile)
        print(uniqueAudioFiles)
        if len(uniqueAudioFiles) > 1:
            self.multiAudio = True
        elif len(uniqueAudioFiles)== 1:
            self.multiAudio = False
            self.audioPath = uniqueAudioFiles[0]
        else:
            self.multiAudio = False
            self.audioPath = ''
        self.valid=True

    def saveInfoJson(self, path):
        infoJson = {    'songName':self.songName,
                        'songSubName':self.songSubName,
                        'authorName':self.authorName,
                        'beatsPerMinute':self.beatsPerMinute,
                        'previewStartTime':self.previewStartTime,
                        'previewDuration':self.previewDuration,
                        'coverImagePath':self.coverImagePath,
                        'environmentName':self.environmentName,
                        'difficultyLevels':[]
                    }
        for level in self.levelExists:
            if self.levelExists[level]:
                infoJson['difficultyLevels'].append({   'difficulty':level,
                                                        'difficultyRank':self.levelRank[level],
                                                        'audioPath':self.audioFile[level],
                                                        'jsonPath': self.jsonFile[level]
                                                    })
        print (json.dumps(infoJson))

class CyphusMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.song = Song('')
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
        self.editorTab = EditorPanel()

        self.mainPanel.addTab(self.songInfoTab, 'Song &Info')
        self.mainPanel.addTab(self.editorTab, 'Edi&tor')
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
        QApp.quit()

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
