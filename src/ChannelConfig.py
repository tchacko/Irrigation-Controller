'''
Created on Mar 5, 2017

@author: chacktho
'''
from Constants import Constants
 
class ChannelConfig(object):
    '''
    classdocs
    '''


    def __init__(self, data, deviceCfg):
        '''
        Constructor
        '''
        if data is None:
            return
        
        self.number = None
        self.enabled = None
        self.type = None
        self.device = deviceCfg
        self.action = None
        
        if 'number' in data:
            self.number = data['number']
        if 'enabled' in data:
            self.enabled = data['enabled']
        if 'type' in data:
            self.type = data['type']
        if 'action' in data:
            self.action = data['action']
        
    def getType(self):
        return self.type
    
    def getNumber(self):
        return self.number
    
    def getId(self):
        return self.getNumber()
    
    def isEnabled(self):
        enabled = False
        if self.enabled == 'true':
            enabled = True
        return enabled
    
    def getEnabled(self):
        return self.enabled
    
    def getAction(self):
        return self.action
    
    def getDeviceAction(self):
        if self.device is None:
            if self.getAction() is not None:
                return self.getAction()
            else:
                return Constants.CHANNEL_OFF
        else:
            if self.device.getDeviceAction() is not None:
                return self.device.getDeviceAction()
            else:
                return Constants.CHANNEL_OFF
            
    
    def compare(self, newChannel):
        if self.compareChannelConfig(newChannel) == True:
            return True
        return False
    
    
    def compareChannelConfig(self, newChannel):
        if newChannel.getNumber() != self.getNumber() or \
           newChannel.getType() != self.getType() or \
           newChannel.getEnabled() != self.getEnabled() or \
           newChannel.getAction() != self.getAction():
            return True
        return False
    
        
    def toString(self):
        return '            ChannelConfig => number='+self.number+', enabled='+self.enabled+', type='+self.type + '\n'
    