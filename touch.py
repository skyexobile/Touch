import serial, datetime, time, re, pickle, os, select, sys
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import numpy as np

#import plotly.plotly as py
#import plotly.graph_objs as go

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

#Connect to Devices -----------------------------------------
print("Connecting to Touch Input")
input_serial = serial.Serial('/tmp/cu.LightBlue-Bean')
input_serial.setBaudrate(9600)

print("Connecting to Touch Output")
output_serial = serial.Serial('/dev/cu.usbmodem1421')
output_serial.setBaudrate(115200)
output_serial.setDTR(False)
output_serial.setRTS(False)
time.sleep(2.0)

#Get data from input device ---------------------------------------
input_value = "not number";
def read_input():
    input_serial.flushInput()
    global input_value
    input_value = "not number"
    while not input_value.isdigit():
        input_value = str(input_serial.readline())
        input_value = input_value[2:-5]
    #output results to console
    print('Time: ' + str(datetime.datetime.now().time()))
    print(input_value)


#Send command to output device ---------------------------------------
home_angle =0
angle = home_angle

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

move_servo_to_angle()#starting position,
                     #  optional: comment out if arduino is guaranteed to be reset

#Controller to Configuration ---------------------------------
#input
input_light_values = np.array([])
input_medium_values = np.array([])
input_hard_values = np.array([])

min_input = 99999999999999
max_input = -1

def input_store(touch_type):
    global input_value
    read_input()
    if touch_type == "light":
        global input_light_values
        input_light_values = np.append(input_light_values,input_value)
        print(input_light_values)
    elif touch_type == "medium":
        global input_medium_values
        input_medium_values = np.append(input_medium_values,input_value)
        print(input_medium_values)
    elif touch_type == "hard":
        global input_hard_values
        input_hard_values = np.append(input_hard_values,input_value)
        print(input_hard_values)

    global min_input,max_input
    int_input = int(input_value)
    if int_input > max_input:
        max_input = int_input
    if int_input < min_input:
        min_input = int_input

#output
output_light_values = np.array([])
output_medium_values = np.array([])
output_hard_values = np.array([])

min_output = 99999999999999
max_output = -1

def output_store(touch_type):
    global angle
    if touch_type == "light":
        global output_light_values
        output_light_values = np.append(output_light_values,angle)
        print(output_light_values)
    elif touch_type == "medium":
        global output_medium_values
        output_medium_values = np.append(output_medium_values,angle)
        print(output_medium_values)
    elif touch_type == "hard":
        global output_hard_values
        output_hard_values = np.append(output_hard_values,angle)
        print(output_hard_values)

    global min_output,max_output
    if angle > max_output:
        max_output = angle
    if angle < max_output:
        min_output = angle

# input into output ----------------------
model = make_pipeline(PolynomialFeatures(2), Ridge())
def train():
    X = np.array([[np.average(input_light_values.astype(np.float))],[np.average(input_medium_values.astype(np.float))],[np.average(input_hard_values.astype(np.float))]])
    y = np.array([[np.average(output_light_values.astype(np.float)),np.average(output_medium_values.astype(np.float)),np.average(output_hard_values.astype(np.float))]]).ravel()
    print(X)
    print(y)
    global model
    model.fit(X,y)

    #py.sign_in('anberman', '51a3nj2fos')
    
    #x_plot = np.arange(0,np.amax(X),.01)
    #y_plot = model.predict(x_plot.reshape(-1, 1))
    #trace = go.Scatter(
    #    x = x_plot,
    #    y = y_plot
    #)
    #data = [trace]
    #py.iplot(data, filename='basic-line')

def translate():
    print("------------------------")
    read_input()
    global input_value
    #fit input within bounds of max/min
    global max_input,min_input
    int_input = int(input_value)
    if int_input > max_input:
        int_input = max_input
        print("MAX INPUT: "+str(max_input))
    elif int_input < min_input:
        int_input = min_input
        print("MIN INPUT: "+str(min_input))

    #model input to output
    global model
    output_angle = model.predict(int_input)
    print("P angle: "+str(output_angle))

    #fit input within bounds of max/min
    global max_output,min_output
    if int(output_angle) > max_output:
        output_angle = max_output
        print("MAX OUTPUT")
    min_bound = home_angle
    if int(output_angle) < min_bound:
        output_angle = min_bound
        print("MIN OUTPUT")

    print("Input Force: "+str(input_value))
    global angle
    angle = int(output_angle)
    move_servo_to_angle()

#file IO --------------------------------------------

def save():
    with open('objs.pickle','bw') as f:
        global output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input
        pickle.dump([output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input],f);
    print("File Saved")

def load():
    with open('objs.pickle','br') as f:
        global output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input
        output_light_values,output_medium_values,output_hard_values,min_output,max_output,input_light_values,input_medium_values,input_hard_values,min_input,max_input = pickle.load(f)
    print("File Loaded")

#GUI ---------------------------------------------------------
class App:
    def run(self):
        root.destroy()
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Devices are synced to each other. Press Enter to stop me!")
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                output_serial.close()
                input_serial.close()
                break

            translate()
            time.sleep(0.9)
            
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        #==== input
        self.input_label = Label(frame,
                                 text="Input Device").grid(row=0,column=1)
        
        self.input_light_button = Button(frame,
                                         text="Light",
                                         command=lambda: input_store("light")).grid(row=1,column=0)
        
        self.input_medium_button = Button(frame,
                                          text="Medium",
                                          command=lambda: input_store("medium")).grid(row=1,column=1)
        
        self.input_hard_button = Button(frame,
                                        text="Hard",
                                        command=lambda: input_store("hard")).grid(row=1,column=2)
        #==== output
        self.output_label = Label(frame,
                                 text="Output Device").grid(row=2,column=1)
            
        self.tighten_button = Button(frame,
                                    text="loosen",
                                    command=lambda: move_servo(-90)).grid(row=3,column=0)
                                    
        self.loosen_button = Button(frame,
                                    text="tighten",
                                    command=lambda: move_servo(90)).grid(row=3,column=2)
        
        self.output_light_button = Button(frame,
                                   text="Light",
                                   command=lambda: output_store("light")).grid(row=4,column=0)
                                 
        self.output_medium_button = Button(frame,
                                    text="Medium",
                                    command=lambda: output_store("medium")).grid(row=4,column=1)
                                 
        self.output_hard_button = Button(frame,
                                  text="Hard",
                                  command=lambda: output_store("hard")).grid(row=4,column=2)

        #==== control
        self.control_label = Label(frame,
                                  text="Controls").grid(row=5,column=1)
        self.train_button = Button(frame,
                                   text="train",
                                   command=train).grid(row=6,column=0)
        self.train_button = Button(frame,
                                   text="translate",
                                   command=translate).grid(row=6,column=1)
        self.run_button = Button(frame,
                                 text="run",
                                 command=self.run).grid(row=6,column=2)

        #==== file IO
        self.filler_label = Label(frame,
                                  text=" ").grid(row=7,column=0)
        self.file_label = Label(frame,
                                text="Files").grid(row=8,column=1)
        self.train_button = Button(frame,
                                   text="save settings",
                                   command=save).grid(row=9,column=0)
        self.train_button = Button(frame,
                                   text="load settings",
                                   command=load).grid(row=9,column=2)


root = Tk()
app = App(root)
root.wm_title("Touch Controls")
root.mainloop()
