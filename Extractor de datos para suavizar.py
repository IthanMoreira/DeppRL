# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:52:16 2019

@author: Ithan
"""

import csv
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter 

lista=['Data/bueno bueno y optimoMaestro3.csv',
       'Data/DNN-interactive-agenteIthan.csv',
       'Data/DNN-interactive-humano-CamilaHuenchu.csv',
       'Data/DNN-interactive-humano-CamilaNavarro.csv',
       'Data/DNN-interactive-humano-ConsueloCelis.csv',
       'Data/DNN-interactive-humano-ConsueloMarchant.csv',
       'Data/DNN-interactive-humano-Ithan.csv',
       'Data/DNN-interactive-humano-Javier.csv',
       'Data/DNN-interactive-humano-JavieraLuengo.csv',
       'Data/DNN-interactive-humano-karin.csv',
       'Data/DNN-interactive-humano-LuisMoreno.csv',
       'Data/DNN-interactive-humano-MatiasHuenchu.csv',
       'Data/DNN-interactive-humano-RebecaTello.csv',
       'Data/DNN-interactive-humano-yohan.csv']








'''


yhat2 = savgol_filter(re2, 9,3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

yhat = savgol_filter(re, 9, 3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

#plt.plot(ep,re) 
plt.plot(ep,yhat, color='red') 
plt.plot(ep2,yhat2, color='blue') 

plt.show()
'''

 
 
