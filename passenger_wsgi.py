import imp
import os
import sys
import logging

logging.basicConfig(filename='/home/oropezar/apuestas/logs.log',level=logging.DEBUG)

logging.debug('starting.\n')

#PassengerAppEnv = development
sys.path.insert(0, os.path.dirname(__file__))

logging.warn('Before getting application')

apuestasapp = imp.load_source('', 'main.py')

logging.warn('Before returning application')

application = apuestasapp.app
