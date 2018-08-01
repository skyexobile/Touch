import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk

#input_serial = serial.Serial('/dev/cu.usbmodem1421')
#input_serial.setBaudrate(115200)
print("Connected to Sensor")
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])server.connect(("localhost", 5000))
'''

root = tk.Tk()
label1 = tk.Label(root, text = "Calibration")


def getCali():
    input_serial.write(str("9").encode())
B =  tk.Button(root, text = "Calibrate", command = getCali)

B.pack(side = tk.BOTTOM)
root.update()
while True:

    input_value = (input_serial.readline().decode())
    message = str(input_value)
    message= message.replace("\n", "")
    server.send(message.encode())
    root.update()

server.close()
