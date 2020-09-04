'''
Created on 09-Mar-2017

@author: root
'''
from BoardStatus import BoardStatus 
from DeviceStatus import DeviceStatus

class StatusManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        print 'StatusManager started'
        self.boardStatus = {}
        self.deviceStatus = {}
        
    def createBoardStatus(self, board):
        bs = BoardStatus(board)
        boardId = bs.getBoard().getId()
        self.boardStatus[boardId] = bs
        
        self.createDevicesStatus(boardId, board.getDevices())
        
    def getBoards(self):
        return self.boardStatus;
    
    def createDevicesStatus(self, boardId, devices):
        if devices is None:
            return
        for dId in devices:
            try:
                device = devices[dId]
                if device is None:
                    continue
                self.createDeviceStatus(boardId, device)
            except:
                continue
    
            
    
    def createDeviceStatus(self, boardId, device):
        try:
            bs = self.boardStatus[boardId]
            ds = DeviceStatus(device, bs)
            dId = ds.getId()
            self.deviceStatus[dId] = ds
            
        except:
            print 'Failed to create device status boardId=' + boardId + ' device=' + device
            
    def getBoardStatus(self, boardId):
        try:
            bs = self.boardStatus[boardId]
            return bs
        except:
            print 'Failed to find the board status for boardId=' + boardId
            
        return None
    
    def getSingleBoardStatus(self):
        if len(self.boardStatus) == 1:
            return self.boardStatus.values()[0] 
        return None
    
    '''
    Get the device status from the single board
    '''
    def getDeviceSatusFromSingleBoard(self, deviceId):
        board = self.getSingleBoardStatus()
        if board is None:
            return None
        return self.getDeviceStatus(board.getId(), deviceId)
        
    
    def getDeviceStatus(self, boardId, deviceId):
        try:
            for dsId in self.deviceStatus:
                status = self.deviceStatus[dsId]
                if status.getBoardId() == boardId:
                    if dsId == deviceId:
                        return status.getDeviceStatus()
        except:
            print 'failed to get device status for boardId=' + boardId + ' deviceId=' + deviceId
            
        return None
    
    def updateDeviceStatus(self, boardId, deviceId, status):
        for dId in self.deviceStatus:
            device = self.deviceStatus[dId]
            if device.getBoardId() == boardId and device.getId() == deviceId:
                device.updateStatus(status)
                print 'Status update for device = ' + deviceId + ', board=' + boardId + ', STATUS = ' + status
                
    def getJsonStatus(self):
        boards = []
        for boardId in self.boardStatus:
            boardStatus = self.boardStatus[boardId]
            boardObj = boardStatus.buildJSONObject()
            boards.append(boardObj)
            devicesStatus = []

            for deviceId in self.deviceStatus:
                deviceStatus = self.deviceStatus[deviceId]
                statusObj = deviceStatus.getDeviceStatusObject()
                devicesStatus.append(statusObj)
            devicesObj = {}
            devicesObj['device'] = devicesStatus
        boardsObj = {}
        boardsObj['board'] = boards
        return boardsObj

            
            
            
            

            
        
        
            
    
    
                
        