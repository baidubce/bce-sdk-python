#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Configuration for sms samples.
"""

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

#HOST = 'nmg02-bce-test8.nmg02.baidu.com:8887'
#HOST = b'10.42.177.14:8181'
HOST = b'10.227.94.157:8181'
AK = b'39fe0068d78f4db4a4c18891c74862a8'
SK = b'c7d23dc1463e44f8ab132a8a85264b9e'

logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler('sms_sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
