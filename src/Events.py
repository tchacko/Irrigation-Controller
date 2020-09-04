'''
Created on 08-Mar-2017

@author: root
'''
from BoardConfiguration import BoardConfiguration
from SystemStatus import SystemStatus
from Controller import Controller

class Task:
    
    def  __init__(self):
        print 'Not implemented'
        
    def execute(self):
        print 'Not implemented'
        
class FileChangeEvent(Task):
    
    FILE_MODIFIED = 1
    FILE_DELETED = 2
    FILE_CREATED = 3
    
    
    def __init__(self, path, change):
        self.filePath = path
        self.change = change
        
    def execute(self):
        if self.change == FileChangeEvent.FILE_MODIFIED:
            if self.isModified(BoardConfiguration.BOARD_CONFIG_FILE):
                #File Modified
                self.processConfigFileModified()
    
    def isModified(self, mofiedFile):
        if BoardConfiguration.BOARD_CONFIG_FILE == mofiedFile:
            return True
        
        return False
    
    def processConfigFileModified(self):
        boardStatus = SystemStatus()
        if boardStatus.getStatus() != SystemStatus.STATUS_REGISTERED:
            print 'Device ', boardStatus.getUid(), ' not Registered.'
            return
        
        boardConfig = BoardConfiguration('RpiBoard');
        controller = Controller.getController()
        controller.configModified(boardConfig)
       
            
                
                
            
    
        