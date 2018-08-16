from tkinter import *
from tkinter import ttk
root = Tk()

def survey(): # new window definition
    global CheckVar1, CheckVar2,CheckVar3,CheckVar5, E1
    global newwin
    newwin = Toplevel(root)
    display = Label(newwin, text="What did you think the intent was?")
    display.pack()
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    C1 = Checkbutton(newwin, text = "Emotion 1", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C2 = Checkbutton(newwin, text = "Emotion 2", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)
    C3 = Checkbutton(newwin, text = "Emotion 3", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C4 = Checkbutton(newwin, text = "Emotion 4", variable = CheckVar4, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)
    C1.pack()
    C2.pack()
    C3.pack()
    C4.pack()
    L1 = Label(newwin, text = "Other")
    L1.pack()
    E1 = Entry(newwin)
    E1.pack()
    submit_button =Button(newwin, text ="Submit", command =submit_response) #command linked
    submit_button.pack()
    #submit_button.pack()
def submit_response():
    global CheckVar1, CheckVar2,CheckVar3,CheckVar4, newwin, E1
    print('value1 is ', CheckVar1.get())
    print('value2 is ', CheckVar2.get())
    print('other value is ', E1.get())
    newwin.destroy()
button1 =Button(root, text ="open new window", command= survey) #command linked
button1.pack()

while True:

    root.update()
