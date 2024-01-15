#!/usr/bin/env python
# coding=utf8

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
rds configuration
"""

import logging

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

RDS_HOST1 = b''
RDS_AK1 = b''
RDS_SK1 = b''
RDS_HOST2 = b''
RDS_AK2 = b''
RDS_SK2 = b''

logger = logging.getLogger('baidubce.services.rds.rdsclient')
fh = logging.FileHandler('rds_sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

config1 = BceClientConfiguration(credentials=BceCredentials(RDS_AK1, RDS_SK1), endpoint=RDS_HOST1)
config2 = BceClientConfiguration(credentials=BceCredentials(RDS_AK2, RDS_SK2), endpoint=RDS_HOST2)
