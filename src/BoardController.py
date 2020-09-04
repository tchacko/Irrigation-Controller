'''
Created on 10-Mar-2017

@author: chacktho
'''
from RpiBoard import RpiBoard 

class BoardController(object):
    '''
    classdocs
    '''


    def __init__(self, controller, boardConfig):
        '''
        Constructor
        '''
        self.controller = controller
        self.configuration = boardConfig
        self.rpiBoard = RpiBoard(self.controller, self.configuration)
        
    def activate(self, board):
        if board.isEnabled():
            devices = board.getDevices()
            for dId in devices:
                device = devices[dId]
                if device.isEnabled():
                    channel = device.getControlChannel()
                    if channel.isEnabled():
                        self.rbiBoard.turnOnChannel(channel.getId())
                else:
                    channel = device.getControlChannel()
                    if channel.isEnabled():
                        self.rbiBoard.turnOffChannel(channel.getId())
        else:
            self.rpiBoard.activate(board, False)
            
    def turnOffDevice(self, device):
        dev = self.getDevice(device.getId())
        if dev is None:
            return
        dev.turnOffDevice()
        
    def turnOffBoard(self, board):
        print 'turn off board'
        