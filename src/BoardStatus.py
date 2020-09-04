'''
Created on 08-Mar-2017

@author: root
'''
import os
from Constants import Constants 
import json
import Utils


class BoardStatus(object):
    '''
    classdocs
    '''
    BOARD_PREFIX = 'board-'
    STATUS_FILE = BOARD_PREFIX + 'status.json'
    
    def __init__(self, board):
        '''
        Constructor
        '''
        self.board = Utils.deepCopy(board)
        self.create()
        
    def create(self):
        if self.board is None:
            print 'Board is None'
            return
        statusBase = Constants.STATUS_BASE_FOLDER
        self.makeDir(statusBase)
        
        boardId = self.board.getId()
        boardPath = Constants.STATUS_BASE_FOLDER+'/'+ BoardStatus.BOARD_PREFIX+boardId
        if self.dirExists(boardPath) == False:
            self.makeDir(boardPath)
        
        self.updateStatus()
        
    def enableBoard(self, s):
        status = 'false'
        if s is True:
            status = 'true'

        self.board['enabled'] = status
        
    def updateStatus(self):
        jsonObj = self.buildJSONObject()
        statusFilePath = Constants.STATUS_BASE_FOLDER+'/'+ BoardStatus.BOARD_PREFIX +self.board.getId()+'/'+BoardStatus.STATUS_FILE
        with open(statusFilePath, 'w') as fh: 
            try:
                json.dump(jsonObj,fh)
                fh.close()
            except:
                fh.close();
                raise ValueError('Failed to write the configuration '+statusFilePath)
            
    def getBoard(self):
        self.updateStatus()
        return self.board;
        
    def buildJSONObject(self):
        data = {}
        data['id'] = self.board.getId()
        data['enabled'] = self.board.getEnabled()
        return data
        
            
    def dirExists(self, path):
        if os.path.exists(path):
            return True
        else:
            return False
         
    def makeDir(self, path):     
        try :
            os.makedirs(path)
        except OSError:
            if os.path.exists(path):
                print 'Path '+ path + ' already exists'
            else:
                raise        
    def getId(self):
        return self.board.getId()
    