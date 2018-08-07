import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk
import csv
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

def reset():
    input_serial.write(str("0").encode())
def set_soft():
    offset = 0
    value_list = []
    max_list = []
    global soft_value
    counter = 0
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            elapsed_time = time.time() - init_time
            input_value = float(value) + offset
        if input_value > 50:
            while input_value >20:
                value_list.append(input_value)
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
    global med_value
    counter = 0
    while counter <3:
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            elapsed_time = time.time() - init_time
            input_value = float(value) + offset
        if input_value > 50:
            while input_value >20:
                value_list.append(input_value)
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
        value = (input_serial.readline().decode())
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            elapsed_time = time.time() - init_time
            input_value = float(value) + offset
        if input_value > 50:
            while input_value >20:
                value_list.append(input_value)
            index = value_list.index(max(value_list))
            max_list.append(value_list[index])
            max_list.append(value_list[index+1])
            max_list.append(value_list[index+2])
            max_list.append(value_list[index+3])
            counter = counter +1
        elif input_value < -20:
            offset = offset - input_value
    hard_value = sum(max_list)/len(max_list)
def save_settings():
    global soft_value, med_value, hard_value
    data = [soft_value, med_value, hard_value]
    csv_writer(data, "Settings.csv")

def record():
    init_time = time.time()
    offset = 0
    while True:
        value = (input_serial.readline().decode())
        elapsed_time = time.time() - init_time
        try:
            input_value = float(value) + offset
        except:
            value = (input_serial.readline().decode())
            elapsed_time = time.time() - init_time
            input_value = float(value) + offset
        if input_value <-20:
            offset = offset -input_value
            try:
                input_value = float(value) + offset
            except:
                value = (input_serial.readline().decode())
                elapsed_time = time.time() - init_time
                input_value = float(value) + offset
        message ='{:.2f}'.format(elapsed_time) + "," + str(input_value)
        message= message.replace("\n", "")
        data.append(message)
        print(message)
        csv_writer(data, path)
        root.update()
B =  tk.Button(root, text = "Reset Sensor", command = reset)
B2 =  tk.Button(root, text = "Record", command = record)
B3  =  tk.Button(root, text = "Define Soft", command = set_soft)
B4  =  tk.Button(root, text = "Define Medium", command = set_medium)
B5  =  tk.Button(root, text = "Define Hard", command = set_hard)
B6  =  tk.Button(root, text = "Save Settings", command = save_settings)

B.pack(side = tk.BOTTOM)
B2.pack(side = tk.BOTTOM)
B3.pack(side = tk.BOTTOM)
B4.pack(side = tk.BOTTOM)
B5.pack(side = tk.BOTTOM)
B6.pack(side = tk.BOTTOM)
root.update()
aquired_flag = False
message = "0"
previous_read = -5000
path = "Input_Values.csv"
data = []
def csv_writer(data, path):
    with open(path, "w", newline = '') as csv_file:
        writer = csv.writer(csv_file, delimiter = ' ')
        for value in data:
            csv_file.write(value + '\n')
        csv_file.close()

while True:
    root.update()
