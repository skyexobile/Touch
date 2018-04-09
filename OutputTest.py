import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv


print("Connecting to Load Cell")
input_serial = serial.Serial('/dev/cu.usbmodem1421')
input_serial.setBaudrate(38400)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)
time.sleep(2.0)
data = {'SubID': "0", 'Cond': "0",'Input_Time': "0", 'Input_Value': "0", 'Output_Time': "0", 'Output_Value': "0", 'Elapsed_Time': "0", 'Duration': "0"}
def read_input():
    input_serial.flushInput()

    input_value = str(input_serial.readline().decode())
    print("testing")

    print("READ: ", input_value)
    if (input_value  == ' ' or input_value == '\0'):
        print("NULL")
        return
    else:
        return float(input_value)
'''

def read_input():
    global timeBegin
    global flag
    global inputTime
    #input_serial.flushInput()
    global input_value
    input_value = str(input_serial.readline().decode())
    print("reading")

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
'''
def soft_pulse():
    then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(50).encode())
    output_serial.flush()
    # 50 * 20ms = 1second
    time.sleep(2)
    output_serial.write(str(-50).encode())
    output_serial.flush()
def medium_pulse():
    then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(60).encode())
    output_serial.flush()
    #60 * 20ms = 1.2 seconds
    time.sleep(2.2)
    output_serial.write(str(-60).encode())
    output_serial.flush()

def hard_pulse():
    then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(75).encode())
    output_serial.flush()
    time.sleep(2.5)
    output_serial.write(str(-75).encode())
    output_serial.flush()

def csv_writer(data, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow(value)

path = "Output_ST.csv"
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

B = tk.Button(root, text = "Soft", command = soft_pulse)
B.place(relx=.5, rely=1.5, anchor="center")
B2 = tk.Button(root, text = "Medium", command = medium_pulse)
B2.place(relx=.5, rely=1.5, anchor="center")
B3 = tk.Button(root, text = "Hard", command = hard_pulse)
B3.place(relx=.5, rely=1.5, anchor="center")

B.pack()
B2.pack()
B3.pack()


label1 = tk.Label(root, text = "Squeeze Amount")
E1 = tk.Entry(root, bd = 5)
label2 = tk.Label(root, text = "Subject ID")
E2 = tk.Entry(root, bd = 5)

def Squeeze():

    steps = float(E1.get())
    #if angle.isdigit():
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(steps).encode())
    output_serial.flush()
    delay = ((steps * 20.0)/1000) + 1.0
    print("delay", delay)
    time.sleep(delay)
    output_serial.write(str(-1 * steps).encode())
    output_serial.flush()
    E1.delete(0, tk.END)

def getSubID():
    subID= E2.get()
    if subID is None:
        subID = 0

    data['SubID'] = str(subID)

def getAll():
    getSubID()

submit = tk.Button(root, text="Enter", command = Squeeze)
label1.pack()
E1.pack()
label2.pack()
E2.pack()
submit.pack(side = tk.BOTTOM)
root.update()

myFile = open(path, 'a')
myFile.write(str(time.strftime("%X")))
print('Time: ' + str(time.strftime("%X")))
flag = False
timeBegin = time.time()

while True:
    #read_input()
    root.update()
