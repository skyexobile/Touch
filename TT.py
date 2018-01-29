import serial, datetime, time, re, pickle, os, select, sys
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
print("Connecting to Touch Input")

input_serial = serial.Serial('/tmp/cu.LightBlue-Bean')
input_serial.setBaudrate(9600)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1411')
output_serial.setBaudrate(115200)
output_serial.setDTR(False)
output_serial.setRTS(False)
time.sleep(2.0)


#Send command to output device ---------------------------------------
home_angle =0
angle = home_angle
val = 0
input_time = 0

#Get data from input device ---------------------------------------
input_value = "not number"
def read_input():
    input_serial.flushInput()
    global input_value
    input_value= "not number"
    while not input_value.isdigit():
        input_value = str(input_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    return int(input_value)

def move_servo_to_angle():
    global angle
    send_angle = str(angle)
    output_serial.write(send_angle.encode())
    print("moving to: "+send_angle)
    output_serial.flush()

def move_servo(d_angle):
    global angle
    angle = angle + d_angle
    move_servo_to_angle()

release = 110
stop_angle = 90
s_angle = 80
run = True
then = int(strftime('%S'))
cali_speed = 84

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

def soft_pulse():
    release = 80
    stop_angle = 90
    s_angle = 100
    run = True
    then = int(strftime('%S'))
    output_serial.write(str(98).encode())
    output_serial.flush()
    time.sleep(2)

    output_serial.write(str(80).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)



def medium_pulse():
    output_serial.write(str(103).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(80).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)


def hard_pulse():
    output_serial.write(str(110).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(80).encode())
    output_serial.flush()
    time.sleep(1)
    output_serial.write(str(90).encode())
    output_serial.flush()
    time.sleep(2)


#time.sleep(2)
#soft_pulse()
medium_pulse()
time.sleep(2)
calibrate()
medium_pulse()
#hard_pulse()
'''
output_serial.write(str(80).encode())
output_serial.flush()
time.sleep(1)
output_serial.write(str(90).encode())

'''
while True:
    if read_input() > 20:
        medium_pulse()

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)
path = "Input_ST.csv"
data = []
