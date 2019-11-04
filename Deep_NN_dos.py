# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 14:51:19 2019

@author: Ithan
"""

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
from collections import deque 
import matplotlib.pyplot as plt
    
K.clear_session()
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True)) #el javier usa este comando
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

class Deep_NN:
    def __init__(self, aprendizaje=0.1, epsilon=1, cantidad_acciones=4, estado=np.array([])):
        self.aprendizaje = aprendizaje
        self.epsilon = epsilon # exploracion inicial
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.9 #0.4
        self.estado=estado #imagen de entrada matriz
        self.memory = deque(maxlen=1000000)
        #self.buenos_recuerdos = deque(maxlen=2000)
        self.cantidad_acciones = cantidad_acciones # numero de acciones posibles        
        self.tamano_filtro1 = (8, 8)
        self.tamano_filtro2 = (4, 4)
        self.tamano_filtro3 = (2, 2)
        self.longitud=128
        self.altura = 64
        self.filtrosConv1 = 8
        self.filtrosConv2 = 16
        self.filtrosConv3 = 32
        self.tamano_pool = (2, 2)
        self.episodios=10000
        self.funcion=self.contruModelo()
        self.target=self.contruModelo()
        self.actualizarTarget()
    
    def contruModelo (self):
        cnn = Sequential()
        cnn.add(Convolution2D(self.filtrosConv1, self.tamano_filtro1, padding ="same", input_shape=(self.altura,self.longitud, 3), activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Convolution2D(self.filtrosConv2, self.tamano_filtro2, padding ="same",activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(Convolution2D(self.filtrosConv3, self.tamano_filtro3, padding ="same",activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(Flatten())
        #cnn.add(Dense(256, activation='relu'))#sigmoidal--- lineal
        cnn.add(Dense(self.cantidad_acciones, activation='softmax'))
        
        cnn.compile(loss='mse',
            optimizer=optimizers.Adam(lr=self.aprendizaje),
            metrics=['accuracy'])
        return cnn
    def experiencia(self, estado, accion, recompensa, estado_siguiente, logrado):
        self.memory.append((estado, accion, recompensa, estado_siguiente, logrado))


    def decision(self, estado): #toma una accion sea random o la mayor
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.cantidad_acciones)
        valores = self.funcion.predict(estado)
        #print (valores)
        return np.argmax(valores[0])  # accion random o mayor
       
    def entrenar(self, batch_size, memo):
        miniBatch = random.sample(self.memory, batch_size)#con lo guardado se entrena la red con experiencias random

        estados = np.zeros((batch_size, 64, 128, 3))

        est_sig = np.zeros((batch_size, 64, 128, 3))
        acciones, recompensas, logrados = [], [], []

        for i in range(batch_size):
            estados[i] = miniBatch[i][0]
            acciones.append(miniBatch[i][1])
            recompensas.append(miniBatch[i][2])
            est_sig[i] = miniBatch[i][3]
            logrados.append(miniBatch[i][4])
            
        target=self.funcion.predict(estados)
        target_val=self.target.predict(est_sig)
        
        
        
        for x in range(batch_size):      
            if logrados[x]:
                target[x][acciones[x]]=recompensas[x]
            else:
                target[x][acciones[x]]= (recompensas[x] + self.gamma *
                          np.amax(target_val[x]))
                    
        self.funcion.fit(estados,target,
                                    epochs=1,verbose=0)
        

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
        

    def cargar_modelo(self, name):
        self.modelo.load_weights(name)

    def guardar_modelo(self, name):
        self.modelo.save_weights(name)
        
    def actualizarTarget(self):
        self.target.set_weights(self.funcion.get_weights())
    
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
    #agente.cargar_modelo("uno")

    #agente.modelo.summary()
    done = False
    batch_size = 500
    times=[]
    recom=[]
    es=[]
    rewardCum=0
    timer=0
    timercum=0
    act=0
    while len(agente.memory) < 500:
        act=act+1
        action = agente.decision(state)            
        next_state, reward, done = sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
        
        if reward==-0.01 and timer>6:
                reward=reward*(timer-6)
        rewardCum=reward+rewardCum
        agente.experiencia(state, action, np.sign(reward), next_state, done)              
        state = next_state
        
        if done:
                timercum=timer+timercum
                print(" score: ",rewardCum," time : ",timer," timeTotal : ",timercum)#                      
                sim.restartScenario()
                rewardCum=0
                timer=0
        timer=timer+1
        
   

    for e in range(agente.episodios):
        
        state = sim.kinectVisionRGB()# reseteo el estaado y le entrego la imagen nuevamente
        rewardCum=0
        time=0
        
        while True:
            #print(time)
            act=act+1
            action = agente.decision(state)#int(input("accion = "))
                        
            next_state, reward, done= sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
            if reward==-0.01 and time>6:
                reward=reward*(time-6)
                       
            state = next_state
            rewardCum=reward+rewardCum
            agente.experiencia(state, action, np.sign(reward), next_state, done)
            if done:
                
                times.append(time)
                recom.append(rewardCum)
                es.append(e)
                print("episode: ",e," score: ",rewardCum," e : ",agente.epsilon," time ",time)# 
                                                 
                break
              
        
            if len(agente.memory) >= batch_size:
                agente.entrenar(batch_size,agente.memory)
            if act%1000==0:
                agente.actualizarTarget()
                
            time=time+1
        if e%20==0:
            #plt.plot(times,recom) 
            #plt.show()               
            plt.plot(es,recom)
            plt.show()
            plt.plot(es,times)
            plt.show()           
            
        sim.restartScenario()
        tim.sleep(1)

        
    #plt.plot(times,recom) 
    #plt.show()               
    plt.plot(es,recom)
    plt.show()
    plt.plot(es,times)
    plt.show()           
    
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")
#agente.guardar_modelo("uno")
#agente.cargar_modelo("uno")
