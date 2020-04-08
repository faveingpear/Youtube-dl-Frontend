#!/usr/bin/python3

# Version 0.0.2 by Matthew Pearson

import sys
import os
import tkinter
from tkinter import filedialog
import youtube_dl
import threading

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer

import display.Videoplayer

class MessageDialoge():
	
	container = ""
	
	def displayError(self,error):
		
		self.container = tkinter.Tk()
	
		tkinter.Label(self.container,text=str(error)).pack()

	def displayMessage(self,message):
		
		self.container = tkinter.Tk()
		
		tkinter.Label(self.container,text=str(message)).pack()


class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


class downloader(MyLogger):
	
	def download(self,videolink,videoquality,downloadpath):

		os.chdir(downloadpath)

		ydl_opts = {
			'format':videoquality,
			'forcedid':1,
			'logger': self
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				thread1 = threading.Thread(target=ydl.download([videolink]))
				thread1.start()
				
	def __init__(self):
		MyLogger.__init__(self)
		
class qt_main_screen(QWidget,downloader,MessageDialoge):
	
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
			print(self.downloaddir + "*" + self.link_text_box.text() + "*")
			self.playVideo(self.downloaddir + "/*" + self.link_text_box.text() + "*.mp4")

		except Exception as e:
			print(e)

	def playVideo(self,path):
		os.system("mpv " + path)
		#self.player = display.Videoplayer.App() // Work on using the video player I just made
		#self.player.resize(640, 480)
		#self.player.playFile(path)
		#self.player.show()

	def getFileDir(self):
		self.downloaddir = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
		

# class main_screen(tkinter.Tk,downloader,MessageDialoge): # I don't really know if this is a good way of using inheritance but I wanted to try it out since I just learned about it.
	
# 	menu = ""
	
# 	linkEntry = ""
# 	qualityEntry = ""
# 	downloaddir = ""
# 	browsebutton  = ""
# 	downloadbutton = ""
	
# 	def getFileDir(self):
		
# 		self.downloaddir = filedialog.askdirectory()
		
# 		print(self.downloaddir)
		
# 	def downloadvideo(self):
		
# 		try:
# 			self.download(self.linkEntry.get(),self.qualityEntry.get(),self.downloaddir)
# 			self.displayMessage("Download Completed\n " + self.downloaddir)
# 		except Exception as Error:
# 			self.displayError(Error)
			
# 	def __init__(self):
# 		tkinter.Tk.__init__(self)
# 		downloader.__init__(self)
# 		MessageDialoge.__init__(self)
		
# 		self.menu = tkinter.Menu()

# 		#self.geometry("640x580")
# 		self.config(menu=self.menu)
		
# 		firstmenu = tkinter.Menu(self.menu)
# 		firstmenu.add_command(label="Quit",command=quit)
		
# 		self.menu.add_cascade(label="file",menu=firstmenu)
		
# 		tkinter.Label(self,text="Link:").grid(column=0)
# 		self.linkEntry = tkinter.Entry(self)
# 		self.linkEntry.grid(row=0,column=1)
		
# 		tkinter.Label(self,text="Quality:").grid(row=1,column=0)
# 		self.qualityEntry = tkinter.Entry(self)
# 		self.qualityEntry.grid(row=1,column=1)
		
# 		self.browsebutton = tkinter.Button(self,text="Browse",command=self.getFileDir)
# 		self.browsebutton.grid(row=2,column=1)
		
# 		self.downloadbutton = tkinter.Button(self,text="Download",command=self.downloadvideo)
# 		self.downloadbutton.grid(row=0,column=2)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = qt_main_screen()
	sys.exit(app.exec_())
