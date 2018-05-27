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

from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
    QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
    QButtonGroup, QGridLayout, QAction, QSizePolicy, QFileDialog, QDialog, \
    QGraphicsScene, QGraphicsView, QErrorMessage, QGraphicsScale, QGraphicsItem
from PyQt5.QtGui import QIcon, QPixmap, QPen, QBrush, QTransform, QColor, QPainter
from PyQt5.QtCore import QSize,Qt, QRect, QPointF, pyqtSignal, pyqtSlot

graphics_dir = "graphics/"


class Note():
    def __init__(self, noteJson):
        self.time = noteJson['_time']
        self.lineIndex = noteJson['_lineIndex']
        self.lineLayer = noteJson['_lineLayer']
        self.type = noteJson['_type']
        self.cutDirection = noteJson['_cutDirection']

class EnvEvent():
    def __init__(self, envEventJson):
        pass

class CustomEvent():
    def __init__(self, envEventJson):
        pass

class Obstacle():
    def __init__(self, obstacleJson):
        pass

class Level():
    def __init__(self,path,level):
        self.path = path
        self.difficulty = level['difficulty']
        self.difficultyRank = level['difficultyRank']
        self.audioPath = level['audioPath']
        self.jsonPath = level['jsonPath']

        self.parseLevelJson()

    def parseLevelJson(self):
        #DEBUG need to add validation
        print(self.path+'/'+self.jsonPath)
        with open(self.path+'/'+self.jsonPath,'r') as jsonFile:
            self.levelJson = json.load(jsonFile)
        self.BPMs =[]
        self.levelVersion = self.levelJson['_version']
        self.baseBPM =   self.levelJson['_beatsPerMinute']
        self.beatsPerBar = self.levelJson['_beatsPerBar']
        self.noteJumpSpeed = self.levelJson['_noteJumpSpeed']
        self.shuffle = self.levelJson['_shuffle']
        self.shufflePeriod = self.levelJson['_shufflePeriod']
        self.eventsJson = self.levelJson['_events']
        self.notesJson = self.levelJson['_notes']
        self.obstaclesJson = self.levelJson['_obstacles']
        if 'customEvents' in self.levelJson:
            self.customJson = self.levelJson['_customEvents']
        else:
            self.BPMs =[(0,self.baseBPM)]
            self.customJson =[]

        self.notes =[]
        self.envEvents =[]
        self.obstacles =[]
        for note in self.notesJson:
            self.notes.append(Note(note))
        for customEvent in self.customJson:
            self.variableBPM = True
            if customEvent['_type'] == 0:
                self.BPMs.append((customEvent['_time'],customEvent['_value']))
        print(self.BPMs)


    def secToBeat(self, sec):
        #DEBUG temp stub
        return sec*128/60

    def beatToSec(self, beat):
        seconds = 0

        bpmLength =[]
        numBPMS = len(self.BPMs)
        if numBPMS >1:
            for i in range(len(self.BPMs)-1):
                bpmLength.append(self.BPMs[i+1][0]-self.BPMs[i][0])
            bpmLength.append(self.lengthInBeats-self.BPMs[i+1][0])

            for i in range (len(bpmLength)-1):
                if beat >= self.BPMs[i+1][0]:
                    seconds += self.secPerBeat(self.BPMs[i][1])*bpmLength[i]
                elif beat >= self.BPMs[i][0] and beat < self.BPMs[i+1][0]:
                    seconds += self.secPerBeat(self.BPMs[i][1])*(beat - self.BPMs[i][0])

        if beat >= self.BPMs[-1][0]:
            seconds += self.secPerBeat(self.BPMs[-1][1]) * (beat -self.BPMs[-1][0])
        return seconds


    def secPerBeat(self, bpm):
        return 60.0/bpm
