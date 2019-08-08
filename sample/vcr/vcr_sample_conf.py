# !/usr/bin/env python
# coding=utf-8
"""
Configuration for vcr samples.
"""
import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

HOST = 'http://vcr.bj.baidubce.com'
AK = 'Fill AK here'
SK = 'Fill SK here'

logger = logging.getLogger('baidubce.services.vcr.vcrclient')
fh = logging.FileHandler('sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
