# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:52:16 2019

@author: Ithan
"""

import csv
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter 


data=[]
ep=[]
re=[]
ti=[]
with open('bueno bueno y optimoMaestro3.csv', newline='') as File:  
    reader = csv.reader(File)
    
    for row in reader:
        data.append(row)
    
    del(data[0])
    
    for row in data:
         ep.append(int(row[0]))
         re.append(float(row[1]))
         ti.append(int(row[2]))
         if len(ep)>350:
             break
         

data=[]
ep2=[]
re2=[]
ti2=[]
with open('DNN-interactive-agenteIthan.csv', newline='') as File:  
    reader = csv.reader(File)
    
    for row in reader:
        data.append(row)
    
    del(data[0])
    
    for row in data:
        ep2.append(int(row[0]))
        re2.append(float(row[1]))
        ti2.append(int(row[2]))
        if len(re2)>350:
            break
         





yhat2 = savgol_filter(re2, 11,3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

yhat = savgol_filter(re, 11, 3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

#plt.plot(ep,re) 
plt.plot(ep,yhat, color='red') 
plt.plot(ep2,yhat2, color='blue') 

plt.show()


 
 
