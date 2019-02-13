#!/usr/bin/env python2.7
# Copyright (C) 2019 MuS
# http://answers.splunk.com/users/2122/mus
#

import sys
import os
import csv
import socket
import splunk
import logging
import logging.handlers

# set debug
myDebug='no'

# get SPLUNK_HOME form OS
SPLUNK_HOME = os.environ['SPLUNK_HOME']

# get myScript name and path
myScript = os.path.basename(__file__)
myPath = os.path.dirname(os.path.realpath(__file__))
myHost = socket.gethostname()

# define the logger to write into log file
def setup_logging(n):
    logger = logging.getLogger(n)
    if myDebug == 'yes':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = '%s.log' % myScript
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = '%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s'
    splunk_log_handler = logging.handlers.RotatingFileHandler(
        os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE,
                             LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger

# start the logger for troubleshooting
logger = setup_logging('starting logger ...')  # logger

# reading lookup file
logger.info('reading lookup ...')  # logger
myLookup = '{0}/../lookups/loadbalancer.csv'.format(myPath)
logger.info('reading lookup %s ...' % myLookup)
with open(myLookup) as csvfile:
    logger.info('opening lookup ...')  # logger
    readCSV = csv.reader(csvfile, delimiter=',')
    logger.info('reading lines ...')  # logger
    for row in readCSV:
        logger.info('looping lines ...')  # logger
        if myHost in row[0]:
            logger.info('host found in lookup %s ...' % myHost)  # logger
            rest_response = row[1]
            logger.info('rest_response %s ...' % rest_response)  # logger

class status(splunk.rest.BaseRestHandler):
     logger.info('Starting the status class ...')  # logger
     def handle_submit(self):
         logger.info('Starting the handle_submit def ...')  # logger
         try:
             logger.info('setting REST response to %s ...' % rest_response)  # logger
             self.response.setHeader('content-type', 'text/html')
             self.response.write('%s' % rest_response)
         except:
             logger.info('except ...')  # logger
             self.response.setHeader('content-type', 'text/html')
             self.response.write('Uh oh! This server is not in the lookup yet')

     handle_GET = handle_submit
