'''
Created on Mar 7, 2017

@author: chacktho
'''
import json

class SystemStatus(object): 
    '''
    classdocs
    '''
    BOARD_STATUS_FILE = 'data/board/status.json'
    STATUS_REGISTERED = 'Registered'
    STATUS_NEW = 'New'
    STATUS_UNKNOWN = 'Unknown'
    STATUS_DENIED = 'Denied'
    
    DEVICE_TYPE_RPI_08 = 'Rpi08'
    DEVICE_TYPE_RPI_PROTO = 'Rpi01'

    def __init__(self):
        '''
        Constructor
        '''
        self.uid = None
        self.status = SystemStatus.STATUS_UNKNOWN
        self.device = SystemStatus.DEVICE_TYPE_RPI_08
        self.service_interval = 2
        data = None
        with open(SystemStatus.BOARD_STATUS_FILE) as dataFile: 
            try:   
                data = json.load(dataFile);
                dataFile.close()
            except :
                dataFile.close()
                
            if data is None:
                return
            data = data['board']
            self.uid = data['uid']
            self._deviceId = data['uid']
            self._authKey = data['auth-key']
            self._orgId = data['org-id']
            self._deviceName = data['device-name']
            self._deviceType = data['device-type']
            self._deviceVersion = data['device-version']
            self._softwareRelease = data['software-release']
            self.status = data['status']
            self.service_interval = int(data['service-interval'])
            
    @property
    def deviceId(self):
        return self._deviceId
    
    @property
    def authKey(self):
        return self._authKey
    
    @property
    def orgId(self):
        return self._orgId
    
    @property
    def deviceName(self):
        return self._deviceName
    
    @property
    def deviceType(self):
        return self._deviceType
    
    @property
    def deviceVersion(self):
        return self._deviceVersion
    
    @property
    def softwareRelease(self):
        return self._softwareRelease
    
    
    
    def getUid(self):
        return self.uid
    
    def getDevice(self):
        return self.device
    
    def getStatus(self):
        return self.status
    
    def isRegistered(self):
        reg = False
        if self.status == SystemStatus.STATUS_REGISTERED:
            reg = True
        return reg
    
    def setStatus(self, status):
        self.status = status
    
    
    def getServiceSleepInterval(self):
        return self.service_interval
    
    def setRegistrationStatus(self, name, dId, status):
        if name is self.deviceName():
            self.deviceId = dId
            self.status = status
            self.update()
            
    def update(self, sysStatus=None):
        jsonObj = sysStatus
        if sysStatus is None:
            jsonObj = self.buildSystemSatusJSONObject()
        if sysStatus is None:
            print 'System Status object is not valid. Not saving the data to disk'
            return
        
        statusFilePath = SystemStatus.BOARD_STATUS_FILE
        with open(statusFilePath, 'w') as fh: 
            try:
                json.dump(jsonObj,fh)
                fh.close()
            except:
                fh.close();
                raise ValueError('Failed to write the configuration '+statusFilePath)
    
    def buildSystemSatusJSONObject(self):
        data = {}
        board = {}
        data['board'] = board
        
        if self.uid is not None:
            board['uid'] = self.uid
        if  self._authKey is not None:
            board['auth-key'] = self._authKey
        if self.orgId is not None:
            board['org-id'] = self._orgId
        if self.deviceName is not None:
            board['device-name'] = self._deviceName
        if self.deviceType is not None:
            board['device-type'] = self._deviceType
        if self.deviceVersion is not None:
            board['device-version'] = self._deviceVersion
        if self.softwareRelease is not None:
            board['software-release'] = self._softwareRelease
        if self.status is not None:
            board['status'] = self.status
        board['service-interval'] = self.service_interval
        

    

    