

from tkinter import *

keypad_count = 0 # This will show as 0-3 because you have to complete three different codes to finish the keypad phase
button_status = 0 #0 means button phase not complete, 1 means button phase complete
wires_status = 0 # 0 means wire not complete, 1 means wire complete
font_example = ("Arial", 16, "bold")

def evil_messages(keypad_count):
  messages = ["Nothing can stop me now","THIS ISN'T EVEN MY FINAL FORM!","Nice try!","[from evil_libraries import maniacal_laugh","Didn't anyone ever teach you internet safety?"]
  sleep(2)
  text = random.choice(messages)

if keypad_count == 0:
    text = "generic evil message"
if keypad_count == 1:
    text = "first riddle hehehe"

######## have an if statement for text and define text variable outside class. if phone number keypad phase
# hasn't been solved, the text is a generic message or a cycle of npc sounding messages
# if they already got past the phone number one the message is either riddle 1 or riddle 2


class App(Frame):
    def __init__(self, window):
        global keypad_count
        global text
        Frame.__init__(self, window)
        self.keypadlabel = Label(window, text='Keypad:  {}/3'.format(keypad_count), fg = '#00008B',bg='#D3D3D3',font=font_example)
        self.buttonlabel = Label(window, text='Button:  {}'.format(button_status), fg = '#00008B', bg='#D3D3d3',font=font_example)
        self.wireslabel = Label(window, text='Wires:  {}'.format(wires_status), fg = '#00008B', bg='#D3D3D3',font=font_example)
        self.textbox = Text(window,  width = 30, height = 10,fg = '#00008B', bg = '#FFFFFF', font = font_example, wrap=WORD)
        textboxtext = "{}".format(text)
        self.textbox.insert(END, textboxtext)
        self.viruscharacter = PhotoImage(file="viruscharacter.gif")
        self.viruscharacter2 = Label(window, image=self.viruscharacter, bg='#D3D3D3')
        
        self.keypadlabel.grid(row=0, column=3,ipadx=50)
        self.buttonlabel.grid(row=0, column=5,ipadx=50)
        self.wireslabel.grid(row=0, column=10,ipadx=50)
        self.textbox.grid(row=1, column = 1, columnspan=50, rowspan= 50,pady=300, padx= 0,sticky="NW")
        self.textbox.grid_propagate(False)
        
        self.viruscharacter2.grid(row=1,column=0, padx = 0, pady = 350)
        #self.text_frame = Frame(self, width=2, height=2)
        #self.speechbox = Text(self.text_frame,bg="red", state=DISABLED, wrap=WORD) 
        #self.speechbox.pack(fill=Y, expand=1)
        #self.text_frame.pack(side=TOP, fill=Y)
        #self.text_frame.pack_propagate(False)
        
window = Tk()
window.title("Adding an Image")
app = App(window)
window.config(bg='#D3D3D3')

window.mainloop()
# use window.geometry to change the resolution based on resolution of the pi
