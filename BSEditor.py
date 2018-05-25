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
import pydub
import soundfile

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
   QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
   QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
   QButtonGroup, QGridLayout, QAction, QSizePolicy, QFileDialog, QDialog, \
   QGraphicsScene, QGraphicsView, QErrorMessage, QGraphicsScale, QGraphicsItem, \
   QStackedLayout
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QTransform, QColor, QPainter
from PyQt5.QtCore import QSize,Qt, QRect, QRectF, QPointF, QTimer, pyqtSignal, pyqtSlot

graphics_dir = "graphics/"

class LayerValue():
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.w = width

# class MyGraphicsView(QGraphicsView):
#     def __init__(self,graphicsScene):
#         super().__init__(graphicsScene)
#
#     def drawForeground(self,x,y):
#         foreground = QPainter()
#         foreground.
#         foreground.setPen(QPen(Qt.white,10,Qt.SolidLine))
#         foreground.drawLine(0,300,800,300)
#         QGraphicsView.drawForeground(self,x,y)
#         self.viewport().update()

class Editor(QWidget):
    songLenInBeats =100
    songBeatsPBar = 4
    reverse = 1
    pixPSec =400.0
    disp8 = True
    disp12 = False
    disp16 = False
    disp24 = False
    disp32 = False
    disp48 = False
    disp64 = False
    spectrogramDisplay = True
    spectrogramExist = False
    songPlaying = False
    cursorExists = False

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.editorTheme = self.getTheme()
        self.boxw = self.editorTheme['BoxWidth']
        self.topLayout=QVBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)

        self.timer= QTimer()
        self.songPos =0
        self.setLayout(self.topLayout)
        self.gs = QGraphicsScene()
        self.gv = QGraphicsView(self.gs)
        self.drawBG()

#        self.drawArrowDemo()

        self.topLayout.addWidget(self.gv)

    def update(self,song):
        self.song = song

        self.data, self.samplerate = soundfile.read(self.song.songPath+'/'+self.song.audioFile['Expert'])

        print (self.samplerate)
        self.mixer = MX
        self.mixer.pre_init(self.samplerate, -16, 2, 2048)
        self.mixer.init()
        self.songSound = self.mixer.Sound(self.song.songPath+'/'+self.song.audioFile['Expert'])
        self.songLenInSecs = self.songSound.get_length()
        self.songLenInBeats = self.secToBeat(self.songLenInSecs)
        self.songPos =0
        if '_customEvents' in self.song.levelsJson['Expert']:
            self.songBPMs =[]
            for event in self.song.levelsJson['Expert']['_customEvents']:
                self.variableBPM = True
                if event['_type'] == 0:
                    self.songBPMs.append((event['_time'],event['_value']))
        else:
            self.songBPMs = [(0,self.song.levelsJson['Expert']['_beatsPerMinute'])]
        print(self.songBPMs)

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
            print(width,self.songLenInSecs,self.pixPSec)
            self.spectrogramPixMap.setTransform(QTransform().scale(-1,(self.songLenInSecs*self.pixPSec)/width))
        self.drawGrid()
        self.drawArrowDemo()
        #self.playSong(0)
        self.time = time.time()

    def keyPressEvent(self, event):
        key = event.key()
        shiftPressed = event.modifiers() == Qt.ShiftModifier
        ctrlPressed = event.modifiers() == Qt.ControlModifier
        restart = self.songPlaying
        print(shiftPressed)

        if key == Qt.Key_Space:
            if self.songPlaying:
                self.pauseSong()
            else:
                self.playSong(self.songPos/1000)
                print(self.songPos/1000)
        elif key == Qt.Key_BracketRight:
            restart = self.songPlaying
            self.pauseSong()
            if ctrlPressed:
                self.songPos+=10000
            elif shiftPressed:
                self.songPos+=1000
            else:
                self.songPos+=200

            if not(self.songPos > self.songLenInSecs*1000):
                if restart:
                    self.playSong(self.songPos/1000)
            else:
                self.songPos = self.songLenInSecs*1000-1
            self.updatescreen()
        elif key == Qt.Key_BracketLeft:
            self.pauseSong()
            if ctrlPressed:
                self.songPos-=10000
            elif shiftPressed:
                self.songPos-=1000
            else:
                self.songPos-=200
            if self.songPos <0:
                self.songPos =0
            if restart:
                self.playSong(self.songPos/1000)
            self.updatescreen()
        elif key == Qt.Key_BraceRight:
            restart = self.songPlaying
            self.pauseSong()
            if ctrlPressed:
                self.songPos+=10000
            elif shiftPressed:
                self.songPos+=1000
            else:
                self.songPos+=200

            if not(self.songPos > self.songLenInSecs*1000):
                if restart:
                    self.playSong(self.songPos/1000)
            else:
                self.songPos = self.songLenInSecs*1000-1
            self.updatescreen()
        elif key == Qt.Key_BraceLeft:
            self.pauseSong()
            if ctrlPressed:
                self.songPos-=10000
            elif shiftPressed:
                self.songPos-=1000
            else:
                self.songPos-=200
            if self.songPos <0:
                self.songPos =0
            if restart:
                self.playSong(self.songPos/1000)
            self.updatescreen()

    def QGraphicsSceneWheelEvent(self, event):
        x = event.angleDelta()
        print(x.y(), 'wheelEvent')
        if x.y() >0:
            self.songPos+=100
        else:
            self.songPos -=100


    def pauseSong(self):
        self.songPlaying= False
        MX.music.pause()
        self.timer.stop()
        print(self.songPos/1000)


    def playSong(self,startTime):
        print("PLAYING!")
        self.songPlaying = True
        self.startTime = startTime

        self.timer.timeout.connect(self.updatescreen)
        self.timer.start(1)
        self.songMusic = self.mixer.music.load(self.song.songPath+'/'+self.song.audioFile['Expert'])
        MX.music.play(start=startTime)
        self.framecount =0
        self.time = time.time()

    def updatescreen(self):
        if self.songPlaying:
            self.songPos = MX.music.get_pos()+self.startTime*1000
            self.framecount+=1
            curTime = time.time()
            if (curTime-self.time >1):
    #            print(self.framecount)
                self.framecount =0
                self.time=curTime


        if self.cursorExists:
            self.gs.removeItem(self.cursorLine)
        ypos = (self.songPos/1000.0*self.pixPSec)
        self.gv.centerOn(0,ypos)
        self.cursorLine = self.gs.addLine(0,ypos,1000,ypos,self.editorTheme['GridMeasure'])
        self.cursorExists = True
        self.cursor=True
        if self.songPos <0:
            self.songPos =0
            self.gv.centerOn(0,0)
            self.pauseSong()


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
            boxy = (self.vbeatToSec(beatBox['_time'])*self.pixPSec-(self.reverse*20))*self.reverse

            boxx = 40*beatBox['_lineIndex']+170*beatBox['_lineLayer']
            #print(boxx,boxy)
            box.setPos(boxx,boxy)


    def drawBG(self):
        self.gs.setBackgroundBrush(self.editorTheme['BG'])

    def secPerBeat(self, bpm):
        return 60.0/bpm

    def vbeatToSec(self, beat):
        self.offset = 0
        seconds = self.offset

        #if self.variableBPM:
        if True:
            #JKL
            #print('variable')
            j=  self.secPerBeat(self.song.beatsPerMinute)*beat
            return j
        else:
            return self.beatToSec(self.bpm)

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
        return {    'BoxWidth': 60,
                    'LaneSpacing': 20,
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
