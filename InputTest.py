import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk

input_serial = serial.Serial('/dev/cu.usbmodem1411')
input_serial.setBaudrate(115200)
print("Connected to Sensor")
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
'''

root = tk.Tk()
label1 = tk.Label(root, text = "Calibration")


def getCali():
    input_serial.write(str("0").encode())
B =  tk.Button(root, text = "Calibrate", command = getCali)

B.pack(side = tk.BOTTOM)
root.update()
aquired_flag = False
previous_read = -5000
message = "0"
while True:
    if not aquired_flag:
        value = (input_serial.readline().decode())
        input_value = float(value)
        if input_value >= previous_read:
            message = str(input_value)
            message= message.replace("\n", "")
            previous_read = input_value
        else:
            acquired_flag = True
            message = "0"
            while(acquired_flag and input_value >= 30):
                value = (input_serial.readline().decode())
                input_value = float(value)
                input_serial.write(str("0").encode())
                input_serial.readline().decode()
                # server.send(message.encode())
            print('ready')
            acquired_flag = false
        #server.send(message.encode())
    root.update()

server.close()
