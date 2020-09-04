'''
Created on 09-Apr-2017

@author: root
'''
from Scheduler import Scheduler
import Utils
from ScheduleStatus import ScheduleStatus
from FileMonitor import Task

class ScheduleManager(object):
    '''
    classdocs
    '''


    def __init__(self, controller, evtProcessor):
        '''
        Constructor
        '''
        self.controller = controller
        self.eventProcessor = evtProcessor
        self.scheduler = Scheduler()
        
    def addDeviceSchedules(self, devices):
        for deviceId in devices:
            device = devices[deviceId]
            scheduleStr = device.getSchedule()
            self.addSchedule(scheduleStr, deviceId)
            
    def addSchedule(self, schedule, deviceId):
        self.scheduler.addSchedule(schedule, deviceId)
        ScheduleStatus(deviceId)
        
    def getSchedule(self, deviceId):
        return self.scheduler.getSchedule(deviceId)
        
    def isScheduleReached(self, deviceId):
        return self.scheduler.isScheduleReached(deviceId)
    
    def checkSchedules(self):
        self.execute()
        
    def execute(self):
        devices = self.scheduler.getDeviceIds()
        for deviceId in devices:
            self.updateScheduleStatusTime(deviceId)
            print 'processing schedule for ' + deviceId + ' at ' + Utils.getFormatedTime()
            if not self.isRecurrencePassed(deviceId) and self.scheduler.isScheduleReached(deviceId):
                print 'schedule time has reached for device ' + deviceId
                # Check scheduleStatus for the device status, runtime, pending time
                if self.isScheduleCompleted(deviceId):
                    print 'device ' + deviceId + ' is already completed the scheduled run'
                    continue
                if self.isDeviceActivated(deviceId):
                    print 'device ' + deviceId + ' is already activated'
                    #check for the end
                    if self.isScheduleEnding(deviceId):
                        self.stopDevice(deviceId)
                        self.scheduler.cancelScheduleIfRequired(deviceId)
                    continue
                #if self.isRunConmpleted(deviceId):
                #    print 'device ' + deviceId + ' has completed the run'
                #   self.updateScheduleStatus(deviceId, ScheduleStatus.SCHEDULE_STATUS_COMPLETED)
                #    continue
                
                print 'Activating the device ' + deviceId
                self.activateDevice(deviceId)
                #self.updateScheduleStatus(deviceId, ScheduleStatus.SCHEDULE_STATUS_RUNNING)
            else:
                print 'schedule time has not reached for device ' + deviceId
                
    def updateScheduleStatusTime(self, deviceId):
            status = ScheduleStatus.getScheduleStatus(deviceId)
            if status is not None:
                status.updateTime()
                
    def updateScheduleStatus(self, deviceId, statusCode):
            status = ScheduleStatus.getScheduleStatus(deviceId)
            if status is not None:
                status.updateStatus(statusCode)
    
    def isScheduleEnding(self, deviceId):
        schedStatus = ScheduleStatus.getScheduleStatus(deviceId)
        if schedStatus is None:
            return False
        if schedStatus.getStatus() != ScheduleStatus.SCHEDULE_STATUS_RUNNING:
            return False
        
        sched = self.scheduler.getSchedule(deviceId)
        schedDuration = sched.getScheduleDurationInSec()
        schedElapsedTime = schedStatus.getRunningTime()
        schedElapsedTime = schedElapsedTime/1000
        if schedElapsedTime >= schedDuration:
            return True
        return False   
    
    def isRecurrencePassed(self, deviceId):
        sched = self.scheduler.getSchedule(deviceId)
        if sched is None:
            return False
        sched.isRecurrencePassed()
    
    def isScheduleCompleted(self, deviceId):
        schedStatus = ScheduleStatus.getScheduleStatus(deviceId)
        if schedStatus is not None:
            if schedStatus.getStatus() == ScheduleStatus.SCHEDULE_STATUS_COMPLETED:
                return True
            sched = self.scheduler.getSchedule(deviceId)
            schedDuration = sched.getScheduleDurationInSec()
            schedElapsedTime = schedStatus.getRunningTime()
            schedElapsedTime = schedElapsedTime/1000
        
            if schedElapsedTime > schedDuration:
                return True
        else:
            print 'Schedule Status not found for device ' + deviceId
        return False
                    
                
    
    def isDeviceActivated(self, deviceId):
        # check the Schedule status first, if it is not in running state
        # check the board/device status, if it running then 
        # update Schedules status and return true
        schedStatus = ScheduleStatus.getScheduleStatus(deviceId)
        if schedStatus is not None:
            if schedStatus.getStatus() == ScheduleStatus.SCHEDULE_STATUS_RUNNING:
                return True
        
        rpiChannel = self.getDeviceControlChannel(deviceId)
        if rpiChannel is None:
            return False
        
        devStatus = rpiChannel.getChannelStatus()
        if devStatus == 0:
            self.updateScheduleStatus(deviceId, ScheduleStatus.SCHEDULE_STATUS_RUNNING)
            return True
        
        return False
    
    def getDeviceControlChannel(self, deviceId):
        boardManager = self.controller.getBoardManager()
        rpiBoard = boardManager.getBoard('1'); # default board id is 0
        rpiDevice = rpiBoard.getDevice(deviceId)
        if rpiDevice is None:
            return None
        
        rpiChannel = rpiDevice.getControlChannel()
        return rpiChannel
    
    def stopDevice(self, deviceId):
        event = DeviceTriggerEvent('high', deviceId, self.controller, self)
        self.eventProcessor.enqueue(event)
        self.updateScheduleStatus(deviceId, ScheduleStatus.SCHEDULE_STATUS_COMPLETED)
        
    def activateDevice(self, deviceId):
        event = DeviceTriggerEvent('low', deviceId, self.controller, self)
        self.eventProcessor.enqueue(event)
        self.updateScheduleStatus(deviceId, ScheduleStatus.SCHEDULE_STATUS_RUNNING)
        
    def updateStatus(self, deviceId, statusCode ):
        if statusCode in [ScheduleStatus.SCHEDULE_STATUS_COMPLETED, ScheduleStatus.SCHEDULE_STATUS_RUNNING]:
            self.updateScheduleSatus(deviceId, statusCode)
        else:
            print 'Unknown status code ' + statusCode + ' in ScheduleManager::updateScheduleStatus()'
        
        
    '''''''''''''''''''''''''''''''''''''''
    Event Processor
    '''''''''''''''''''''''''''''''''''''''

        
class DeviceTriggerEvent(Task):
    
    def __init__(self, action, deviceId, controller, schedMgr=None ):
        self.action = action
        self.deviceId = deviceId
        self.controller = controller
        self.schedMgr = schedMgr
        
    def execute(self):
        boardMgr = self.controller.getBoardManager()
        device = boardMgr.getDevice('1', self.deviceId)
        if device is None:
            return
        
        ctrChannel = device.getControlChannel()
        if ctrChannel is None:
            return

        if ctrChannel.isEnabled():
            ctrChannel.triggerAction(self.action)
            
        self.update()

    def update(self):
                    
        if self.schedMgr is None:
            return
            
        status = ScheduleStatus.SCHEDULE_STATUS_INITIALIZED
        if self.action == 1:
            status = ScheduleStatus.SCHEDULE_STATUS_COMPLETED
        elif self.action == 0:
            status = ScheduleStatus.SCHEDULE_STATUS_RUNNING
            
        self.schedMgr.updateStatus(self.deviceId, status )
        
        
        
        