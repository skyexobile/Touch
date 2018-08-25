import serial, datetime, time, re, pickle, os, select, sys
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import numpy as np
from time import gmtime, strftime
import csv
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
import tkinter.messagebox

if len(sys.argv) != 2:
    print ("Correct usage: script, Participant ID")
    exit()

PID = str(sys.argv[1])
pygame.mixer.init(44100, -16,2,2048)
print("Connecting to Touch Output")
#Niloofar's computer
#output_serial = serial.Serial('/dev/cu.usbmodem14631')
#Angela's computer
'''
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)
'''
surveyMode = False
mappingData = []
type = 0
typevalue = 0
acquired_flag = False
data = []
loaded = False
soft_value = 100
medium_value = 200
hard_value = 300
def toSurvey():
    global surveyMode
    surveyMode = True
    print("Survey Mode is ", surveyMode)
def release():
    output_serial.write(str(9).encode())
    output_serial.readline().decode()

def auto_load_file(file):
    with open(file) as csv_file:
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

def generate_all():
    while True:
        generate()

def generate():
    global acquired_flag, soft_value, medium_value, hard_value, start_time
    global previous_read
    global isPlaying
    global media_time
    global data_time, touchFile, surveyMode
    with open(touchFile) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
    global isPlaying
    isPlaying = True
    releaseFlag = True
    pygame.mixer.music.play(0,float(0))
    while True:
        root.update()
        while(isPlaying and len(data) >0):
            input_value = data[0]
            last_value = data[-1]
            #print("last value is " + last_value)
            media_time = pygame.mixer.music.get_pos()
            w_sum = (float(media_time) + (float(start_time)*1000))
            media_time = w_sum
            #print("media time is" + str(media_time/1000))
            #print("start time is" + str(start_time))
            # if pygame.mixer.music.get_busy():
            #     media_time = pygame.mixer.music.get_pos()
            # else:
            #     media_time = 0
            data_time = input_value[:input_value.find(',')]
            print("data time is" + str(data_time))
            print("media time is ", media_time)
            #print('data time is ', data_time)
            diff = float(data_time) - float(media_time +start_time)
            while abs(diff) > 30 and float(media_time) < float(data_time):
                #print("diff is ", abs(diff))
                media_time = pygame.mixer.music.get_pos()
                if media_time == -1:
                    print("stuck and media time is -1")
                    pygame.mixer.music.play(0,start_time)
                    media_time = pygame.mixer.music.get_pos()



                w_sum = (float(media_time) + (float(start_time)*1000))
                media_time = w_sum
                #print("w_media time is" + str(media_time/1000))
                #print("w_start time is" + str(start_time))
                #print("waiting and media time is " + str(media_time/1000))
                # if pygame.mixer.music.get_busy():
                #     print("waiting in loop")
                #     media_time = pygame.mixer.music.get_pos()
                #     print("media time is ", media_time)
                diff = float(data_time) - float(media_time+start_time)



                #     media_time = 0
                #     print("still waiting")
                # media_time = pygame.mixer.music.get_pos()


            input_value = (input_value[input_value.find(',')+1:])
            #print(time.time())
            #check this is the last release
            print('value is ', input_value)
            if(acquired_flag and (previous_read - float(input_value) >=3)):
                #print('release')
                #output_serial.write(str(0).encode())
                #output_serial.readline().decode()
                if surveyMode and releaseFlag is False:
                    print("survey here")
                    manual_pause()
                    isPlaying = False
                    print('is playing is ', isPlaying)
                    survey()
                    print('after survey value is ', input_value)
                    while(float(previous_read) > float(input_value)):
                        #print('previous is ', previous_read)
                        #print('current is ', input_value)
                        del data[0]
                        previous_read = input_value
                        input_value = data[0]
                        input_value = (input_value[input_value.find(',')+1:])
                        data_time = input_value[:input_value.find(',')]

                        #print("released data time is" + str(data_time))
                    releaseFlag = True
                acquired_flag = False
            if( float(input_value) >= soft_value-10 and float(input_value) < medium_value  ):
                print("soft squeeze")
                initial_read = (input_value)
                #output_serial.write(str(1).encode())
                #output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
                print("medium squeeze")
                initial_read = (input_value)
                #output_serial.write(str(2).encode())
                #output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            elif( float(input_value) >= hard_value):
                print("hard squeeze")
                initial_read = float(input_value)
                #output_serial.write(str(3).encode())
                #output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            previous_read = float(input_value)
            del data[0]
        # else:
        #print("reached EOF")
        if isPlaying == False:
            break
            #print("isplaying is false")
        elif len(data)<=0:
            print('end of song')
            pygame.mixer.music.stop()
            break


def survey(): # new window definition
    global CheckVar1, CheckVar2,CheckVar3,CheckVar4,CheckVar5,CheckVar6, E1
    global newwin, surveyFlag
    surveyFlag = False
    newwin = Toplevel(root)
    display = Label(newwin, text="What did you think the intent was?")
    display.pack()
    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    CheckVar5 = IntVar()
    CheckVar6 = IntVar()
    C1 = Checkbutton(newwin, text = "Sympathetic", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C2 = Checkbutton(newwin, text = "Fear", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)
    C3 = Checkbutton(newwin, text = "Loving", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C4 = Checkbutton(newwin, text = "Anger", variable = CheckVar4, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)

    C5 = Checkbutton(newwin, text = "disgust", variable = CheckVar5, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)

    C6 = Checkbutton(newwin, text = "Surprise", variable = CheckVar6, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)

    C1.pack()
    C2.pack()
    C3.pack()
    C4.pack()
    C5.pack()
    C6.pack()
    L1 = Label(newwin, text = "Other")
    L1.pack()
    E1 = Entry(newwin)
    E1.pack()
    submit_button =Button(newwin, text ="Submit", command =submit_response) #command linked
    submit_button.pack()
    while surveyFlag is False:
        root.update()
    #submit_button.pack()
def submit_response():
    global CheckVar1, CheckVar2,CheckVar3,CheckVar4, CheckVar5,CheckVar6,newwin, E1, isPlaying
    print('value1 is ', CheckVar1.get())
    print('value2 is ', CheckVar2.get())
    print('other value is ', E1.get())
    newwin.destroy()
    manual_pause()
    surveyFlag = True


def csv_writer(data2, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data2.items():
            writer.writerow(value)
def csv_writer_append(item, path):
    with open(path, "a", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in item:
            csv_file.write(str(value) + ',')
        csv_file.write('\n')
        csv_file.close()

def load_settings():
    global soft_value, medium_value, hard_value
    settings = []
    with open("Emotional music/DataFiles/" + PID + "/Settings.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            settings.append(row[0])
    soft_value = settings[0]
    medium_value = settings[1]
    hard_value = settings[2]
    soft_value = float(soft_value)
    medium_value = settings[1]
    medium_value = float(medium_value)
    hard_value = settings[2]
    hard_value = float(hard_value)
    print('soft is ', soft_value, ' medium is ', medium_value, ' hard is ', hard_value)

root = tk.Tk()

flag = False
init_flag = False

load_settings_button = tk.Button(root, text = "Load Settings", command = load_settings)
B = tk.Button(root, text = "Release", command = release)
B2 = tk.Button(root, text = "Play Touches", command = generate_all)
B3 = tk.Button(root, text = "Sample Squeezes", command = sample)
B4 = tk.Button(root, text = "Survey Mode", command = toSurvey)
B2.place(relx=.5, rely=1.5, anchor="center")
B3.place(relx=.5, rely=1.5, anchor="center")
B.pack()
B2.pack()
B3.pack()
B4.pack()
load_settings_button.pack()

v =tk.StringVar()
songlabel =tk.Label(root,textvariable=v,width=80)
index=0
count=0
start_time = 0
global ctr
ctr=0
global freq
isPlaying = False
aquired_flag = False
previous_read = -5000
message = "0"
listofsongs=[]
realnames = []
touchFileNames = []
def updatelabel():
    global index
    global songname
    global start_time
    v.set(listofsongs[index])
    #return songname

def pausesong(event):
    global ctr, isPlaying, resume_time
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        resume_time = pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
    if(ctr%2==0):
        isPlaying = True
        pygame.mixer.music.load(listofsongs[index])
        start_time = resume_time/1000.0
        pygame.mixer.music.play(0,start_time)



def manual_pause():
    global ctr, isPlaying, resume_time
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        resume_time = pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
        print('player stopped')

    else:
        pygame.mixer.music.load(listofsongs[index])
        print('player loaded')
        isPlaying = True
        start_time = resume_time/1000.0
        print('start time is ', start_time)
        pygame.mixer.music.play(0,start_time)



def playsong(event):
    global isPlaying
    isPlaying = True
    pygame.mixer.music.play(0,0.0)
    print("play is pressed")
    #need to do something about generate() when music is paused



def nextsong(event):
    global index
    index += 1
    if (index < count):
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        auto_load_file(touchFileNames[index])
        isPlaying = True
        pygame.mixer.music.play(0,0.0)
    else:
        index = 0
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        auto_load_file(touchFileNames[index])
        isPlaying = True
        pygame.mixer.music.play(0,0.0)
    try:
      updatelabel()
    except NameError:
        print("")

def previoussong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    touchFile = touchFileNames[index]
    auto_load_file(touchFileNames[index])
    isPlaying = True
    pygame.mixer.music.play(0,0.0)
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
 global touchFile, PID
 global path2
    #count=0
 load_settings()
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
          touchFileName = "DataFiles/"+PID+"/" +fileName + '.csv'
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
        csv_writer_append(["Media Time", "Sympathetic", "Fear", "Loving", "Anger", "Disgust", "Surprise","Other"], "DataFiles/"+PID+"/" + str(touchFile)+ "_Responses.csv")
        print("touchfile is set")
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

B.pack(side = tk.BOTTOM)

while True:
    root.update()
    if (isPlaying and len(data)>0):
        generate()
