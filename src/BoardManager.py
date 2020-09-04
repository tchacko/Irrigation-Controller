'''
Created on 08-Mar-2017

@author: root
'''
from BoardConfiguration import BoardConfiguration
from BoardStatus import BoardStatus
from DeviceStatus import DeviceStatus

class BoardManager(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.boardConfig = BoardConfiguration()
        if self.boardConfig is None:
            print 'board configuration is None'
            return
        self.boardStatus = {}
        self.deviceStatus = self.createDeviceStatus()
        
    def updateStatus(self, board):
        self.boardStatus.updateStatus()
        
        
    def createDeviceStatus(self):
        boards = self.boardConfig.getBoards()
        for num in boards: #currently one board
            board = boards[num]
            self.boardStatus[0] = BoardStatus(board)
        
        for num in boards:
            devices = board.getDevices()
            self.updateDeviceStatus(devices)
                    
    def updateDeviceStatus(self, devices):
        for indx in devices:
            status = DeviceStatus(devices[indx])
            if status is not None:
                self.deviceStatus[status.getDeviceId()] = status
    

                
        