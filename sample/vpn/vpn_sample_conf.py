# !/usr/bin/env python
# coding=utf-8
"""
Configuration for vpn samples.
"""
import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

HOST = b'host'
AK = b'ak'
SK = b'sk'

logger = logging.getLogger('baidubce.services.vpn.vpnclient')
fh = logging.FileHandler('sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
