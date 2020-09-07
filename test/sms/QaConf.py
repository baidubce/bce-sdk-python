#!/usr/bin/env python
#coding=utf8

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

SMS_HOST1 = b''
SMS_AK1 = b''
SMS_SK1 = b''
SMS_HOST2 = b''
SMS_AK2 = b''
SMS_SK2 = b''

logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler('sms_sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config1 = BceClientConfiguration(credentials=BceCredentials(SMS_AK1, SMS_SK1), endpoint=SMS_HOST1)
config2 = BceClientConfiguration(credentials=BceCredentials(SMS_AK2, SMS_SK2), endpoint=SMS_HOST2)
