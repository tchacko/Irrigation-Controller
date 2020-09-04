'''
Created on 13-Mar-2017

@author: chacktho
'''
from FileMonitor import Task
import Utils

class SensorManager(object):
    '''
    classdocs
    '''
    DEFAULT_CONTROLLER_STATUS = 'running'

    def __init__(self, controller, eventProcessor):
        '''
        Constructor
        '''
        self.configMgr = controller.getConfigManager()
        self.boardMgr = controller.getBoardManager()
        self.statusMgr = controller.getStatusManager()
        self.eventProcessor = eventProcessor
        self.controller = controller
        
    def checkSensors(self):
        if self.configMgr is None:
            print 'SensorManager.init() Configuration Manage is not initialized'
            return
        
        sensorMap = {}
        rpiBoards = self.boardMgr.getBoards()
        for bId in rpiBoards:
            rpiDevices = self.boardMgr.getDevices(bId)
            self.createSensorMap(rpiDevices, sensorMap)
        
        if len(sensorMap) != 0:
            self.checkAndFire(sensorMap, bId)
            
    def createSensorMap(self, rpiDevices, sensorMap):
        for dId in rpiDevices:
            rpiDevice = rpiDevices[dId]
            channels = rpiDevice.getChannels()
            self.addChannelsToMap(channels, rpiDevice, sensorMap)

    def addChannelsToMap(self, channels, rpiDevice, sensorMap):
        if sensorMap is None or channels is None:
            return
        
        for cId in channels:
            deviceList = None
            channel = channels[cId]
            if cId in sensorMap:
                deviceList = sensorMap[cId]
            else:
                deviceList = []
            deviceList.append(rpiDevice)
            sensorMap[channel] = deviceList
            
        
    def checkAndFire(self, sensorMap, bId):
        for channel in sensorMap:
            rpiDevices = sensorMap[channel]
            self.fireEvents(channel, rpiDevices, bId)
            
            
    def fireEvents(self, channel, rpiDevices, boardId):
        rpiBoard = self.boardMgr.getBoard(boardId)
        if rpiBoard is None or rpiBoard.isEnabled() == False:
            return
    
        for rpiDevice in rpiDevices:
            if rpiDevice.isEnabled() == False:
                continue
            
            ctrChannel = rpiDevice.getControlChannel()
            if channel.getNumber() == ctrChannel.getNumber():
                continue
            
            # Read the action from the sensor associated with the device
            # and fire event accordingly
            
            rpiChannel = rpiDevice.getChannel(channel.getNumber())
            if rpiChannel is None or rpiChannel.isEnabled() == False:
                continue
            
            value = channel.getChannelStatus()
    
            #Add logic to parse action. This will tell whether to fire event or not
            #delegate this work the associated channel
            needTrigger = self.needActionTrigger(value, rpiChannel, rpiDevice.getId(), boardId)
            if needTrigger:
                trigger = self.getDeviceActionMatchingTrigger(value, rpiChannel.getNumber(), rpiDevice)
                if self.deviceActionCriteriaMet(trigger, value):
                    value = self.getTargetTriggerValue(trigger)
                    event = ChannelTriggerEvent(value, rpiDevice.getId(), boardId, self.controller)
                    self.eventProcessor.enqueue(event)
                
                
    def needActionTrigger(self, value, rpiChannel, deviceId, boardId):
        needTrigger = False
        action = rpiChannel.getAction()
        triggers = action['trigger']
        for trigger in triggers:
            triggerValue = trigger['trigger-value']
            if triggerValue != Utils.translateTriggerValue(str(value)):
                continue
            if not self.isTargetControlChannel(trigger):
                continue
            
            if self.triggerConditionMet(trigger, deviceId, boardId):
                return True
            
            # get Device Status
        
        return needTrigger
    
    def isTargetControlChannel(self, trigger):
        target = trigger['target']
        if target == 'control-channel':
            return True
        
        return False
    
    def triggerConditionMet(self, trigger, deviceId, boardId):
        condition = trigger['condition']
        if condition is None:
            return True
        
        if 'controller-status' not in condition and 'controller-elapsed' not in condition:
            return True
        
        deviceStatus = self.statusMgr.getDeviceStatus(boardId, deviceId)  
        if deviceStatus is None:
            return False
        status = deviceStatus.getStatus()
        elapsedTime = deviceStatus.getElapsedTime()
        
        if 'controller-status' in condition and 'controller-elapsed' not in condition :
            if condition['controller-status'] == status:
                return True
            else:
                return False
            
        if 'controller-elapsed' in condition and 'controller-status' not in condition:
            if self.elapsedTimeExceeded(elapsedTime, condition['elapsed-time']) and status == SensorManager.DEFAULT_CONTROLLER_STATUS:
                return True
            else:
                return False
        
        if condition['controller-status'] == status and self.elapsedTimeExceeded(elapsedTime, Utils.convertTime2Sec(condition['controller-elapsed'])):
            return True
        
        return False

    def elapsedTimeExceeded(self, elapsedTime, condition_time):
        if elapsedTime > condition_time:
            return True
        
        return False

    def deviceActionCriteriaMet(self, trigger, value):
        if trigger is None:
            return False
        triggerValue = trigger['trigger-value']
        if triggerValue == Utils.translateTriggerValue(value):
            return True
                        
        return False   
    
    def getDeviceActionMatchingTrigger(self, value, channelNum, rpiDevice):  
        dAction = rpiDevice.getDeviceAction()
        triggers = self.getTriggers(dAction)
        if triggers is None:
            return None
        
        for trigger in triggers:
            if 'sensor' not in trigger:
                continue
            
            sensorStr = trigger['sensor']
            sensorIds = sensorStr.split(',')
            for sensorId in sensorIds:
                if sensorId == str(channelNum):
                    return trigger
        return None       

    def getTargetTriggerValue(self, trigger):
        ret = 'high'
        if trigger is None:
            return ret
        if 'target-value' in trigger:
            ret = trigger['target-value'] 
        
        return ret
        
    def getTriggers(self, dAction):
        triggers = None
        if dAction is None:
            return triggers
        if 'sensor' not in dAction:
            return triggers
        sensors = dAction['sensor']
        if 'trigger' not in sensors:
            return triggers
        triggers = sensors['trigger']
        
        return triggers
    
            
        
                
class ChannelTriggerEvent(Task):
    
    def __init__(self, action, deviceId, boardId, controller ):
        self.action = action
        self.deviceId = deviceId
        self.boardId = boardId
        self.controller = controller
        
    def execute(self):
        boardMgr = self.controller.getBoardManager()
        device = boardMgr.getDevice(self.boardId, self.deviceId)
        if device is None:
            return
        
        ctrChannel = device.getControlChannel()
        if ctrChannel is None:
            return

        if ctrChannel.isEnabled():
            ctrChannel.triggerAction(self.action)
        
            
            
            
        