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
#Niloofar's computer
input_serial = serial.Serial('/dev/cu.usbmodem14131')
#Angela's computer
# input_serial = serial.Serial('/dev/cu.usbmodem1411')

input_serial.setBaudrate(115200)
print("Connected to Sensor")
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
'''
soft_value = 100
med_value = 500
hard_value = 1000
root = tk.Tk()



def reset():
    input_serial.write(str("0").encode())
def set_soft():
    print('soft function')
    offset = 0
    value_list = []
    max_list = []
    global soft_value
    counter = 0
    while counter <3:
        print('counter value ', counter)
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        print(input_value)
        if input_value > 100:
            while input_value >30:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
                print(input_value)

            index = value_list.index(max(value_list))
            max_list.append(value_list[index])
            max_list.append(value_list[index+1])
            max_list.append(value_list[index+2])
            max_list.append(value_list[index+3])
            counter = counter +1
        elif input_value < -20:
            offset = offset - input_value
    soft_value = sum(max_list)/len(max_list)
def set_medium():
    offset = 0
    value_list = []
    max_list = []
    global medium_value
    counter = 0
    while counter <3:
        print('counter value ', counter)
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        print(input_value)
        if input_value > 200:
            while input_value >50:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
            print(input_value)

            index = value_list.index(max(value_list))
            max_list.append(value_list[index])
            max_list.append(value_list[index+1])
            max_list.append(value_list[index+2])
            max_list.append(value_list[index+3])
            counter = counter +1
        elif input_value < -20:
            offset = offset - input_value
    med_value = sum(max_list)/len(max_list)
def set_hard():
    offset = 0
    value_list = []
    max_list = []
    global hard_value
    counter = 0
    while counter <3:
        print('counter value ', counter)
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        print(input_value)
        if input_value > 400:
            while input_value >40:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
            index = value_list.index(max(value_list))
            max_list.append(value_list[index])
            max_list.append(value_list[index+1])
            max_list.append(value_list[index+2])
            max_list.append(value_list[index+3])
            counter = counter +1
            print(input_value)

        elif input_value < -20:
            offset = offset - input_value
    hard_value = sum(max_list)/len(max_list)
def save_settings():
    global soft_value, med_value, hard_value
    settings = [soft_value, med_value, hard_value]
    csv_writer(settings, "Settings.csv")

reset_button =  tk.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tk.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tk.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tk.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tk.Button(root, text = "Save Settings", command = save_settings)

reset_button.pack(side = tk.BOTTOM)
soft_button.pack(side = tk.BOTTOM)
medium_button.pack(side = tk.BOTTOM)
hard_button.pack(side = tk.BOTTOM)
save_button.pack(side = tk.BOTTOM)
listofsongs=[]
realnames = []
touchFileNames = []


v =tk.StringVar()
songlabel =tk.Label(root,textvariable=v,width=80)
index=0
count=0
global touchFile
touchFile = "touches.csv"
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
    # print(touchFileNames)
    isPlaying = True
    pygame.mixer.music.play()



def nextsong(event):
    global index
    index += 1
    if (index < count):
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        isPlaying = True
        pygame.mixer.music.play()
    else:
        index = 0
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
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
    touchFile = touchFileNames[index]
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
 global touchFile
    #count=0

 directory = askdirectory()
 print(directory)
 if(directory):
    count=0
    index=0
    #listbox.delete(0, END)
    del listofsongs[:]
    del realnames[:]
    del touchFileNames[:]
    os.chdir(directory)
    for files in os.listdir(directory):
      if files.endswith('.mp3'):
          realdir = os.path.realpath(files)
          fileName = os.path.splitext(files)[0]
          touchFileName = fileName + '.csv'
          audio = ID3(realdir)
          realnames.append(audio.get('TIT2', 'No Title'))
          listofsongs.append(files)
          touchFileNames.append(touchFileName)
      else:
        print(files+" is not a song")
    print(listofsongs)
    if listofsongs == [] :
       okay=tkinter.messagebox.askretrycancel("No songs found","no songs")
       if(okay==True):
           directorychooser()
    else:
        listbox.delete(0, tk.END)
        realnames.reverse()
        pygame.mixer.music.load(listofsongs[0])
        touchFile = touchFileNames[0]
        for items in realnames:
            listbox.insert(0, items)
        for i in listofsongs:
            count = count + 1

        # realdir = os.path.realpath(listofsongs[0])
        # audio = ID3(realdir)
        # freq = audio.info.sample_rate
        # pygame.mixer.init(22050, -16, 2)
        # print(pygame.mixer.get_init())

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

root.update()
'''
This is the one Niloofar is using
def csv_writer(data, path):
    with open(path, "a", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in data:
            csv_file.write(str(value) + ',')
        csv_file.write('\r\n')
        csv_file.close()
'''
def csv_writer(data, path):
    with open(path, "w", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in data:
            csv_file.write(str(value) + '\n')
        csv_file.close()
offset = 0
data = []
while True:
    # a.encode('utf-8').strip()
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset

    if input_value <-20:
        offset = offset -input_value
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
    if pygame.mixer.music.get_busy() and ctr%2==0:
        print('sending to csv!')
        time = pygame.mixer.music.get_pos()
        message =str(time) + "," + str(input_value)
        message= message.replace("\n", "")
        data.append(message)
        # print(message)
        print(touchFile)
        csv_writer(data, touchFile)
        '''
        data = [time,input_value]
        print(data)
        csv_writer(data,'touches.csv')
        '''

    #server.send(message.encode())
    root.update()


# server.close()
