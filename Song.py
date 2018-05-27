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

import soundfile
from PIL import Image
from pygame import mixer as MX
from pygame import sndarray as SA
from Level import Level
graphics_dir = "graphics/"


class Song():

    def __init__(self, infoFile):
        self.saved = True
        self.valid = False
        self.spectrogramExist = True
        self.isPlaying = False
        self.BPMs=[]
        self.levels={}
        self.startTime =0
        self.offset =-0.715
        self.initSong(infoFile)


    def initSong(self, infoFile):
        print('Loading Info.json : ',infoFile)
        self.loadInfoJson(infoFile)
        for level in self.levels:
            pass


        self.data, self.samplerate = soundfile.read(self.songPath+'/'+self.audioFile)
        self.beatsPerBar =4
        MX.quit()
        self.mixer = MX

        print('Sample rate: ',self.samplerate)

        self.mixer.pre_init(self.samplerate, -16, 2, 2048)
        self.mixer.init(self.samplerate)
        self.sound = self.mixer.Sound(self.songPath+'/'+self.audioFile)
        self.lengthInSeconds = self.sound.get_length()
        self.lengthInBeats= 1000#self.secToBeat(self.lengthInSeconds)
        self.pos =0
        self.music = self.mixer.music.load(self.songPath+'/'+self.audioFile)


        if not self.spectrogramExist:
            print ('getting samples')
            samples = SA.array(self.sound)
            print('average stereo')
            fade = []
            for sample in samples:
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



    def updatePos(self):
        self.pos =MX.music.get_pos()+self.startTime*1000

    def pauseSong(self):
        self.isPlaying= False
        MX.music.pause()
        #self.updatePos()


    def playSong(self,startTime):
        self.isPlaying = True
        self.startTime = startTime

        MX.music.play(start=startTime)
        self.time = time.time()
        #self.updatePos()




    def loadInfoJson(self, infoFile):
        self.infoJson ={}

        if infoFile != '':
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
        self.levelRank={}
        self.levelExists={}
        self.levelsJson={}
        if 'difficultyLevels' in self.infoJson:
            for difficulty in self.infoJson['difficultyLevels']:
                self.levels[difficulty['difficulty']]=Level(self.songPath, difficulty)
        audioPaths =[]
        for level,data in self.levels.items():
            if data.audioPath not in audioPaths:
                audioPaths.append(data.audioPath)
        if len(audioPaths) >1:
            print('MORE THEN ONE AUDIO FILE NOT SUPPORTED')
            return
        else:
            self.audioFile = audioPaths[0]

        self.valid = True

    # def loadLevelJson(self,path):
    #     self.level = Level()
    #     try:
    #         with open (path,'r') as level:
    #             self.levelJson = json.load(level)
    #     except (FileNotFoundError):
    #         print('level json not found')
    #         fileError = QDialog()
    #         fileErrorLayout = QVBoxLayout()
    #         fileError.setLayout(fileErrorLayout)
    #         fileErrorOKBtn = QPushButton('OK')
    #         fileErrorOKBtn.clicked.connect(fileError.close)
    #         fileErrorLayout.addWidget(QLabel('level json not found.'))
    #         fileErrorLayout.addWidget(fileErrorOKBtn)
    #         fileError.exec_()
    #         return
    #     except (json.decoder.JSONDecodeError):
    #         print('level json invalid')
    #         fileError = QDialog()
    #         fileErrorLayout = QVBoxLayout()
    #         fileError.setLayout(fileErrorLayout)
    #         fileErrorOKBtn = QPushButton('OK')
    #         fileErrorOKBtn.clicked.connect(fileError.close)
    #         fileErrorLayout.addWidget(QLabel('level json Invalid'))
    #         fileErrorLayout.addWidget(fileErrorOKBtn)
    #         fileError.exec_()
    #         return
    #
    #     return self.levelJson

    # def saveInfoJson(self, path):
    #     infoJson = {    'songName':self.songName,
    #                     'songSubName':self.songSubName,
    #                     'authorName':self.authorName,
    #                     'beatsPerMinute':self.beatsPerMinute,
    #                     'previewStartTime':self.previewStartTime,
    #                     'previewDuration':self.previewDuration,
    #                     'coverImagePath':self.coverImagePath,
    #                     'environmentName':self.environmentName,
    #                     'difficultyLevels':[]
    #                 }
    #     for level in self.levelExists:
    #         if self.levelExists[level]:
    #             infoJson['difficultyLevels'].append({   'difficulty':level,
    #                                                     'difficultyRank':self.levelRank[level],
    #                                                     'audioPath':self.audioFile[level],
    #                                                     'jsonPath': self.jsonFile[level]
    #                                                 })
    #     print (json.dumps(infoJson))
