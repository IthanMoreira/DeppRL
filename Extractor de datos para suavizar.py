# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:52:16 2019

@author: Ithan
"""

import csv
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

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


"""
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
             #ep1.append(int(row[0]))
             re1.append(float(row[1]))
             #ti1.append(int(row[2]))
             if len(ep)>350:
                 break    
        #ep.append(ep1)
        #re.append(savgol_filter(re1, 55,3))
        #ti.append(ti1)    
"""   

#data = np.concatenate(([PSuccessEvolutionAcc, PChooseEvoAcc, PSuccessFormAcc, MXRLNoise]), axis=1)

lista2=['Data/recompensa.csv']

re0=[]
re1=[]
re2=[]
re3=[]
re4=[]
re5=[]
re6=[]
re7=[]
re8=[]
re9=[]
re10=[]
re11=[]
re12=[]

for x in lista2:
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
            re1.append(float(row[1]))
            re2.append(float(row[2]))
            re3.append(float(row[3]))
            re4.append(float(row[4]))
            re5.append(float(row[5]))
            re6.append(float(row[6]))
            re7.append(float(row[7]))
            re8.append(float(row[8]))
            re9.append(float(row[9]))
            re10.append(float(row[10]))
            re11.append(float(row[11]))
            re12.append(float(row[12]))
            re0.append(int(row[0]))
            
            if len(re12)>354:
                break    

#print(re1,re5,re11)
re1=np.transpose(np.concatenate([re0,re1]))
re2=np.transpose(np.concatenate([re0,re2]))
re3=np.transpose(np.concatenate([re0,re3]))
re4=np.transpose(np.concatenate([re0,re4]))
re5=np.transpose(np.concatenate([re0,re5]))
re6=np.transpose(np.concatenate([re0,re6]))
re7=np.transpose(np.concatenate([re0,re7]))
re8=np.transpose(np.concatenate([re0,re8]))
re9=np.transpose(np.concatenate([re0,re9]))
re10=np.transpose(np.concatenate([re0,re10]))
re11=np.transpose(np.concatenate([re0,re11]))
re12=np.transpose(np.concatenate([re0,re12]))

"""
re1=np.concatenate([re0,re1])
re2=np.concatenate([re0,re2])
re3=np.concatenate([re0,re3])
re4=np.concatenate([re0,re4])
re5=np.concatenate([re0,re5])
re6=np.concatenate([re0,re6])
re7=np.concatenate([re0,re7])
re8=np.concatenate([re0,re8])
re9=np.concatenate([re0,re9])
re10=np.concatenate([re0,re10])
re11=np.concatenate([re0,re11])
re12=np.concatenate([re0,re12])
"""
          
data = np.stack(([re1,re2,re3,re4,re5,re6,re7,re8,re9,re10,re11,re12]))     


"f = plt.figure(figNumber) "
plt.rcParams.update({'font.size': 14})
corr = np.corrcoef(data, rowvar=False)
#   plt.matshow(corr)
plt.imshow(corr, cmap='Oranges', interpolation='nearest', aspect='auto') #interpolation='bilinear'
plt.colorbar()
#   plt.title(title)
plt.xlabel("Reward")
plt.ylabel("Reward")
plt.xticks(np.arange(12), ('$A_A$', '$A_M$', '$A_H1$', '$A_H2$', '$A_H3$', '$A_H4$', '$A_H5$', '$A_H6$', '$A_H7$', '$A_H8$', '$A_H9$', '$A_H10$'))
plt.yticks(np.arange(12), ('$A_A$', '$A_M$', '$A_H1$', '$A_H2$', '$A_H3$', '$A_H4$', '$A_H5$', '$A_H6$', '$A_H7$', '$A_H8$', '$A_H9$', '$A_H10$'))
plt.show()






"""
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
"""


'''


yhat2 = savgol_filter(re2, 9,3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

yhat = savgol_filter(re, 9, 3) # window size 51, polynomial order 3 plt.plot(x,y) plt.plot(x,yhat, color='red') plt.show()

#plt.plot(ep,re) 
plt.plot(ep,yhat, color='red') 
plt.plot(ep2,yhat2, color='blue') 

plt.show()
'''

 
 
