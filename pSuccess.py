# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 14:41:57 2020

@author: ithan
"""

import numpy as np
#Q is the Q-value
#reward is the total reward collected
#gamma is the discount factor
def pSuccess(Q, reward, gamma):
    n = np.log(Q/reward)/np.log(gamma) #corresponde a Eq. 6 del paper. Python no tiene logaritmo en base gamma, pero por propiedades de logaritmos se puede calcular en base 10 y dividir por el logaritmos de gamma. Es lo mismo, cualquier duda revisar propiedades de logaritmos.
    log10baseGamma = np.log(10)/np.log(gamma) # Es un valor constante. Asumiendo que gamma no cambia. Se ocupa en la linea que viene a continuacion
    probOfSuccess = (n / (2*log10baseGamma)) + 1 #Corresponde a Eq. 7 del paper. Sin considerar la parte estocastica.
    probOfSuccessLimit = np.minimum(1,np.maximum(0,probOfSuccess)) #Corresponde a Eq. 9 del paper. Lo mismo anterior, solo que limita la probabilidad a valores entre 0 y 1.
    #probOfSuccessLimit = probOfSuccessLimit * (1 - stochasticity) #Usar solo si usamos transiciones estocasticas o el parametro sigma
    return probOfSuccessLimit


#Aca tienes que reemplazar la llamada por los Q-values obtenidos, el reward total que se obtiene al terminar la tarea de forma exitosa y tu discount factor.
print(pSuccess(0.6, 1, 0.9))