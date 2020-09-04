'''
Created on 10-Mar-2017

@author: chacktho
'''

class BoardConfig(object):
    '''
    classdocs
    '''


    def __init__(self, boardData):
        '''
        Constructor
        '''
        self.config = boardData
        if self.config is None:
            return
        
        self.id = self.config['id']
        self.mode = self.config['mode']
        self.enabled = self.config['enabled']
        
    def getId(self):
        return self.id;
    
    def getMode(self):
        return self.mode
    
    def getEnabled(self):
        return self.enabled
    
    def compare(self, newConfig):
        
        if newConfig is None:
            return False
        if newConfig.getId() != self.getId() or newConfig.getMode() != self.getMode() or newConfig.getEnabled() != self.getEnabled():
            return True
        
        return False
    
        
    
        