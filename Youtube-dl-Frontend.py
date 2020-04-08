#!/usr/bin/python3

# Version 0.0.1 by Matthew Pearson

import os
import tkinter
from tkinter import filedialog
import youtube_dl
import threading

class MessageDialoge():
	
	container = ""
	
	def displayError(self,error):
		
		self.container = tkinter.Tk()
	
		tkinter.Label(self.container,text=str(error)).pack()

	def displayMessage(self,message):
		
		self.container = tkinter.Tk()
		
		tkinter.Label(self.container,text=str(message)).pack()

class downloader():
	
	def download(self,videolink,videoquality,downloadpath):

		os.chdir(downloadpath)

		ydl_opts = {
			'format':videoquality,
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				thread1 = threading.Thread(target=ydl.download([videolink]))
				thread1.start()
				
		

class main_screen(tkinter.Tk,downloader,MessageDialoge): # I don't really know if this is a good way of using inheritance but I wanted to try it out since I just learned about it.
	
	menu = ""
	
	linkEntry = ""
	qualityEntry = ""
	downloaddir = ""
	browsebutton  = ""
	downloadbutton = ""
	
	def getFileDir(self):
		
		self.downloaddir = filedialog.askdirectory()
		
		print(self.downloaddir)
		
	def downloadvideo(self):
		
		try:
			self.download(self.linkEntry.get(),self.qualityEntry.get(),self.downloaddir)
			self.displayMessage("Download Completed\n " + self.downloaddir)
		except Exception as Error:
			self.displayError(Error)
			
	def __init__(self):
		tkinter.Tk.__init__(self)
		downloader.__init__(self)
		MessageDialoge.__init__(self)
		
		self.menu = tkinter.Menu()

		#self.geometry("640x580")
		self.config(menu=self.menu)
		
		firstmenu = tkinter.Menu(self.menu)
		firstmenu.add_command(label="Quit",command=quit)
		
		self.menu.add_cascade(label="file",menu=firstmenu)
		
		tkinter.Label(self,text="Link:").grid(column=0)
		self.linkEntry = tkinter.Entry(self)
		self.linkEntry.grid(row=0,column=1)
		
		tkinter.Label(self,text="Quality:").grid(row=1,column=0)
		self.qualityEntry = tkinter.Entry(self)
		self.qualityEntry.grid(row=1,column=1)
		
		self.browsebutton = tkinter.Button(self,text="Browse",command=self.getFileDir)
		self.browsebutton.grid(row=2,column=1)
		
		self.downloadbutton = tkinter.Button(self,text="Download",command=self.downloadvideo)
		self.downloadbutton.grid(row=0,column=2)
		
screen = main_screen()
screen.mainloop()
