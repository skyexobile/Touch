import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv
'''
print("Connecting to Bean")
Bean_serial = serial.Serial('/tmp/cu.LightBlue-Bean')
Bean_serial.setBaudrate(9600)



input_value = "not number"
def read_beanInput():
    Bean_serial.flushInput()
    global input_value
    input_value= "not number"
    while not input_value.isdigit():
        input_value = str(Bean_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    return int(input_value)


print("Connecting to Load Cell")
input_serial = serial.Serial('/dev/cu.usbmodem1421')
input_serial.setBaudrate(38400)
'''
print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1421')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)
time.sleep(2.0)
data = {'SubID': "0", 'Cond': "0",'Input_Time': "0", 'Input_Value': "0", 'Output_Time': "0", 'Output_Value': "0", 'Elapsed_Time': "0", 'Duration': "0"}

'''
#calibration with squeeze device
def calibrate():
    Bean_serial.flushInput()

    input_value= "not number"
    while not input_value.isdigit():
        input_value = str(Bean_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    stop= int(input_value)


    release = 110
    stop_angle = 90
    s_angle = 80
    run = True
    then = int(strftime('%S'))
    cali_speed = 95
    global input_time

    while run:

        output_serial.write(str(cali_speed).encode())
        time.sleep(2)
        g= read_input()
        r = int(g/15) + 90

        if stop >= 110:
            input_time = int(strftime('%S'))
            print('Time: ' + str(datetime.datetime.now().time()))
            print('Other ',int(strftime('%S')))
            output_serial.write(str(stop_angle).encode())
            time.sleep(2)

            run = False
        print('read input is ', r, 'gram input is', g, 'stop is ', stop)

#Get data from input device ---------------------------------------
'''

def read_input():
    global timeBegin
    global flag
    global inputTime
    output_serial.flushInput()
    global input_value
    input_value = str(output_serial.readline().decode())
    lc = time.time()
    lc_time = time.strftime("%H:%M:%S", time.localtime(lc))
    if (input_value  == ' ' or input_value == '\0'):
        print("NULL")
        return
    else:

        if flag == True:
            strlen = len(input_value)
            new_val = input_value[:strlen-2]
            data['Output_Value'] = new_val
            data['Output_Time'] = lc_time
            duration = lc- inputTime
            data['Duration'] = str(round(duration))
            elapsed =  lc- timeBegin
            #change elapsed time in seconds
            data['Elapsed_Time'] =time.strftime("%H:%M:%S", time.localtime(elapsed))
            print(data)
            for key in data.keys():
                myFile.write(str(data[key])+",")
            flag = False
        print("read: ")
        print(input_value)

def soft_pulse():
    then = int(strftime('%S'))
    output_serial.write(str(94).encode())
    output_serial.flush()

def medium_pulse():
    then = int(strftime('%S'))
    output_serial.write(str(97).encode())
    output_serial.flush()

def hard_pulse():
    then = int(strftime('%S'))
    output_serial.write(str(100).encode())
    output_serial.flush()

def reset():
    output_serial.write("r".encode())
    output_serial.flush()
    time.sleep(2.0)

    output_serial.write("r".encode())
    output_serial.flush()

def tighten():
    print("Tightening..")
    output_serial.write("t".encode())
    output_serial.flush()
    time.sleep(2.0)


    output_serial.write("t".encode())
    output_serial.flush()



def stop():
    output_serial.write("s".encode())
    output_serial.flush()
    time.sleep(2.0)


    output_serial.write("s".encode())
    output_serial.flush()
def release():
    print("Releasing...")
    output_serial.write("l".encode())
    output_serial.flush()
    time.sleep(2.0)

    output_serial.write("l".encode())
    output_serial.flush()

def csv_writer(data, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow(value)

path = "Input_ST.csv"
'''
with open(path, 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for line in data.keys():
        writer.writerow(line)
input_value = "not number"
def read_input():
    Bean_serial.flushInput()
    global input_value
    input_value= "not number"
    while not input_value.isdigit():
        input_value = str(Bean_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    return int(input_value)'''
#calibrate()
#calibrate()
## For when you have input device

root = tk.Tk()

flag = False

B2 = tk.Button(root, text = "Release", command = release)
B2.place(relx=.5, rely=1.5, anchor="e")
B3 = tk.Button(root, text = "Tighten", command = tighten)
B3.place(relx=2.5, rely=1.5, anchor="w")
B4 = tk.Button(root, text = "Stop", command = stop)
B4.place(relx=.5, rely=2.5, anchor="center")
B5 = tk.Button(root, text = "Reset", command = reset)
B5.place(relx=2.5, rely=2.5, anchor="center")
B6 = tk.Button(root, text = "Soft", command = soft_pulse)
B6.place(relx=.5, rely=1.5, anchor="center")
B7 = tk.Button(root, text = "Medium", command = medium_pulse)
B7.place(relx=.5, rely=1.5, anchor="center")
B8 = tk.Button(root, text = "Hard", command = hard_pulse)
B8.place(relx=.5, rely=1.5, anchor="center")

B2.pack()
B3.pack()
B4.pack()
B5.pack()
B6.pack()
B7.pack()
B8.pack()

label1 = tk.Label(root, text = "Squeeze Amount")
E1 = tk.Entry(root, bd = 5)
label2 = tk.Label(root, text = "Subject ID")
E2 = tk.Entry(root, bd = 5)
label3 = tk.Label(root, text = "Condition")
E3 = tk.Entry(root, bd = 5)
def getAngle():
    global flag
    global inputTime
    angle = E1.get()
    #if angle.isdigit():

    output_serial.write(str(angle).encode())
    output_serial.flush()

    input_value = str(output_serial.readline().decode())
    print(input_value)
    #write to csv here
    data['Input_Value'] = str(angle)
    inputTime = time.time()
    in_Time =  time.strftime("%H:%M:%S", time.localtime(inputTime))
    data['Input_Time'] = in_Time
    if flag == False:
        flag = True
    else:
        flag = False
    E1.delete(0, tk.END)

def getSubID():
    subID= E2.get()
    if subID is None:
        subID = 0

    data['SubID'] = str(subID)
def getCond():
    condID = E3.get()
    if condID is None:
        condID = 0
    data['Cond']= str(condID)
def getAll():
    getSubID()
    getCond()
    getAngle()

submit = tk.Button(root, text="Enter", command = getAll)
label1.pack()
label2.pack()
label3.pack()
E1.pack()
E2.pack()
E3.pack()
submit.pack(side = tk.BOTTOM)
root.update()

myFile = open(path, 'a')
myFile.write(str(time.strftime("%X")))
print('Time: ' + str(time.strftime("%X")))
flag = False
timeBegin = time.time()

while True:

    read_input()

    root.update()
