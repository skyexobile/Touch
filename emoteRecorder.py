import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk
import csv
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
import tkinter.messagebox


pygame.mixer.init(44100, -16,2,2048)
input_serial = serial.Serial('/dev/cu.usbmodem14631')
input_serial.setBaudrate(115200)
print("Connected to Sensor")
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
'''

root = tk.Tk()
label1 = tk.Label(root, text = "Calibration")


def getCali():
    input_serial.write(str("0").encode())
B =  tk.Button(root, text = "Calibrate", command = getCali)

listofsongs=[]
realnames = []

v =tk.StringVar()
songlabel =tk.Label(root,textvariable=v,width=80)
index=0
count=0

global ctr
ctr=0
global freq
isPlaying = False
aquired_flag = False
previous_read = -5000
message = "0"

def updatelabel():
    global index
    global songname
    v.set(listofsongs[index])
    #return songname

def pausesong(event):
    global ctr
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        pygame.mixer.music.pause()
    if(ctr%2==0):
        isPlaying = True
        pygame.mixer.music.unpause()


def playsong(event):
    isPlaying = True
    pygame.mixer.music.play()



def nextsong(event):
    global index
    index += 1
    if (index < count):
        pygame.mixer.music.load(listofsongs[index])
        isPlaying = True
        pygame.mixer.music.play()
    else:
        index = 0
        pygame.mixer.music.load(listofsongs[index])
        isPlaying = True
        pygame.mixer.music.play()
    try:
      updatelabel()
    except NameError:
        print("")

def previoussong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    isPlaying = True
    pygame.mixer.music.play()
    try:
        updatelabel()
    except NameError:
        print("")


def stopsong(event):
    isPlaying = False
    pygame.mixer.music.stop()
    # pygame.mixer.quit()
    #v.set("")
    #return songname

label = tk.Label(root,text="Music Player")
label.pack()

listbox=tk.Listbox(root,selectmode=tk.MULTIPLE,width=100,height=20,bg="grey",fg="black")
listbox.pack(fill=tk.X)

def toggle():
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    if t_btn.config('text')[-1] == 'True':
        t_btn.config(text='False')
    else:
        t_btn.config(text='True')



def directorychooser():
 global count
 global index
    #count=0

 directory = askdirectory()
 print(directory)
 if(directory):
    count=0
    index=0
    #listbox.delete(0, END)
    del listofsongs[:]
    del realnames[:]
    os.chdir(directory)
    for files in os.listdir(directory):
      if files.endswith('.mp3'):
          realdir = os.path.realpath(files)
          audio = ID3(realdir)
          realnames.append(audio.get('TIT2', 'No Title'))
          listofsongs.append(files)
      else:
        print(files+" is not a song")

    if listofsongs == [] :
       okay=tkinter.messagebox.askretrycancel("No songs found","no songs")
       if(okay==True):
           directorychooser()
    else:
        listbox.delete(0, tk.END)
        realnames.reverse()
        for items in realnames:
            listbox.insert(0, items)
        for i in listofsongs:
            count = count + 1
        # realdir = os.path.realpath(listofsongs[0])
        # audio = ID3(realdir)
        # freq = audio.info.sample_rate
        # pygame.mixer.init(22050, -16, 2)
        # print(pygame.mixer.get_init())
        pygame.mixer.music.load(listofsongs[0])
        # pygame.mixer.music.play()
        try:
            updatelabel()
        except NameError:
            print("")
 else:
    return 1

# try:
#     directorychooser()
# except OSError as e:
#          print("thank you")


def call(event):
 if(True):
    try:
        pygame.mixer.music.stop()
        k=directorychooser()

    except OSError as e:
         print("thank you")

realnames.reverse()

songlabel.pack()



# submit = tk.Button(root, text="Enter", command = Squeeze)
# submit.place(relx=.5, rely=1.5, anchor="center")
# label1.pack()
# E1.pack()
# label2.pack()
# E2.pack()
# submit.pack(side = tk.TOP)
root.update()

path = "Output_ST2.csv"
myFile = open(path, 'a')
myFile.write(str(time.strftime("%X")))
print('Time: ' + str(time.strftime("%X")))
flag = False
timeBegin = time.time()

framemiddle = tk.Frame(root,width=100,height=30)
framemiddle.pack()


framedown = tk.Frame(root,width=200,height=300)
framedown.pack()

openbutton = tk.Button(framedown,text="open")
openbutton.pack(side=tk.LEFT)

# mutebutton = tk.Button(framedown,text=u"\U0001F507")
# mutebutton.pack(side=tk.LEFT)

previousbutton = tk.Button(framedown,text="◄◄")
previousbutton.pack(side=tk.LEFT)


playbutton = tk.Button(framedown,text="►")
playbutton.pack(side=tk.LEFT)

stopbutton = tk.Button(framedown,text="■")
stopbutton.pack(side=tk.LEFT)

nextbutton = tk.Button(framedown,text="►►")
nextbutton.pack(side=tk.LEFT)


pausebutton = tk.Button(framedown,text="►/║║")
pausebutton.pack(side=tk.LEFT)

v = tk.IntVar()

# Button1 = tk.Radiobutton(framedown, text="Adding Touches", variable=v, value=1).pack(anchor=tk.W)
# Button2 = tk.Radiobutton(framedown, text="Receiving Touches", variable=v, value=2).pack(anchor=tk.W)



# mutebutton.bind("<Button-1>",mute)
openbutton.bind("<Button-1>",call)
playbutton.bind("<Button-1>",playsong)
nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",previoussong)
stopbutton.bind("<Button-1>",stopsong)
pausebutton.bind("<Button-1>",pausesong)

B.pack(side = tk.BOTTOM)
root.update()

def save_to_csv(time,val):
    print("time,val")

while True:
    print('This is happening!')
    if not aquired_flag:
        # a.encode('utf-8').strip()
        value = (input_serial.readline().decode(errors='ignore'))
        if type(value).__name__ != "int":
            value = 1
        input_value = float(value)
        if pygame.mixer.music.get_busy():
            print('sending to csv!')
            time = pygame.mixer.music.get_pos()
            save_to_csv(time,input_value)
        if input_value >= previous_read:
            message = str(input_value)
            message= message.replace("\n", "")
            previous_read = input_value
            # print(time)
        else:
            acquired_flag = True
            message = "0"
            while(acquired_flag and input_value >= 30):
                value = (input_serial.readline().decode())
                input_value = float(value)
                input_serial.write(str("0").encode())
                input_serial.readline().decode()
                if isPlaying:
                    save_to_csv(time,input_value)
                # server.send(message.encode())
            print('ready')
            acquired_flag = False
        #server.send(message.encode())
    root.update()


# server.close()
