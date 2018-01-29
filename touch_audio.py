import pyaudio
import wave
import wave
import datetime
from time import gmtime, strftime
import csv


from tkinter import *
CHUNK = 1024 #arbitrarily chosen size of buffer
FORMAT = pyaudio.paInt16 #size of each sample is 2 bytes
CHANNELS = 2 #each frame has 2 audio channels--stereo
RATE = 44100 #number of samples in a frame per sec
RECORD_SECONDS = 5 #duration of audio file
FILENAME = "clip.wav"


def record():
    p = pyaudio.PyAudio()
    

    stream = p.open(format=FORMAT,channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK) #buffer

    print("Recording in progress")

    frames = []
    times = ["Start"]
    
    hours = (int(strftime('%H')) * 3600)
    minutes = (int(strftime('%M')) * 60)
    seconds = (int(strftime('%S')))
    total_time = (hours + minutes + seconds)
    times.append(total_time)
    print(times)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #how many iterations
        dt = datetime.datetime.today()
        print(dt.timestamp())
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes per channel

    print("Recording Finished!")
    stream.stop_stream()
    stream.close()
    with open("Recording_ST.csv", "a") as f:
        writer = csv.writer(f, lineterminator='\n')
        for val in times:
            writer.writerow([val])
    p.terminate()

    w_file= wave.open(FILENAME, 'wb')
    w_file.setnchannels(CHANNELS)
    w_file.setsampwidth(p.get_sample_size(FORMAT))
    w_file.setframerate(RATE)
    w_file.writeframes(b''.join(frames))
    w_file.close()

def listen():

    if e1.get() is not None:
    
        start = int(e1.get())
    else:
        start = input_time
    length = int(e2.get())
    filename = str(e3.get())
    # open wave file
    wave2 = wave.open('clip.wav', 'rb')

    # initialize audio
    py_audio = pyaudio.PyAudio()
    chan = wave2.getnchannels()
    frate = wave2.getframerate()
    swidth = wave2.getsampwidth()
    
    stream = py_audio.open(format=py_audio.get_format_from_width(wave2.getsampwidth()),channels=wave2.getnchannels(), rate=wave2.getframerate(),output=True)

    # skip unwanted frames
    n_frames = int(start * wave2.getframerate())
    wave2.setpos(n_frames)
    w_file2 = wave.open(filename + '.wav', 'wb')
    w_file2.setnchannels(chan)
    w_file2.setsampwidth(swidth)

    w_file2.setframerate(frate)

    # write desired frames to audio buffer
    n_frames = int(length * wave2.getframerate())
    frames = wave2.readframes(n_frames)
    stream.write(frames)
    w_file2.writeframes(frames)
    w_file2.close()

    # close and terminate everything properly
    wave2.close()
    stream.close()
    py_audio.terminate()


master = Tk()
Label(master, text="Start").grid(row=0)
Label(master, text="Duration").grid(row=1)
Label(master, text="New Filename").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row = 2, column =1)

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Listen', command=listen).grid(row=3, column=1, sticky=W, pady=4)
Button(master, text='Record', command=record).grid(row=5, column=1, sticky=W, pady=4)

mainloop( )
