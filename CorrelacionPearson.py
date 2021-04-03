# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:17:04 2020

@author: Ithan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:52:16 2019

@author: Ithan
"""

import csv
import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter 
'''
'Data/Promedio-DNN.csv',
       'Data/Promedio-agentes.csv',
'''
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
#ti=[]
for x in lista:
    data1=[]
    ep1=[]
    re1=[]
    #ti1=[]
    with open(x, newline='') as File:  
        reader = csv.reader(File)
        
        for row in reader:
            data1.append(row)
        
        del(data1[0])
        
        for row in data1:
             ep1.append(int(row[0]))
             re1.append(float(row[1]))
             #ti1.append(int(row[2]))
             if len(ep1)>299:
                 break    
        ep.append(ep1)
        re.append(savgol_filter(re1, 55,3))
        #ti.append(ti1)    
        
re=np.asarray(re)


plt.rcParams.update({'font.size': 14})

corr = np.corrcoef(re)
f= plt.figure(figsize=(10,8))
#print(corr)
#plt.matshow(corr)d
plt.imshow(corr, cmap='Oranges', interpolation='nearest', aspect='auto') #interpolation='bilinear'
plt.colorbar()
#   plt.title(title)
plt.xlabel("Reward")
plt.ylabel("Reward")

#plt.xticks(np.arange(11), ( '$A_H1$', '$A_H2$', '$A_H3$', '$A_H4$', '$A_H5$', '$A_H6$', '$A_H7$', '$A_H8$', '$A_H9$', '$A_H10$', '$A_H11$'))
#plt.yticks(np.arange(11), ( '$A_H1$', '$A_H2$', '$A_H3$', '$A_H4$', '$A_H5$', '$A_H6$', '$A_H7$', '$A_H8$', '$A_H9$', '$A_H10$', '$A_H11$'))
Y=( '$A_{Au}$', '$A_{AT}$','$A_{H1}$', '$A_{H2}$', '$A_{H3}$', '$A_{H4}$', '$A_{H5}$', '$A_{H6}$', '$A_{H7}$', '$A_{H8}$', '$A_{H9}$', '$A_{H10}$', '$A_{H11}$')
plt.xticks(np.arange(13), ( '$A_{Au}$', '$A_{AT}$','$A_{H1}$', '$A_{H2}$', '$A_{H3}$', '$A_{H4}$', '$A_{H5}$', '$A_{H6}$', '$A_{H7}$', '$A_{H8}$', '$A_{H9}$', '$A_{H10}$', '$A_{H11}$'))
#plt.barh(Y,re,align = "center")
plt.yticks(np.arange(13), ( '$A_{Au}$', '$A_{AT}$','$A_{H1}$', '$A_{H2}$', '$A_{H3}$', '$A_{H4}$', '$A_{H5}$', '$A_{H6}$', '$A_{H7}$', '$A_{H8}$', '$A_{H9}$', '$A_H{10}$', '$A_{H11}$'))
#plt.barh(Y,re,align = "center")  

f.savefig('graf.pdf', bbox_inches='tight')
