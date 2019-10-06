# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:40:16 2019

@author: javie
"""
import vrep
import math
import numpy as np
import time
class Simulador(object):
 
    def __init__(self):
        self.clientID,self.home = self.connectRobot()
        self.home[2]=(self.home[2]-0.2)
        if self.clientID != -1:
            self.actionNumber = 1
            #self.performAnAction(4) #go home
        #endif
    #end of __init__ method

    def connectRobot(self):
        vrep.simxFinish(-1)
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
        if clientID!=-1:
            print ('Conectado a la remote API server with clientID: ', clientID)
            vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait) 
            errorCode1, handleJoint = vrep.simxGetObjectHandle(clientID,'m_Sphere' , vrep.simx_opmode_oneshot_wait)
            returnCode,home=vrep.simxGetObjectPosition(clientID,handleJoint,-1,vrep.simx_opmode_blocking)#deje estatico la primera posicion de target
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
        self.performAnAction(100)
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
            print ('Error. Got no handle: ', errorCode, errorCode1)
    #end of moveTarget method
    
    def moverLados(self,moveTarget,Object):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget , vrep.simx_opmode_oneshot_wait)
        errorCode, obj = vrep.simxGetObjectHandle(self.clientID, Object, vrep.simx_opmode_oneshot_wait)
                                                  
        if errorCode1==vrep.simx_error_noerror and errorCode==vrep.simx_error_noerror :
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            n=(positionObj1[0],positionObj1[1],positionObj1[2]+0.25)
            vrep.simxSetObjectPosition(self.clientID,handleJoint,-1,n,vrep.simx_opmode_oneshot)
            
            time.sleep(1)
            
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)

            n=(positionObj1[0],positionObj1[1],positionTar[2])
            
            while round(positionTar[2],3)>=round((positionObj1[2]+0.12),3): 
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
            
            
        else:
            print ('Error. Got no handle: ', errorCode, errorCode1)
    #end of moveLeft method
    
    def tomarObjeto(self, moveTarget, Object):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget, vrep.simx_opmode_oneshot_wait)
        errorCode, obj = vrep.simxGetObjectHandle(self.clientID, Object, vrep.simx_opmode_oneshot_wait)

        if errorCode1==vrep.simx_error_noerror and errorCode==vrep.simx_error_noerror :
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            
            n=(positionObj1[0],positionObj1[1],positionTar[2])

            while round(positionTar[2],3)>=round((positionObj1[2]+0.05),3): 
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
            print ('Error. Got no handle: ', errorCode)
    #end of orientationTarget method
    
    def soltarObjeto(self, moveTarget, Object):
        errorCode1, handleJoint = vrep.simxGetObjectHandle(self.clientID, moveTarget, vrep.simx_opmode_oneshot_wait)
        errorCode, obj = vrep.simxGetObjectHandle(self.clientID, Object, vrep.simx_opmode_oneshot_wait)
        
        if errorCode1==vrep.simx_error_noerror and errorCode==vrep.simx_error_noerror :
            returnCode,positionTar=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
            returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,obj,-1,vrep.simx_opmode_blocking)
            returnCode,distanciaTarObj1=vrep.simxGetObjectPosition(self.clientID,obj,handleJoint,vrep.simx_opmode_blocking)

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
                
        else:
            print ('Error. Got no handle: ', errorCode)
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
            print ('Error. Got no handle: ', errorCode)
    #end of orientationTarget method
    
    def kinectVisionRGB(self):
        errorCode,rgb=vrep.simxGetObjectHandle(self.clientID,'kinect_rgb',vrep.simx_opmode_oneshot_wait)

        if errorCode==vrep.simx_error_noerror :        
            res,resolution,imegenRgb=vrep.simxGetVisionSensorImage(self.clientID,rgb,0,vrep.simx_opmode_buffer)
            
            imgRgb = np.array(imegenRgb,dtype=np.uint8)
            
            imgRgb.resize([200,200,3])
            
            imgRgb= np.expand_dims(imgRgb, axis=0)
        
        else:
            print ('Error. Got no handle: ', errorCode)
        
        return imgRgb
    #end of KinectVisionRGB method
    
    def kinectVisionPATH(self):
        errorCode1,path=vrep.simxGetObjectHandle(self.clientID,'kinect_depth',vrep.simx_opmode_oneshot_wait)


        if errorCode1==vrep.simx_error_noerror :        
            res,resolution,imagenPath=vrep.simxGetVisionSensorImage(self.clientID,path,0,vrep.simx_opmode_buffer)

            imgPath = np.array(imagenPath,dtype=np.uint8)
            imgPath.resize([resolution[1],resolution[0],3])
        
        else:
            print ('Error. Got no handle: ', errorCode1)
        
        return imgPath
    #end of KinectVisionPATH method
    
    def completado (self, Objeto): #True dejo en su lugar el objeto !!! SOLO MESA IZQ!!!
        errorCode, handleJoint = vrep.simxGetObjectHandle(self.clientID, Objeto, vrep.simx_opmode_oneshot_wait)
        errorCode, Mesa = vrep.simxGetObjectHandle(self.clientID, 'customizableTable_tableTop#0', vrep.simx_opmode_oneshot_wait)
                                                   
        returnCode,positionObj1=vrep.simxGetObjectPosition(self.clientID,handleJoint,-1,vrep.simx_opmode_blocking)
        returnCode,positionMesa=vrep.simxGetObjectPosition(self.clientID,Mesa,-1,vrep.simx_opmode_blocking)   
                                        
        if errorCode==vrep.simx_error_noerror:
            if((positionMesa[0]-0.20)<=positionObj1[0] and (positionMesa[0]+0.20)>=positionObj1[0] and (positionMesa[1]-0.20)<=positionObj1[1] and (positionMesa[1]+0.20)>=positionObj1[1] ):
                
                return self.kinectVisionRGB(),1,True
            
            
            return self.kinectVisionRGB(),0,False

        else:
            print ('Error. Got no handle: ', errorCode)
            return False,0

    def seleccion(self, accion):
        if(accion==0):
            self.tomarObjeto('m_Sphere','Cylinder')
            
            return self.completado('Cylinder')
        if(accion==1):
            self.moverLados('m_Sphere','customizableTable_tableTop#0')
            
            return self.completado('Cylinder')
        if(accion==2):
            self.moverLados('m_Sphere','customizableTable_tableTop#1')
            
            return self.completado('Cylinder')
        if(accion==3):
            self.volverCasa()
            
            return self.completado('Cylinder')
        
        
    #end of Reward method  
    
    
    