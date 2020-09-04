'''
Created on Mar 4, 2017

@author: chacktho
'''
'''''''''''''''''''''''''''''''''''''''''''''''
Globals
'''
from RPi import GPIO 

class Constants:
    SYSTEM_CONFIG_FILE ='data/board/config.json' 
    CHANNELS = {'GPIO2':3, 'GPIO3':5, 'GPIO4':7, 'GPIO14':8,'GPIO15':10,'GPIO17':11,'GPIO18':12,'GPIO27':13,'GPIO22':15, 'GPIO23':16,'GPIO24':18,
                'GPIO10':19, 'GPIO9':21, 'GPIO25':22, 'GPIO11':23, 'GPIO8':24, 'GPIO7':26, 'GPIO5':29, 'GPIO6':31, 'GPIO12':32, 'GPIO13':33, 
                'GPIO19':35, 'GPIO16':36, 'GPIO26':37, 'GPIO20':38, 'GPIO21':40,}
    IO_CHANNEL =     {'GPIO2':2, 'GPIO3':5, 'GPIO4':7, 'GPIO14':8,'GPIO15':10,'GPIO17':11,'GPIO18':12,'GPIO27':13,}
    LEVEL_CHANNELS = {'GPIO22':15, 'GPIO23':16,'GPIO24':18, 'GPIO10':19, 'GPIO9':21, 'GPIO25':22, 'GPIO11':23, 'GPIO8':24,}
    FLOW_CHANNELS =  {'GPIO7':26, 'GPIO5':29, 'GPIO6':31, 'GPIO12':32, 'GPIO13':33, 'GPIO19':35, 'GPIO16':36, 'GPIO26':37, 'GPIO20':38, 'GPIO21':40,}
    CHANNEL_TYPE = [GPIO.IN, GPIO.OUT]
    IN = 0
    OUT = 1
    UNKOWN_TYPE = -1
    UNKNOWN = -1
    DEFAULT_OUT_VALUE = 0;
    UNKNOWN_CHANNEL = -1
    CHANNEL_ON = GPIO.LOW
    CHANNEL_OFF = GPIO.HIGH
    ACTION_DELIM = '='
    STATUS_BASE_FOLDER = 'data/status/board'
    BOARD_PREFIX = 'board-'
    DEVICE_PREFIX = 'device-'
    SERVICE_STATUS_UNKNOWN = -1
    SERVICE_STATUS_STARTING = 0
    SERVICE_STATUS_RUNNING = 1
    SERVICE_STATUS_STOPPED = 2
    