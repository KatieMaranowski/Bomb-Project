

from tkinter import *

keypad_count = 0
button_status = 0
wires_status = 0
font_example = ("Comic Sans MS", 16, "bold")

class App(Frame):
    def __init__(self, window):
        global keypad_count
        Frame.__init__(self, window)
        self.keypadlabel = Label(window, text='Keypad:  {}/3'.format(keypad_count), bg='#D2B48C',font=font_example)
        self.buttonlabel = Label(window, text='Button:  {}'.format(button_status), bg='#D2B48C',font=font_example)
        self.wireslabel = Label(window, text='Wires:  {}'.format(wires_status), bg='#D2B48C',font=font_example)
        self.viruscharacter = PhotoImage(file="viruscharacter.gif")
        self.viruscharacter2 = Label(window, image=self.viruscharacter)
        self.keypadlabel.grid(row=0, column=0,ipadx=50)
        self.buttonlabel.grid(row=0, column=1,ipadx=50)
        self.wireslabel.grid(row=0, column=2,ipadx=50)
        self.viruscharacter2.grid(row=0,column=2)
        
window = Tk()
window.title("Adding an Image")
app = App(window)
window.config(bg='#D2B48C')

window.mainloop()

