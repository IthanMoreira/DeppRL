# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 15:09:29 2019

@author: Javier e Ithan
"""

import pandas as pd
import pickle
import random
import tensorflow as tf
import numpy as np
import time as tim
from Simulador import Simulador as simu 
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Flatten, Dense
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import Sequential, load_model
from collections import deque 
import matplotlib.pyplot as plt
    
K.clear_session()
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True)) #el javier usa este comando
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

class Deep_NN:
    def __init__(self, aprendizaje=0.001, epsilon=1, cantidad_acciones=4, estado=np.array([])):
        self.aprendizaje = aprendizaje
        self.epsilon = epsilon # exploracion inicial
        
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995
        
        self.gamma = 0.9 #0.4
        self.estado=estado #imagen de entrada matriz
        self.memory = deque(maxlen=20000)
        #self.buenos_recuerdos = deque(maxlen=2000)
        self.cantidad_acciones = cantidad_acciones # numero de acciones posibles  
        self.longitud=64
        self.altura = 64
        self.tamano_filtro1 = (8, 8)
        self.tamano_filtro2 = (4, 4)
        self.tamano_filtro3 = (2, 2)
        
        self.filtrosConv1 = 4
        self.filtrosConv2 = 8
        self.filtrosConv3 = 16
        self.tamano_pool = (2, 2)
        self.episodios=10000
        self.modelo=self.contruModelo()
    
    def contruModelo (self):
        cnn = Sequential()
        cnn.add(Convolution2D(self.filtrosConv1, self.tamano_filtro1, padding ="same", input_shape=(self.altura,self.longitud, 3), activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Convolution2D(self.filtrosConv2, self.tamano_filtro2, padding ="same",activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(Convolution2D(self.filtrosConv3, self.tamano_filtro3, padding ="same",activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(Flatten())
        #cnn.add(Dense(16,activation='relu'))
        cnn.add(Dense(256, activation='relu'))#sigmoidal--- lineal
        cnn.add(Dense(self.cantidad_acciones,activation='softmax'))#tanh
        
        cnn.compile(loss='mse', optimizer=optimizers.RMSprop(lr=self.aprendizaje))
        return cnn
    def experiencia(self, estado, accion, recompensa, estado_siguiente, logrado):
        self.memory.append((estado, accion, recompensa, estado_siguiente, logrado))

    def decision(self, estado): #toma una accion sea random o la mayor
        
        if np.random.rand() <= self.epsilon:
            return  random.randrange(self.cantidad_acciones)
        else:
            valores = self.modelo.predict(estado)
        #print (valores)
        return np.argmax(valores[0])  # accion random o mayor
    
    def decision_maestro(self, estado): #toma una accion ingresada por el maestro
        try:    
            print("Acciones:")
            print("0) Tomar objeto")
            print("1) Mover derecha")
            print("2) Mover izquierda")
            print("3) Soltar")
            accion_Maestro=int(input("Introduce una accion: "))
        except ValueError:
            accion_Maestro=0
        
        if accion_Maestro>3 or accion_Maestro < 0:
            accion_Maestro=0
            
        return accion_Maestro  # accion 
       
    def entrenar(self, batch_size, memo):
        miniBatch = random.sample(self.memory, batch_size)#con lo guardado se entrena la red con experiencias random
        #miniBatch = random.sample(agente.memory, batch_size)
        estados = np.zeros((batch_size, 64, 64, 3))

        est_sig = np.zeros((batch_size, 64, 64, 3))
        acciones, recompensas, logrados = [], [], []

        for i in range(batch_size):
            estados[i] = miniBatch[i][0]
            acciones.append(miniBatch[i][1])
            recompensas.append(miniBatch[i][2])
            est_sig[i] = miniBatch[i][3]
            logrados.append(miniBatch[i][4])

        target = self.modelo.predict(estados)
        #target = agente.modelo.predict(estados)
        target_val = self.modelo.predict(est_sig)
        #target_val = agente.modelo.predict(est_sig)
        for x in range(batch_size):      
            if logrados[x]:
                target[x][acciones[x]]=recompensas[x]
                #target[2][acciones[0]]=recompensas[0]
            else:
                target[x][acciones[x]]= (recompensas[x] + self.gamma *
                          np.amax(target_val[x]))
                #target[x][acciones[x]]= (recompensas[x] + agente.gamma *np.amax(target_val[x]))
        # and do the model fit!
        self.modelo.fit(estados, target,
                       epochs=1, verbose=0)        
        #fit_generator([estados,target], epochs=1,verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def cargar_modelo(self, name):
        self.modelo=load_model('DNN-interactive-humano/modelo_'+name)
        self.modelo.load_weights('DNN-interactive-humano/pesos_'+name)
        
   
    def guardar_modelo(self, name):
        self.modelo.save_weights('pesos_'+name)
        self.modelo.save('modelo_'+name)
    ##def actualizar (self):
     #   self.modelo.set_weights(self.modelo.get_weights())
     
    def guardar_memoria(self, name):
        #print (self.memory)
        file=open("DNN-interactive-humano/"+name,'wb')               #file object in binary write mode
        pickle.dump(self.memory,file)      #dump the data in the file object
        file.close()                       #close the file to write into the file
        
    def cargar_memoria(self, name):
       file=open("DNN-interactive-humano/"+name,'rb')  #file object in binary read mode
       data=pickle.load(file)      #load the data back
       file.close()
       self.memory=data
       #print(data)
       
if __name__ == "__main__":
    
  
    
    sim = simu()
    """
    a=sim.seleccion(0)
    a=sim.seleccion(1)
    a=sim.seleccion(2)
    a=sim.seleccion(3)
   
    sim.restartScenario()
    
    
    #print(len(posiciones))
    sim.tomarObjeto('m_Sphere')           
    #dere
    sim.moverLados('m_Sphere','customizableTable_tableTop#0')  
    #izq
    sim.moverLados('m_Sphere','customizableTable_tableTop#1')  
    #soltar
    sim.soltarObjeto('m_Sphere')
    #casa
    sim.volverCasa()
    
    sim.completado()
    sim.enMesa()
    sim.obtenerPos()
    sim.posEnMesa()
    sim.quedaAlgo()
    sim.objetoTomado()
    sim.restartScenario()    
    print(agente.modelo.predict(state))
    """
    state=sim.kinectVisionRGB()
    agente = Deep_NN(estado=state)     
    #agente.modelo.summary()
    done = False
    terminado = 0 
    batch_size = 128
    times=[]
    recom=[]
    es=[]
    rewardCum=0
    timer=0
    timercum=0
    
    """
    while len(agente.memory) < 900:
        action = agente.decision(state)            
        next_state, reward, done = sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
        
        if reward==-0.01 and timer>18:
            reward=reward*(timer-18)
        elif reward==-0.01:
            reward=0
        
        rewardCum=reward+rewardCum
        agente.experiencia(state, action, reward, next_state, done)       
        
        state = next_state
        
        if done or timer>250:
                timercum=timer+timercum
                print(" score: ",rewardCum," time : ",timer," timeTotal : ",timercum)#                      
                sim.restartScenario()
                rewardCum=0
                timer=0
        timer=timer+1

    agente.guardar_memoria("1000 pasos")
    timercum=0
    """
    """
    count=0
    
    # Interactive inicio early advising (se enseña cuando el agente aun no conose muy bien el escenario)
    agente.cargar_memoria("1000 pasos")
    while  count <= 100:
        action = agente.decision_maestro(state)            
        next_state, reward, done = sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
        
        if reward==-0.01 and timer>18:
            reward=reward*(timer-18)
        elif reward==-0.01:
            reward=0   
            
        rewardCum=reward+rewardCum
        agente.experiencia(state, action, reward, next_state, done)              
        state = next_state
        
        if done or timer>250:
                timercum=timer+timercum
                print(" score: ",rewardCum," time : ",timer," timeTotal : ",timercum)#                      
                sim.restartScenario()
                rewardCum=0
                timer=0
        
        if len(agente.memory) >= batch_size:
            agente.entrenar(batch_size,agente.memory) 
                        
        timer=timer+1
        count=count+1
        
    agente.guardar_modelo("DNN-interactive-humano-.....")
    agente.guardar_memoria("memoria-....")

    timercum=0
    """
    lista=["RebecaTello","karin"]
    for x in lista:
        
        agente.cargar_memoria("memoria-"+x)
        agente.cargar_modelo("DNN-interactive-humano-"+x)
        
        
        for e in range(agente.episodios):
            state = sim.kinectVisionRGB()# reseteo el estaado y le entrego la imagen nuevamente
            rewardCum=0
            time=0
            
            while True:
                action = agente.decision(state)#int(input("accion = "))
                ultima_accion=action
                next_state, reward, done= sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
                #if reward==-0.01 and time>6:
                #    reward=reward*(time-6)
                agente.experiencia(state, action, reward, next_state, done)          
                
                state = next_state
                
                rewardCum=reward+rewardCum
                
                if done or time>250:
                    timercum=time+timercum
                    times.append(time)
                    recom.append(rewardCum)
                    es.append(e)
                    print("episode: ",e," score: ",rewardCum," e : ",agente.epsilon," time ",time ," timeTotal : ",timercum)#
                    terminado=terminado+1
                    break
                    
                if len(agente.memory) >= batch_size:
                    agente.entrenar(batch_size,agente.memory)     
                                
                time=time+1
                    
            if e%10==0 and e>9:
                     
                plt.plot(es,recom)
                plt.show()
                plt.plot(es,times)
                plt.show()
                
            if e>=350:
                agente.guardar_modelo("DNN-interactive-humano-"+x)
                data={'recom':recom,'times':times}
                df = pd.DataFrame(data, columns = ['recom', 'times'])
                df.to_csv('DNN-interactive-humano-'+x+'.csv')
                break
            
            sim.restartScenario()
            tim.sleep(1)
        agente.epsilon=1
        state=sim.kinectVisionRGB()
        agente = Deep_NN(estado=state)     
        #agente.modelo.summary()
        done = False
        terminado = 0 
        batch_size = 128
        times=[]
        recom=[]
        es=[]
        rewardCum=0
        timer=0
        timercum=0
            
    
        #plt.plot(times,recom) 
        #plt.show()               
        plt.plot(es,recom)
        plt.show()
        plt.plot(es,times)
        plt.show()   
            
    
  # desde aqui de se comenta

    
    next_state, reward, done= sim.seleccion(2) # segun la accion retorna desde el entorno todo eso    
    tar=agente.modelo.predict(next_state)
    tar[0][0]=0
    tar[0][1]=1
    tar[0][2]=0
    tar[0][3]=0
    for x in range(1000):
        his=agente.modelo.fit(next_state,tar,epochs=1, verbose=0)
    
    type(his)
    plt.figure(0)  
    plt.plot(his.history['acc'],'r')  
    plt.plot(his.history['val_acc'],'g')  
    plt.xticks(np.arange(0, 11, 2.0))  
    plt.rcParams['figure.figsize'] = (8, 6)  
    plt.xlabel("Numero de Epocas")  
    plt.ylabel("Precisión")  
    plt.title("Precisión de entrenamiento vs Precisión de Validación")  
    plt.legend(['entrenamiento','Validación'])
    
    """
         #if e % 10 == 0:
          #   agent.save("./save/cartpole-dqn.h5")
    #agente.guardar_memoria("prueba")
    #agente.cargar_modelo("6 figuras 30 buenos")
    
        time=0
        e=1
        ee=0.91
        while True:
            time=time+1
            if e > 0.01:
                e *= ee
            else:
                print(time)
                break
                

"""     

