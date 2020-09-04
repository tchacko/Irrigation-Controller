'''
Created on Mar 5, 2017

@author: chacktho
'''
from ChannelConfig import ChannelConfig 

class DeviceConfig(object):
    '''
    classdocs
    '''
    def __init__(self, data, board):
        '''
        Constructor
        '''
        self.board = board
        self.channels = {}
        self.groupId = None
        self.id = None
        self.enabled = None
        
        if data is None:
            return
        
        self.groupId = data['groupid'];
        self.enabled = data['enabled']
        self.id = data['id']
        self.action = None
        self.deviceAction = None
        self.schedule = None
        
        if 'action' in data:
            self.action = data['action']
            
        if 'device-action' in data:
            self.deviceAction = data['device-action']
        
        if 'schedule' in data:
            self.schedule = data['schedule']
        
        self.addChannels(data['channel'])
        
        
        
    def addChannels(self, data):
        if data is None:
            return
        for channel in data:
            configCfg = ChannelConfig(channel, self)
            if configCfg.number in self.channels:
                print 'Duplicate channel ' + configCfg.number + ' found in device' + self.getId() + ', board ' + self.board.getId()
                continue
            self.channels[configCfg.number] = configCfg
            
    def isEnabled(self):
        if self.enabled == 'true':
            return True
        else:
            return False
    
    def getControlChannel(self):
        for c in self.channels:
            channel = self.channels[c];
            if channel.getType() == 'io':
                return channel
        return None
    
    def getBoard(self):
        return self.board
    
    def getChannels(self):
        return self.channels
    
    def getId(self):
        return self.id
    
    def getEnabled(self):
        return self.enabled
    
    def getGroup(self):
        return self.groupId
    
    def getDeviceAction(self):
        return self.deviceAction
    
    def getSchedule(self):
        return self.schedule
    
    def compare(self, newDevice):
        if self.compareDeviceConfig(newDevice) == True:
            return True
        if self.compareChannelsConfig(newDevice) == True:
            return True
        return False
    
    def compareDeviceConfig(self, newDevice):
        if newDevice.getId() != self.getId() or newDevice.getGroup() != self.getGroup() or \
            newDevice.getEnabled() != self.getEnabled() or \
            newDevice.getDeviceAction() != self.getDeviceAction() or newDevice.getSchedule() != self.getSchedule():
            return True
        return False
    
    def compareChannelsConfig(self, newDevice):
        if newDevice is None:
            return False
    
        newChannels = newDevice.getChannels()
        
        newIds = newChannels.keys()
        myIds = self.channels.keys()
        
        if len(newIds) != len(myIds):
            return True
        
        if self.channelsDeleted(newChannels) == True:
            return True
        
        for cId in newChannels:
            channel = newChannels[cId]
            if self.isNewChannel(channel) is True:
                return True
            if self.compareChannel(channel) is True:
                return True
                
        return False    
    
        
    def isNewChannel(self, channel):
        cId = channel.getId();
        Ids = self.channels.keys()
        if cId in Ids:
            return False
        
        return True
    
    def compareChannel(self, newChannel):
        cId = newChannel.getId()
        myChannel = self.channels[cId]
        if myChannel.compare(newChannel) == True:
            return True
        
        return False
    
    def channelsDeleted(self, newChannel):
        Ids = newChannel.keys()
        for myId in self.channels:
            if myId in Ids:
                continue
            else:
                return True
        return False
        
    def toString(self):
        outStr = '        DeviceConfig => id='+self.id+', enabled='+self.enabled+', groupid='+self.groupId +'\n'
        for c in self.channels:
            chan = self.channels[c]
            outStr = outStr + chan.toString();
        return outStr
            