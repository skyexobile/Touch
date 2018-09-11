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
import pyaudio, wave


py_audio = pyaudio.PyAudio()
paused = False
difference = 0.0
root = tk.Tk()
isPlaying = False
path=""
replay = False
touchFileDirectory2 = ""
touchFileDirectory = ""
#Niloofar's computer

input_serial = serial.Serial('/dev/cu.usbmodem14641')
#Angela's computer

# input_serial = serial.Serial('/dev/cu.usbmodem1421')

input_serial.setBaudrate(115200)
print("Connected to Sensor")

#Niloofar's computer
output_serial = serial.Serial('/dev/cu.usbmodem14631')
# output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)
#
output_serial.setDTR(False)
output_serial.setRTS(False)
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
start_time = 0
soft_value = 100
med_value = 500
hard_value = 1000
data = []
acquired_flag = False
surveyMode = False
survey_response = []
receive_Mode = True
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
    csv_writer([soft_value, medium_value, hard_value],"EmotionalMusic/DataFiles/" + PID_value+"/Settings.csv")
    print("Your settings have been saved!")
    '''print("soft is ", soft_value)
    print("medium is ", medium_value)
    print("hard is ", hard_value)
    '''

def load_settings():
    global soft_value, medium_value, hard_value, PID_value
    settings = []
    with open("EmotionalMusic/DataFiles/" + PID_value+"/Settings.csv") as csv_file:
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
    global acquired_flag, soft_value, medium_value, hard_value, start_time, initial_time
    global previous_read
    global isPlaying
    global stream_time
    global data_time, touchFile, surveyMode, difference, replay
    replay = True
    start_time = 0
    data = []
    surveyCounter = 0
    print('touch file is ', touchFile)
    with open(touchFileDirectory2) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
    global isPlaying
    isPlaying = True
    releaseFlag = True
    media_list = []
    play()
    difference = 0.0
    initial_time = stream.get_time()
    while True:
        root.update()
        print('is playing is ', isPlaying)
        while(isPlaying and len(data) >0):
            root.update()
            if isPlaying:
                if len(data) == 0:
                    print('no more data 1')
                    stop()
                    break
                input_value = data[0]
                last_value = data[-1]

            #print("media time is" + str(stream_time/1000))
            #print("start time is" + str(start_time))
            # if pygame.mixer.music.get_busy():
            #     stream_time = pygame.mixer.music.get_pos()
            # else:
            #     stream_time = 0

                data_time = input_value[:input_value.find(',')]
                print('data time is ', data_time)
            #print("data time is" + str(data_time))
            #print("media time is ", stream_time)
            #print('data time is ', data_time)
                stream_time = (stream.get_time() - difference) - initial_time
                diff = float(data_time) - float(stream_time)
                #print('data time is ', data_time)
                #print('stream time is', stream_time)
                while abs(diff) >= 0.2 and float(stream_time) < float(data_time):
                    stream_time = (stream.get_time() - difference)- initial_time
                    if surveyCounter == 0:
                        timeout = stream_time +5
                    #print("w_media time is" + str(stream_time/1000))
                    #print("w_start time is" + str(start_time))
                    #print("waiting and media time is " + str(stream_time/1000))
                    # if pygame.mixer.music.get_busy():
                    #     print("waiting in loop")
                    #     stream_time = pygame.mixer.music.get_pos()
                    #     print("media time is ", stream_time)
                    diff = float(data_time) - float(stream_time)

                    #     stream_time = 0
                    #     print("still waiting")
                    # stream_time = pygame.mixer.music.get_pos()


                input_value = (input_value[input_value.find(',')+1:])
                #print(time.time())
                #check this is the last release
                #print('value is ', input_value)
                if(acquired_flag and (float(previous_read) - float(input_value) >=1)):
                    print('release', surveyCounter)

                    output_serial.write(str(0).encode())
                    output_serial.readline().decode()
                    if surveyCounter == 0:
                        timeout = stream_time + 5

                    if surveyMode and releaseFlag is False:
                        #isPlaying = False
                        if surveyCounter%5==0:
                            pause()
                            survey()
                            # if stream_time >= timeout:
                            #     surveyCounter = 0
                        surveyCounter +=1
                        stream_time = (stream.get_time() - initial_time) - difference
                    while(float(previous_read) > float(input_value) and len(data)>0):
                        #print('previous is ', previous_read)
                        #print('current is ', input_value)
                        if len(data)<=0:
                            print('end of touches')
                            stop()
                            break

                        del data[0]
                        if len(data)==0:
                            print('not more data 2')
                            stop()
                            break
                        previous_read = input_value
                        input_value = data[0]
                        input_value = (input_value[input_value.find(',')+1:])
                        data_time = input_value[:input_value.find(',')]
                        print('wait')
                    if len(data)<=0:
                        print('end of touches')
                        stop()
                        break

                            #print("released data time is" + str(data_time))
                        releaseFlag = True
                    acquired_flag = False
                if( float(input_value) >= soft_value-10 and float(input_value) < medium_value  ):
                    #print("soft squeeze")
                    initial_read = (input_value)
                    output_serial.write(str(1).encode())
                    output_serial.readline().decode()
                    acquired_flag = True
                    releaseFlag = False
                elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
                    #print("medium squeeze", input_value, " ", data_time)
                    initial_read = (input_value)
                    output_serial.write(str(2).encode())
                    output_serial.readline().decode()
                    acquired_flag = True
                    releaseFlag = False
                elif( float(input_value) >= hard_value):
                    #print("hard squeeze", input_value, " ", stream_time)
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
            print('end of touches')
            stop()
            output_serial.write(str(0).encode())
            output_serial.readline().decode()
            break

def sample():
    output_serial.write(str(4).encode())
    output_serial.readline().decode()
    output_serial.write(str(5).encode())
    output_serial.readline().decode()
    output_serial.write(str(6).encode())
    output_serial.readline().decode()

def submit_demo():
    global demo_win, gender, role
    global survey_response
    global UIN, Age, PID, PID_value
    print('saved ', [UIN.get(), gender.get(), Age.get(), role.get(), PID.get()])
    csv_writer_append([UIN.get(),gender.get(), Age.get(), role.get(), PID.get()], "DemoResponses.csv")
    PID_value = PID.get()
    demo_win.destroy()
def demog():
    global UIN, Age, PID, demo_win, gender, role
    demo_win = Toplevel(root)
    display = Label(demo_win, text="Please answer the following.")
    display.pack()
    L1 = Label(demo_win, text = "UIN")
    L1.pack()
    UIN = Entry(demo_win)
    UIN.pack()

    L4 = Label(demo_win, text = "Gender")
    L4.pack()
    gender = Entry(demo_win)
    gender.pack()
    L5 = Label(demo_win, text = "role")
    L5.pack()
    role = Entry(demo_win)
    role.pack()


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
    global Sympathetic, Fear,Loving,Anger,Disgust,Surprise, E_value, difference
    global newwin, surveyFlag, stream_time
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
    pause()
    #submit_button.pack()
def submit_response():
    global Sympathetic, Fear,Loving,Anger, Disgust,Surprise,newwin, E_value, isPlaying
    global survey_response, stream_time, PID_value, touchFile, surveyFlag, touchFileDirectory
    e_value =E_value.get()
    if e_value == "":
        e_value = "None"
    csv_writer_append([stream_time,Sympathetic.get(), Fear.get(),Loving.get(),Anger.get(), Disgust.get(),Surprise.get(),e_value], touchFileDirectory)
    newwin.destroy()

    surveyFlag = True
    print('survey flag is ', surveyFlag)

def release():
    output_serial.write(str(0).encode())
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
initial_time = 0.0
def updatelabel():
    global index
    global songname
    v.set(listofsongs[index])
    #return songname



def playsong(event):
    global initial_time, stream
    play()
    initial_time = stream.get_time()

def nextsong(event):
    global index, touchFile
    print("next song")
    index += 1
    if (index < count):
        #pygame.mixer.music.load(listofsongs[index])
        touchFile = touchFileNames[index]
        #isPlaying = True
        #pygame.mixer.music.play(0,0.0)
    else:
        index = 0
        #pygame.mixer.music.load(listofsongs[index])
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
    #pygame.mixer.music.load(listofsongs[index])
    touchFile = touchFileNames[index]
    try:
        updatelabel()
    except NameError:
        print("")

def pausesong(event):
    global ctr, isPlaying
    pause()

def stopsong(event):
    global isPlaying
    isPlaying = False
    stop()

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
 global wave
 global touchFileDirectory, touchFileDirectory2
 global directory

 script_dir = os.path.dirname(os.path.abspath(__file__))
 directory = askdirectory()
 print(directory)

 # if first_time:
 #     first_time = False
 #     load_settings(directory)
 if(directory):
    count=0
    index=0
    #listbox.delete(0, END)
    del listofsongs[:]
    del realnames[:]
    del touchFileNames[:]
    os.chdir(directory)
    for files in os.listdir(directory):
      if files.endswith('.wav'):
          print("files is ", files)
          print("***script_dir is ", script_dir)
          realdir = os.path.realpath(files)
          print("***realdir is ", realdir)
          relPath = realdir.replace(script_dir, '')
          print("***relPath is ", relPath)
          fileName = os.path.splitext(files)[0]
          touchFileName = fileName + '.csv'
          realnames.append(fileName)
          listofsongs.append(realdir)
          touchFileNames.append(touchFileName)
      else:
        print(files+" is not a song")
    os.chdir(script_dir)
    print(listofsongs)
    if listofsongs == [] :
       okay=tkinter.messagebox.askretrycancel("No songs found","no songs")
       if(okay==True):
           directorychooser()
    else:
        listbox.delete(0, tk.END)
        realnames.reverse()
        wave = wave.open(listofsongs[0], "rb")
        # print("****here1")
        touchFile = touchFileNames[0]

        touchFileDirectory2 = directory + "/" + str(touchFile)
        # print("****touchFileDirectory is ", touchFileDirectory)
        # print("****here2" + directory + "/" + path + str(touchFile))
        #csv_writer(["Media Time,Sympathetic,Fear,Loving,Anger,Disgust,Surprise,Other"],touchFileDirectory)
        # print("touchfile is set")
        for items in realnames:
            listbox.insert(0, items)
        for i in listofsongs:
            count = count + 1
        try:
            updatelabel()
        except NameError:
            print("")
 else:
    return 1

def call(event):
    try:
        #pygame.mixer.music.stop()
        k=directorychooser()
    except OSError as e:
        print(e.errno)
        print("thank you")

realnames.reverse()

songlabel.pack()



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


#myFile = open(path, 'a')
# csv_writer_append(["Media Time", "Sympathetic", "Fear", "Loving", "Anger", "Disgust", "Surprise","Other"], path + str(touchFile)+ "_Responses.csv")
def callback(in_data, frame_count, time_info, status):
    data = wave.readframes(frame_count)

    return (data, pyaudio.paContinue)
def play():
    global stream, isPlaying, initial_time
    isPlaying = True
    wave.rewind()
    stream = py_audio.open(format=py_audio.get_format_from_width(wave.getsampwidth()),
                       channels=wave.getnchannels(),
                       rate=wave.getframerate(),
                       output=True,
                       stream_callback = callback)

def stop():
    global stream, isPlaying
    print('in stop function')
    print ('is playing is ', isPlaying)
    if isPlaying:
        stream.stop_stream()
    isPlaying = False
    print('stopped')
    stream.close()

def pause():
    global difference, paused, isPlaying, stream_time, initial_time
    if paused:
        p_time = stream.get_time() - initial_time
        print('initial time is ', initial_time)
        difference = p_time - stream_time
        print('diference is ', difference)
        stream.start_stream()
        stream_time = stream.get_time() - initial_time - difference
        print('resume', stream_time )
        paused = False
        isPlaying = True
        return
    paused = True
    stream.stop_stream()
    isPlaying = False

def send_mode():
    global receive_Mode, path, touchFile, touchFileDirectory, directory
    receive_Mode = False
    print('sending mode')
    path= "intention_"
    touchFileDirectory = directory + "/" + path + str(touchFile)
    csv_writer(["Media Time,Sympathetic,Fear,Loving,Anger,Disgust,Surprise,Other"],touchFileDirectory)

def recv_mode():
    global receive_Mode, path, touchFile, directory, touchFileDirectory
    receive_Mode = True
    print('receiving mode')
    path = "perception_"
    touchFileDirectory = directory + "/" + path + str(touchFile)
    csv_writer(["Media Time,Sympathetic,Fear,Loving,Anger,Disgust,Surprise,Other"],touchFileDirectory)


sending = tk.Button(root, text = "send mode", command = send_mode)
sending.place(relx=.5, rely=1.5, anchor="center")
sending.pack()
recv = tk.Button(root, text = "receive mode", command = recv_mode)
recv.place(relx=.5, rely=1.5, anchor="center")
recv.pack()
load_button = tk.Button(root, text = "load settings", command = load_settings)
load_button.pack()
rec_data = []

demog()
while True:

    # a.encode('utf-8').strip()
    root.update()
    value = (input_serial.readline().decode())
    try:
        input_value = float(value) + offset
    except:
        value = (input_serial.readline().decode())
        input_value = float(value) + offset
    print(input_value)

    if receive_Mode == False:
        while isPlaying and replay is False:
            if stream.is_active():


                value = (input_serial.readline().decode())
                try:
                    input_value = float(value) + offset
                except:
                    value = (input_serial.readline().decode())
                    input_value = float(value) + offset
                print(input_value)
                if input_value <-3:
                    offset = offset -input_value
                    try:
                        input_value = float(value) + offset
                    except:
                        value = (input_serial.readline().decode())
                        input_value = float(value) + offset


                stream_time = (stream.get_time() - difference) - initial_time
                message =str(stream_time) + "," + str(input_value)
                message= message.replace("\n", "")
                rec_data.append(message)
                print('this is being appended ', message)
                print(touchFile)
                csv_writer(rec_data, touchFileDirectory2)
                root.update()
            else:

                stop()
                break


            #data = [time,input_value]
            #print(data)
            #csv_writer(data,'touches.csv')



        #server.send(message.encode())




    # server.close()
