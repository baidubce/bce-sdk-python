#!/usr/bin/env python
#coding=utf8

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

SMS_HOST = b'HOST:PORT'
SMS_AK = b'ak'
SMS_SK = b'sk'

logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler('sms_sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(SMS_AK, SMS_SK), endpoint=SMS_HOST)