'''
Created on 11-Mar-2017

@author: chacktho

Mocking the RPi.GPIO package to test the code on non-RPi hardware
'''
import random as Random
class GPIO(object):
    '''
    classdocs
    '''
    IN = 100
    OUT = 200
    LOW = 0
    HIGH = 1
    BCM = 1000
    BOARD = 1001
    
    mode = None

    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def setup(number, ctype):
        print 'GPIO.setup('+str(number)+', '+str(ctype)+') executed'
    
    @staticmethod
    def output(number, io):
        print 'GPIO.out('+str(number)+', '+str(io)+') executed'
        
    @staticmethod   
    def input(number):
        val = Random.randint(0,1)
        print 'GPIO.input('+str(number)+') executed. Returned ' + str(val)
        return val
    
    @staticmethod
    def setmode(mode):
        print 'GPIO.setmode('+str(mode)+') called'
        GPIO.mode = mode
        
    @staticmethod
    def getmode():
        print 'GPIO.getmode() called. Returning ' + str(GPIO.mode)
        return GPIO.mode
    
    @staticmethod
    def cleanup():
        print 'GPIO.cleanup() called'
        
        
    