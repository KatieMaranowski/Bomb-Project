#This code was taken from https://discuss.python.org/t/centered-scrolling-text/20740 to get a template on how to get a good -
# -text scroll. Parts were scrapped and changed to make it function with a GUI for the viruscharacter of the project. 
from os import system
from time import sleep
import sys

black = "\033[0;30m"
purple = "\033[0;35m"
blue = "\033[0;34m"
green = "\033[0;32m"
red = "\033[0;31m"
yellow = "\033[0;33m"
white = "\033[0;37m"

def clear():
	system('clear')

def scrollTxt(text, color, speed):
	if color == "":
		for char in text:
			sys.stdout.write(char)
			sys.stdout.flush()
			sleep(speed)
		print()
	else:
		print(color, end="")
		for char in text:
			sys.stdout.write(char)
			sys.stdout.flush()
			sleep(speed)
		print()
		print(white, end="")


scrollTxt("Welcome...", blue, 0.1)