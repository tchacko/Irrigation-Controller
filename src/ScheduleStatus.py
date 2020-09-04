'''
Created on 09-Apr-2017

@author: root
'''
import Utils
import json

class ScheduleStatus(object):
    '''
    classdocs
    '''
    STATUS_FILE = 'data/status/schedule-status.json'
    
    STATUS_CODES = [0, 1, 2, 3]
    STATUS_STR = ['initialized','running','completed','stopped']
    
    SCHEDULE_STATUS_INITIALIZED = 0
    SCHEDULE_STATUS_RUNNING = 1
    SCHEDULE_STATUS_COMPLETED = 2
    SCHEDULE_STATUS_STOPPED = 3
    
    
    status = {}



    def __init__(self, deviceId):
        '''
        Constructor
        '''
        if deviceId not in ScheduleStatus.status:
            ScheduleStatus.status[deviceId] = self
            self.deviceId = deviceId
            self.status = ScheduleStatus.SCHEDULE_STATUS_INITIALIZED
            self.timestamp = Utils.getTimeMs()
            self.lastUpdateTime = Utils.getTimeMs()
            self.runningTime = 0
            
    @staticmethod 
    def getScheduleStatus(deviceId):
        if deviceId in ScheduleStatus.status:
            return ScheduleStatus.status[deviceId]
        return None
    
    def getStatus(self):
        return self.status;
    
    def getRunningTime(self):
        if self.status == ScheduleStatus.SCHEDULE_STATUS_RUNNING:
            return self.runningTime;
        return 0;
            
    def updateStatus(self, statusCode):
        if self.verifyStatusCode(statusCode) == False:
            print 'Unknown status code ' + str(statusCode)
            return
        
        if statusCode == ScheduleStatus.SCHEDULE_STATUS_RUNNING and self.status != ScheduleStatus.SCHEDULE_STATUS_RUNNING:
            self.runningTime = 0
        elif statusCode == ScheduleStatus.SCHEDULE_STATUS_RUNNING and self.status == ScheduleStatus.SCHEDULE_STATUS_RUNNING:
            if self.lastUpdateTime > 0:
                self.runningTime = self.runningTime + (Utils.getTimeMs() - self.lastUpdateTime)

        if statusCode != self.status:
            self.timestamp = Utils.getTimeMs()
        
        self.status = statusCode
        self.lastUpdateTime = Utils.getTimeMs()

        self.persistStatus()
    
    def updateTime(self, timeMs=None):
        if timeMs is None:
            timeMs = Utils.getTimeMs()
            
        if self.status == ScheduleStatus.SCHEDULE_STATUS_RUNNING:
            self.runningTime = self.runningTime + (timeMs - self.lastUpdateTime)
            
        self.lastUpdateTime = timeMs
        self.persistStatus()        
    
    def verifyStatusCode(self, statusCode):
        if statusCode in ScheduleStatus.STATUS_CODES:
            return True
        return False
    
    def lastUpdate(self, timeMs=None):
        if timeMs is None:
            timeMs = Utils.getTimeMs()
        self.lastUpdateTime = timeMs
        self.persistStatus()
        
    def persistStatus(self):
        jsonObj = self.buildJSONObject()
        with open(ScheduleStatus.STATUS_FILE, 'w') as fh: 
            try:
                json.dump(jsonObj,fh)
                fh.close()
            except:
                fh.close();
                raise ValueError('Failed to write the Schedule Status to: '+ScheduleStatus.STATUS_FILE)
            
    def buildJSONObject(self):
        data = self.loadJsonFromFile()
        device = self.getThisDeviceStatus(data['schedule-status'])
        if device is None:
            device = {}
            device['id'] = self.deviceId
            data.append(device)
        
        device['status'] = ScheduleStatus.STATUS_STR[ScheduleStatus.SCHEDULE_STATUS_INITIALIZED]
        device['timestamp'] = self.timestamp
        device['update-time'] = self.lastUpdateTime
        device['running-time'] = self.runningTime
        return data  
          
    def loadJsonFromFile(self):
        data = None
        with open(ScheduleStatus.STATUS_FILE) as dataFile:   
            try: 
                data = json.load(dataFile);
                dataFile.close()
            except  ValueError:
                dataFile.close()
        return data
    
    def getThisDeviceStatus(self, data):
        devices = None
        if 'device' in data:
            devices = data['device']
        if devices is None:
            return None
        for device in devices:
            if 'id' not in device:
                continue
            myId = device['id']
            if myId == self.deviceId:
                return device
        return None
            