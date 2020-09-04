'''
Created on 29-Mar-2017

@author: root
'''
from Schedule import Schedule

class Scheduler(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.schedules = {}

    def addSchedule(self, schedule, deviceId):
        '''
        Constructor
        '''
        if schedule is None:
            return
        s = self.createSchedule(schedule)
        if s is not None:
            self.schedules[deviceId] = s
        else:
            print 'Invalid schedule for device ' + deviceId
            
    def createSchedule(self, schedule):
        if self.validateSchedule(schedule) is False:
            return None
        s = Schedule(schedule)
        return s
    
    def validateSchedule(self, schedule):
        if schedule is None:
            return False
        return True
        
    def isScheduleReached(self, deviceId):
        schedule = self.getSchedule(deviceId)
        if schedule is None:
            return False
        return schedule.match()
    
    def isRecurrencePassed(self, deviceId):
        schedule = self.getSchedule(deviceId)
        if schedule is not None:
            return schedule.isRecurrencePassed()
        return False
        
    def getSchedule(self, deviceId):
        if deviceId in self.schedules:
            return self.schedules[deviceId]
        print 'No schedule found for device ' + deviceId
        return None
    
    def getDeviceIds(self):
        keys = list(self.schedules);
        return keys
    
        
    
    
        
            
            