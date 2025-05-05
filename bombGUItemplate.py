# DESTROY WIDGETS IN CONCLUSION SECTION OF BOMBPHASES NOT SHOW BUTTONS

from tkinter import *
from threading import Thread
import random
from time import sleep

keypad_count = 0 # This will show as 0-3 because you have to complete three different codes to finish the keypad phase
button_status = 0 #0 means button phase not complete, 1 means button phase complete
wires_status = 0 # 0 means wire not complete, 1 means wire complete
font_example = ("Arial", 16, "bold")
toggle_status = 0
messages = ["Nothing can stop me now","THIS ISN'T EVEN MY FINAL FORM!","Nice try!","[from evil_libraries import maniacal_laugh]","Didn't anyone ever teach you internet safety?"]

    
    

#def evil_messages(keypad_count):
 # messages = ["Nothing can stop me now","THIS ISN'T EVEN MY FINAL FORM!","Nice try!","[from evil_libraries import maniacal_laugh","Didn't anyone ever teach you internet safety?"]
 # while True:
      #text = random.choice(messages)
      #sleep(1)
     # text = random.choice(messages)
     # sleep(1)


######## have an if statement for text and define text variable outside class. if phone number keypad phase
# hasn't been solved, the text is a generic message or a cycle of npc sounding messages
# if they already got past the phone number one the message is either riddle 1 or riddle 2


class App(Frame):
    def __init__(self, window):
        global keypad_count
        global messages
        global wires_status
        global button_status
        global toggle_status
        message = random.choice(messages)
        self.keypadlabel = Label(window, text='Keypad:  {}/3'.format(keypad_count), fg = '#00008B',bg='#D3D3D3',font=font_example)
        self.buttonlabel = Label(window, text='Button:  {}'.format(button_status), fg = '#00008B', bg='#D3D3d3',font=font_example)
        self.wireslabel = Label(window, text='Wires:  {}'.format(wires_status), fg = '#00008B', bg='#D3D3D3',font=font_example)
        self.toggleslabel = Label(window, text='Toggles:  {}'.format(toggle_status), fg = '#00008B', bg='#D3D3D3',font=font_example)
        self.textbox = Text(window,  width = 30, height = 10,fg = '#00008B', bg = '#FFFFFF', font = font_example, wrap=WORD)
        textboxtext = "{}".format(message)
        self.textbox.insert(END, textboxtext)
        self.viruscharacter = PhotoImage(file="viruscharacter.gif")
        self.viruscharacter2 = Label(window, image=self.viruscharacter, bg='#D3D3D3')
            
        self.keypadlabel.grid(row=0, column=0)
        self.buttonlabel.grid(row=1, column=0)
        self.wireslabel.grid(row=2, column=0)
        self.toggleslabel.grid(row=3,column=0)
        self.textbox.grid(row=1, column = 1,rowspan = 2,sticky="NW")
        self.textbox.grid_propagate(False)
        self.viruscharacter2.grid(row=1,column=3,rowspan=3)
        #def update_gui_message(messages):
           # newmessage = random.choice(messages)
#         self.textbox.config(text=new3message)
        print("ASDD")
            
class Text_Thread(Thread):
    global messages
    def __init__(self, app):
        super().__init__()
        self.app = app
    
    def run(self):
        while True:
            self.app.textbox.delete('1.0',END)
            newmessage = random.choice(messages)
            self.app.textbox.insert(END, "{}".format(newmessage))
            sleep(5)
#class Riddles_Thread(Thread):
   # def __init__(self,keypad,toggles):
       # super().__init__()
   # global riddles 
   # def run(self):
       # if toggles self defused = true:
           # if keypad self value = 0:
                #self.app.textbox.delete('1.0',END)
                #self.app.textbox.insert(END, "{}".format(riddles[0])) ## ADD RIDDLE ARRAY AT TOP OF PROGRAM
            # if keypad self value = 1:
                #self.app.textbox.delete('1.0',END)
                #self.app.textbox.insert(END, "{}".format(riddles[1]))
            # if keypad self value = 2:
                #self.app.textbox.delete('1.0',END)
                #self.app.textbox.insert(END, "{}".format(riddles[2]))
            # if keypad self value = 3:
                #while True:
                    #self.app.textbox.delete('1.0',END)
                    #newmessage = random.choice(messages)
                    #self.app.textbox.insert(END, "{}".format(newmessage))
                    #sleep(5)
                
            

    
      
window = Tk()
app = App(window)
  
x = Text_Thread(app)
x.start()
# y = Riddles_Thread(args = app, keypad.value,toggles.defused)
# y.start()
window.title("Adding an Image")
window.config(bg='#D3D3D3')

window.mainloop()      

