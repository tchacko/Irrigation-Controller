'''
Created on 29-Mar-2017

@author: root
'''
import datetime
import time

class Schedule(object):
    '''
    classdocs
    '''

    DAYS = ['mon','tue','wed','thu','fri','sat','sun']

    def __init__(self, schedule):
        '''
        Constructor
        '''
        self.startTime = None
        if 'start' in schedule:
            start = schedule['start']
            self.startTime = self.getTimeInSec(start)
            
        self.endTime = None
        if 'end' in schedule:
            end = schedule['end']
            self.endTime = self.getTimeInSec(end)
            
        self.duration = None
        if 'duration' in schedule:
            duration = schedule['duration']
            self.duration = self.getTimeInSec(duration)
        self.recurrence = None
        if 'recurrence' in schedule:
            rec = schedule['recurrence']
            self.recurrence = ScheduleRecurrence(rec)
        else: # no recurrence, only for today
            self.recurrence = ScheduleRecurrence(self.createStaticRecurrence())

    def createStaticRecurrence(self):
        today = datetime.datetime.today().strftime('%d/%m/%Y')
        recur = {}
        recur['pattern'] = 'once'
        Rrange = {}
        Rrange['start'] = today
        Rrange['end'] = today
        recur['range'] = Rrange
        return recur
             
    def getScheduleDurationInSec(self):
        if self.duration is not None:
            return self.duration
        if self.endTime > self.startTime:
            return self.endTime - self.startTime
            
    def getTimeInSec(self, timeStr):
        hour = 0
        minutes = 0;
        sec = 0
        parts = timeStr.split(':')
        if len(parts) > 0:
            hour = int(parts[0])
        if len(parts) >= 1:
            minutes = int(parts[1])
        if len(parts) >= 2:
            sec = int(parts[2])
            
        return hour*60*60 + minutes*60 + sec
    
    def match(self):
        if self.recurrence is None: # No recurrence
            if self.startTimePassed() and not self.scheduleComplete():
                return True           
            else:
                return False
            
        if self.recurrence.match():
            '''
            match time
            '''
            if self.startTimePassed() and not self.scheduleComplete():
                return True
        return False
    
    def isRecurrencePassed(self, dateStr=None):
        if self.recurrence is None: # today only
            return True
        
        return self.recurrence.dateRangePassed(dateStr)
        
                
    def startTimePassed(self):
        '''
        '''
        now = self.getCurrentTimeInSec()
        if now >= self.startTime:
            return True
        return False
        
    def getCurrentTimeInSec(self):
        now = datetime.datetime.now()
        
        return now.hour*60*60 + now.minute*60 + now.second
        
        
    def scheduleComplete(self):
        scTime = 0;
        if self.duration is not None: # duration has precedence
            scTime = self.startTime + self.duration
        elif self.endTime is not None:
            scTime = self.endTime
            
        now = self.getCurrentTimeInSec()
        if now >= scTime:
            return True
        return False
    
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
class ScheduleRecurrence(object):
    '''
    classdocs
    '''
    def __init__(self, recurrence):
        '''
        Constructor
        '''
        self.pattern = None
        if 'pattern' in recurrence:
            self.pattern = recurrence['pattern']
        self.startDate = None
        self.endDate = None
        if 'range' not in recurrence:
            return
        Rrange = recurrence['range']
        if 'start' in Rrange:
            self.startDate = time.strptime(Rrange['start'], '%d/%m/%Y')
        if 'end' in Rrange:
            self.endDate = time.strptime(Rrange['end'], '%d/%m/%Y')
    
    def getPattern(self):
        return self.pattern
    
    def getStartDate(self):
        return self.startDate
    
    def getEndDate(self):
        return self.endDate
    
    def isDateInRange(self, dateStr):
        date = time.strptime(dateStr, '%d/%m/%Y')
        if date >= self.startDate and date <= self.endDate:
            return True
        return False
    
    
    
    def match(self):
        if self.isPatternMatching():
            return True
        return False
    
    def dateRangePassed(self, dateStr):
        if dateStr is None or dateStr == '':
            dateStr = datetime.datetime.today().strftime('%d/%m/%Y')
        if self.endDate is not None:
            date = time.strptime(dateStr, '%d/%m/%Y')
            if date > self.endDate:
                return True
        return False
    
    def isPatternMatching(self, dateStr=None):
        if dateStr is None or dateStr == '':
            dateStr = datetime.datetime.today().strftime('%d/%m/%Y')
            
        if self.pattern == 'daily':
            return self.isDateInRange(dateStr)
        
        if self.isPatternDayRange() or self.isPatternDayList(): # mon-thu
            daysRange = self.getDayRangeInt()
            date = time.strptime(dateStr, '%d/%m/%Y')
            if date.tm_wday in daysRange and self.isDateInRange(date):
                return True
        
        return False
    
    def isPatternDayRange(self):
        if self.pattern is None:
            return False
        if self.pattern.find('-') > 0:
            return True
        return False
    
    def isPatternDayList(self):
        if self.pattern is None:
            return False
        if self.pattern.find(',') > 0:
            return True
        return False
            
    def getDayRangeInt(self):
        days = []
        if self.pattern.find('-') > 0:
            dayRange = self.pattern.split('-')
            if len(dayRange) == 2:
                start = dayRange[0]
                end = dayRange[1]
                startIndx = self.getDayIndex(start)
                endIndx = self.getDayIndex(end)
                if startIndx >= 0 and endIndx >= 0 and startIndx <= endIndx:
                    for n in range(startIndx, endIndx):
                        days.append(n)
        if self.pattern.find(',') > 0:
            dayList = self.pattern.split(',')
            for day in dayList:
                indx = self.getDayIndex(day)
                days.append(indx)
        return days
    
    def getDayIndex(self, day):
        if day in Schedule.DAYS:
            return Schedule.DAYS.index(day)
        return -1
    
            
        
    