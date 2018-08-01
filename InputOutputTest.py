import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv

print("Connecting to Load Cell")
input_serial = serial.Serial('/dev/cu.usbmodem1421')
input_serial.setBaudrate(115200)
input_serial.setDTR(False)
input_serial.setRTS(False)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)

output_serial.setDTR(False)
output_serial.setRTS(False)
mappingData = []
type = 0
typevalue = 0
acquired_flag = False
data = {'SubID': "0", 'Cond': "0",'Input_Time': "0", 'Input_Value': "0", 'Output_Time': "0", 'Output_Value': "0", 'Elapsed_Time': "0", 'Duration': "0"}
def read_input():
    global message
    global s_time
    #output_serial.flushInput()
    try:
        input_value = (input_serial.readline().decode())
        s_time = time.time()
        input_serial.flush()
        message = str(input_value)
        message= message.replace("\n", "")
        return (float(message))
        if (input_value  == ' ' or input_value == '\0'):
            print("NULL")
    except:
        pass
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
    global type
    time.sleep(1.5)
    sum = 0
    for i in (1, 6):
        sum = sum + read_input()
    average = sum/5
    type = average
    '''then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(50).encode())
    output_serial.flush()
    # 50 * 20ms = 1second
    time.sleep(2)
    output_serial.write(str(-50).encode())
    output_serial.flush()
    '''
def medium_pulse():
    global type
    time.sleep(1.5)
    sum = 0
    for i in (1, 6):
        sum = sum + read_input()
    average = sum/5
    type = average
    '''
    then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(60).encode())
    output_serial.flush()
    #60 * 20ms = 1.2 seconds
    time.sleep(2.2)
    output_serial.write(str(-60).encode())
    output_serial.flush()
    '''
def hard_pulse():
    global type
    time.sleep(1.5)
    sum = 0
    for i in (1, 6):
        sum = sum + read_input()
    average = sum/5
    type = average

    '''
    then = int(strftime('%S'))
    print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(75).encode())
    output_serial.flush()
    time.sleep(2.5)
    output_serial.write(str(-75).encode())
    output_serial.flush()
    '''
def release():
    output_serial.write(str(9).encode())
    output_serial.readline().decode()



def csv_writer(data, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow(value)

path = "Output_ST.csv"
myFile = open(path, 'a')

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
def Confirm():
    global steps, initial_squeeze, squeeze_amount, release_amount
    myFile.write(str(steps))
    myFile.write(",")
    myFile.write(str(initial_squeeze))
    myFile.write(",")
    myFile.write(str(squeeze_amount))
    myFile.write(",")
    myFile.write(str(release_amount))
    myFile.write('\n')

root = tk.Tk()

flag = False
init_flag = False

B = tk.Button(root, text = "Soft", command = soft_pulse)
B.place(relx=.5, rely=1.5, anchor="center")
B2 = tk.Button(root, text = "Medium", command = medium_pulse)
B2.place(relx=.5, rely=1.5, anchor="center")
B3 = tk.Button(root, text = "Release", command = release)
B3.place(relx=.5, rely=1.5, anchor="center")
B4 = tk.Button(root, text = "Confirm Map", command = Confirm)
B4.place(relx=.5, rely=1.5, anchor="center")
B4.pack()

B.pack()
B2.pack()
B3.pack()


label1 = tk.Label(root, text = "Squeeze Amount")
E1 = tk.Entry(root, bd = 5)
#label2 = tk.Label(root, text = "Subject ID")
#E2 = tk.Entry(root, bd = 5)

def Squeeze(s_value):
    global steps, initial_squeeze, squeeze_amount, release_amount
    initial_squeeze = read_input()
    print(initial_squeeze)
    steps = E1.get()
    if not steps:
        step_value = s_value
        print('no defined steps in input box')
    else:
        step_value = float(steps)
    #if angle.isdigit():
    #print('Time: ' + str(time.strftime("%X")))
    output_serial.write(str(step_value).encode())
    output_serial.flush()
    squeeze_amount = read_input()
    print(squeeze_amount)
    release_amount = read_input()
    print(release_amount)
    '''
    delay = abs(((steps * 20.0)/1000) + 1.0)
    val1 = read_input()
    val1 = val1.replace("\n", "")

    print(val1)
    #print(value1)
    time.sleep(delay)
    val2 = read_input()
    #print(val2)
    val2 = val2.replace("\n", "")


    output_serial.write(str(release).encode())
    output_serial.flush()
    '''
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
#label2.pack()
#E2.pack()
submit.pack(side = tk.BOTTOM)
root.update()
previous_read = -5000

while True:
    value = (input_serial.readline().decode())
    input_value = float(value)
    print(input_value)
    s_time = time.time()
    if( (input_value) >= 100 and (input_value) < 250 and not acquired_flag):
        #print(s_time)
        initial_read = (input_value)
        output_serial.write(str(1).encode())
        #print("initiate squeeze ", time.time())
        o_val = output_serial.readline().decode()
        #print(time.time())
        acquired_flag = True
    elif( (input_value) >= 250 and (input_value) <400 ):
        initial_read = (input_value)
        output_serial.write(str(2).encode())
        #print("initiate squeeze ", time.time())
        o_val = output_serial.readline().decode()
        #print(time.time())
    elif( (input_value) >= 400):
        initial_read = (input_value)
        output_serial.write(str(3).encode())
        #print("initiate squeeze ", time.time())
        o_val = output_serial.readline().decode()
        #print(time.time())
    elif(acquired_flag and (previous_read-15)> input_value):
        output_serial.write(str(0).encode())
        output_serial.readline().decode()

        #print(time.time())

        while(input_value >=30):
            value = (input_serial.readline().decode())
            input_value = float(value)


        input_serial.write(str(0).encode())

        print('ready')

        acquired_flag = False

    previous_read = input_value


    root.update()
