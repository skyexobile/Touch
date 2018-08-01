import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv



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

root = tk.Tk()

flag = False
init_flag = False

B = tk.Button(root, text = "Release", command = release)
B.place(relx=.5, rely=1.5, anchor="center")
B.pack()

root.update()
previous_read = -5000

while True:
    input_value =0
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
