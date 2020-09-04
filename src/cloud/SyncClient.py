'''
Created on 26-Jun-2017

@author: chacktho
'''
from cloud.HttpClient import HttpClient
from SystemStatus import SystemStatus

class SyncClient(HttpClient):
    '''
    class for making  sync request and updating system parameters and configuration
    '''


    def __init__(self, host, args={}):
        '''
        Constructor
        '''
        super(host, args)
        self.systemStatus = SystemStatus()
        self.syncRequest = None
        
    def sync(self, args):
        # Collect device info
        self.createSyncRequest()
        # Collect statistics
        self.collectDeviceStats()
        # send request
        # Check status and set the status
        # Check config change and modify device config
        
        
    def createSyncRequest(self):
        sysStatus = self.systemStatus
        self.syncRequest = {}
        self.syncRequest['orgId'] = sysStatus.orgId
        self.syncRequest['deviceId'] = sysStatus.deviceId
        self.syncRequest['authKey'] = sysStatus.authKey
        
    def collectDeviceStats(self):
        global controller
        statusMgr = controller.getStatusManager()
        if statusMgr is None:
            print 'Status Manager instance is invalid'
            return
        statusObj = statusMgr.getJsonStatus()
        self.syncRequest['status'] = statusObj
        
        

        
        
        