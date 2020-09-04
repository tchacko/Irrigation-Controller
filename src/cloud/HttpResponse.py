'''
Created on 26-Jun-2017

@author: chacktho
'''

class HttpResponse(object):
    '''
    classdocs
    '''


    def __init__(self, response):
        '''
        Constructor
        '''
        self._code = response.getcode()
        self._body = response.read()
        self._headers = response.info()
        
    @property
    def code(self):
        return self._code
    
    @property
    def body(self):
        return self._body
    
    @property
    def headers(self):
        return self._headers
    
    def getHeader(self, header):
        if header in self.headers:
            return self.headers[header]
        
        return ""
    
    
        