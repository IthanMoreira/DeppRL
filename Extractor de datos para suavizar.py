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
       'Data/DNN-interactive-humano-yohan.csv',
       'Data/DNN-interactive-humano-ConsueloCelis.csv']



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
      



f = plt.figure(1)   
plt.rcParams.update({'font.size': 14})

plt.plot(ep[0],re[0],color="red" ,label="autonomous DeepRL",linestyle = '-') 
#plt.plot(ep[1],re[1],color="blue" , label="agent-IDeepRL" , linestyle = '-')
 
plt.plot(ep[6],re[6] , label="human-IDeepRL1",linestyle = '-',color='green')
#plt.plot(ep[7],re[7], label="human-IDeepRL2",linestyle = '-')
#plt.plot(ep[4],re[4], label="human-IDeepRL1",linestyle = '-')
#plt.plot(ep[9],re[9], label="human-IDeepRL4",linestyle = '-',color='y')
#plt.plot(ep[10],re[10], label="human-IDeepRL5",linestyle = '-',color='r')
plt.plot(ep[2],re[2], label="human-IDeepRL2",linestyle = '-')
#plt.plot(ep[3],re[3], label="human-IDeepRL7",linestyle = '-')
#plt.plot(ep[5],re[5], label="human-IDeepRL8",linestyle = '-')
plt.plot(ep[8],re[8], label="human-IDeepRL3",linestyle = '-')
#plt.plot(ep[11],re[11], label="human-IDeepRL10",linestyle = '-')
#plt.plot(ep[12],re[12], label="human-IDeepRL11",linestyle = '-')
plt.legend(loc='lower right',fontsize='small')
plt.xlabel("Episode",fontsize='xx-large')   # Establece el título del eje x
plt.ylabel("Reward",fontsize='xx-large')   # Establece el título del eje y
#       plt.title(title)
plt.legend(loc='best',prop={'size':1})
plt.xlabel("Episodes")
plt.ylabel("Reward")
plt.grid()
plt.xlim(0, 300)
plt.ylim(-3, 3)
plt.show()   

#f.savefig('graf3.pdf', bbox_inches='tight')
