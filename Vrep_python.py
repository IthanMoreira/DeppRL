# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:02:31 2019

@author: javie
"""
"Conexion"

import vrep
import numpy as np
import math
import time

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

if clientID!=-1:
    print ('Conexion exitosa')
    
    emptyBuff = bytearray()

"renombrar objetos "

[returnCode,target]=vrep.simxGetObjectHandle(clientID,'m_Sphere',vrep.simx_opmode_blocking)
[returnCode,objeto1]=vrep.simxGetObjectHandle(clientID,'Cylinder',vrep.simx_opmode_blocking)
[returnCode,suctionPad]=vrep.simxGetObjectHandle(clientID,'active',vrep.simx_opmode_blocking)

"""
"activo y desactivo pad(chupon)"

"estado del chupon"
returnCode,signalValue=vrep.simxGetIntegerSignal(clientID,'suctionPadSensor',vrep.simx_opmode_blocking)    
print "estado pad: ", signalValue

"activo del chupon"
returnCode=vrep.simxSetIntegerSignal(clientID,'suctionPadSensor',1,vrep.simx_opmode_oneshot)               

"estado chupon "
returnCode,signalValue=vrep.simxGetIntegerSignal(clientID,'suctionPadSensor',vrep.simx_opmode_blocking)
print "estado pad: ", signalValue

"desactivo del chupon"
returnCode=vrep.simxClearIntegerSignal(clientID,'suctionPadSensor',vrep.simx_opmode_blocking)               

"estado chupon"
returnCode,signalValue=vrep.simxGetIntegerSignal(clientID,'suctionPadSensor',vrep.simx_opmode_blocking)
print "estado pad: ", signalValue
"""

"posicion Target y objeto1 "

returnCode,positionTar=vrep.simxGetObjectPosition(clientID,target,-1,vrep.simx_opmode_blocking)
returnCode,orientacionTar=vrep.simxGetObjectOrientation(clientID,target,-1,vrep.simx_opmode_blocking)

returnCode,positionObj1=vrep.simxGetObjectPosition(clientID,objeto1,-1,vrep.simx_opmode_blocking)
returnCode,orientacionObj1=vrep.simxGetObjectOrientation(clientID,objeto1,-1,vrep.simx_opmode_blocking)

returnCode,distanciaTarObj1=vrep.simxGetObjectPosition(clientID,objeto1,target,vrep.simx_opmode_blocking)
returnCode,orientacionObj1Tar=vrep.simxGetObjectOrientation(clientID,target,objeto1,vrep.simx_opmode_blocking)

home = positionTar

"""
print "distancia target-objeto1: ", distanciaTarObj1

 


print "TargetPos", positionTar
print "TargetOri", orientacionTar

print "Objeto1Pos", positionObj1
print "Objeto1Ori", orientacionObj1
"""

"estado sesor pad"
"returnCode,signalValue=vrep.simxGetIntegerSignal(clientID,'succtionPadSensor',vrep.simx_opmode_blocking)"



"positionObj1"
"""
Quiero hacer un while con distancia/2 y a esa posicion mando el target, mientras mas cerca 
del objeto1, mas lento se movera y utilizando un sensor de colicion ver cuando lo toque.
"""

position2=[];

for i in range(len(positionTar)):
    if i == 2: 
        position2.append(positionTar[i]+distanciaTarObj1[i] + 0.10)  
    else:
        position2.append(positionTar[i]+distanciaTarObj1[i])

    
"""	

orientation2=[];

for i in range(len(orientacionObj1)):
        if i == 2: 
            orientation2.append((orientacionTar[i]+orientacionObj1Tar[i])*-1)
        else:
            orientation2.append(orientacionTar[i]+orientacionObj1Tar[i])
            


print orientacionTar, "  target";
print orientacionObj1, " objeto";
print orientation2, " orientacion sumada";
print orientacionObj1Tar, " tar obj1";
"""
 

returnCode=vrep.simxSetObjectOrientation(clientID,target,-1,(0,math.pi,0),vrep.simx_opmode_oneshot)

np.array(position2)
n=(position2[0],position2[1],positionTar[2])
returnCode=vrep.simxSetObjectPosition(clientID,target,-1,n,vrep.simx_opmode_oneshot)


"baja"

while round(positionTar[2],3)!=round((positionObj1[2]+0.05),3): 
    n=(position2[0],position2[1],positionTar[2]-0.001)
    returnCode=vrep.simxSetObjectPosition(clientID,target,-1,n,vrep.simx_opmode_oneshot)
    returnCode,positionTar=vrep.simxGetObjectPosition(clientID,target,-1,vrep.simx_opmode_blocking)


returnCode,paramValue=vrep.simxGetBooleanParameter(clientID,suctionPad,vrep.simx_opmode_blocking)

print paramValue

returnCode,signalValue=vrep.simxGetIntegerSignal(clientID,'suctionPad',vrep.simx_opmode_blocking)

print signalValue

fal=False

returnCode=vrep.simxSetBooleanParameter(clientID,suctionPad,False,vrep.simx_opmode_oneshot)

print returnCode

returnCode=vrep.simxSetIntegerSignal(clientID,'suctionPad',0,vrep.simx_opmode_oneshot)

print returnCode

returnCode=vrep.simxClearIntegerSignal(clientID,'suctionPad',vrep.simx_opmode_blocking)               


"sube"


while round(positionTar[2],2)!=round((home[2]),2): 
    n=(position2[0],position2[1],positionTar[2]+0.005)
    returnCode=vrep.simxSetObjectPosition(clientID,target,-1,n,vrep.simx_opmode_oneshot)
    returnCode,positionTar=vrep.simxGetObjectPosition(clientID,target,-1,vrep.simx_opmode_blocking)
              

returnCode=vrep.simxSetObjectPosition(clientID,target,-1,position2,vrep.simx_opmode_oneshot)




print returnCode;

"""
"Vision kinect"

res,v0=vrep.simxGetObjectHandle(clientID,'kinect_rgb',vrep.simx_opmode_oneshot_wait)
res,v1=vrep.simxGetObjectHandle(clientID,'kinect_depth',vrep.simx_opmode_oneshot_wait)

res,resolution,image=vrep.simxGetVisionSensorImage(clientID,v0,0,vrep.simx_opmode_streaming)
res,resolution,image1=vrep.simxGetVisionSensorImage(clientID,v1,0,vrep.simx_opmode_streaming)

print image

print "----------------------------------------------------------------------------------------"

print v0

"""

"""     
"aviso de conexion iniciada"
vrep.simxAddStatusbarMessage(clientID,'comunicacion iniciada con Python',vrep.simx_opmode_blocking)
print ('comunicacion iniciada con V-rep')


"camara segunddo valor"

res,v0=vrep.simxGetObjectHandle(clientID,'kinect_rgb',vrep.simx_opmode_oneshot_wait)
res,v1=vrep.simxGetObjectHandle(clientID,'kinect_depth',vrep.simx_opmode_oneshot_wait)

res,resolution,image=vrep.simxGetVisionSensorImage(clientID,v0,0,vrep.simx_opmode_streaming)
res,resolution,image1=vrep.simxGetVisionSensorImage(clientID,v1,0,vrep.simx_opmode_streaming)

print image

print "----------------------------------------------------------------------------------------"

print v0
"""


"Desconexion"
 

vrep.simxAddStatusbarMessage(clientID,'comunicacion finalizada',vrep.simx_opmode_blocking)
vrep.simxFinish(-1)
print ('comunicacion finalizada con V-rep')



























