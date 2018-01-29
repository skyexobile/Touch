import socket
import threading
import time
import tkinter as tk
import datetime
import pyaudio
import wave
import pygame

def listen(filename):
    start = 0
    length = 1

    # initialize audio
    wave2 = wave.open(filename, 'rb')
    py_audio = pyaudio.PyAudio()
    chan = wave2.getnchannels()
    frate = wave2.getframerate()
    swidth = wave2.getsampwidth()

    stream = py_audio.open(format=py_audio.get_format_from_width(wave2.getsampwidth()),channels=wave2.getnchannels(), rate=wave2.getframerate(),output=True)

    # skip unwanted frames
    n_frames = int(start * wave2.getframerate())
    wave2.setpos(n_frames)

    # write desired frames to audio buffer
    n_frames = int(length * wave2.getframerate())
    frames = wave2.readframes(n_frames)
    stream.write(frames)

    # close and terminate everything properly
    wave2.close()
    stream.close()
    py_audio.terminate()
class Win(tk.Tk):

    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y
root = Win()

def Change(c):
    if "c" != "":
        window = tk.Toplevel(root)

        window.attributes('-fullscreen', True)

        try:
            t2 = threading.Thread(target = listen, args=["boop.wav"])
            t2.daemon = True
            t2.start()
        except:
            print("unable to start thread")

        window.config(bg = c.decode("utf-8"))

        window.after(1000, window.update())

        try:
            t2 = threading.Thread(target = listen, args=["boop.wav"])
            t2.daemon = True
            t2.start()
        except:
            print("unable to start thread")

        window.config(bg = c.decode("utf-8"))

        window.after(1000, window.update())



        window.config(bg = c.decode("utf-8"))

        try:
            t2 = threading.Thread(target = listen, args=["output.wav"])
            t2.daemon = True
            t2.start()
        except:
            print("unable to start thread")
        window.after(500, window.update())

        window.config(bg = "white")

        print( datetime.datetime.now().time())

        window.after(500, window.update())






        #white clap window.after(500, window.update())
        #window.after(1000), window.update()

        #white clap listen()
        window.destroy()
        #window.update()
    if b_pressed == True:
        s.sendto("end".encode(), server)
        Close()


def Close():

    root.destroy()

def initiate():

    global b_pressed
    b_pressed = True


    print('button has been pressed')
    s.sendto("black".encode(), server)

host = 'localhost'
port = 0


server = ('localhost',5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.sendto("init".encode(), server)
global b_pressed
shutdown = False
b_pressed =  False
while True:
    data, addr = s.recvfrom(1024)
    d = data.decode("utf-8")
    if d != "init":
        print('Received ', d)
    else:
        print('no data')
    print(' > ')

    B = tk.Button(root, text ="Flash", command = initiate)
    B.pack()
    B.place(relx=.5, rely=.5, anchor="center")


    root.overrideredirect(True)
    root.overrideredirect(False)
    print('window ready')
    s.sendto("init2".encode(), server)
    while True:
        data, addr = s.recvfrom(1024)
        d = data.decode("utf-8")
        if d != "init2":
            print('Received ', d)
            if d == "black":
                Change(data)
            if d == "end":
                s.close()
                Close()


        else:
            root.update()
            s.sendto("init2".encode(), server)

s.close()
