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


'''

global input_serial

print("Connecting to Load Cell")
input_serial = serial.Serial('/dev/cu.usbmodem1421')
input_serial.setBaudrate(38400)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)
output_serial.setDTR(False)
output_serial.setRTS(False)

time.sleep(2.0)

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
    input_serial.flushInput()
    global input_value
    input_value = str(input_serial.readline().decode())
    print("READ: ", input_value)
    if (input_value  == ' ' or input_value == '\0'):
        print("NULL")
        return
    else:
        return float(input_value)

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

    return float(input_value)
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


def calibrate():
    release = 110
    stop_angle = 90
    s_angle = 80
    run = True
    then = int(strftime('%S'))
    cali_speed = 95
    global input_time

    while run:
        print("calibrating..")
        output_serial.write(str(cali_speed).encode())
        time.sleep(1)
        if read_input() >= 120:
            input_time = int(strftime('%S'))
            print('Time: ' + str(datetime.datetime.now().time()))
            print('Other ',int(strftime('%S')))
            output_serial.write(str(stop_angle).encode())
            run = False
        print('read input is ', read_input())
        #record load cell value
def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

path = "Input_ST.csv"
data = []

input_value = "not number"
'''def read_input():
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
B6 = tk.Button(root, text = "Soft", command = soft_pulse)
B6.place(relx=.5, rely=1.5, anchor="center")
B7 = tk.Button(root, text = "Medium", command = medium_pulse)
B7.place(relx=.5, rely=1.5, anchor="center")
B8 = tk.Button(root, text = "Hard", command = hard_pulse)
B8.place(relx=.5, rely=1.5, anchor="center")
B.pack()
B2.pack()
B3.pack()
B4.pack()
B5.pack()
B6.pack()
B7.pack()
B8.pack()
root.update()

print("moving...")
output_serial.write(str(80).encode())
output_serial.flush()

print('Time: ' + str(datetime.datetime.now().time()))

while True:

    root.update()

    #if while g <= threshold
    #initial calibration

    g= read_input()
    #r = int(g/15) + 90
    #print(r, g)
    if flag == False:

        if(g >80):

            print("Releasing...")
            output_serial.write(str(95).encode())
            output_serial.flush()
            time.sleep(2)
            output_serial.write(str(90).encode())
            output_serial.flush()
            input_serial.write("c".encode())
            input_serial.write("c".encode())
            input_serial.write("c".encode())

            flag = True

    if flag2 ==True:
        print("fit val is", fit_val)
        flag3= False
        medium_pulse()
        '''
        output_serial.write(str(95).encode())
        output_serial.flush()
        time.sleep(2)

        output_serial.write(str(90).encode())
        output_serial.flush()
        time.sleep(2)
        output_serial.write(str(85).encode())
        output_serial.flush()
        time.sleep(2)
        flag3 = False
        '''
        while True:
            root.update()


            g= read_input()

            print(g)
            print("fit val is", fit_val)

            if flag3 == False:
                print("DIFFERENCE", (fit_val-g))

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
                    flag3 = True
