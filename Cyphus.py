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
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStyleFactory,\
    QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, \
    QDoubleSpinBox, QSpinBox, QComboBox, QPushButton, QSplitter, QGraphicsView, \
    QButtonGroup, QGridLayout, QAction, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

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
        self.fileDialogIn.setMaximumWidth(20)  #DEBUG need to change this to  dynamic instead of static at some point
        topLayout.addWidget(self.textIn,3)
        topLayout.addWidget(self.fileDialogIn,1)
        self.setLayout(topLayout)


class SongInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        self.audioOffsetIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Audio Offset (s)'),self.audioOffsetIn)
        self.BPMIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Display BPM'),self.BPMIn)
        self.previewStartIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Preview Start'),self.previewStartIn)
        self.previewLengthIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Preview Length'),self.previewLengthIn)
        self.enviromentIn = QComboBox()
        self.enviromentIn.addItem('DefaultEnvironment')
        self.enviromentIn.addItem('NiceEnviroment')
        self.enviromentIn.addItem('BigMirrorEnviroment')
        self.enviromentIn.addItem('TriangleEnviroment')
        self.enviromentIn.addItem('TutorialEnviroment')
        formLayout.addRow(QLabel('Enviroment'),self.enviromentIn)
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
        self.beatIn = QDoubleSpinBox()
        self.beatIn.setRange(0,10000)
        noteInfoLayout.addRow(QLabel('Beat'),self.beatIn)
        self.timeIn = QDoubleSpinBox()
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
        self.baseBPMIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Base BPM'),self.baseBPMIn)
        self.audioOffsetIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Audio Offset (s)'),self.audioOffsetIn)
        self.beatsPerBarIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Beats per Bar'),self.beatsPerBarIn)
        self.noteJumpSpeedIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Note Jump Speed'),self.noteJumpSpeedIn)
        self.shuffleIn = QDoubleSpinBox()
        formLayout.addRow(QLabel('Shuffle'),self.shuffleIn)
        self.shufflePeriodIn = QDoubleSpinBox()
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

        self.initUI()

    def initUI(self):
        self.topLayout=QVBoxLayout()
        self.topLayout.setContentsMargins(0,0,0,0)

        self.setLayout(self.topLayout)
        self.gv = QGraphicsView()
#        self.gv.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.topLayout.addWidget(self.gv)

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

class CyphusMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cyphus")

        self.statusBar()

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QIcon(graphics_dir+'cyphus.png'))

        self.mainPanel = QTabWidget()

        self.songInfoTab = SongInfoPanel()
        self.editorTab = EditorPanel()

        self.mainPanel.addTab(self.songInfoTab, 'Song Info')
        self.mainPanel.addTab(self.editorTab, 'Editor')
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        newAct = QAction('&New',self)
        newAct.setShortcut('Ctrl+N')
        #newAct.triggered.connect(self.newSong)
        openAct = QAction('&Open', self)
        openAct.setShortcut('Ctrl+O')
        saveAct = QAction('&Save',self)
        saveAct.setShortcut('Ctrl+S')
        saveAsAct= QAction('Save &As...',self)
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


def main():

    app = QApplication(sys.argv)

    cyphus = CyphusMainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
