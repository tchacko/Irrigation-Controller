'''
Created on 07-Mar-2017

@author: root
'''
import threading
from Queue import Queue
import Utils

class EventProcessor(object):
    '''
    classdocs
    '''
    MAX_QUEUE_SIZE = 500
    WORKERS = 1

    def __init__(self):
        '''
        Constructor
        '''
        self.queue = Queue(EventProcessor.MAX_QUEUE_SIZE)

        for i in range(EventProcessor.WORKERS):
            Worker(self.queue, 'Worker-0'+str(i)).start() # start a worker
        
    def enqueue(self, event):
        self.queue.put(event)
        
''' Worker Class '''
class Worker(threading.Thread):

    def __init__(self, queue, name):
        self.queue = queue
        self.workerName = name
        threading.Thread.__init__(self,None, None, 'EventProcessor-' + self.workerName)

    def run(self):
        print 'starting Event Processor thread '+ self.name + ' at ' + Utils.getFormatedTime()
        while 1:
            task = self.queue.get()
            if task is None:
                continue 
            
            task.execute()
            print "task ", task, " executed by ", self.name


    

