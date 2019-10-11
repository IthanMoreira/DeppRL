# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:40:16 2019

@author: javie
"""
import vrep
import math
import numpy as np
import time
import random

class Simulador(object):
 
    def __init__(self):
        self.clientID,self.home= self.connectRobot()
        self.home[2]=(self.home[2]-0.2)
        self.posObj1,self.obj1Id=self.obtenerPos('Cuboid0')
        self.posObj2,self.obj2Id=self.obtenerPos('Cuboid1')
        self.posObj3,self.obj3Id=self.obtenerPos('Cylinder')
        self.posObj4,self.obj4Id=self.obtenerPos('Cylinder0')
        self.posObj5,self.obj5Id=self.obtenerPos('Disc0')
        self.posObj6,self.obj6Id=self.obtenerPos('Disc1')
        self.objTomado=0
        self.mesa=0
        self.objetos = [self.obj1Id,self.obj2Id ,self.obj3Id ,self.obj4Id ,self.obj5Id ,self.obj6Id]
        self.posicionIni=[ self.posObj1, self.posObj2, self.posObj3, self.posObj4, self.posObj5, self.posObj6]
        self.posEnMesa()
        self.cont=0
        
        if self.clientID != -1:
            self.actionNumber = 1
            #self.performAnAction(4) #go home
        #endif
    #end of __init__ method
    
    def obtenerPos(self,objeto):
        errorCode1, idObj = vrep.simxGetObjectHandle(self.clientID,objeto, vrep.simx_opmode_oneshot_wait)
        returnCode,posObj=vrep.simxGetObjectPosition(self.clientID,idObj,-1,vrep.simx_opmode_blocking)
        
        return posObj,idObj
    
    def posEnMesa(self):
        errorCode1, mesa = vrep.simxGetObjectHandle(self.clientID,'customizableTable_tableTop', vrep.simx_opmode_oneshot_wait)
        returnCode,posMesa=vrep.simxGetObjectPosition(self.clientID,mesa,-1,vrep.simx_opmode_blocking)
        
        if errorCode1==vrep.simx_error_noerror:
            pos1=(posMesa[0]+0.20,posMesa[1]+0.15,posMesa[2]+0.06)
            pos2=(posMesa[0],posMesa[1]+0.15,posMesa[2]+0.06)
            pos3=(posMesa[0]-0.20,posMesa[1]+0.15,posMesa[2]+0.06)   
            
            pos4=(posMesa[0]+0.20,posMesa[1],posMesa[2]+0.06)
            pos5=(posMesa[0],posMesa[1],posMesa[2]+0.06)
            pos6=(posMesa[0]-0.2,posMesa[1],posMesa[2]+0.06)
            
            pos7=(posMesa[0]+0.20,posMesa[1]-0.15,posMesa[2]+0.06)
            pos8=(posMesa[0],posMesa[1]-0.2,posMesa[2]+0.06)
            pos9=(posMesa[0]-0.20,posMesa[1]-0.15,posMesa[2]+0.06)
            
            posiciones=[pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9]
            
            for obj in self.objetos:
                aux=random.choice(posiciones)
                vrep.simxSetObjectPosition(self.clientID,obj,-1,aux,vrep.simx_opmode_oneshot)
                posiciones.remove(aux)
            
    
    def connectRobot(self):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
        if clientID!=-1:
            print ('Conectado a la remote API server with clientID: ', clientID)
            vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait) 
            errorCode1, handleJoint = vrep.simxGetObjectHandle(clientID,'m_Sphere' , vrep.simx_opmode_oneshot_wait)
            errorCode1, objeto = vrep.simxGetObjectHandle(clientID,'Cylinder' , vrep.simx_opmode_oneshot_wait)
            returnCode,home=vrep.simxGetObjectPosition(clientID,handleJoint,-1,vrep.simx_opmode_blocking)#deje estatico la primera posicion de target
            returnCode,obj=vrep.simxGetObjectPosition(clientID,objeto,-1,vrep.simx_opmode_blocking)
            vrep.simxSetObjectOrientation(clientID,handleJoint,-1,(0,math.pi,0),vrep.simx_opmode_oneshot)
            errorCode,rgb=vrep.simxGetObjectHandle(clientID,'kinect_rgb',vrep.simx_opmode_oneshot_wait)
            res,resolution,imegenRgb=vrep.simxGetVisionSensorImage(clientID,rgb,0,vrep.simx_opmode_streaming)
            time.sleep(1)
        else:
            print ('Error de conexion a remote API server')
        return clientID,home
    #end of connectRobot method
    
    def disconnectSimulator(self):
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot_wait)
        vrep.simxFinish(self.clientID)
        print ('Robot y simulacion desconectado')
    #end of disconnectSimulator method
    
    def restartScenario(self):
        
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID,'m_Sphere' , vrep.simx_opmode_oneshot_wait)
        vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,self.home,vrep.simx_opmode_oneshot)
        
        aux1=self.posicionIni[:]
        
        for obj in self.objetos:
                aux=random.choice(aux1)
                vrep.simxSetObjectPosition(self.clientID,obj,-1,(aux[0],aux[1],aux[2]+0.06),vrep.simx_opmode_oneshot)
                aux1.remove(aux)
                
        time.sleep(1)
        
        self.posEnMesa()
        
        
    #end of disconnectRobot method
    
    """  
    def orientationTarget(self, orientationTarget):
        errorCode, handleJoint = vrep.simxGetObjectHandle(self.clientID, orientationTarget, vrep.simx_opmode_oneshot_wait)
        if errorCode==vrep.simx_error_noerror:
            vrep.simxSetObjectOrientation(self.clientID,handleJoint,-1,(0,math.pi,0),vrep.simx_opmode_oneshot)
        else:
            print ('Error. Got no handle: ', errorCode)

    #end of orientationTarget method
    """  

    def movTarget(self, moveTarget, Object):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget, vrep.simx_opmode_oneshot_wait)
        errorCode, obj = vrep.simxGetObjectHandle(self.clientID, Object, vrep.simx_opmode_oneshot_wait)
        if errorCode1==vrep.simx_error_noerror and errorCode==vrep.simx_error_noerror :
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            n=(positionObj1[0],positionObj1[1],positionObj1[2]+0.25)
            vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
            time.sleep(1)
        else:
            print ('Error. MovTarget ', errorCode, errorCode1)
    #end of moveTarget method
    
    def moverLados(self,moveTarget,Object):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget , vrep.simx_opmode_oneshot_wait)
        errorCode, obj = vrep.simxGetObjectHandle(self.clientID, Object, vrep.simx_opmode_oneshot_wait)
                                                  
        if errorCode1==vrep.simx_error_noerror and errorCode==vrep.simx_error_noerror :
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            n=(positionObj1[0],positionObj1[1],positionObj1[2]+0.25)
            vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
            self.mesa=obj
            time.sleep(1)                     
        else:
            print ('Error. MoverLados ', errorCode, errorCode1)
    #end of moveLeft method
    
    def enMesa(self,obj):
        errorCode1, mesa = vrep.simxGetObjectHandle(self.clientID,'customizableTable_tableTop', vrep.simx_opmode_oneshot_wait)
        returnCode,posMesa=vrep.simxGetObjectPosition(self.clientID,mesa,-1,vrep.simx_opmode_blocking)
        returnCode,posObj=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
        
        if((posMesa[0]-0.22)<=posObj[0] and (posMesa[0]+0.22)>=posObj[0] and (posMesa[1]-0.22)<=posObj[1] and (posMesa[1]+0.22)>=posObj[1] ):
                return True
            
    def quedaAlgo(self):
        errorCode1, mesa = vrep.simxGetObjectHandle(self.clientID,'customizableTable_tableTop', vrep.simx_opmode_oneshot_wait)
        returnCode,posMesa=vrep.simxGetObjectPosition(self.clientID,mesa,-1,vrep.simx_opmode_blocking)
        
        for obj in self.objetos:
            returnCode,posObj=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            if((posMesa[0]-0.22)<=posObj[0] and (posMesa[0]+0.22)>=posObj[0] and (posMesa[1]-0.22)<=posObj[1] and (posMesa[1]+0.22)>=posObj[1] ):
                    return False
        
        return True
    
    def tomarObjeto(self, moveTarget): 
        
        obj=random.choice(self.objetos)
        if self.enMesa(obj):
            self.objTomado=obj
            errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget, vrep.simx_opmode_oneshot_wait)
    
            if errorCode1==vrep.simx_error_noerror :
                returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
                returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
                
                n=(positionObj1[0],positionObj1[1],positionTar[2])
                
                aux=(positionObj1[2]+0.05)
                
                if obj == self.obj5Id or obj == self.obj6Id:
                    aux=(positionObj1[2]+0.01)
                    
                while round(positionTar[2],3)>=round(aux,3): 
                    n=(positionObj1[0],positionObj1[1],positionTar[2]-0.002)
                    vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
                    returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
    
                inputBuffer=bytearray()
                res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(self.clientID,
                                                                                       'suctionPad',
                                                                                       vrep.sim_scripttype_childscript,
                                                                                       'sysCall_cleanup',
                                                                                       [],
                                                                                       [],
                                                                                       [],
                                                                                       inputBuffer,
                                                                                       vrep.simx_opmode_blocking)
              
                while round(positionTar[2],2)<=round((self.home[2]),2): 
                    n=(positionObj1[0],positionObj1[1],positionTar[2]+0.005)
                    vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
                    returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
                    
            else:
                print ('Error. tomarObjeto ', errorCode1)
        else:
            print ('Objeto no esta en la mesa central') 
    #end of orientationTarget method
    
    def soltarObjeto(self, moveTarget):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget, vrep.simx_opmode_oneshot_wait)
        if self.mesa!=0:
            if errorCode1==vrep.simx_error_noerror :
                returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
                returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,self.mesa,-1,vrep.simx_opmode_blocking)
                returnCode,distanciaTarObj1=vrep.simxGetObjectPosition(self.clientID,self.mesa,handleJoint,vrep.simx_opmode_blocking)
    
                n=(positionObj1[0],positionObj1[1],positionTar[2])
                
                while round(positionTar[2],3)!=round((positionObj1[2]+0.12),3): 
                    n=(positionObj1[0],positionObj1[1],positionTar[2]-0.002)
                    vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
                    returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
    
                inputBuffer=bytearray()
                res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(self.clientID,
                                                                                       'suctionPad',
                                                                                       vrep.sim_scripttype_childscript,
                                                                                       'sysCall_cleanup',
                                                                                       [],
                                                                                       [],
                                                                                       [],
                                                                                       inputBuffer,
                                                                                       vrep.simx_opmode_blocking)
              
                while round(positionTar[2],2)!=round((self.home[2]),2): 
                    n=(positionObj1[0],positionObj1[1],positionTar[2]+0.005)
                    vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
                    returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
                    
                self.mesa=0
                
            else:
                print ('Error. soltarObjeto ', errorCode1)
        else:
            print ('no hay mesa')
    #end of orientationTarget method
    
    def volverCasa(self):
        inputBuffer=bytearray()
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(self.clientID,
                                                                                   'suctionPad',
                                                                                   vrep.sim_scripttype_childscript,
                                                                                   'sysCall_cleanup',
                                                                                   [],
                                                                                   [],
                                                                                   [],
                                                                                   inputBuffer,
                                                                                   vrep.simx_opmode_blocking)
        errorCode, handleJoint = vrep.simxGetObjectHandle(self.clientID, 'm_Sphere', vrep.simx_opmode_oneshot_wait)
        if errorCode==vrep.simx_error_noerror:
            vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,self.home,vrep.simx_opmode_oneshot)
            time.sleep(1)
            
        else:
            print ('Error. volver a casa ', errorCode)
    #end of orientationTarget method
    
    def kinectVisionRGB(self):
        errorCode,rgb=vrep.simxGetObjectHandle(self.clientID,'kinect_rgb',vrep.simx_opmode_oneshot_wait)

        if errorCode==vrep.simx_error_noerror :        
            res,resolution,imegenRgb=vrep.simxGetVisionSensorImage(self.clientID,rgb,0,vrep.simx_opmode_buffer)
            
            imgRgb = np.array(imegenRgb,dtype=np.uint8)
            
            imgRgb.resize([200,200,3])
            
            imgRgb= np.expand_dims(imgRgb, axis=0)
        
        else:
            print ('Error. kinectvisionRGB ', errorCode)
        
        return imgRgb
    #end of KinectVisionRGB method
    
    def kinectVisionPATH(self):
        errorCode1,path=vrep.simxGetObjectHandle(self.clientID,'kinect_depth',vrep.simx_opmode_oneshot_wait)


        if errorCode1==vrep.simx_error_noerror :        
            res,resolution,imagenPath=vrep.simxGetVisionSensorImage(self.clientID,path,0,vrep.simx_opmode_buffer)

            imgPath = np.array(imagenPath,dtype=np.uint8)
            imgPath.resize([resolution[1],resolution[0],3])
        
        else:
            print ('Error. kinectvisionPath ', errorCode1)
        
        return imgPath
    #end of KinectVisionPATH method
    
    def completado (self): #True dejo en su lugar el objeto !!! SOLO MESA IZQ!!!
        
        errorCode, mesaIzq = vrep.simxGetObjectHandle(self.clientID, 'customizableTable_tableTop#0', vrep.simx_opmode_oneshot_wait)
        errorCode, mesaDer = vrep.simxGetObjectHandle(self.clientID, 'customizableTable_tableTop#1', vrep.simx_opmode_oneshot_wait)
                                                   
        returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,self.objTomado,-1,vrep.simx_opmode_blocking)
        returnCode,positionMesaIzq=vrep.simxGetObjectPosition(self.clientID,mesaIzq,-1,vrep.simx_opmode_blocking)  
        returnCode,positionMesaDer=vrep.simxGetObjectPosition(self.clientID,mesaDer,-1,vrep.simx_opmode_blocking)
                                        
        if errorCode==vrep.simx_error_noerror:
            if((positionMesaIzq[0]-0.20)<=positionObj1[0] and (positionMesaIzq[0]+0.20)>=positionObj1[0] and (positionMesaIzq[1]-0.20)<=positionObj1[1] and (positionMesaIzq[1]+0.20)>=positionObj1[1]):
                
                if (self.obj3Id==self.objTomado or self.obj2Id==self.objTomado or self.obj6Id==self.objTomado):
                    
                    vrep.simxSetObjectPosition(self.clientID,self.objTomado,-1,self.posicionIni[self.cont],vrep.simx_opmode_oneshot)
                    self.cont = self.cont+1
                    self.objTomado=0
                    return self.kinectVisionRGB(),1,self.quedaAlgo()
                
            if((positionMesaDer[0]-0.20)<=positionObj1[0] and (positionMesaDer[0]+0.20)>=positionObj1[0] and (positionMesaDer[1]-0.20)<=positionObj1[1] and (positionMesaDer[1]+0.20)>=positionObj1[1] ):
                if (self.obj1Id==self.objTomado or self.obj4Id==self.objTomado or self.obj5Id==self.objTomado):
                    vrep.simxSetObjectPosition(self.clientID,self.objTomado,-1,self.posicionIni[self.cont],vrep.simx_opmode_oneshot)
                    self.cont = self.cont+1
                    self.objTomado=0
                    return self.kinectVisionRGB(),1,self.quedaAlgo()
            
            return self.kinectVisionRGB(),0,self.quedaAlgo()

        else:
            print ('Error. Completado', errorCode)
            return False,0

    def seleccion(self, accion):
        if(accion==0):
            self.tomarObjeto('m_Sphere')           
            
            return self.completado()
            
        
        if(accion==1):
            self.moverLados('m_Sphere','customizableTable_tableTop#0')  
            return self.completado()
        
        if(accion==2):
            self.moverLados('m_Sphere','customizableTable_tableTop#1')  
            return self.completado()
        
        if(accion==3):
            self.soltarObjeto('m_Sphere')
            return self.completado()
            
        if(accion==4):
            self.volverCasa()
            return self.completado() 
            
        if(accion==5):
            self.restartScenario()
            return self.completado()

        
    #end of Reward method
    
    
    