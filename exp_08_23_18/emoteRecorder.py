import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk
from tkinter import*
import csv
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3,ID3NoHeaderError
from mutagen.easyid3 import EasyID3
import mutagen
import tkinter.messagebox


pygame.mixer.init(44100, -16,2,2048)
#Niloofar's computer
#input_serial = serial.Serial('/dev/cu.usbmodem14431')
#Angela's computer

input_serial = serial.Serial('/dev/cu.usbmodem1421')

input_serial.setBaudrate(115200)
print("Connected to Sensor")
#Niloofar's computer
#output_serial = serial.Serial('/dev/cu.usbmodem14411')
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)
#
output_serial.setDTR(False)
output_serial.setRTS(False)
#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
start_time = 0
soft_value = 100
med_value = 500
hard_value = 1000
root = tk.Tk()
data = []
acquired_flag = False
surveyMode = False
survey_response = []
receive_Mode = False
first_time = True

def toSurvey():
    global surveyMode, touchFile
    surveyMode = not surveyMode
    print("surveyMode is now ", surveyMode)
def reset():
    global offset
    input_serial.write(str("0").encode())
    offset = 0
    print("Reset Complete")
def set_soft():
    print('Please provide three 2-second soft squeezes')
    global offset
    value_list = []
    max_list = []
    global soft_value
    counter = 0
    previous = -100
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 50:
            while (previous - input_value) < 20:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value
                #print(new_input_value)

            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1

            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    soft_value = sum(max_list)/len(max_list)
    print("Soft touches have been trained")
def set_medium():
    print('Please provide three 2-second medium squeezes')

    global offset
    value_list = []
    max_list = []
    global med_value
    counter = 0
    previous = -100
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 200:
            while (previous - input_value) < 30:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value

            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1
            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    med_value = sum(max_list)/len(max_list)
    print("Medium touches have been trained")
def set_hard():
    global offset, hard_value
    value_list = []
    max_list = []
    counter = 0
    previous = -10
    print('Please provide three 2-second hard squeezes')

    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
        #print(input_value)
        if input_value > 400:
            while (previous - input_value) < 30:
                value_list.append(input_value)
                value = (input_serial.readline().decode())
                try:
                    new_input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    new_input_value = float(value) + offset
                #print(new_input_value)
                previous = input_value
                input_value = new_input_value
            index = value_list.index(max(value_list))
            for i in range(0, index):
                max_list.append(value_list[i])
            counter = counter +1
            print("Trial " + str(counter) + " completed!")
            value = (input_serial.readline().decode())
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                input_value = float(value) + offset
            while (previous - input_value) >5:
                previous = input_value
                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
        elif input_value < -3:
            offset = offset - input_value
    hard_value = sum(max_list)/len(max_list)
    print("Hard touches have been trained")
def save_settings():
    global soft_value, med_value, hard_value, PID_value, medium_value
    if soft_value > med_value:
        temp = soft_value
        soft_value = med_value
        med_value = temp
    if med_value > hard_value:
        temp = med_value
        med_value = hard_value
        hard_value = temp
    medium_value = med_value
    csv_writer([soft_value, medium_value, hard_value],"Emotional music/DataFiles/" + PID_value+"/Settings.csv")
    print("Your settings have been saved!")
    '''print("soft is ", soft_value)
    print("medium is ", medium_value)
    print("hard is ", hard_value)
    '''

def manual_pause():
    global ctr, isPlaying, resume_time, media_time, start_time
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        if start_time == 0:
            resume_time = pygame.mixer.music.get_pos()
        else:
            resume_time = pygame.mixer.music.get_pos()  + resume_time
        pygame.mixer.music.stop()
        print('player stopped')
        pygame.mixer.music.load(listofsongs[index])
        print('music loaded')
        print("resume time is ", resume_time/1000)
    else:
        isPlaying = True
        print('player resumed')
        start_time = resume_time/1000.0
        print("start time is ", start_time)
        media_time = start_time + media_time
        print("music time set")
        pygame.mixer.music.play(0, start_time)

def load_settings():
    global soft_value, medium_value, hard_value, PID_value
    settings = []
    with open("Emotional music/DataFiles/" + PID_value + "/Settings.csv") as csv_file:
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
    global acquired_flag, soft_value, medium_value, hard_value, start_time
    global previous_read
    global isPlaying
    global media_time
    global data_time, touchFile, surveyMode
    start_time = 0
    print('touch file is ', touchFile)
    with open(touchFile) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
    global isPlaying
    isPlaying = True
    releaseFlag = True
    pygame.mixer.music.play(0,0.0)
    while True:
        print('inside main loop')
        root.update()
        print('is playing is ', isPlaying)
        while(isPlaying and len(data) >0):
            root.update()
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
            #print("data time is" + str(data_time))
            #print("media time is ", media_time)
            #print('data time is ', data_time)
            diff = float(data_time) - float(media_time +start_time)
            while abs(diff) > 30 and float(media_time) < float(data_time):
                print('in while loop')
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
            #print('value is ', input_value)
            print('outside of while loop')
            if(acquired_flag and (previous_read - float(input_value) >=1)):
                print('release')
                output_serial.write(str(0).encode())
                output_serial.readline().decode()
                if surveyMode and releaseFlag is False:
                    manual_pause()
                    isPlaying = False
                    survey()
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
                output_serial.write(str(1).encode())
                output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
                print("medium squeeze")
                initial_read = (input_value)
                output_serial.write(str(2).encode())
                output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            elif( float(input_value) >= hard_value):
                print("hard squeeze")
                initial_read = float(input_value)
                output_serial.write(str(3).encode())
                output_serial.readline().decode()
                acquired_flag = True
                releaseFlag = False
            previous_read = float(input_value)
            del data[0]
        # else:
        #print("reached EOF")
            #print("isplaying is false")
        if len(data)<=0:
            print('end of song')
            pygame.mixer.music.stop()
            output_serial.write(str(0).encode())
            output_serial.readline().decode()
            break
        print('out of main loop')


def sample():
    output_serial.write(str(4).encode())
    output_serial.readline().decode()
    output_serial.write(str(5).encode())
    output_serial.readline().decode()
    output_serial.write(str(6).encode())
    output_serial.readline().decode()

def submit_demo():
    global demo_win
    global survey_response
    global UIN, Age, PID, PID_value
    print('saved ', [UIN.get(), Age.get(), PID.get()])
    csv_writer_append([UIN.get(), Age.get(), PID.get()], "DemoResponses.csv")
    PID_value = PID.get()
    demo_win.destroy()
def demog():
    global UIN, Age, PID, demo_win
    demo_win = Toplevel(root)
    display = Label(demo_win, text="Please answer the following.")
    display.pack()
    L1 = Label(demo_win, text = "UIN")
    L1.pack()
    UIN = Entry(demo_win)
    UIN.pack()
    L2 = Label(demo_win, text = "Age")
    L2.pack()
    Age = Entry(demo_win)
    Age.pack()
    L3 = Label(demo_win, text = "Participant ID")
    L3.pack()
    PID = Entry(demo_win)
    PID.pack()
    submit_button =Button(demo_win, text ="Submit", command =submit_demo) #command linked
    submit_button.pack()

def survey(): # new window definition
    global Sympathetic, Fear,Loving,Anger,Disgust,Surprise, E_value
    global newwin, surveyFlag
    surveyFlag = False
    newwin = Toplevel(root)
    display = Label(newwin, text="What did you think the intent was?")
    display.pack()
    Sympathetic = IntVar()
    Fear = IntVar()
    Loving = IntVar()
    Anger = IntVar()
    Disgust = IntVar()
    Surprise = IntVar()
    C1 = Checkbutton(newwin, text = "Sympathetic", variable = Sympathetic, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C2 = Checkbutton(newwin, text = "Fear", variable = Fear, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)
    C3 = Checkbutton(newwin, text = "Loving", variable = Loving, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20, )
    C4 = Checkbutton(newwin, text = "Anger", variable = Anger, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)

    C5 = Checkbutton(newwin, text = "Disgust", variable = Disgust, \
                 onvalue = 1, offvalue = 0, height=2, \
                 width = 20)

    C6 = Checkbutton(newwin, text = "Surprise", variable = Surprise, \
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
    E_value = Entry(newwin)
    E_value.pack()
    submit_button =Button(newwin, text ="Submit", command =submit_response) #command linked
    submit_button.pack()
    while surveyFlag is False:
        root.update()

    #submit_button.pack()
def submit_response():
    global Sympathetic, Fear,Loving,Anger, Disgust,Surprise,newwin, E_value, isPlaying
    global survey_response, media_time, PID_value, touchFile, surveyFlag
    e_value =E_value.get()
    if e_value == "":
        e_value = "None"
    csv_writer_append([media_time,Sympathetic.get(), Fear.get(),Loving.get(),Anger.get(), Disgust.get(),Surprise.get(),e_value], path + str(touchFile))
    newwin.destroy()
    manual_pause()
    surveyFlag = True
    print('survey flag is ', surveyFlag)
def release():
    output_serial.write(str(9).encode())
    output_serial.readline().decode()

reset_button =  tk.Button(root, text = "Reset Sensor", command = reset)
soft_button =  tk.Button(root, text = "Define Soft", command = set_soft)
medium_button =  tk.Button(root, text = "Define Medium", command = set_medium)
hard_button  =  tk.Button(root, text = "Define Hard", command = set_hard)
save_button  =  tk.Button(root, text = "Save Settings", command = save_settings)
playback_button  =  tk.Button(root, text = "Replay Touches", command = generate)
sMode_button = tk.Button(root, text = "Survey Mode", command = toSurvey)
sample_button = tk.Button(root, text = "Sample Squeezes", command = sample)
release_button = tk.Button(root, text = "Release", command = release)
release_button.pack()
reset_button.pack(side = tk.BOTTOM)
soft_button.pack(side = tk.BOTTOM)
medium_button.pack(side = tk.BOTTOM)
hard_button.pack(side = tk.BOTTOM)
save_button.pack(side = tk.BOTTOM)
playback_button.pack()
sMode_button.pack()
sample_button.pack()
listofsongs=[]
realnames = []
touchFileNames = []


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
    global ctr, isPlaying
    ctr += 1
    if (ctr%2!=0):
        isPlaying = False
        pygame.mixer.music.pause()
    if(ctr%2==0):
        isPlaying = True
        pygame.mixer.music.unpause()


def playsong(event):
    global isPlaying
    # print(touchFileNames)
    isPlaying = True
    pygame.mixer.music.play(0,0.0)



def nextsong(event):
    global index, touchFile
    print("next song")
    index += 1
    if (index < count):
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        #isPlaying = True
        #pygame.mixer.music.play(0,0.0)
    else:
        index = 0
        pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        #isPlaying = True
        #pygame.mixer.music.play(0,0.0)
    try:
        print("touch file is ", touchFile)
        updatelabel()
    except NameError:
        print("")

def previoussong(event):
    global index, touchFile
    print("previous song")
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    touchFile = touchFileNames[index]
    try:
        updatelabel()
    except NameError:
        print("")


def stopsong(event):
    global isPlaying
    isPlaying = False
    pygame.mixer.music.stop()
    output_serial.write(str(0).encode())
    output_serial.readline().decode
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
 global touchFile, PID_value
 global path2
 global first_time
    #count=0
 if first_time:
    first_time = False
    load_settings()
 # load_settings()
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
          try:
              audio = EasyID3(realdir)
          except mutagen.id3.ID3NoHeaderError:
              audio = mutagen.File(realdir, easy=True)
              audio.add_tags()
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
        csv_writer_append(["Media Time", "Sympathetic", "Fear", "Loving", "Anger", "Disgust", "Surprise","Other"], path + str(touchFile))

        #csv_writer(["Media Time,Sympathetic,Fear,Loving,Anger,Disgust,Surprise,Other", path + str(touchFile))
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
    try:
        pygame.mixer.music.stop()
        k=directorychooser()
    except OSError as e:
        print(e.errno)
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

def csv_writer_append(item, path):
    with open(path, "a", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in item:
            csv_file.write(str(value))
            if value is not item[-1]:
                csv_file.write(',')
        csv_file.write('\n')
        csv_file.close()

def csv_writer(data, path):
    with open(path, "w", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in data:
            csv_file.write(str(value) + '\n')
        csv_file.close()
offset = 0
data = []
PID_value = "1"
# touchFile = ""
if len(sys.argv) != 2:
    print ("Sending Mode")
    demog()
    path= "intention_"
else:
    print("Receiving Mode")
    PID_value = PID_value = str(sys.argv[1])
    path = "perception_"


#myFile = open(path, 'a')
# csv_writer_append(["Media Time", "Sympathetic", "Fear", "Loving", "Anger", "Disgust", "Surprise","Other"], path + str(touchFile)+ "_Responses.csv")

while True:

    # a.encode('utf-8').strip()
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset

    if input_value <-3:
        offset = offset -input_value
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            input_value = float(value) + offset
    if pygame.mixer.music.get_busy() and ctr%2==0 and surveyMode is False:
        #print('sending to csv!')
        time = pygame.mixer.music.get_pos()
        message =str(time) + "," + str(input_value)
        message= message.replace("\n", "")
        data.append(message)
        #print('this is being appended ', message)
        #print(touchFile)
        csv_writer(data, touchFile)

        #data = [time,input_value]
        #print(data)
        #csv_writer(data,'touches.csv')



    #server.send(message.encode())
    root.update()



# server.close()
