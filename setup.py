import os

try:
	os.system("sudo pip3 install youtube_dl")
except:
	print("Pip3 could not install a vital libary") # Wait what is this except statment for? Pip can't return an error because it is being ran in the terminal not 'inside' this program. Will I fix it? idk")

try:
	os.system("chmod +x Youtube-dl-Frontend.py && cp Youtube-dl-Frontend.py ~/.local/bin/Youtube-dl-Frontend") # Grants the program Executions permission and then copies it to ~/.local/bin/ so it should not have root privs
except:
	print("Error copying file to ~/.local/bin")
