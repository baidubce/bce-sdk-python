#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: media_config.py
Author: wangpeng41(wangpeng41@baidu.com)
Date: 2015/06/10 15:14:13
"""


import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_COMMON_PATH = _NOW_PATH + '../../../'
sys.path.insert(0, _COMMON_PATH)

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


bos_host = "http://multimedia.bce-testinternal.baidu.com"

#wangpeng41 sandbox
#access_key_id = "d53cba68243040e9ad57833d081c51b6"
#secret_access_key = "234d997357544485b21fd79f34abcefa"

#access_key_id = "11f9634810b743ad9255266b064ddba1"
#secret_access_key = "d5b8dd75acca40f8bb6cd75269305a1c"

#线上测试账号 AK 和 SK 
access_key_id = "11f9634810b743ad9255266b064ddba1"
secret_access_key = "d5b8dd75acca40f8bb6cd75269305a1c"

config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                            endpoint = bos_host)
