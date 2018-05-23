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
from pygame import mixer as MX
from pygame import sndarray as SA
import time
import numpy
import numpy.fft as fft
from scipy import signal
import math
from PIL import Image

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
    QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
    QButtonGroup, QGridLayout, QAction, QSizePolicy, QFileDialog, QDialog, \
    QGraphicsScene, QGraphicsView, QErrorMessage, QGraphicsScale, QGraphicsItem
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QTransform, QColor, QPainter
from PyQt5.QtCore import QSize,Qt, QRect, QPointF, QTimer, pyqtSignal, pyqtSlot

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
        #print(fileName)
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


class LayerValue():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.w = width

# class MyGraphicsView(QGraphicsView):
#     def __init__(self,gs):
#         super().__init__(gs)
#
#     def drawForeground(self,painter,x1,y1,x2,y2):
#         painter.drawLine(x1,y1,x2,y2)





class Editor(QWidget):
    songLenInBeats =100
    songBeatsPBar = 4
    reverse = 1
#    songBPMs=[(0.000,80.000),(4.000,80.000),(36.000,100.000),(68.000,120.000),(100.000,140.010),(132.000,160.000),(164.000,180.000)]
    songBPMs=[(0,128)]
    pixPSec = 600
    disp8 = True
    disp12 = False
    disp16 = False
    disp24 = False
    disp32 = False
    disp48 = False
    disp64 = False
    spectrogramDisplay = True
    spectrogramExist = True
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.editorTheme = self.getTheme()
        self.boxw = self.editorTheme['BoxWidth']
        self.topLayout=QVBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)


        self.setLayout(self.topLayout)
        self.gs = QGraphicsScene()
        self.gv = QGraphicsView(self.gs)
        self.drawBG()
#        self.drawArrowDemo()
        self.topLayout.addWidget(self.gv)

    def update(self,song):
        self.song = song
        self.mixer = MX
        self.mixer.init(48000)

        self.songSound = self.mixer.Sound(self.song.songPath+'/'+self.song.audioFile['Expert'])
        self.songLenInSecs = self.songSound.get_length()
        self.songLenInBeats = self.secToBeat(self.songLenInSecs)



        if not self.spectrogramExist:
            print ('getting samples')
            samples = SA.array(self.songSound)
            print('average stereo')
            fade = []
            for sample in samples:
                #print(sample[0],sample[1])
                fade.append((int(sample[0])+int(sample[1]))/2.0)
            fade = numpy.asarray(fade)
            print('fft')
            f, t, Sxx = signal.spectrogram(fade,48000,nperseg=256,nfft=2048)

            print('coloring')
            data = []
            colormax =255
            map = []
            j = colorscale =256
            k=j/2
            for i in range(colorscale):
                red = colormax - (i/colorscale*colormax)
                if i<k:
                    green = (i/colorscale*colormax)
                else:
                    green = (j/colorscale*colormax)
                blue = (i/colorscale*colormax)
                j-=1
                alpha = 100
                map.append((int(blue),int(red),int(green),alpha))
            j = 255
            while j>0:
                j-=15
                map.append((0,0,j))
            for s in Sxx:
                for d in (s.tolist()):
                    if d>4000:
                        data.append(map[0])
                    elif d == 0:
                        data.append(map[-1])
                    else:
                        data.append(map[int((len(map)-(d/4000*len(map)))-1)])
            print ('Creating Pixmap')
            im = Image.new('RGBA',(len(t),len(f)))
            im.putdata(data)
            im.save(graphics_dir+'/spectrogram.png')
        if self.spectrogramDisplay:
            self.spectrogramPixMap = QPixmap(graphics_dir+'/spectrogram.png')
            width = self.spectrogramPixMap.width()
            height = self.spectrogramPixMap.height()

            self.spectrogramPixMap = self.gs.addPixmap(self.spectrogramPixMap)
            self.spectrogramPixMap.setRotation(90)
            self.spectrogramPixMap.setTransform(QTransform().scale(-1,self.songLenInSecs*self.pixPSec/width))
        self.drawGrid()
        self.drawArrowDemo()
        #self.gv.setSceneRect(0,0,1000,-10000)
        self.gv.verticalScrollBar().setSliderPosition(100)
        self.fullScene =self.gv.sceneRect()
        self.gv.setSceneRect(self.fullScene)
        self.timer= QTimer()
        self.timer.timeout.connect(self.movescreen)
        self.timer.start(1)
        self.songMusic = self.mixer.music.load(self.song.songPath+'/'+self.song.audioFile['Expert'])
        MX.music.play()
        self.cursor = False
    def movescreen(self):
        #print('movescreen',self.playTime*self.pixPSec)
        pos = MX.music.get_pos()
        curpos=400
        #print(pos
        if self.cursor:
            self.gs.removeItem(self.cursorLine)
        self.gv.setSceneRect(0,(pos/1000*self.pixPSec)-curpos,1000,1000)
        self.cursorLine = self.gs.addLine(0,(pos/1000*self.pixPSec),1000,(pos/1000*self.pixPSec),self.editorTheme['GridMeasure'])
        self.cursor=True
    def drawArrowDemo(self):

        boxRotation=[180,0,90,270,225,135,315,45,0]

        for beatBox in self.song.levelsJson['Expert']['_notes']:
            if beatBox['_type']==0:
                if beatBox['_cutDirection']==8:
                    notePixmap = QPixmap(graphics_dir+'redcircle.png')
                else:
                    notePixmap = QPixmap(graphics_dir+'redarrow.png')
            elif beatBox['_type']==1:
                if beatBox['_cutDirection']==8:
                    notePixmap = QPixmap(graphics_dir+'bluecircle.png')
                else:
                    notePixmap = QPixmap(graphics_dir+'bluearrow.png')
            else:
                notePixmap =QPixmap(graphics_dir+'mine.png')

            notePixmap = notePixmap.scaled(40,40)
            box = self.gs.addPixmap(notePixmap)

            box.setTransformOriginPoint(20,20)
            #print(beatBox['_cutDirection'])
            box.setRotation(boxRotation[beatBox['_cutDirection']])
            boxy = (self.beatToSec(beatBox['_time'])*self.pixPSec-(self.reverse*20))*self.reverse

            boxx = 40*beatBox['_lineIndex']+170*beatBox['_lineLayer']
            #print(boxx,boxy)
            box.setPos(boxx,boxy)


    def drawBG(self):
        self.gs.setBackgroundBrush(self.editorTheme['BG'])

    def secPerBeat(self, bpm):
        return 60.0/bpm

    def beatToSec(self, beat):
        self.offset = 0
        seconds = self.offset

        bpmLength =[]
        numBPMS = len(self.songBPMs)
        if numBPMS >1:
            for i in range(len(self.songBPMs)-1):
                bpmLength.append(self.songBPMs[i+1][0]-self.songBPMs[i][0])
            bpmLength.append(self.songLenInBeats-self.songBPMs[i+1][0])

            for i in range (len(bpmLength)-1):
                if beat >= self.songBPMs[i+1][0]:
                    seconds += self.secPerBeat(self.songBPMs[i][1])*bpmLength[i]
                elif beat >= self.songBPMs[i][0] and beat < self.songBPMs[i+1][0]:
                    seconds += self.secPerBeat(self.songBPMs[i][1])*(beat - self.songBPMs[i][0])

        if beat >= self.songBPMs[-1][0]:
            seconds += self.secPerBeat(self.songBPMs[-1][1]) * (beat -self.songBPMs[-1][0])

        return seconds


    def secToBeat(self, sec):
        #DEBUG temp stub
        return sec*128/60

    def drawGrid(self):
        #DEBUG need to through a clear grid in here

        self.drawGridConstantTime()

    def drawGridConstantBeat(self):
        pass
    def drawGridConstantTime(self):

        # DONT FORGET TO ADD REVERSE SCROLL

#        self.disp192 = True
        #print(self.beatToSec(self.songLenInBeats))
        self.noteLayer1 = self.gs.createItemGroup([])
        self.noteLayer2 = self.gs.createItemGroup([])
        self.noteLayer3 = self.gs.createItemGroup([])
        self.obstacleLayer = self.gs.createItemGroup([])
        self.eventLayer = self.gs.createItemGroup([])
        width = self.editorTheme['BoxWidth']*4
        spacing = self.editorTheme['LaneSpacing']
        self.noteLayer1Values = LayerValue(0,0,width)
        self.noteLayer2Values = LayerValue((width+spacing),0,width)
        self.noteLayer3Values = LayerValue((width+spacing)*2,0,width)
        self.obstacleLayerValues = LayerValue((width+spacing)*3,0,width)
        self.eventLayerValues = LayerValue((width+spacing)*4,0,width)

        self.drawGridLaneConstantTime(self.noteLayer1,self.noteLayer1Values)
        self.drawGridLaneConstantTime(self.noteLayer2,self.noteLayer2Values)
        self.drawGridLaneConstantTime(self.noteLayer3,self.noteLayer3Values)
        self.drawGridLaneConstantTime(self.obstacleLayer,self.obstacleLayerValues)
        self.drawGridLaneConstantTime(self.eventLayer,self.eventLayerValues)

    def drawGridLaneConstantTime(self, lane, values):
        #debug songlen not a int need to address leftover time
        for beat in range(int(self.songLenInBeats)):
            #print(beat,self.reverse*self.beatToSec(beat),self.reverse*self.beatToSec(beat)*self.pixPSec)
            if beat % self.songBeatsPBar == 0:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat)*self.pixPSec,self.editorTheme['GridMeasure']))
            else:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat)*self.pixPSec,self.editorTheme['Grid4']))
            if self.disp8:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.5)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.5)*self.pixPSec,self.editorTheme['Grid8']))
            if self.disp16:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.25)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.25)*self.pixPSec,self.editorTheme['Grid16']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.75)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.75)*self.pixPSec,self.editorTheme['Grid16']))
            if self.disp32:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.125)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.125)*self.pixPSec,self.editorTheme['Grid32']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.375)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.375)*self.pixPSec,self.editorTheme['Grid32']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.625)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.625)*self.pixPSec,self.editorTheme['Grid32']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.875)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.875)*self.pixPSec,self.editorTheme['Grid32']))
            if self.disp64:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.0625)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.0625)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.1875)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.1875)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.3125)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.3125)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.4375)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.4375)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.5625)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.5625)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.6875)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.6875)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.8125)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.8125)*self.pixPSec,self.editorTheme['Grid64']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.9375)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.9375)*self.pixPSec,self.editorTheme['Grid64']))
            if self.disp12:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+1/3)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+1/3)*self.pixPSec,self.editorTheme['Grid12']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+2/3)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+2/3)*self.pixPSec,self.editorTheme['Grid12']))
            if self.disp24:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+1/6)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+1/6)*self.pixPSec,self.editorTheme['Grid24']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.5)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.5)*self.pixPSec,self.editorTheme['Grid24']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+5/6)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+5/6)*self.pixPSec,self.editorTheme['Grid24']))
            if self.disp48:
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+1/12)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+1/12)*self.pixPSec,self.editorTheme['Grid48']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.25)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.25)*self.pixPSec,self.editorTheme['Grid48']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+5/12)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+5/12)*self.pixPSec,self.editorTheme['Grid48']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+7/12)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+7/12)*self.pixPSec,self.editorTheme['Grid48']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+.75)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+.75)*self.pixPSec,self.editorTheme['Grid48']))
                lane.addToGroup(self.gs.addLine(values.x+self.editorTheme['GridLineWidth'],self.reverse*self.beatToSec(beat+11/12)*self.pixPSec,values.x+values.w-self.editorTheme['GridLineWidth']*2,self.reverse*self.beatToSec(beat+11/12)*self.pixPSec,self.editorTheme['Grid48']))
        lane.addToGroup(self.gs.addLine(values.x,values.y,values.x,self.reverse*self.beatToSec(self.songLenInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.25,values.y,values.x+values.w*.25,self.reverse*self.beatToSec(self.songLenInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.5,values.y,values.x+values.w*.5,self.reverse*self.beatToSec(self.songLenInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.75,values.y,values.x+values.w*.75,self.reverse*self.beatToSec(self.songLenInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w,values.y,values.x+values.w,self.reverse*self.beatToSec(self.songLenInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))


    def getTheme(self):
        return {    'BoxWidth': 40,
                    'LaneSpacing': 10,
                    'BG': QBrush(QColor(0,0,0),Qt.SolidPattern),
                    'GridLayer1Vert': QPen(QBrush(QColor(255,255,255)),1,Qt.SolidLine),
                    'GridLayer1BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridLayer2Vert': QPen(Qt.white,Qt.SolidLine),
                    'GridLayer2BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridLayer3Vert': QPen(Qt.white,Qt.SolidLine),
                    'GridLayer3BG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridObs': QPen(Qt.blue,Qt.SolidLine),
                    'GridObsBG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridEventVert': QPen(Qt.red,Qt.SolidLine),
                    'GridEventBG': QBrush(Qt.black,Qt.SolidPattern),
                    'GridMeasure': QPen(QBrush(QColor(255,0,0)),1,Qt.SolidLine),
                    'Grid4': QPen(QBrush(QColor(255,255,255)),1,Qt.DashLine),
                    'Grid8': QPen(QBrush(QColor(0,150,255)),1,Qt.DotLine),
                    'Grid12': QPen(QBrush(QColor(100,255,50)),1,Qt.DotLine),
                    'Grid16': QPen(QBrush(QColor(255,255,50)),1,Qt.DotLine),
                    'Grid24': QPen(QBrush(QColor(150,100,255)),1,Qt.DotLine),
                    'Grid32': QPen(QBrush(QColor(0,255,150)),1,Qt.DotLine),
                    'Grid48': QPen(QBrush(QColor(255,100,150)),1,Qt.DotLine),
                    'Grid64': QPen(QBrush(QColor(150,200,100)),1,Qt.DotLine),
#                    'Grid192': QPen(Qt.red,Qt.SolidLine),
                    'GridLineWidth': 1
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

    def update(self, song):
        self.editor.update(song)

class Level():
    def __init__(self):
        print('level')

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
        self.songPath = os.path.dirname(infoFile)
        print (self.songPath)
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

        self.loadedKeys = ['songName', 'songSubName', 'authorName','chartAuthor','beatsPerMinute','previewStartTime','previewDuration','coverImagePath','environmentName','offset','difficultyLevels']

        self.extraKeys=[]
        for key in self.infoJson:
            if key not in self.loadedKeys:
                self.extraKeys.append((key,self.infoJson[key]))
        print ("extra keys",self.extraKeys)
        self.jsonFile={}
        self.audioFile={}
        self.levelRank={}
        self.levelExists={}
        self.levelsJson={}
        if 'difficultyLevels' in self.infoJson:
            for difficulty in self.infoJson['difficultyLevels']:
                self.jsonFile[difficulty['difficulty']]=difficulty['jsonPath']
                self.levelsJson[difficulty['difficulty']] = self.loadLevelJson(self.songPath+'/'+difficulty['jsonPath'])
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

        #print(self.levelsJson)

        # DEBUG this needs to be fixed, this will probably break.
        uniqueAudioFiles = []
        for difficulty, audioFile in self.audioFile.items():
            if audioFile not in uniqueAudioFiles and audioFile!='':
                uniqueAudioFiles.append(audioFile)
        #print(uniqueAudioFiles)
        if len(uniqueAudioFiles) > 1:
            self.multiAudio = True
        elif len(uniqueAudioFiles)== 1:
            self.multiAudio = False
            self.audioPath = uniqueAudioFiles[0]
        else:
            self.multiAudio = False
            self.audioPath = ''
        self.valid=True


    def loadLevelJson(self,path):
        self.level = Level()
        print(path)
        try:
            with open (path,'r') as level:
                self.levelJson = json.load(level)
        except (FileNotFoundError):
            print('level json not found')
            fileError = QDialog()
            fileErrorLayout = QVBoxLayout()
            fileError.setLayout(fileErrorLayout)
            fileErrorOKBtn = QPushButton('OK')
            fileErrorOKBtn.clicked.connect(fileError.close)
            fileErrorLayout.addWidget(QLabel('level json not found.'))
            fileErrorLayout.addWidget(fileErrorOKBtn)
            fileError.exec_()
            return
        except (json.decoder.JSONDecodeError):
            print('level json invalid')
            fileError = QDialog()
            fileErrorLayout = QVBoxLayout()
            fileError.setLayout(fileErrorLayout)
            fileErrorOKBtn = QPushButton('OK')
            fileErrorOKBtn.clicked.connect(fileError.close)
            fileErrorLayout.addWidget(QLabel('level json Invalid'))
            fileErrorLayout.addWidget(fileErrorOKBtn)
            fileError.exec_()
            return

        return self.levelJson

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
    songLoaded= pyqtSignal(object)

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
                self.editorTab.update(self.song)
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
