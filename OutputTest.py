import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
from tkinter import filedialog
import numpy as np
from time import gmtime, strftime
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
data = []
loaded = False
def release():
    output_serial.write(str(9).encode())
    output_serial.readline().decode()

def load_file():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("CSV files", "*.csv")])
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            data.append(', '.join(row))
def sample():
    output_serial.write(str(4).encode())
    output_serial.readline().decode()
    output_serial.write(str(5).encode())
    output_serial.readline().decode()
    output_serial.write(str(6).encode())
    output_serial.readline().decode()

def generate():
    global acquired_flag, soft_value, medium_value, hard_value
    previous_read = -5000
    for (input_value) in data:
        print("input value is ", float(input_value))
        if( float(input_value) >= soft_value-10 and float(input_value) < medium_value and not acquired_flag):
            print("soft squeeze")
            initial_read = (input_value)
            output_serial.write(str(1).encode())
            #we need to read dummy value after write.
            output_serial.readline().decode()
            acquired_flag = True
        elif( float(input_value) >= medium_value and float(input_value) <hard_value ):
            initial_read = (input_value)
            output_serial.write(str(2).encode())
            output_serial.readline().decode()
        elif( float(input_value) >= hard_value):
            initial_read = float(input_value)
            output_serial.write(str(3).encode())
            output_serial.readline().decode()
        elif(acquired_flag and (previous_read-15)> float(input_value)):
            output_serial.write(str(0).encode())
            output_serial.readline().decode()
            acquired_flag = False
        previous_read = float(input_value)

def csv_writer(data, path):
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data.items():
            writer.writerow(value)
def load_settings():
    global soft_value, medium_value, hard_value
    settings = []
    with open("Settings.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter = '\n')
        #Here is where you should be reading through the file and sending values to output serial
        for row in reader:
            settings.append(row[0])
    soft_value = settings[0]
    medium_value = settings[1]
    hard_value = settings[2]
path = "Output_ST.csv"
myFile = open(path, 'a')

root = tk.Tk()

flag = False
init_flag = False

B = tk.Button(root, text = "Release", command = release)
B1 = tk.Button(root, text = "Load File", command = load_file)
B2 = tk.Button(root, text = "Squeeze Playback", command = generate)
B3 = tk.Button(root, text = "Sample Squeezes", command = sample)
B.place(relx=.5, rely=1.5, anchor="center")
B1.place(relx=.5, rely=1.5, anchor="center")
B2.place(relx=.5, rely=1.5, anchor="center")
B3.place(relx=.5, rely=1.5, anchor="center")
B.pack()
B1.pack()
B2.pack()
B3.pack()
while True:
    root.update()
