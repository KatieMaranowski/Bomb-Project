
##### 8UIJRN FNPOWVJINOKLGNRLKWR

from tkinter import *

class App(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.label1 = Label(window, text='Email:', bg='#E200E6')
        self.label2 = Label(window, text='Password:', bg='#E200E6')
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0)
        self.emailBox = Entry(window)
        self.pwBox = Entry(window)
        self.emailBox.grid(row=0, column=1)
        self.pwBox.grid(row=1, column=1)
        self.loginBtn = Button(window, text='Login', command=None)
        self.loginBtn.grid(row=2, columnspan=2)

window = Tk()
window.title("Adding an Image")
app = App(window)
window.config(bg='#E200E6')

window.mainloop()

