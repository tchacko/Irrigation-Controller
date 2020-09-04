'''
Created on Mar 5, 2017

@author: chacktho
'''
from DeviceConfig import DeviceConfig 

class RpiBoardConfig(object):
    '''
    classdocs
    '''
    def __init__(self, board, controller):
        '''
        Constructor
        '''
        self.controller = controller
        self.devices = {}
        self.id = board['id']
        self.mode = board['mode']
        self.enabled = board['enabled']
        
        self.addDevices(board['device'])
    
    def addDevices(self, data):
        if data is None:
            return
        
        for deviceData in data:
            device = DeviceConfig(deviceData, self)
            if device.getId() in self.devices:
                print 'Duplicate device id ' + device.getId() + ' in board ' + self.getId()
                continue
            self.devices[device.getId()] = device
    
    def isEnabled(self):
        if self.enabled == 'true':
            return True
        return False
    
    def getDevices(self):
        return self.devices
    
    def getId(self):
        return self.id
    
    def getMode(self):
        return self.mode
    
    def getEnabled(self):
        return self.enabled
    
    
    def compare(self, newBoard):
        if self.compareBoardConfig(newBoard) == True:
            return True
        if self.compareDevicesConfig(newBoard) == True:
            return True
        return False
    
    def compareBoardConfig(self, newBoard):
        if newBoard.getId() != self.getId() or newBoard.getMode() != self.getMode() or newBoard.getEnabled() != self.getEnabled():
            return True
        return False
    
    def compareDevicesConfig(self, newBoard):
        if newBoard is None:
            return False
    
        newDevices = newBoard.getDevices()
        
        newIds = newDevices.keys()
        myIds = self.devices.keys()
        
        if len(newIds) != len(myIds):
            return True
        
        if self.devicesDeleted(newDevices) == True:
            return True
        
        for dId in newDevices:
            device = newDevices[dId]
            if self.isNewDevice(device) is True:
                return True
            if self.compareDevice(device) is True:
                return True
                
        return False    
    
        
    def isNewDevice(self, device):
        dId = device.getId();
        Ids = self.devices.keys()
        if dId in Ids:
            return False
        
        return True
    
    def compareDevice(self, newDevice):
        dId = newDevice.getId()
        myDevice = self.devices[dId]
        if myDevice.compare(newDevice) == True:
            return True
        
        return False
    
    def devicesDeleted(self, newDevice):
        Ids = newDevice.keys()
        for myId in self.devices:
            if myId in Ids:
                continue
            else:
                return True
        return False
    
    
    def toString(self):
        outStr = '    RpiBoardConfig => id='+self.id+', mode='+self.mode+', enabled='+self.enabled +'\n'
        for d in self.devices:
            dev = self.devices[d]
            outStr = outStr + dev.toString();
        return outStr      