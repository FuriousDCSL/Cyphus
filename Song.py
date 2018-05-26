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

graphics_dir = "graphics/"

class Level():
    def __init__(self):
        print('level')

class Song():

    def __init__(self, infoFile):
        self.saved = True
        self.valid = False
        self.spectrogramExist = True
        self.isPlaying = False
        self.BPMs=[(0,128)]
        self.startTime =0
        print('loading',infoFile)
        self.loadInfoJson(infoFile)
        self.initSong()

    def secToBeat(self, sec):
        #DEBUG temp stub
        return sec*128/60

    def beatToSec(self, beat):
        self.offset = 0
        seconds = self.offset

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

    def initSong(self):
        print(self.songPath+'/'+self.audioFile['Expert'])
        self.data, self.samplerate = soundfile.read(self.songPath+'/'+self.audioFile['Expert'])
        self.beatsPerBar =4
        MX.quit()
        self.mixer = MX

        print('Sample rate: ',self.samplerate)

        self.mixer.pre_init(self.samplerate, -16, 2, 2048)
        self.mixer.init(self.samplerate)
        self.sound = self.mixer.Sound(self.songPath+'/'+self.audioFile['Expert'])
        self.lengthInSeconds = self.sound.get_length()
        self.lengthInBeats= self.secToBeat(self.lengthInSeconds)
        self.pos =0
        self.music = self.mixer.music.load(self.songPath+'/'+self.audioFile['Expert'])


        if not self.spectrogramExist:
            print ('getting samples')
            samples = SA.array(self.sound)
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


    def getNotes(self,level):
        if '_customEvents' in self.levelsJson[level]:
            self.BPMs =[]
            for event in self.levelsJson[level]['_customEvents']:
                self.variableBPM = True
                if event['_type'] == 0:
                    self.BPMs.append((event['_time'],event['_value']))
        else:
            self.BPMs = [(0,self.levelsJson[level]['_beatsPerMinute'])]
        print(self.BPMs)

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
