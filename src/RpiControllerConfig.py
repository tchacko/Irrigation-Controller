'''
Created on Mar 5, 2017

@author: chacktho
'''

class RpiControllerConfig:
    '''
    classdocs
    '''


    def __init__(self, controller):
        '''
        Constructor
        '''
        self.id = None
        self.custId = None
        self.authKey = None
        self.regId = None
        
        
        if controller is None:
            return
        self.id = controller['id']
        self.custId = controller['custid']
        self.authKey = controller['authkey']
        self.regId = controller['regid']
        
    def getId(self):
        return self.id
    
    def getCustId(self):
        return self.custId
    
    def getAuthKey(self):
        return self.authKey
    
    def getRegId(self):
        return self.regId
    
    def compare(self, newConfig):
        if newConfig is None:
            return False
        newControllerCfg = newConfig.getControllerConfig()
        
        if newControllerCfg.getId() != self.getId() or \
           newControllerCfg.getCustId() != self.getCustId() or \
           newControllerCfg.getAuthKey() != self.getAuthKey() or \
           newControllerCfg.getRegId() != self.getRegId():
            return True
        
        return False
    
        
    def toString(self):
        outStr = 'RpiControllerConfig => id='+self.getId()+', custd='+self.getCustId()+', authkey='+self.getAuthKey()+', regid='+self.getRegId()
        return outStr
        