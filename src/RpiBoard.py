'''
Created on Mar 4, 2017
RpiBoard is initialized by the registration trigger
All Devices during the registration is the final set of devices

@author: chacktho
'''
#import RPi.GPIO as GPIO
from RPi import GPIO
from RpiDevice import RpiDevice

class RpiBoard:
    '''
    classdocs
    '''
        
    GPIO_MODE = [GPIO.BCM, GPIO.BOARD]

    def __init__(self, board, controller, gpioMode=GPIO.BOARD): 
        self.gpioMode = None
        self.devices = {}
        self.controller = controller
        self.enabled = board.getEnabled()
        if gpioMode in RpiBoard.GPIO_MODE:
            GPIO.setmode(gpioMode)
            self.gpioMode = GPIO.getmode() 
            self.loadChannels(board)
        
    def isEnabled(self):
        ret = False
        if self.enabled == 'true':
            ret = True
            
        return ret
    
    def loadChannels(self, board):
        devices = board.getDevices()
        for dId in devices:
            device = devices[dId]
            rpiDevice = RpiDevice(device,board, self.controller)
            self.devices[rpiDevice.getId()] = rpiDevice
            
    def activate(self, boardCfg, enabled):
        if enabled == False:
            self.disableAllDevices()
        else:
            self.activateDevices(boardCfg)
           
    def disableAllDevices(self):
        for dId in self.devices:
            device = self.devices[dId]
            device.disable()
        
    def activateDevices(self, board):
        dCfgs = board.getDevices()
        for dId in dCfgs:
            deviceCfg = dCfgs[dId]
            device = self.getDevice(dId)
            if device is None:
                continue
            device.activate(deviceCfg)
            
    def getDevices(self):
        return self.devices
    
    def getDevice(self, deviceId):
        deviceIds = self.devices.keys()
        if deviceId in deviceIds:
            return self.devices[deviceId]
        return None
        
    def turnOffChannel(self, deviceId, channelId):
        device = self.devices[deviceId]
        device.turnOffChannel()
        
    def turnOnChannel(self, deviceId, channelId):
        device = self.devices[deviceId]
        device.turnOnChannel()
               
    def resetBoard(self):
        if self.gpioMode is not None:
            GPIO.cleanup() 
            GPIO.setmode(self.gpioMode)
        
    def reloadChannels(self, boardCfg):
        self.enabled = boardCfg.getEnabled()
        devicesCfg = boardCfg.getDevices()
        for deviceCfg in devicesCfg:
            if deviceCfg not in self.devices:
                print "New configuration has a new device. This is not allowed. Ignoring the device = " + deviceCfg
                continue
            rpiDevice = self.devices[deviceCfg]
            rpiDevice.reloadChannels(devicesCfg[deviceCfg])

        
        