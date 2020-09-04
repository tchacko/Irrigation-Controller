'''
Created on 08-Mar-2017

@author: root
'''
from Constants import Constants
import Utils 
import json

class DeviceStatus(object):
    '''
    classdocs
    '''
    DEVICE_BASE = Constants.STATUS_BASE_FOLDER
    STATUS_FILE_NAME = 'device-status.json'
    BOARD_PREFIX = 'board-'
    DEVICE_PREFIX = 'device-'
    CHANNEL_PREFIX = 'channel-'
    CHANNEL_STATUS_FILE = 'channel-status.json'

    def __init__(self, device, boardStatus):
        '''
        Constructor
        '''
        if device is None:
            print 'Device is None'
            return
        self.device = Utils.deepCopy(device)
        self.board = Utils.deepCopy(boardStatus)
        self.deviceStatus = InternalStatus()
        self.channelStatus = None
        self.schedule = None
        
        self.create()
        
    def getId(self):
        return  self.device.getId()
        
    def create(self):
        if self.device is None:
            print 'Device is None'
            return
        
        base = Constants.STATUS_BASE_FOLDER
        Utils.makeDir(base)
        base = base + '/' + Constants.BOARD_PREFIX + self.board.getId() 
        Utils.makeDir(base)
        base = base + '/' + Constants.DEVICE_PREFIX + self.device.getId()
        Utils.makeDir(base)
        
        self.updateStatus()
    
    def updateStatus(self, status=None):
        self.deviceStatus = InternalStatus(self.updateDeviceStatus(status))
        self.channelStatus = Utils.deepCopy(self.updateChannelStatus())
        

    def updateDeviceStatus(self, status = None):
        jsonObj = self.buildDeviceSatusJSONObject(status)
        statusFilePath = Constants.STATUS_BASE_FOLDER+ '/' + Constants.BOARD_PREFIX + self.board.getId() \
            + '/' + Constants.DEVICE_PREFIX + self.device.getId() + '/'+ DeviceStatus.STATUS_FILE_NAME
        with open(statusFilePath, 'w') as fh: 
            try:
                json.dump(jsonObj,fh)
                fh.close()
            except:
                fh.close();
                raise ValueError('Failed to write the configuration '+statusFilePath)
        return jsonObj
    
    def getStatus(self):
        self.deviceStatus.getStatus()
    
    def getElapsedTime(self):
        return Utils.getTimeMs() - self.deviceStatus.getLastUpdateTime()
    
        
    def buildDeviceSatusJSONObject(self, status=None):
        data = {}
        data['id'] = self.device.getId()
        data['enabled'] = self.device.getEnabled()
        if status is not None:
            if self.deviceStatus.getStatus() != status:
                data['last-update-time'] = Utils.getTimeMs()
                data['status'] = status
        else:
            data['last-update-time'] = Utils.getTimeMs()
            data['status'] = 'stopped'
        return data
    
    def updateChannelStatus(self):
        jsonObject = self.buildChannelStatusJSONObject()
        
        path = Constants.STATUS_BASE_FOLDER+ '/' + Constants.BOARD_PREFIX + self.board.getId() \
            + '/' + Constants.DEVICE_PREFIX + self.device.getId() + '/'+ DeviceStatus.CHANNEL_PREFIX \
            + self.device.getControlChannel().getId()
        Utils.makeDir(path)
        statusFilePath = path + '/' + DeviceStatus.CHANNEL_STATUS_FILE
        
        with open(statusFilePath, 'w') as fh: 
            try:
                json.dump(jsonObject,fh)
                fh.close()
            except:
                fh.close();
                raise ValueError('Failed to write the configuration '+statusFilePath)
        return jsonObject
    
    def buildChannelStatusJSONObject(self):
        channel = self.device.getControlChannel()
        data = {}
        data['number'] = channel.getNumber()
        data['enabled'] = channel.getEnabled()
        
        if self.schedule is not None:
            data['status'] = self.schedule['status'] # scheduled/running/stopped/not-scheduled
            data['next-run'] =self.schedule['next-run'] # '20170316:203000'
            data['run-duration'] = self.schedule['duration'] #'030000'
            data['run-completed'] = self.schedule['completed'] #'000000'
            data['time-stamp'] = self.schedule['time-stamp'] 
        return data
    
    def refresh(self, boardStatus, device, schedule):
        if device is not None:
            self.device = Utils.deepCopy(device)
            self.board = Utils.deepCopy(boardStatus)
        self.schedule = Utils.deepCopy(schedule)
        self.updateStatus();

        
    
    def getBoardId(self):
        return self.board.getId()
    
        
    def getDeviceStatus(self):
        return self.deviceStatus
    
    def getEnabled(self):
        return self.deviceStatus.getEnabled()
    
    def getLastUpdateTime(self):
        return self.deviceStatus.getLastUpdateTime()

    def getDeviceStatusObject(self):
        obj = {}
        obj['id'] = self.getId()
        obj['enabled'] = self.getEnabled()
        obj['last-update-time'] = self.getLastUpdateTime()
        obj['elapsed-time'] = self.getElapsedTime()
        return obj
    
class InternalStatus():
    def __init__(self, statusData=None):
        
        self.id = ''
        self.enabled = 'false'
        self.status = 'stopped'
        self.lastUpdateTime = Utils.getTimeMs()
        
        if statusData is None:
            return
        
        if 'id' in statusData:
            self.id = statusData['id']
        if 'enabled' in statusData:
            self.enabled = statusData['enabled']
        
        if 'status' in statusData:
            self.status = statusData['status']
        if 'last-update-time' in statusData:
            self.lastUpdateTime = statusData['last-update-time']
            
    def getId(self):
        return self.id
    
    def getEnabled(self):
        return self.enabled
    
    def getStatus(self):
        return self.status
    
    def getLastUpdateTime(self):
        return self.lastUpdateTime

    def getElapsedTime(self):
        return Utils.getTimeMs() - self.getLastUpdateTime()
    
    
            
        
        
    
    
    
        