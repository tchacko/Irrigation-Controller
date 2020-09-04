'''
Created on 19-Jun-2017

@author: chacktho
'''
import urllib2 as urllib
from urllib2 import HTTPError
from urllib import urlencode
import json

from HttpResponse import HttpResponse

class HttpClient(object):
    '''
    classdocs
    '''
    CONTENT_TYPE_JSON = 'application/json'
    HEADER_CONTENT_TYPE = 'Content-Type'

    def __init__(self, host, headers=None, path=None):
        '''
        Constructor
        '''
        self.host = host
        self.headers = headers or {}
        self.path  = path
        
    def getContentTypeHeaderValue(self):
        if 'Content-Type' in self.headers:
            return self.headers['Content-Type']
        return ''
    
    def updateHeaders(self, headers):
        if headers is not None:
            self.headers.update(headers)
            
    def Request(self, args, data=None):
        if 'headers' in args:
            self.updateHeaders(args['headers'])
            
        if data is not None:
            if self.getContentTypeHeaderValue() == HttpClient.CONTENT_TYPE_JSON:
                self.data = json.dumps(data).encode('UTF-8')   
            else:
                self.data = data.encode('UTF-8')
        else:
            self.data = None
            
        if 'params' in args:
            self.queryParams = args['params']
        else:
            self.queryParams = {}
        
        if 'path' in args:
            self.path = args['path']
            
        if 'method' in args:
            self.method = args['method'].upper()
        else:
            self.method = 'GET'
        
        return HttpResponse(self.makeRequest())
        
    def makeRequest(self):
        request = urllib.Request(self.buildURL(), data=self.data)
        if self.headers is not None:
            for key, value in self.headers.items():
                request.add_header(key, value)
        if not ( self.headers is not None and 'Content-Type' in self.headers):
            request.add_header('Content-Type', HttpClient.CONTENT_TYPE_JSON)
        
        request.get_method = lambda: self.method
        try:
            opener = urllib.build_opener()
            return opener.open(request)
        except HTTPError as error:
            print ' HttpClient::makeRequest Failed with HTPError --> Code: ' + error.code + ' Reason: ' + error.reason
            raise error
            
    def buildURL(self):
        url = ''
        if self.path is not None:
            url = '/{0}'.format(self.path)
            
        values = None
        if self.queryParams is not None:
            values = urlencode(sorted(self.queryParams.items()), True)
            
        url = '{0}?{1}'.format(url, values)
        
        return self.host + url
    
    
    
host = 'https://www.google.com'
    
client = HttpClient(host)
response = client.Request({})
print("Code = "+str(response.code) + "\n headers: " + str(response.headers) + "\n Body: " + response.body)
print ("\nContent-Type = " + response.getHeader('Content-Type'))

        
        
        