from tkinter import *
from threading import Thread

messages = [1,2,3]


def create_gui():
        global messages
        message = random.choice(messages)
        window = tk.Tk()
        # Add your widgets (buttons, labels, etc.) here
        button = tk.Button(window, text="Start Task", command=start_threaded_task)
        button.pack()
        # ... other GUI elements
        window.config(bg='#D3D3D3')
        keypadlabel = Label(window, text='Keypad:  {}/3'.format(keypad_count), fg = '#00008B',bg='#D3D3D3',font=font_example)
        buttonlabel = Label(window, text='Button:  {}'.format(button_status), fg = '#00008B', bg='#D3D3d3',font=font_example)
        wireslabel = Label(window, text='Wires:  {}'.format(wires_status), fg = '#00008B', bg='#D3D3D3',font=font_example)
        toggleslabel = Label(window, text='Toggles:  {}'.format(toggle_status), fg = '#00008B', bg='#D3D3D3',font=font_example)
        textbox = Text(window,  width = 30, height = 10,fg = '#00008B', bg = '#FFFFFF', font = font_example, wrap=WORD)
        textboxtext = "{}".format(message)
        textbox.insert(END, textboxtext)
        viruscharacter = PhotoImage(file="viruscharacter.gif")
        viruscharacter2 = Label(window, image= viruscharacter, bg='#D3D3D3')
            
        keypadlabel.grid(row=0, column=0)
        buttonlabel.grid(row=1, column=0)
        wireslabel.grid(row=2, column=0)
        toggleslabel.grid(row=3,column=0)
        textbox.grid(row=1, column = 1,rowspan = 2,sticky="NW")
        textbox.grid_propagate(False)
        window.mainloop()
def long_running_task():
        # Perform your time-consuming operations here
        # ...
        # If needed, update GUI elements using after() method
        # Example: update_gui_element("Task finished!")
        tk.call_after(10000000, update_gui_element, "Task finished!")
def start_threaded_task():
    thread = threading.Thread(target=long_running_task)
    thread.start()
def update_gui_element(messages):
        newmessage = random.choice(messages)
       # Access and modify GUI elements safely here
       # Example: label.config(text=message)
        textbox.config(text=newmessage)
if __name__ == "__main__":
        create_gui()