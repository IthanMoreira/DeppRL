# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 15:09:29 2019

@author: Ithan
"""
import random
import tensorflow as tf
import numpy as np
from Simulador import Simulador as simu 
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from collections import deque 
import matplotlib.pyplot as plt
    
K.clear_session()
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True)) #el javier usa este comando
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

class Deep_NN:
    def __init__(self, aprendizaje=0.1, descuento=0.85, epsilon=0.9, cantidad_acciones=4, estado=np.array([])):
        self.aprendizaje = aprendizaje
        self.descuento = descuento # Descuennto de la recompensa futura
        self.epsilon = epsilon # exploracion inicial
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.9 #0.4
        self.estado=estado #imagen de entrada matriz
        self.memory = deque(maxlen=10000)
        self.buenos_recuerdos = deque(maxlen=10000)
        self.cantidad_acciones = cantidad_acciones # numero de acciones posibles        
        self.tamano_filtro1 = (8, 8)
        self.tamano_filtro2 = (4, 4)
        self.tamano_filtro3 = (3, 3)
        self.longitud=110
        self.altura = 84
        self.filtrosConv1 = 32
        self.filtrosConv2 = 64
        self.filtrosConv3 = 64
        self.tamano_pool = (2, 2)
        self.episodios=1000
        self.modelo=self.contruModelo()
    
    def contruModelo (self):
        cnn = Sequential()
        cnn.add(Convolution2D(self.filtrosConv1, self.tamano_filtro1, padding ="VALID", input_shape=(self.longitud, self.altura, 3), activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Convolution2D(self.filtrosConv2, self.tamano_filtro2, padding ="VALID", activation='elu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))
        
        cnn.add(Convolution2D(self.filtrosConv3, self.tamano_filtro3, padding ="VALID"))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Flatten())
        cnn.add(Dense(512, activation='relu'))#sigmoidal--- lineal
        cnn.add(Dropout(0.5))
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
        valores = self.modelo.predict(estado)
        return np.argmax(valores[0])  # accion random o mayor
       
    def entrenar(self, batch_size, memo):
        minibatch = random.sample(memo, batch_size)#con lo guardado se entrena la red con experiencias random
        for estado, accion, recompensa, estado_siguiente, logrado in minibatch:
            target = recompensa
            if not logrado:
                target = (recompensa + self.gamma *
                          np.amax(self.modelo.predict(estado_siguiente)[0]))
            target_f = self.modelo.predict(estado)           
            target_f[0][accion] = target            
            self.modelo.fit(estado, target_f, epochs=1, verbose=0)
            
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def cargar_modelo(self, name):
        self.modelo.load_weights(name)

    def guardar_modelo(self, name):
        self.modelo.save_weights(name)
    def actualizar (self):
        self.modelo.set_weights(self.modelo.get_weights())
if __name__ == "__main__":
    
  
    
    sim = simu()
    """
    sim.seleccion(0)
    sim.seleccion(1)
    sim.seleccion(2)
    sim.seleccion(3)
    sim.seleccion(4)
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
    print(agente.modelo.predict(est))
    """
    est=sim.kinectVisionRGB()
    agente = Deep_NN(estado=est) 
    

   
    done = False
    batch_size = 100
    rewardCum=0
    state = sim.kinectVisionRGB()# reseteo el estaado y le entrego la imagen nuevamente
    times=[]
    recom=[]
    es=[]
    
    
    while len(agente.memory) < 300:
        action = agente.decision(state)
        next_state, reward, done= sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
        agente.experiencia(state, action, reward, next_state, done)        
        state = next_state
        if done:
                print(" score: ",reward," e : ",agente.epsilon)
                sim.restartScenario()
                rewardCum=0
    
 
    for e in range(agente.episodios):
        sim.restartScenario()
        state = sim.kinectVisionRGB()# reseteo el estaado y le entrego la imagen nuevamente
        rewardCum=0
        time=0
        while True:
            
            action = agente.decision(state)            
            next_state, reward, done= sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
            agente.experiencia(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                agente.actualizar()
                times.append(time)
                recom.append(rewardCum)
                es.append(e)
                print("episode: ",e," score: ",reward," e : ",agente.epsilon," time ",time)# 
                                                 
                break
              
        
            if len(agente.memory) > batch_size:                
                agente.entrenar(batch_size,agente.memory)
            time=time+1

        
    plt.plot(times,recom) 
    plt.show()               
    plt.plot(es,recom)
    plt.show()
    plt.plot(es,times)
    plt.show()           

        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")

