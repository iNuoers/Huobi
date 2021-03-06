#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Charles on 2018/6/20
# Function:
'''
Provide a function  for anyone who want to configure log parameters easily,
just call init_log_config before your use the module of logging that build-in python
'''


import os
import logging
from datetime import datetime
from logging import handlers

# formatter
FORMATTER = "%(asctime)s %(filename)s[line:%(lineno)d] " \
            "[%(module)s:%(funcName)s] [%(threadName)s:%(thread)d] " \
            "%(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# log file args
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_NAME = "debug_{}.log".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))       # your_log_file_name.log
LOG_FILE_PATH = os.path.join(BASE_DIR, LOG_FILE_NAME)   # your log full path
LOG_FILE_SIZE = 10 * 1024 * 1024                        # the limit of log file size
LOG_BACKUP_COUNT = 5                                    # backup counts

# log mail args, You need to correct the following variables if you want to use email notification function
MAIL_SERVER = 'smtp.xxxx.com'
MAIL_PORT = 25
FROM_ADDR = 'from@xxx.com'
TO_ADDRS = "to1@xxx.com;to2@xxx.com"
SUBJECT = 'Application Error'
CREDENTIALS = ('your_account@xxx.com', 'your_password')

# log level args
LOG_OUTPUT_LEVEL = logging.DEBUG
LOG_FILE_LEVEL = logging.INFO
LOG_CONSOLE_LEVEL = logging.DEBUG
LOG_MAIL_LEVEL = logging.ERROR


def init_log_config(use_mail=False):
    '''
    Do basic configuration for the logging system. support ConsoleHandler, RotatingFileHandler and SMTPHandler
    :param use_mail: Whether to use the email notification function, default False
    :return: None
    '''
    logging.basicConfig(level=LOG_OUTPUT_LEVEL,
                        format=FORMATTER,
                        datefmt=DATE_FORMAT)

    # add rotating file handler
    rf_handler = handlers.RotatingFileHandler(LOG_FILE_PATH, maxBytes=LOG_FILE_SIZE, backupCount=LOG_BACKUP_COUNT)
    rf_handler.setLevel(LOG_FILE_LEVEL)
    formatter = logging.Formatter(FORMATTER)
    rf_handler.setFormatter(formatter)
    logging.getLogger().addHandler(rf_handler)

    # add smtp handler if use_mail is True
    if use_mail:
        mail_handler = handlers.SMTPHandler(
            mailhost=(MAIL_SERVER, MAIL_PORT),
            fromaddr=FROM_ADDR,
            toaddrs=TO_ADDRS.split(";"),
            subject=SUBJECT,
            credentials=CREDENTIALS
        )
        mail_handler.setLevel(LOG_MAIL_LEVEL)
        mail_handler.setFormatter(logging.Formatter(FORMATTER))
        logging.getLogger().addHandler(mail_handler)
