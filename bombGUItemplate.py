########### GUI Template ##############

from tkinter import *
button = 0 # Status of button (0 = not complete, 1 = complete)
keypad = 0 # Status of keypad 

window = Tk()
text = Label(window,text="Button {}".format(button))
text.pack()
window.mainloop()
