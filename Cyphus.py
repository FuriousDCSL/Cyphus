import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

graphics_dir = "graphics/"

class NoteDirSelectPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        noteDirNames = [    'downRight', 'down',     'downLeft',
                            'Right',     'circle',   'left',
                            'upRight',   'up',       'upLeft']
        positions = [(i,j) for i in range(3) for j in range(3)]
        print(positions)
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

class NoteTypeSelectPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

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
        confirmButtonLayout = QHBoxLayout()
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

        self.applyBtn = QPushButton('Apply')
        self.revertBtn = QPushButton('Revert')
        confirmButtonLayout.addWidget(self.applyBtn)
        confirmButtonLayout.addWidget(self.revertBtn)

        topLayout.addLayout(noteInfoLayout)
        topLayout.addLayout(confirmButtonLayout)

class CyphusMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cyphus")

        self.statusBar()

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        print(self.style().objectName())
        self.setWindowIcon(QIcon(graphics_dir+'cyphus.png'))

        testPanel = QWidget()
        topLayout = QHBoxLayout()
        graphicsView = QGraphicsView()
        noteTypeSel = NoteInfoPanel()
        #topLayout.addWidget(testPanel)
        topLayout.addWidget(graphicsView)
        topLayout.addWidget(noteTypeSel)
        testPanel.setLayout(topLayout)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.quitApp)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        self.setCentralWidget(testPanel)
        self.show()

    def quitApp(self):
        QApp.quit()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    cyphus = CyphusMainWindow()
    sys.exit(app.exec_())
