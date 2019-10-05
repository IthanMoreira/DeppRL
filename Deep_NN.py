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



K.clear_session()
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

class Deep_NN:
    def __init__(self, aprendizaje=0.1, descuento=0.85, epsilon=1.0, iteraciones=100, cantidad_acciones=4, estado=np.array([])):
        
        self.aprendizaje = aprendizaje
        self.descuento = descuento # Descuennto de la recompensa futura
        self.epsilon = epsilon # exploracion inicial
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.9 #0.4
        self.estado=estado #imagen de entrada matriz
        self.memory = deque(maxlen=2000)
        self.cantidad_acciones = cantidad_acciones # numero de acciones posibles
        self.modelo=self.contruModelo
        self.tamano_filtro1 = (3, 3)
        self.tamano_filtro2 = (2, 2)
        self.longitud, self.altura = 150, 150
        self.filtrosConv1 = 32
        self.filtrosConv2 = 64
        self.tamano_pool = (2, 2)
        self.episodios=100
    
    
    
    def contruModelo (self):
        cnn = Sequential()
        cnn.add(Convolution2D(self.filtrosConv1, self.tamano_filtro1, padding ="same", input_shape=(self.longitud, self.altura, 3), activation='relu'))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Convolution2D(self.filtrosConv2, self.tamano_filtro2, padding ="same"))
        cnn.add(MaxPooling2D(pool_size=self.tamano_pool))

        cnn.add(Flatten())
        cnn.add(Dense(256, activation='relu'))
        cnn.add(Dropout(0.5))
        cnn.add(Dense(self.cantidad_acciones, activation='softmax'))

        cnn.compile(loss='categorical_crossentropy',
            optimizer=optimizers.Adam(lr=self.aprendizaje),
            metrics=['accuracy'])
        
    def experiencia(self, estado, accion, recompensa, estado_siguiente, logrado):
        self.memory.append((estado, accion, recompensa, estado_siguiente, logrado))
    
    def decision(self, estado): #toma una accion sea random o la mayor
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.cantidad_acciones)
        valores = self.modelo.predict(estado)
        return np.argmax(valores[0])  # accion random o mayor
        
    def entrenar(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)#con lo guardado se entrena la red con experiencias random
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
        
if __name__ == "__main__":
    
    sim = simu()
    
    """
    sim.seleccion(0)
    sim.seleccion(2)
    sim.seleccion(3)
    print (sim.completado('Cylinder'))
    sim.restartScenario()
"""
    est=sim.kinectVisionRGB()
    agente = Deep_NN(estado=est)
    #print(agente.decision(est))
    




    #agent.load("./save/cartpole-dqn.h5")
   
    """
    sim.grabObject('m_Sphere', 'Cylinder')

    sim.dropObject('m_Sphere','customizableTable_tableTop')

    sim.moveTarget('m_Sphere', 'Cuboid')
    sim.grabObject('m_Sphere', 'Cuboid')
    sim.dropObject('m_Sphere','customizableTable_tableTop#')
    """
    
    
    done = False
    batch_size = 3
    for e in range(agente.episodios):
        state = sim.kinectVisionRGB()# reseteo el estaado y le entrego la imagen nuevamente
        
        for time in range(500):
           
            action = agente.decision(state)
            print(action)
            next_state, reward, done = sim.seleccion(action) # segun la accion retorna desde el entorno todo eso
            agente.experiencia(state, action, reward, next_state, done)                        
            #reward = reward if not done else -1
            state = next_state
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, agente.episodios, time, agente.epsilon))
                break
              
        
            if len(agente.memory) > batch_size:
                print("asdasdasdasdasdasaqui")
                agente.entrenar(batch_size)
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")
        
"""
cnn.fit(
    entrenamiento_generador,
    steps_per_epoch=pasos,
    epochs=epocas,
    validation_data=validacion_generador,
    validation_steps=validation_steps)

"""
