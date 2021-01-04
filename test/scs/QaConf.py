#!/usr/bin/env python
#coding=utf8

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

SCS_HOST1 = b''
SCS_AK1 = b''
SCS_SK1 = b''
SCS_HOST2 = b''
SCS_AK2 = b''
SCS_SK2 = b''

logger = logging.getLogger('baidubce.services.scs.scsclient')
fh = logging.FileHandler('scs_sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config1 = BceClientConfiguration(credentials=BceCredentials(SCS_AK1, SCS_SK1), endpoint=SCS_HOST1)
config2 = BceClientConfiguration(credentials=BceCredentials(SCS_AK2, SCS_SK2), endpoint=SCS_HOST2)
