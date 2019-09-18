#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: media_config.py
Date: 2015/06/10 15:14:13
"""


import sys
import os
#import imp
#imp.reload(sys)


_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_COMMON_PATH = _NOW_PATH + '../../../'
sys.path.insert(0, _COMMON_PATH)

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


bos_host = b"http://multimedia.bce-testinternal.baidu.com"
access_key_id = b""
secret_access_key = b""




config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                            endpoint = bos_host)
