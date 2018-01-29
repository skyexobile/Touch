# telnet program example
import socket, select, string, sys, serial, datetime, time as timer, re, pickle, os, re

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', dest='output_enabled', action='store_true', default=False)
parser.add_argument('--input', dest='input_enabled', action='store_true', default=False)
parser.add_argument('--ip', action="store", dest="ip",default='127.0.0.1')
parser.add_argument('--port', action="store", dest="port",default='5000')
parameters = parser.parse_args()

def load_configuration():
    with open('objs.pickle','br') as f:
        global output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input
        output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input = pickle.load(f)
    print("File Loaded")

model = make_pipeline(PolynomialFeatures(2), Ridge())
def train():
    X = np.array([[np.average(input_light_values.astype(np.float))],[np.average(input_medium_values.astype(np.float))],[np.average(input_hard_values.astype(np.float))]])
    y = np.array([[np.average(output_light_values.astype(np.float)),np.average(output_medium_values.astype(np.float)),np.average(output_hard_values.astype(np.float))]]).ravel()
    print(X)
    print(y)
    global model
    model.fit(X,y)

if parameters.input_enabled:
    print("Connecting to Input Device")
    input_serial = serial.Serial('/dev/cu.Bluetooth-Incoming-Port')
if parameters.output_enabled:
    print("Connecting to Output Device")
    output_serial = serial.Serial('/dev/cu.usbmodem1421')
    output_serial.setBaudrate(115200)
    output_serial.dsrdtr=False
    output_serial.setDTR(level=False)
    timer.sleep(2)

input_value = "not number";
def read_input():
    #Get data from input device
    input_serial.flushInput()
    global input_value
    input_value = "not number"
    while not input_value.isdigit():
        input_value = str(input_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    #print('Time: ' + str(datetime.datetime.now().time()))
    print(input_value)

#Send commands to output device ---------------------------------------
home_time =0
time = home_time

def move_servo_to_time():
    global time, output_serial
    send_time = str(time)+"\n";
    output_serial.write(send_time.encode())
    print("moving to: "+send_time)
    output_serial.flush()

def move_servo(d_time):
    global time
    time = time + d_time
    move_servo_to_time()

if parameters.output_enabled:
    move_servo_to_time()

def translate_message(connected_input_value):
    #fit input within bounds of max/min
    global max_input,min_input
    int_input = int(connected_input_value)
    if int_input > max_input:
        int_input = max_input
    elif int_input < min_input:
        int_input = min_input

    #model input to output
    global model
    output_time = model.predict(int_input)
    print("P time: "+str(output_time))

    #fit input within bounds of max/min
    global max_output,min_output
    if int(output_time) > max_output:
        output_time = max_output
    min_bound = home_time
    if int(output_time) < min_bound:
        output_time = min_bound

    print("Input Force: "+str(input_value))
    global time
    time = int(output_time)
    move_servo_to_time()

#message handling   ----------------------------------------

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def remove_text_inside_brackets(text):
    return re.sub(r'<.+?>', '', text)

#main function --------------
if __name__ == "__main__":
    host = parameters.ip
    port = int(parameters.port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # connect to remote host
    try :
        s.connect((host, port))
    except Exception as e:
        print('Unable to connect with server')
        print(e)
        sys.exit()

    print('Connected to remote host. Start sending messages')

    # connect to local devices
    load_configuration()
    train()

    while 1:
        timer.sleep(0.2)
        if parameters.input_enabled:
            read_input()
            try:
                s.send((str(input_value)+"\n").encode())
            except socket.error as e:
                print("Didn't send ")
                print(e)
        socket_list = [sys.stdin, s]
        
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                try:
                    data = sock.recv(4096)
                except socket.error:
                    print("Didn't Receive")
                    break
                if str(data)=="exit" :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    #sys.stdout.write(str(data)+"\n")
                    #prompt()
                    #data = str(data)[2:]
                    #print("Received:"+str(data))
                    msg = remove_text_inside_brackets(str(data))[2:]
                    msg = msg[:-3]
                    #print("Trimmed: "+msg)
                    try:
                        input = int(msg)
                        print(input)
                        if parameters.output_enabled:
                            translate_message(input)
                    except ValueError:
                        #Handle the exception
                        print(' ')
            #user entered a message
            #else :
            #    msg = sys.stdin.readline()
            #    s.send(msg.encode())
            #    prompt()
