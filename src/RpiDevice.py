'''
Created on 11-Mar-2017

@author: chacktho
'''
from RpiChannel import RpiChannel 

class RpiDevice(object):
    '''
    classdocs
    '''


    def __init__(self, device, board, controller):
        '''
        Constructor
        '''
        self.board = board
        self.controller = controller
        self.channels = {}
        self.id = device.getId()
        self.enabled = device.getEnabled()
        self.groupId = device.getGroup()
        self.deviceAction = device.getDeviceAction()
        self.loadChannels(device)
        
    
    def getId(self):
        return self.id
    
    def getEnabled(self):
        return self.enabled
    
    def isEnabled(self):
        ret = False
        if self.enabled == 'true':
            ret =  True
            
        return ret
    
    def getGroup(self):
        return self.groupId
    
    def getDeviceAction(self):
        return self.deviceAction
    
    def loadChannels(self, device):
        channels = device.getChannels()
        for cId in channels:
            channel = channels[cId]
            rpiChannel = RpiChannel(channel, self)
            self.channels[rpiChannel.getNumber()] = rpiChannel
            
    def getChannels(self):
        return self.channels
    
    def getChannel(self, num):
        channel = None
        if num in self.channels:
            channel = self.channels[num]
            
        return channel
            
    def disable(self):
        self.enabled = "false"
        for cId in self.channels:
            channel = self.channels[cId]
            if channel.isControlChannel():
                channel.disable()
                
    def turnOffChannel(self, channelId):
        channel = self.channels[channelId]
        channel.turnOffChannel()
        
    def resumeState(self):
        if self.isEnabled() == False:
            return
        rpiChannel = self.getControlChannel()
        if rpiChannel is None:
            return
        rpiChannel.resumeState()
        
        
    def activate(self, device):
        if device.isEnabled() == False:
            self.disable()
            return
        channels = device.getChannels()
        for cId in channels:
            channelCfg = channels[cId]
            channel = self.channels[cId]
            if channel.isControlChannel():
                channel.activate(channelCfg)
        
    def getControlChannel(self):
        for cId in self.channels:
            rpiChannel = self.channels[cId]
            if rpiChannel.isControlChannel():
                return rpiChannel
            
        return None
    
    def updateDeviceStatus(self, status):
        if self.controller is None:
            return
        
        statusMgr =  self.controller.getStatusManager()
        if statusMgr is None:
            return
        statusMgr.updateDeviceStatus(self.board.getId(), self.getId(), status)
        
    def getDeviceStatus(self):
        if self.controller is None:
            return
        
        statusMgr =  self.controller.getStatusManager()
        if statusMgr is None:
            return
        devStatus = statusMgr.getDeviceStatus(self.board.getId(), self.getId())   
        if devStatus is None:
            return None
        return devStatus.getStatus()    
            
    def reloadChannels(self, deviceCfg):
        self.updateProperties(deviceCfg)
        channelsCfg = deviceCfg.getChannels()
        for channelCfg in channelsCfg:
            if channelCfg not in self.channels:
                print "New configuration has a new channel. Adding channel " +channelCfg + " to RPi Device " + self.getId()
                rpiChannel = RpiChannel(channelsCfg[channelCfg], self)
                self.channels[rpiChannel.getNumber()] = rpiChannel
            else:
                cfg = channelsCfg[channelCfg]  
                number = cfg.getNumber()
                rpiChannel = self.channels[number]
                rpiChannel.updateProperties(cfg)
        self.removeOrphanChannels(deviceCfg)
        
    def updateProperties(self, deviceCfg):
        self.enabled = deviceCfg.getEnabled()
        self.deviceAction = deviceCfg.getDeviceAction()
        
    def removeOrphanChannels(self, deviceCfg):
        channelsCfg = deviceCfg.getChannels()
        oChannels = dict(self.channels)
        for cId in self.channels:
            if cId not in channelsCfg:
                rpiChannel = self.channels[cId]
                rpiChannel.disable()
                del oChannels[cId]
                print 'Removed channel ' + cId + " from device " + deviceCfg.getId()
        self.channels = oChannels
            
        