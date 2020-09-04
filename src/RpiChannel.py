'''
Created on Mar 4, 2017

@author: chacktho
'''
#import RPi.GPIO as GPIO
from RPi import GPIO
from Constants import Constants
import Utils

class RpiChannel(object):
    '''
    classdocs
    '''
    def __init__(self, channel, device):
        self.gpio = None
        self.device = device
        self.channel = int(channel.getNumber())
        enabled = channel.getEnabled()
        ctype = channel.getType()
        operation = Constants.CHANNEL_TYPE[Constants.IN]
        if ctype == "io":
            operation = Constants.CHANNEL_TYPE[Constants.OUT]
            
        self.action = channel.getAction()
        
        channelNums = Constants.CHANNELS.values()
        if self.channel not in channelNums:
            self.channel = Constants.UNKNOWN_CHANNEL
            
        
        if self.channel != Constants.UNKNOWN_CHANNEL:
            self.gpio = GpioChannel(self.channel, operation, enabled)
        else:
            raise ValueError ("Channel number " + channel.getNumber() + " is not a valid channel")
        
    def updateProperties(self, channelCfg):
        self.enabled = channelCfg.getEnabled()
        self.action = channelCfg.getAction()
        if self.gpio is None:
            return
        self.gpio.enable(self.enabled)

            
    def getNumber(self):
        return str(self.gpio.getChannel())
    
    def getAction(self):
        return self.action
    
    def isEnabled(self):
        if self.gpio is None:
            return False
        return self.gpio.isEnabled()
                 
    def isControlChannel(self):
        if self.gpio is None:
            return False
        
        if self.gpio.getOperation() == Constants.CHANNEL_TYPE[Constants.OUT]:
            return True
        return False
    
    def turnOnChannel(self, ignoreStatus=False):
        status = 0 #self.getChannelStatus()        
        if self.isControlChannel(): 
            if ignoreStatus is False:
                if self.device.getDeviceStatus() == Utils.translateStatus(status): #Already in running state
                    return
            
            GPIO.output(self.gpio.getChannel(), Constants.CHANNEL_ON)
            self.device.updateDeviceStatus(Utils.translateStatus(status))
    
    def tunOffChannel(self):
        status = 1 #self.getChannelStatus()
        if self.isControlChannel():
            if self.device.getDeviceStatus() == Utils.translateStatus(status): #Already in stopped state
                return
            
            GPIO.output(self.gpio.getChannel(), Constants.CHANNEL_OFF)
            self.device.updateDeviceStatus(Utils.translateStatus(status))
                
    def getChannelStatus(self):
        status = Constants.DEFAULT_OUT_VALUE
        if self.gpio is not None:
            status = GPIO.input(self.gpio.getChannel()) 
        return status
    
    def disable(self):
        if self.gpio is None:
            return
        
        self.gpio.disable()
        self.tunOffChannel()
        
        
    def resumeState(self):
        if self.isEnabled() == False:
            return
        action = self.device.getDeviceAction()
        self.doAction(Utils.translateAction(action), True)       
        
        
        
    def activate(self, channelCfg):
        if channelCfg.isEnabled() is False:
            self.disable()
            return
        
        action = channelCfg.getDeviceAction()
        if 'manual-trigger' in action:
            if action['manual-trigger'] != 'enabled':
                self.disable()
                return 
        self.doAction(Utils.translateAction(action))
                
    def triggerAction(self, action):
        #if self.action == action:
            self.doAction(Utils.translateAction(action))
            
    def doAction(self, action, ignoreStatus=False):
        if action == 0:
            self.turnOnChannel(ignoreStatus)
            return
        if action == 1:
            self.tunOffChannel()
            return

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

class GpioChannel:
    def __init__(self, channel, operation, enabled):
        self.number = channel
        self.operation = operation
        self.enabled = enabled
        
        GPIO.setup(self.number, self.operation)
        
    def getChannel(self):
        return self.number
    
    def getOperation(self):
        return self.operation
    
    def isEnabled(self):
        if self.enabled == "true":
            return True
        else:
            return False
    
    def disable(self):
        self.enabled = "false"
    
    def enable(self, value):
        self.enabled = value

    