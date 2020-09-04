'''
Created on 08-Mar-2017

@author: root
'''
import json
import threading
import time
from SystemStatus import SystemStatus 
from ConfigManager import ConfigManager 
from StatusManager import StatusManager
from SensorManager import SensorManager
from RpiBoardManager import RpiBoardManager
from EventProcessor import EventProcessor
from FileMonitor import FileMonitor 
from Constants import Constants
import Utils
from ScheduleManager import ScheduleManager
from time import sleep

'''
Class to control the boards
This class instance is singleton which will keep an up to date copy of the configuration through ConfogManager
and a copy of board status through Status Manager
ControllerService will be running continuously. Every INTERVAL
'''


class Controller(object):
    '''
    classdocs
    '''

    CONTROLLER_STATS_FILE = 'data/controller/status.json'
    
    controller = None

    def __init__(self):
        '''
        Constructor
        '''
        Controller.controller = self
        self.sysStatus = SystemStatus()
        self.configMgr = ConfigManager()
        self.statusMgr = StatusManager()
        self.boardManager = RpiBoardManager()
        self.eventProcessor = EventProcessor()
        self.sensorMgr = SensorManager(self, self.eventProcessor)
        self.scheduleManager = ScheduleManager(self, self.eventProcessor)
        self.fileMon = FileMonitor(Constants.SYSTEM_CONFIG_FILE, self, self.eventProcessor) 
        self.initializeStatus()
        self.initializeScheduler()
        self.controllerService = ControllerService(self)
        
    def startService(self):
        self.controllerService.start()
        self.fileMon.start()
        if self.isRegistered():
            self.checkPowerOnResume()
        
    def checkPowerOnResume(self):
        while self.controllerService.status != Constants.SERVICE_STATUS_RUNNING:
            sleep(1)
        print ' Controller Service READY'
        
        rpiBoards = self.boardManager.getBoards()
        for boardId in rpiBoards:
            rpiBoard = rpiBoards[boardId]
            rpiDevices = rpiBoard.getDevices()
            for deviceId in rpiDevices:
                self.powerOnResumeDeviceState(rpiDevices[deviceId])
    
    '''
    If manual trigger is enabled and resume-on-power-on is set, then 
    resume the on state
    '''
                
    def powerOnResumeDeviceState(self, rpiDevice):
        if self.isResumeOnPowerOnEnabled(rpiDevice) is False:
            return 
        
        rpiChannel = rpiDevice.getControlChannel()
        if rpiChannel is None:
            return
        
        rpiChannel.resumeState()
        
    def isResumeOnPowerOnEnabled(self, rpiDevice):
        deviceAction = rpiDevice.getDeviceAction()
        if 'manual-trigger' in deviceAction:
            manualTrigger = deviceAction['manual-trigger']
            if manualTrigger != 'enabled':
                return False
            if 'resume-on-power-on' in deviceAction:
                resume = deviceAction['resume-on-power-on']
                if resume != 'true':
                    return False
            else:
                return False
        else:
            return False
        
        return True
            
    def getController(self):
        return self.controller
        
  
    def getConfigManager(self):
        return self.configMgr
    
    def getBoardManager(self):
        return self.boardManager
    
    def getStatusManager(self):
        return self.statusMgr
    
    def isRegistered(self):
        sysStat = self.getSystemStatus();
        return sysStat.isRegistered()
        
    def getSystemStatus(self):
        return self.sysStatus
        
    def initializeStatus(self):
        boards = self.configMgr.getBoards();
        self.boardManager.addBoards(boards, self) # Adds RpiBoard
        for b in boards:
            board = boards[b]
            self.statusMgr.createBoardStatus(board)
        
        bs = self.statusMgr.getBoards();  
        for b in bs:
            board = bs[b]
            devices = self.configMgr.getDevices(b)
            self.statusMgr.createDevicesStatus(board.getId(), devices)
            
            
    def initializeScheduler(self):
        boards = self.configMgr.getBoards();
        for b in boards:
            devices = self.configMgr.getDevices(b)
            self.scheduleManager.addDeviceSchedules(devices)
        
    def syncService(self):
        #print 'sync started at ' + Utils.getFormatedTime()
        if self.isRegistered():
            self.checkSensors()
            self.checkSchedules()
            return
            
        else:
            #print 'sync service at ' + Utils.getFormatedTime() + ' system  Not registered'
            return

    def checkSensors(self):
        self.sensorMgr.checkSensors()
        
    def checkSchedules(self):
        self.scheduleManager.checkSchedules()
        
    
    def configModified(self, config):
        if self.configMgr.isConfigurationChanged(config):
            print 'configuration changed'
            self.reloadChannels(config)
            self.activate(config)
        else:   
            print 'configuration not changed'
        
            
    def reloadChannels(self, config):
        self.boardManager.reloadChannels(config)
            
    '''  Supporting methods '''
    
    def getControllerStatus(self):
        data = None
        with open(Controller.CONTROLLER_STATS_FILE) as dataFile:   
            try: 
                data = json.load(dataFile);
                dataFile.close()
            except  ValueError:
                dataFile.close()
        return data
        
        
    def activate(self, configuration):
        if configuration is None:
            return
        
        boards = configuration.getBoards()
        
        if boards is None or len(boards) == 0:
            return
        
        for boardId in boards:
            enabled = True
            board = boards[boardId]
            if board.isEnabled() == False:
                enabled = False
            self.activateBoard(board, enabled)
            
            
    def activateBoard(self, board, enabled):
        #if board.isEnabled() == False:
        #    return
        rbiBoard = self.boardManager.getBoard(board.getId())
        rbiBoard.activate(board, enabled)
        

        
    def saveControllerStatus(self):
        if self.controllerStatus is None:
            return
        
        with open(Controller.CONTROLLER_STATS_FILE) as dataFile:
            try:
                json.dump(self.controllerStatus, dataFile )
                dataFile.close()
            except:
                dataFile.close()
            
    @staticmethod    
    def getController():
        if Controller.controller is None:
            Controller.controller = Controller()
        
        return Controller.controller


class ControllerService(threading.Thread):
    
    def __init__(self, controller):
        self.controller = controller
        self.status = Constants.SERVICE_STATUS_STARTING
        threading.Thread.__init__(self,None, None, 'ControllerService-Thread')       
           
    def run(self):
        print 'starting sync service thread '+ self.name + ' at ' + Utils.getFormatedTime()
        self.status = Constants.SERVICE_STATUS_RUNNING
        while True:
            self.controller.syncService()
            time.sleep(self.controller.getSystemStatus().getServiceSleepInterval())

                    