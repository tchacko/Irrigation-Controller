'''
Created on 09-Mar-2017

@author: root
'''
import json
import Utils
from BoardConfiguration import BoardConfiguration

class ConfigManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.boardConfig =  BoardConfiguration('rpiBoard')
        print 'Config manager started'
        
    def createConfig(self, config):
        print 'Not Implemented'
        
    def getConfiguration(self):
        return self.boardConfig
    
    def getBoards(self):
        if self.boardConfig is None:
            return None
        return self.boardConfig.getBoards()
    
    def getBoard(self, boardId):
        if self.boardConfig is None:
            return None
        boards = self.boardConfig.getBoards()
        try:
            board = boards[boardId]
            return board
        except:
            print 'Caught exception in ConfigManager.getBoard for board ' + boardId
        return None
    
    def getDevice(self, boardId, deviceId):
        
        devices = self.getDevices(boardId)
        if devices is None:
            return None
        try:
            device = devices[deviceId]
            return device
        except:
            print 'Caught exception in ConfigManager.getDevices. boardId = ' + boardId + ' deviceid=' + deviceId
        return None
    
    
    def getDevices(self, boardId):
        if self.boardConfig is None:
            return None
        
        boards = self.getBoards()
        if boards is None:
            return None
        try:
            board = boards[boardId];
            if board is None:
                return None
            return board.getDevices()
        except:
            print 'Caught exception in ConfdigManage.getDecices for the board ' + boardId
        return None
    
    def getChannels(self, boardId, deviceId):
        board = self.getBoard(boardId)
        if board is None:
            return None
        
        device = self.getDevice(boardId, deviceId)
        if device is None:
            return None
        
        try:
            channels = device.getChannels()
            return channels
        except:
            print 'Caught exception in ConfdigManage.getChannels for the board ' + boardId + ' deviceId=' + deviceId
        return None
    
    def getControlChannel(self, boardId, deviceId):
        channels = self.getChannels(boardId, deviceId)
        if channels is None:
            return None
        for cId in channels:
            channel = channels[cId]
            if channel.gettype() == 'io':
                return channel
        return None
    
    def getNewConfiguration(self):
        return BoardConfiguration()
    
    
    def saveConfig(self):    
        self.boardConfig.save()
        
    def saveNewConfig(self, config):
        #validate with a schema
        jsonObj = Utils.string2Json(config)
        if self.isConfigurationChanged(jsonObj):
            self.saveConfiguration(jsonObj)
        else:
            print 'Configuration not changed'
        #validate
        
    def isConfigurationChanged(self, newConfig):
        changed = False
        if self.boardConfig.compareControllerConfig(newConfig) == True:
            changed = True
        elif self.boardConfig.compareBoardsConfig(newConfig) == True:
            changed = True
        #save new configuration
        if changed:
            self.boardConfig = BoardConfiguration('rpiBoard')
                
        return changed
    
    def saveConfiguration(self, newConfigObj):
        with open(BoardConfiguration.BOARD_CONFIG_FILE) as dataFile:   
            try: 
                json.dump(newConfigObj, dataFile);
                dataFile.close()
            except  ValueError:
                dataFile.close()

            