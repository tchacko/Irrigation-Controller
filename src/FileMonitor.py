'''
Created on Mar 7, 2017

@author: chacktho
'''
import pyinotify
import threading
#from Events import FileChangeEvent  
#from EventProcessor import EventProcessor
from BoardConfiguration import BoardConfiguration
from SystemStatus import SystemStatus
import Utils


# The watch manager stores the watches and provides operations on watches


class FileMonitor(threading.Thread):
    def __init__(self, filePath, controller, eventProcessor):
        self.wm = pyinotify.WatchManager()
        self.mask = pyinotify.IN_MODIFY | pyinotify.IN_DELETE
        self.controller = controller
        self.handler = EventHandler(self.controller, eventProcessor)
        self.filePath = filePath
        threading.Thread.__init__(self,None, None, 'FileMonitor-Thread')
        
    def run(self):
        if self.filePath is None or self.filePath == '':
            print 'File is not specified. FileMonitor::run() exiting'
            return
        print 'starting File Monitor thread '+ self.name + ' at ' + Utils.getFormatedTime()
        notifier = pyinotify.Notifier(self.wm, self.handler)
        self.wm.add_watch(self.filePath, self.mask, rec=True)
        notifier.loop()

class EventHandler(pyinotify.ProcessEvent):
    
    def __init__(self, controller, eventProcessor):
        self.controller = controller
        self.eventProcessor = eventProcessor
        
    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname
        
    def process_IN_MODIFY(self, event):
        print "Changed:", event.pathname
        fce = FileChangeEvent(event.pathname, FileChangeEvent.FILE_MODIFIED, self.controller)
        self.eventProcessor.enqueue(fce)
        
class Task:
    
    def  __init__(self):
        print 'Not implemented'
        
    def execute(self):
        print 'Not implemented'
        
class FileChangeEvent(Task):
    
    FILE_MODIFIED = 1
    FILE_DELETED = 2
    FILE_CREATED = 3
    
    
    def __init__(self, path, change, controller):
        self.filePath = path
        self.change = change
        self.controller = controller
        
    def execute(self):
        if self.change == FileChangeEvent.FILE_MODIFIED:
            if self.isModified(BoardConfiguration.BOARD_CONFIG_FILE):
                #File Modified
                self.processConfigFileModified()
    
    def isModified(self, mofiedFile):
        if BoardConfiguration.BOARD_CONFIG_FILE == mofiedFile:
            return True
        
        return False
    
    def processConfigFileModified(self):
        boardStatus = SystemStatus()
        if boardStatus.getStatus() != SystemStatus.STATUS_REGISTERED:
            print 'Device ', boardStatus.getUid(), ' not Registered.'
            return
        
        boardConfig = BoardConfiguration('RpiBoard');
        #controller = Controller.getController()
        self.controller.configModified(boardConfig)

# Test
#fm = FileMonitor('/home/chacktho/workspace/IrriMate/src/data/board/config.json');
#fm.run();