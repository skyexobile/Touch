import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv

global input_serial

print("Connecting to Load Cell")
input_serial = serial.Serial('/dev/cu.usbmodem1411')
input_serial.setBaudrate(115200)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)
output_serial.setDTR(False)
output_serial.setRTS(False)

time.sleep(2.0)

def soft_pulse():
    release = 80
    stop_angle = 90
    s_angle = 100
    then = int(strftime('%S'))
    output_serial.write(str(83).encode())
    output_serial.flush()
    time.sleep(2)

    output_serial.write(str(95).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)
def medium_pulse():
    release = 80
    stop_angle = 90
    s_angle = 100
    then = int(strftime('%S'))
    output_serial.write(str(80).encode())
    output_serial.flush()
    time.sleep(2)

    output_serial.write(str(100).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)
def hard_pulse():
    release = 80
    stop_angle = 90
    s_angle = 100
    then = int(strftime('%S'))
    output_serial.write(str(75).encode())
    output_serial.flush()
    time.sleep(2)

    output_serial.write(str(100).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)
def mark():
    print("MARKED", read_input())
def tighten():
    print("Tightening..")
    print('Time: ' + str(datetime.datetime.now().time()))

    output_serial.write(str(80).encode())
    output_serial.flush()

def stop():
    print('Time: ' + str(datetime.datetime.now().time()))

    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2.0)
    print("Stopped")
def release():
    print("Releasing...")
    output_serial.write(str(95).encode())
    output_serial.flush()

def getValue():
    global flag2
    global fit_val
    flag2 = False
    output_serial.write(str(90).encode())
    output_serial.flush()
    fit_val = read_input()
    print('Time: ' + str(datetime.datetime.now().time()))
    print('Fit Value is ', fit_val)
    flag2 = True

def read_input():
    input_serial.flushInput()
    global input_value
    input_value = str(input_serial.readline().decode())
    print("READ: ", input_value)
    if (input_value  == ' ' or input_value == '\0'):
        print("NULL")
        return

    return float(input_value)
def tare():
    input_serial.write("c".encode())

def reset():
    output_serial.write(str(83).encode())
    output_serial.flush()
    g = read_input()
    if((fit_val-g)<=3.0):
        print(fit_val-g)
        print("close to fit value")
        output_serial.write(str(90).encode())
        output_serial.flush()
        time.sleep(2)
        if (g==fit_val):
            print("DONE")
        elif(g > fit_val):
            output_serial.write(str(95).encode())
            output_serial.flush()
            time.sleep(1)
            output_serial.write(str(90).encode())
            output_serial.flush()

        elif(g< fit_val):
            output_serial.write(str(85).encode())
            output_serial.flush()
            time.sleep(1)
            output_serial.write(str(90).encode())
            output_serial.flush()


root = tk.Tk()

flag2 =False

flag = False
B = tk.Button(root, text="Set Fit", command = getValue)

B.place(relx=.5, rely=.5, anchor="center")
B2 = tk.Button(root, text = "Release", command = release)
B2.place(relx=.5, rely=1.5, anchor="e")
B3 = tk.Button(root, text = "Tighten", command = tighten)
B3.place(relx=2.5, rely=1.5, anchor="w")
B4 = tk.Button(root, text = "Stop", command = stop)
B4.place(relx=.5, rely=2.5, anchor="center")
B5 = tk.Button(root, text = "Mark", command = mark)
B5.place(relx=2.5, rely=2.5, anchor="center")
B6 = tk.Button(root, text = "Tare", command = tare)
B6.place(relx=2.5, rely=2.5, anchor="center")

B.pack()
B2.pack()
B3.pack()
B4.pack()
B5.pack()
B6.pack()
label1 = tk.Label(root, text = "Rotation Angle")
E1 = tk.Entry(root, bd = 5)

def getAngle():
    angle = E1.get()
    if angle.isdigit():
        output_serial.write(str(angle).encode())
        output_serial.flush()
        time.sleep(2)
        read_input()

        output_serial.write(str(100).encode())
        output_serial.flush()
        time.sleep(1)
        read_input()
        output_serial.write(str(90).encode())
        output_serial.flush()
        time.sleep(2)
        print(angle)

    E1.delete(0, tk.END)
submit = tk.Button(root, text="Enter", command = getAngle)

label1.pack()
E1.pack()
submit.pack(side = tk.BOTTOM)

root.update()

while True:
    #read_input()
    root.update()
