

from tkinter import *

keypad_count = 0
button_status = 0
wires_status = 0
textbox= 0
font_example = ("Comic Sans MS", 16, "bold")

class App(Frame):
    def __init__(self, window):
        global keypad_count
        Frame.__init__(self, window)
        self.keypadlabel = Label(window, text='Keypad:  {}/3'.format(keypad_count), bg='#D2B48C',font=font_example)
        self.buttonlabel = Label(window, text='Button:  {}'.format(button_status), bg='#D2B48C',font=font_example)
        self.wireslabel = Label(window, text='Wires:  {}'.format(wires_status), bg='#D2B48C',font=font_example)
        self.textbox = Label(window, text = "Welcome to the Bomb", bg = '#DDDDDD', font = font_example)
        self.viruscharacter = PhotoImage(file="viruscharacter.gif")
        self.viruscharacter2 = Label(window, image=self.viruscharacter, bg='#D2B48C')
        self.textbox.grid(row=1, column = 1)
        self.keypadlabel.grid(row=0, column=3,ipadx=50)
        self.buttonlabel.grid(row=0, column=5,ipadx=50)
        self.wireslabel.grid(row=0, column=10,ipadx=50)
        self.viruscharacter2.grid(row=2,column=0, pady=350)
        #self.text_frame = Frame(self, width=2, height=2)
        #self.speechbox = Text(self.text_frame,bg="red", state=DISABLED, wrap=WORD) 
        #self.speechbox.pack(fill=Y, expand=1)
        #self.text_frame.pack(side=TOP, fill=Y)
        #self.text_frame.pack_propagate(False)
        
window = Tk()
window.title("Adding an Image")
app = App(window)
window.config(bg='#D2B48C')

window.mainloop()

