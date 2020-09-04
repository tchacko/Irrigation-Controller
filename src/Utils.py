'''
Created on 08-Mar-2017

@author: root
'''
import os
import copy
import time
import datetime
import json

DEFAULT_TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
           
def dirExists(path):
    if os.path.exists(path):
        return True
    else:
        return False
     
def makeDir(path):     
    try :
        os.makedirs(path)
    except OSError:
        if os.path.exists(path):
            print 'Path '+ path + ' already exists'
        else:
            raise        

def deepCopy(data):
    if data is None:
        return None
    
    copied = copy.deepcopy(data)
    return copied

def getTimeMs():
    return time.time()

def getFormatedTime(fmt=DEFAULT_TIME_FORMAT):
    t = getTimeMs()
    if fmt is None or len(fmt) == 0: 
        fmt = DEFAULT_TIME_FORMAT
    return datetime.datetime.fromtimestamp(t).strftime(fmt)

def string2Json(dataStr):
    if dataStr is None:
        return
    data = None
    try: 
        data = json.loads(dataStr);
    except  ValueError:
        print 'JSON parse error from Utils.string2Json'

    return data

def translateTriggerValue(value):
    ret = 'low'
    if value == '1':
        ret = 'high'
    return ret

def translateAction(action):
    if action == 'low' or action == 'high':
        return getActionValue(action)
    
    if 'trigger-value' in action:
        return getActionValue(action['trigger-value'])
    else:
        return 1
    
    
def getActionValue(action):
    ret = 1
    if action == 'start' or action == 'low':
        ret = 0
    return ret
        
def translateStatus(status):
    if status == 1:
        return 'stopped'
    if status == 0:
        return 'running'
    return 'unknown'

def convertTime2Sec(duration):
    inStr = str(duration)
    
    if inStr.endswith('s'):
        return int(inStr[:-1])
    if inStr.endswith('m'):
        return int(inStr[:-1]) * 60
    if inStr.endswith('h'):
        return int(inStr[:-1]) * 60 * 60
    
    return int(duration)
    
    