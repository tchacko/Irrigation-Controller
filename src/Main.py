'''
Created on 12-Mar-2017

@author: chacktho
'''

import sys
from Controller import Controller 

def main(argv):
    controller = Controller()
    controller.startService()
    

if __name__ == '__main__':
    main(sys.argv)