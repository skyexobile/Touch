import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
from tkinter import filedialog
import numpy as np
from time import gmtime, strftime
import csv
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
import tkinter.messagebox

pygame.mixer.init(44100, -16,2,2048)
print("Connecting to Touch Output")
#Niloofar's computer
#output_serial = serial.Serial('/dev/cu.usbmodem14631')
#Angela's computer
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)
mappingData = []
type = 0
typevalue = 0
acquired_flag = False
data = []
loaded = False
soft_value = 100,
medium_value = 200,
hard_value = 300
def release():
    output_serial.write(str(9).encode())
    output_serial.readline().decode()

def load_file():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("CSV files", "*.csv")])
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
def sample():
    output_serial.write(str(4).encode())
    output_serial.readline().decode()
    output_serial.write(str(5).encode())
    output_serial.readline().decode()
    output_serial.write(str(6).encode())
    output_serial.readline().decode()

def generate():
    global acquired_flag, soft_value, medium_value, hard_value
    previous_read = -5000
    for (input_value) in data:
        media_time = pygame.mixer.music.get_pos()
        data_time = input_value[:input_value.find(',')-1]
        while abs(float(data_time) - float(media_time)) > 30:
            media_time = pygame.mixer.music.get_pos()
            print('2media time is ', media_time)
            print('data time is ', data_time)

        input_value = (input_value[input_value.find(',')+1:])
        print("input value is ", float(input_value))
        print(time.time())
        if( float(input_value) >= soft_value-10 and float(input_value) < medium_value and not acquired_flag):
            print("soft squeeze")
            initial_read = (input_value)
            output_serial.write(str(1).encode())
            #we need to read dummy value after write.
            output_serial.readline().decode()
            acquired_flag = True
        elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
            initial_read = (input_value)
            output_serial.write(str(2).encode())
            output_serial.readline().decode()
        elif( float(input_value) >= hard_value):
            initial_read = float(input_value)
            output_serial.write(str(3).encode())
            output_serial.readline().decode()
        elif(acquired_flag and (previous_read-15)> float(input_value)):
            print('release')
            output_serial.write(str(0).encode())
            output_serial.readline().decode()
            acquired_flag = False
        previous_read = float(input_value)

def csv_writer(data2, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data2.items():
            writer.writerow(value)
def load_settings():
    global soft_value, medium_value, hard_value
    settings = []
    with open("Settings.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            settings.append(row[0])
    soft_value = settings[0]
    medium_value = settings[1]
    hard_value = settings[2]
    soft_value = settings[0]
    soft_value = float(soft_value)
    medium_value = settings[1]
    medium_value = float(medium_value)
    hard_value = settings[2]
    hard_value = float(hard_value)
path = "Output_ST.csv"
myFile = open(path, 'a')

root = tk.Tk()

flag = False
init_flag = False

load_settings_button = tk.Button(root, text = "Load Settings", command = load_settings)
B = tk.Button(root, text = "Release", command = release)
B1 = tk.Button(root, text = "Load Touch File", command = load_file)
B2 = tk.Button(root, text = "Squeeze Playback", command = generate)
B3 = tk.Button(root, text = "Sample Squeezes", command = sample)
B.place(relx=.5, rely=1.5, anchor="center")
B1.place(relx=.5, rely=1.5, anchor="center")
B2.place(relx=.5, rely=1.5, anchor="center")
B3.place(relx=.5, rely=1.5, anchor="center")
B.pack()
B1.pack()
B2.pack()
B3.pack()
load_settings_button.pack()

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
listofsongs=[]
realnames = []

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
    generate()
    #need to do something about generate() when music is paused



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


while True:
    root.update()
