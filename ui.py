#!/usr/bin/python3.7
# Filename: ui.py

__version__ = '0.3'
__author__ = 'Alessio Deidda / Cecilia Baggini'

import sys
import os

import style
import functions
import cv2

# PyQt5 packages
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QSlider, QStyle, QFileDialog

#######################################################################
class VideoStream(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1024, 512, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.wait()




#######################################################################
class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setFixedSize(1280, 720)  # use variables
        #self.setCursor(Qt.BlankCursor)
        #self.showFullScreen()
        self.setStyleSheet(style.playerWindow)

        #########
        hlay = QHBoxLayout(self)
        self.treeview = QTreeView()

        self.listview = QListView()
        hlay.addWidget(self.treeview)
        hlay.addWidget(self.listview)

        path = QDir.rootPath()

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.currentPath('Users/Alex/Music'))
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)

        self.treeview.setModel(self.dirModel)
        self.listview.setModel(self.fileModel)

        self.treeview.setRootIndex(self.dirModel.index(path))
        self.listview.setRootIndex(self.fileModel.index(path))

        self.treeview.clicked.connect(self.on_clicked)
        #self.listview.clicked.connect(self.open_file)

        #######

        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        #create videowidget object
        videowidget = QVideoWidget()

        #create open button
        #openBtn = QPushButton('Open Video')
        #openBtn.clicked.connect(self.open_file)

        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        #create slider
        #self.slider = QSlider(Qt.Horizontal)
        #self.slider.setRange(0,0)
        #self.slider.sliderMoved.connect(self.set_position)

        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        #create hbox layout
        #hboxLayout = QHBoxLayout()
        #hboxLayout.setContentsMargins(0,0,0,0)

        #set widgets to the hbox layout
        #hboxLayout.addWidget(openBtn)
        #hboxLayout.addWidget(self.playBtn)
        #hboxLayout.addWidget(self.slider)

        #hlay.addWidget(openBtn)
        hlay.addWidget(self.playBtn)
        #hlay.addWidget(self.slider)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        #vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        #media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        #self.mediaPlayer.positionChanged.connect(self.position_changed)
        #self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    #def position_changed(self, position):
        #self.slider.setValue(position)

    #def duration_changed(self, duration):
       # self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())




#######################################################################
class CameraWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('camera')
        self.setFixedSize(1280, 720)  # use variables
        #self.setCursor(Qt.BlankCursor)
        #self.showFullScreen()
        self.setStyleSheet(style.cameraWindow)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cLayout = QVBoxLayout()
        
        cLayout.addWidget(self.image_label, 0)
        camera_quit = QPushButton()
        camera_quit.setStyleSheet(style.btn_back)
        cLayout.addWidget(camera_quit, 1)
        camera_quit.clicked.connect(self.CancelFeed)
        camera_quit.clicked.connect(self.close)

        self.setLayout(cLayout)

        self.thread = VideoStream()
        self.thread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.thread.start()

    def ImageUpdateSlot(self, Image):
        self.image_label.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.thread.stop()
    
        
#######################################################################
class Navigator(QMainWindow):

    def _createButtons(self):
        
        # Navit
        btn_navit = QPushButton()
        btn_navit.setStyleSheet(style.btn_navit)
        btn_navit.clicked.connect(functions.startNavit)
        
        # Camera
        btn_camera = QPushButton()
        btn_camera.setStyleSheet(style.btn_camera)
        btn_camera.clicked.connect(self.camera_window)
        
        # Sensors
        btn_sensors = QPushButton()
        btn_sensors.setStyleSheet(style.btn_sensors)
        btn_sensors.clicked.connect(self.music_player)
        
        # Quit
        btn_quit = QPushButton()
        btn_quit.setStyleSheet(style.btn_quit)
        btn_quit.clicked.connect(self.close)
        
        # Add buttonsLayout to the general layout
        mainLayout = QHBoxLayout()
        
        mainLayout.addWidget(btn_navit)
        mainLayout.addWidget(btn_camera)
        mainLayout.addWidget(btn_sensors)
        mainLayout.addWidget(btn_quit)

        self.generalLayout.addLayout(mainLayout)

    ## root window
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Navigator')
        self.setFixedSize(1280, 720)
        #self.setCursor(Qt.BlankCursor) 
        #self.showFullScreen()
        self.setStyleSheet(style.mainWindow)
        
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        
        #self._createDisplay()
        self._createButtons()

    def camera_window(self, checked):
        self.w = CameraWindow()
        self.w.show()

    def music_player(self, checked):
        self.p = MusicPlayer()
        self.p.show()

    def Poweroff(channel):
        os.system("sudo poweroff -h now")

        
#######################################################################
def main():
    
    navigator = QApplication(sys.argv)
    view = Navigator()
    view.show()
    sys.exit(navigator.exec_())

if __name__ == '__main__':
    main()


### NOTES: split files into Functions, Styles. Group layouts by window