'''
Created on 26-Jun-2017

@author: chacktho
'''
from cloud.HttpClient import HttpClient
from SystemStatus import SystemStatus

class RegistrationClient(HttpClient):
    
    REGISGTRASTION_PATH = 'v1/Register'
    STATUS_REGISTERED = 'registered'
    systemStatus = SystemStatus()
    
    '''
    classdocs
    '''
    '''
    Registration data should contain the following information
    organization id, authentication key
    Device Name
    Device Type
    Device Version
    Software Release
    '''


    def __init__(self, host, args={}):
        '''
        Constructor
        '''            
        super(host, args)
        
        '''
        { response: {
            deviceName:"device1",
            deviceId:"123ABC4567890",
            status:"registered"
            }
        }
        '''
        
    def register(self, args):
        data = self.getRegistrationData()
        # headers, query params, path and method

        response = self.Request(args, data)
        if response.code != 200:
            print 'Registration Failed with HTTP Response Code: ' + str(response.code)
            return
        if response.getHeader(HttpClient.HEADER_CONTENT_TYPE) is not  HttpClient.CONTENT_TYPE_JSON:
            print 'Registration Response contains invalid content'
            return
        regResponse = response.body
        if self.getResponseStatus(regResponse) is RegistrationClient.STATUS_REGISTERED:
            self.setRegistrationStatus(self.getDeviceName(regResponse), self.getDeviceId(regResponse), RegistrationClient.STATUS_REGISTERED)
        print 'Device ' + self.getDeviceName(regResponse) + " Redistered successfully"
        
        
    def getRegistrationData(self):
        '''
        { Registration : {
            orgId:'1234567890',
            authKey:'qdqwrqr565677yjfjtyjuyo',
            device: [
             {
                name:"device1',
                type:'RPI_16',
                version:'PI_2',
                release:'1.0.1'
            }]
        }
        }
        '''
        regObj = {}
        sysStatus = RegistrationClient.systemStatus
        regObj['orgId'] = sysStatus.orgId
        regObj['authKey'] = sysStatus.authKey
        deviceObj = {}
        deviceObj['name'] = sysStatus.deviceName
        deviceObj['type'] = sysStatus.deviceType
        deviceObj['version'] = sysStatus.deviceVersion
        deviceObj['release'] = sysStatus.softwareRelease
        
        regObj['device'] = deviceObj
        
        return regObj
    
    def getResponseStatus(self, response):
        return self.getProperty('status', response)
            
    def getDeviceId(self, response):
        return self.getProperty('deviceid', response)
    
    def getProperty(self, key, response):
        body = response.body
        value = ''
        if key in body:
            value = body[key]
            
        return value
    
    def getDeviceName(self, response):
        return self.getProperty('name', response)
    
    def setRegistrationStatus(self, deviceName, deviceId, status):
        RegistrationClient.systemStatus.setRegistrationStatus(deviceName, deviceId, status)
        
    
        
            
    
    