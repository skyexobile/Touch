import serial, datetime, time, re, pickle, os, select, sys
import numpy as np
from time import gmtime, strftime
import socket
import tkinter as tk

input_serial = serial.Serial('/dev/cu.usbmodem18')
input_serial.setBaudrate(38400)
print("Connected to Sensor")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])
server.connect(("localhost", 5000))

start = time.time()
data = []
root = tk.Tk()
label1 = tk.Label(root, text = "Calibration")


def getCali():
    input_serial.write(str("9").encode())
B =  tk.Button(root, text = "Calibrate", command = getCali)

B.pack(side = tk.BOTTOM)
root.update()
while True:

    end = time.time()
    input_value = (input_serial.readline().decode('utf-8').replace('\n',''))
    input_serial.flush()
    elapsed = abs(end - start)


    if elapsed >= 0.01: #10ms
        start = end
        message = str(input_value)
        #print(message)
        server.send(message.encode())
    root.update()

server.close()
