'''
Created on Mar 4, 2017

@author: chacktho
'''
import json
from RpiControllerConfig import RpiControllerConfig 
from RpiBoardConfig import RpiBoardConfig 


class BoardConfiguration(object):
    '''
    classdocs
    '''
    BOARD_CONFIG_FILE = 'data/board/config.json'

    def __init__(self, rpiBoard, config=None):
        '''
        Constructor
        '''
        self.controllerCfg = None
        self.boardConfig = None
        self.boards = {}
        
        data = config
        if data is None:
            data = self.loadJsonFromFile() 
            
        if data is None:
            return
        
        self.controllerCfg = RpiControllerConfig(data['controller'])
        if self.controllerCfg is None:
            return
        
        self.addBoards(data['controller'], self.controllerCfg)
        print self.toString()
           
    def loadJsonFromFile(self):
        data = None
        with open(BoardConfiguration.BOARD_CONFIG_FILE) as dataFile:   
            try: 
                data = json.load(dataFile);
                dataFile.close()
            except  ValueError:
                dataFile.close()
        return data
    
    def addBoards(self, controller, controllerCfg):
        if controller is None:
            return
        data = controller['board']
        if data is None:
            return
        for boardData in data:
            board = RpiBoardConfig(boardData, controllerCfg)
            if board.getId() in self.boards:
                print 'Duplicate board ' + board.getId() +' found'
                continue
            self.boards[board.getId()] = board
    
    def toString(self):
        outStr = self.controllerCfg.toString() +'\n'
        for b in self.boards:
            board = self.boards[b]
            outStr = outStr + board.toString();
        return outStr
    
    def getBoards(self):
        return self.boards
    
    def save(self):
        print 'Not Implemented'
        
    def compareControllerConfig(self, config):
        if config is None:
            return False
        
        if self.controllerCfg.compare(config) is True:
            return True
        
        return False
    
    def compareBoardsConfig(self, config):
        if config is None:
            return False
    
        newBoards = config.getBoards()
        
        newIds = newBoards.keys()
        myIds = self.boards.keys()
        
        if len(newIds) != len(myIds):
            return True
        
        if self.boardsDeleted(newBoards) == True:
            return True
        
        for bId in newBoards:
            board = newBoards[bId]
            if self.isNewBoard(board) is True:
                return True
            if self.compareBoard(board) is True:
                return True
                
        return False
            
    
    def isNewBoard(self, board):
        bId = board.getId();
        Ids = self.boards.keys()
        if bId in Ids:
            return False
        
        return True
    
    def compareBoard(self, newBoard):
        bId = newBoard.getId()
        myBoard = self.boards[bId]
        if myBoard.compare(newBoard) == True:
            return True
        
        return False
    
    def boardsDeleted(self, newBoards):
        Ids = newBoards.keys()
        for myId in self.boards:
            if myId in Ids:
                continue
            else:
                return True
        return False

    def getControllerConfig(self):
        return self.controllerCfg
        

#cfg = BoardConfiguration("board1");


