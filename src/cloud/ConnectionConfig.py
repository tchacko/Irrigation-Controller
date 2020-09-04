'''
Created on 19-Jun-2017

@author: root
'''
import json

class ConnectionConfig(object):
    '''
    classdocs
    '''
    CONNECTION_CONFIG_FILE = "/data/system/connection.json"

    def __init__(self):
        '''
        Constructor
        '''
        data = self.loadJsonFromFile()
        self.sslEnabled = "false"
        if 'ssl-enabled' in data:
            self.sslEnabled = data['ssl-enabled']
        self.certFile = ""
        if 'cert-file' in data:
            self.certFile = data['cert-file']
        self.ciphers = ""
        if 'ciphers' in data:
            self.ciphers = data['ciphers']
            
    def isSSLEnabled(self):
        if self.sslEnabled == 'true':
            return True
        return False
    
    def getCertificateFile(self):
        return self.certFile
    
    def getCiphers(self):
        return self.ciphers
        
        
    def loadJsonFromFile(self):
        data = None
        with open(ConnectionConfig.CONNECTION_CONFIG_FILE) as dataFile:   
            try: 
                data = json.load(dataFile);
                dataFile.close()
            except  ValueError:
                dataFile.close()
        return data
        