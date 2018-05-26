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
import time
import numpy
import numpy.fft as fft
from scipy import signal
import math

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

    def __init__(self,song):
        super().__init__()

        self.initUI(song)

    def initUI(self,song):
        self.songLenInBeats =100
        self.songBeatsPBar = 4
        self.reverse = 1
        self.pixPSec =400.0
        self.disp8 = True
        self.disp12 = False
        self.disp16 = False
        self.disp24 = False
        self.disp32 = False
        self.disp48 = False
        self.disp64 = False
        self.spectrogramDisplay = True
        self.cursorExists = False
        self.framecount =0
        self.timeOutLength=1

        self.timer = QTimer()
        self.editorTheme = self.getTheme()
        self.boxw = self.editorTheme['BoxWidth']
        self.topLayout=QVBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)

        self.song = song
        self.song.pos =0
        self.setLayout(self.topLayout)
        self.gs = QGraphicsScene()
        self.gv = QGraphicsView(self.gs)
        self.drawBG()
        self.song = song
#        self.drawArrowDemo()
        self.topLayout.addWidget(self.gv)

    def update(self,song):
        self.gs.clear()
        print(self.song.pos)
        self.song = song
        self.cursorExists=False
        self.song.pos = 0
        self.play(0)
        self.pause()
        self.updatescreen()

        if self.spectrogramDisplay:
            self.spectrogramPixMap = QPixmap(graphics_dir+'/spectrogram.png')
            width = self.spectrogramPixMap.width()
            height = self.spectrogramPixMap.height()

            self.spectrogramPixMap = self.gs.addPixmap(self.spectrogramPixMap)
            self.spectrogramPixMap.setRotation(90)
            self.spectrogramPixMap.setTransform(QTransform().scale(-1,(self.song.lengthInSeconds*self.pixPSec)/width))
        self.drawGrid()
        self.drawArrowDemo()
        #self.play(0)

    def play(self, pos):
        self.timer.timeout.connect(self.updatescreen)
        self.timer.start(self.timeOutLength)
        self.song.playSong(pos)

    def pause(self):
        self.timer.stop()
        self.song.pauseSong()

    def keyPressEvent(self, event):
        key = event.key()
        shiftPressed = event.modifiers() == Qt.ShiftModifier
        ctrlPressed = event.modifiers() == Qt.ControlModifier
        altPressed = event.modifiers() == Qt.AltModifier
        restart = self.song.isPlaying

        if key == Qt.Key_Space:
            if self.song.isPlaying:
                self.pause()
            else:
                self.play(self.song.pos/1000)
        elif key == Qt.Key_BracketRight:
            restart = self.song.isPlaying
            self.pause()
            if ctrlPressed:
                self.song.pos+=10000
            elif shiftPressed:
                self.song.pos+=1000
            elif altPressed:
                self.song.pos+=10
            else:
                self.song.pos+=100

            if not(self.song.pos > self.song.lengthInSeconds*1000):
                if restart:
                    self.play(self.song.pos/1000)
                else:
                    self.play(self.song.pos/1000)
                    self.pause()
            else:
                self.song.pos = self.song.lengthInSeconds*1000-1
                self.play(self.song.pos/1000)
                self.pause()
            self.updatescreen()
        elif key == Qt.Key_BracketLeft:
            self.pause()
            if ctrlPressed:
                self.song.pos-=10000
            elif shiftPressed:
                self.song.pos-=1000
            elif altPressed:
                self.song.pos-=10
            else:
                self.song.pos-=100
            if self.song.pos <0:
                self.song.pos =0
            if restart:
                self.play(self.song.pos/1000)
            else:
                self.play(self.song.pos/1000)
                self.pause()
            self.updatescreen()
        elif key == Qt.Key_BraceRight:
            restart = self.song.isPlaying
            self.pause()
            if ctrlPressed:
                self.song.pos+=10000
            elif shiftPressed:
                self.song.pos+=1000
            elif altPressed:
                self.song.pos+=10
            else:
                self.song.pos+=200

            if not(self.song.pos > self.song.lengthInSeconds*1000):
                if restart:
                    self.play(self.song.pos/1000)
                else:
                    self.play(self.song.pos/1000)
                    self.pause()
            else:
                self.song.pos = self.song.lengthInSeconds*1000-1
                self.play(self.song.pos/1000)
                self.pause()

            self.updatescreen()
        elif key == Qt.Key_BraceLeft:
            self.pause()
            if ctrlPressed:
                self.song.pos-=10000
            elif shiftPressed:
                self.song.pos-=1000
            elif altPressed:
                self.song.pos+=10
            else:
                self.song.pos-=200
            if self.song.pos <0:
                self.song.pos =0
            if restart:
                self.play(self.song.pos/1000)
            else:
                self.play(self.song.pos/1000)
                self.pause()

            self.updatescreen()

    def QGraphicsSceneWheelEvent(self, event):
        x = event.angleDelta()
        if x.y() >0:
            self.song.pos+=100
        else:
            self.song.pos -=100



    def updatescreen(self):
        self.song.updatePos()

        # if self.song.isPlaying:
        #     self.framecount+=1
        #     curTime = time.time()
        #     if (curTime-self.song.time >1):
        #         self.framecount =0
        #         self.song.time=curTime


        if self.cursorExists:
            self.gs.removeItem(self.cursorLine)
        ypos = (self.song.pos/1000.0*self.pixPSec)
        self.gv.centerOn(0,ypos)
        self.cursorLine = self.gs.addLine(0,ypos,1000,ypos,self.editorTheme['GridMeasure'])
        self.cursorExists = True
        self.cursor=True
        if self.song.pos <0:
            self.song.pos =0
            self.gv.centerOn(0,0)
            self.pause()


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
            box.setRotation(boxRotation[beatBox['_cutDirection']])
            boxy = (self.vbeatToSec(beatBox['_time'])*self.pixPSec-(self.reverse*20))*self.reverse

            boxx = 40*beatBox['_lineIndex']+170*beatBox['_lineLayer']
            box.setPos(boxx,boxy)


    def drawBG(self):
        self.gs.setBackgroundBrush(self.editorTheme['BG'])

    def secPerBeat(self, bpm):
        return 60.0/bpm

    def vbeatToSec(self, beat):
        self.offset = 0
        seconds = self.offset

        if True:
            j=  self.secPerBeat(self.song.beatsPerMinute)*beat
            return j
        else:
            return self.beatToSec(self.bpm)

    def beatToSec(self, beat):
        self.offset = 0
        seconds = self.offset

        bpmLength =[]
        numBPMS = len(self.song.BPMs)
        if numBPMS >1:
            for i in range(len(self.song.BPMs)-1):
                bpmLength.append(self.song.BPMs[i+1][0]-self.song.BPMs[i][0])
            bpmLength.append(self.song.lengthInBeats-self.song.BPMs[i+1][0])

            for i in range (len(bpmLength)-1):
                if beat >= self.song.BPMs[i+1][0]:
                    seconds += self.secPerBeat(self.song.BPMs[i][1])*bpmLength[i]
                elif beat >= self.song.BPMs[i][0] and beat < self.song.BPMs[i+1][0]:
                    seconds += self.secPerBeat(self.song.BPMs[i][1])*(beat - self.song.BPMs[i][0])

        if beat >= self.song.BPMs[-1][0]:
            seconds += self.secPerBeat(self.song.BPMs[-1][1]) * (beat -self.song.BPMs[-1][0])
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
        for beat in range(int(self.song.lengthInBeats)):
            if beat % self.song.beatsPerBar == 0:
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
        lane.addToGroup(self.gs.addLine(values.x,values.y,values.x,self.reverse*self.beatToSec(self.song.lengthInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.25,values.y,values.x+values.w*.25,self.reverse*self.beatToSec(self.song.lengthInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.5,values.y,values.x+values.w*.5,self.reverse*self.beatToSec(self.song.lengthInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w*.75,values.y,values.x+values.w*.75,self.reverse*self.beatToSec(self.song.lengthInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))
        lane.addToGroup(self.gs.addLine(values.x+values.w,values.y,values.x+values.w,self.reverse*self.beatToSec(self.song.lengthInBeats)*self.pixPSec,self.editorTheme['GridLayer1Vert']))


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
