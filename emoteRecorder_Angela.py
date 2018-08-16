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
#input_serial = serial.Serial('/dev/cu.usbmodem14431')
#Angela's computer
input_serial = serial.Serial('/dev/cu.usbmodem1411')

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
data = []


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
def manual_pause():
    global ctr, isPlaying, resume_time
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        resume_time = pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
    if(ctr%2==0):
        isPlaying = True
        pygame.mixer.music.load(listofsongs[index])
        start_time = resume_time/1000
        pygame.mixer.music.play(1,start_time)
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
    soft_value = float(soft_value)
    medium_value = settings[1]
    medium_value = float(medium_value)
    hard_value = settings[2]
    hard_value = float(hard_value)
    print('soft is ', soft_value, ' medium is ', medium_value, ' hard is ', hard_value)

def generate():
    global data
    global acquired_flag, soft_value, medium_value, hard_value
    global previous_read
    global isPlaying
    global media_time
    global data_time
    acquired_flag = False
    with open(touchFile) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
    global isPlaying
    isPlaying = True
    pygame.mixer.music.play()
    print('data is ', data)
    print("play is pressed")
    while len(data)>0:
        if len(data) ==0:
            print("done")
            return
        input_value = data[0]
        media_time = pygame.mixer.music.get_pos()

        '''if pygame.mixer.music.get_busy():
            media_time = pygame.mixer.music.get_pos()
        else:
            media_time =0
        '''
        data_time = input_value[:input_value.find(',')]
        print("media time is1 ", media_time)
        print("data time is2 ", data_time)
        while (float(data_time) - float(media_time)) > 30:
            '''if pygame.mixer.music.get_busy():
                print("waiting in loop")
                media_time = pygame.mixer.music.get_pos()
                print("media time is ", media_time)
            else:
                media_time = 0
                print("still waiting")
            '''
            media_time = pygame.mixer.music.get_pos()
            '''print('media_time is ', media_time)
            print('data time is ', data_time)
            '''
        input_value = (input_value[input_value.find(',')+1:])
        #print(time.time())
        #check this is the last release
        print(soft_value)
        if( float(input_value) >= soft_value-10 and float(input_value) < medium_value  ):
            print("soft squeeze")
            initial_read = (input_value)
            #output_serial.write(str(1).encode())
            #output_serial.readline().decode()
            acquired_flag = True
        elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
            print("medium squeeze")
            initial_read = (input_value)
            #output_serial.write(str(2).encode())
            #output_serial.readline().decode()
            acquired_flag = True
        elif( float(input_value) >= hard_value):
            print("hard squeeze")
            initial_read = float(input_value)
            #output_serial.write(str(3).encode())
            #output_serial.readline().decode()
            acquired_flag = True
        elif(acquired_flag and (previous_read - float(input_value) >=3)):
            print('release')
            #output_serial.write(str(0).encode())
            #output_serial.readline().decode()
            manual_pause()
            print('is playing is ', isPlaying)
            survey()
            acquired_flag = False
        previous_read = float(input_value)
        del data[0]
def survey(): # new window definition
    global CheckVar1, CheckVar2,CheckVar3,CheckVar4,CheckVar5,CheckVar6, E1
    global newwin
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
    #submit_button.pack()
def submit_response():
    global CheckVar1, CheckVar2,CheckVar3,CheckVar4, CheckVar5,CheckVar6,newwin, E1, isPlaying
    print('value1 is ', CheckVar1.get())
    print('value2 is ', CheckVar2.get())
    print('other value is ', E1.get())
    newwin.destroy()
    manual_pause()

reset_button =  tk.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tk.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tk.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tk.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tk.Button(root, text = "Save Settings", command = save_settings)
playback_button  =  tk.Button(root, text = "Replay Touches", command = generate)

reset_button.pack(side = tk.BOTTOM)
soft_button.pack(side = tk.BOTTOM)
medium_button.pack(side = tk.BOTTOM)
hard_button.pack(side = tk.BOTTOM)
save_button.pack(side = tk.BOTTOM)
playback_button.pack()
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
