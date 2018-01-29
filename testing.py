import serial, datetime, time, re, pickle, os, select, sys
import tkinter as tk
import numpy as np
from time import gmtime, strftime
#import plotly.plotly as py
#import plotly.graph_objs as go
import csv


start = time.time()
print(time.strftime("%H:%M:%S", time.localtime(start)))
count = 0
while True:
    if count < 1000000:
        count +=0.1
    else:
        break
end = time.time()
print(time.strftime("%H:%M:%S", time.localtime(end)))
elapsed = end - start
print('Time elapsed: ' + str(round(elapsed)))
