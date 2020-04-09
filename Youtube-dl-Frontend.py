#!/usr/bin/python3

# Version 0.0.2 by Matthew Pearson

import sys
import os
#import tkinter
#from tkinter import filedialog
import youtube_dl
import threading

from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QLineEdit,QFileDialog, QHBoxLayout, QLabel,QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon

#import display.Videoplayer

class Videoplayer(QMainWindow):
	
	def __init__(self , parent = None):
		super(Videoplayer,self).__init__(parent)
		
		self.setWindowTitle("VideoPlayer")
		
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
		
		videoWidget = QVideoWidget()
		
		self.playButton = QPushButton()
		self.playButton.setEnabled(False)
		self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playButton.clicked.connect(self.play)

		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.setPosition)

		self.errorLabel = QLabel()
		self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
			QSizePolicy.Maximum)

		# Create new action
		openAction = QAction(QIcon('open.png'), '&Open', self)        
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open movie')
		openAction.triggered.connect(self.openFile)

		# Create exit action
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.exitCall)

		# Create menu bar and add action
		menuBar = self.menuBar()
		fileMenu = menuBar.addMenu('&File')
		#fileMenu.addAction(newAction)
		fileMenu.addAction(openAction)
		fileMenu.addAction(exitAction)

		# Create a widget for window contents
		wid = QWidget(self)
		self.setCentralWidget(wid)

		# Create layouts to place inside widget
		controlLayout = QHBoxLayout()
		controlLayout.setContentsMargins(0, 0, 0, 0)
		controlLayout.addWidget(self.playButton)
		controlLayout.addWidget(self.positionSlider)

		layout = QVBoxLayout()
		layout.addWidget(videoWidget)
		layout.addLayout(controlLayout)
		layout.addWidget(self.errorLabel)

		# Set widget to contain window contents
		wid.setLayout(layout)

		self.mediaPlayer.setVideoOutput(videoWidget)
		self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)
		self.mediaPlayer.error.connect(self.handleError)

	def openFile(self):
		fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
			QDir.homePath())

		if fileName != '':
			self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
			self.playButton.setEnabled(True)

	def playFile(self,filepath):
		self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
		self.playButton.setEnabled(True)

	def exitCall(self):
		sys.exit(app.exec_())

	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()

	def mediaStateChanged(self, state):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.playButton.setIcon(
					self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playButton.setIcon(
					self.style().standardIcon(QStyle.SP_MediaPlay))

	def positionChanged(self, position):
		self.positionSlider.setValue(position)

	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)

	def setPosition(self, position):
		self.mediaPlayer.setPosition(position)

	def handleError(self):
		self.playButton.setEnabled(False)
		self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

class downloader():
	
	def download(self,videolink,videoquality,downloadpath):

		os.chdir(downloadpath)

		ydl_opts = {
			'format':videoquality,
			'outtmpl':"%(id)s.%(ext)s"
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				thread1 = threading.Thread(target=ydl.download([videolink]))
				thread1.start()
		
class qt_main_screen(QWidget,downloader):
	
	def __init__(self):
		super().__init__()
		downloader.__init__(self)
		
		self.title = "Youtube-dl-Frontend"
		self.left = 10
		self.top = 10
		self.width = 410
		self.height = 160

		self.youtubeBaseUrl = "https://www.youtube.com/watch?v="
		
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left,self.top,self.width,self.height)
		
		self.link_text_box = QLineEdit(self)
		self.link_text_box.move(20,20)
		self.link_text_box.resize(280,40)
		
		self.quality_text_box = QLineEdit(self)
		self.quality_text_box.move(20,60)
		self.quality_text_box.resize(40,40)
		
		self.download_button = QPushButton("Download",self)
		self.download_button.resize(90,40)
		self.download_button.move(300,20)
		
		self.browse_file_button = QPushButton("Browse",self)
		self.browse_file_button.resize(50,40)
		self.browse_file_button.move(20,100)
		
		self.browse_file_button.clicked.connect(self.getFileDir)
		self.download_button.clicked.connect(self.downloadvideo)
		
		self.show()

	def downloadvideo(self):
		
		try:
			print("Downloading")
			self.download(self.youtubeBaseUrl + self.link_text_box.text(),self.quality_text_box.text(),self.downloaddir)
			#print(self.downloaddir + "*" + self.link_text_box.text() + "*")
			self.playVideo(self.downloaddir + "/" + self.link_text_box.text() + ".mp4")

		except Exception as e:
			print(e)

	def playVideo(self,path):
		player.playFile(path)
		player.show()

	def getFileDir(self):
		self.downloaddir = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	player = Videoplayer()
	player.resize(640, 480)
	screen = qt_main_screen()
	app2 = QApplication(sys.argv)
	sys.exit(app.exec_())
