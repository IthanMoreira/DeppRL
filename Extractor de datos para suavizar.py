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
       'Data/DNN-interactive-humano-ConsueloMarchant.csv',
       'Data/DNN-interactive-humano-Ithan.csv',       
       'Data/DNN-interactive-humano-JavieraLuengo.csv',
       'Data/DNN-interactive-humano-karin.csv',
       'Data/DNN-interactive-humano-LuisMoreno.csv',
       'Data/DNN-interactive-humano-MatiasHuenchu.csv',
       'Data/DNN-interactive-humano-RebecaTello.csv',
       'Data/DNN-interactive-humano-yohan.csv']



ep=[]
re=[]
ti=[]
for x in lista:
    data1=[]
    ep1=[]
    re1=[]
    ti1=[]
    with open(x, newline='') as File:  
        reader = csv.reader(File)
        
        for row in reader:
            data1.append(row)
        
        del(data1[0])
        
        for row in data1:
             ep1.append(int(row[0]))
             re1.append(float(row[1]))
             ti1.append(int(row[2]))
             if len(ep)>350:
                 break    
        ep.append(ep1)
        re.append(savgol_filter(re1, 55,3))
        ti.append(ti1)    


plt.figure(figsize=(20,12))

plt.plot(ep[0],re[0],color="red" ,label="autonomo") 
plt.plot(ep[1],re[1],color="blue" , label="maestro-agente" ) 
plt.plot(ep[6],re[6] , label="maestro-humano1")
plt.plot(ep[7],re[7], label="maestro-humano2")
plt.plot(ep[4],re[4], label="maestro-humano3")
plt.plot(ep[9],re[9], label="maestro-humano4")
plt.legend(loc='lower right',fontsize='xx-large')
plt.xlabel("Episodios",fontsize='xx-large')   # Establece el título del eje x
plt.ylabel("Recompensa",fontsize='xx-large')   # Establece el título del eje y

plt.show()





'''


yhat2 = savgol_filter(re2, 9,3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

yhat = savgol_filter(re, 9, 3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

#plt.plot(ep,re) 
plt.plot(ep,yhat, color='red') 
plt.plot(ep2,yhat2, color='blue') 

plt.show()
'''

 
 
