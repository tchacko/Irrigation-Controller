'''
Created on 10-Mar-2017

@author: chacktho
'''
from RpiBoard import RpiBoard

class RpiBoardManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.rpiBoards = {}
        
        
    def addBoards(self, boards, controller):
        for bId in boards:
            board = boards[bId]
            rpiBoard = RpiBoard(board, controller)
            self.rpiBoards[bId] = rpiBoard
    
    def getBoard(self, boardId):
        if boardId in self.rpiBoards:
            return self.rpiBoards[boardId]
        return None
    
    def getBoards(self):
        return self.rpiBoards
    
    
    def getDevices(self, boardId):
        devices = None
        if boardId in self.rpiBoards:
            rpiBoard = self.rpiBoards[boardId]
            devices = rpiBoard.getDevices()
        return devices
    
    def getDevice(self, boardId, deviceId):
        board = self.getBoard(boardId)
        if board is None:
            return None
        
        device = board.getDevice(deviceId)
        return device
    '''
    Boards and Devices are pre-configured. Only channels can be associated or disassociated
    '''
    def reloadChannels(self, config):
        boards = config.getBoards()
        for b in boards:
            rpiBoard = self.getBoard(b)
            if rpiBoard is None:
                print 'New board configuration found. Board configuration can not be changed, skipping board=' + b
                continue
            rpiBoard.reloadChannels(boards[b])
            
    
        