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
Configuration for tsdb samples.
"""

#!/usr/bin/env python
#coding=utf-8

import logging
import baidubce.protocol
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

HOST = '<database_name>.tsdb.iot.<region>.baidubce.com'
AK = '<your ak>'
SK = '<your sk>'

###########optional config#############
protocol=baidubce.protocol.HTTP
# protcol= baidubce.protocol.HTTPS
connection_timeout_in_mills=None
send_buf_size=None
recv_buf_size=None
retry_policy=None
#######################################

logger = logging.getLogger('baidubce.services.tsdb.tsdbclient')
fh = logging.FileHandler('sample.log')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(fh)

config = BceClientConfiguration(
        credentials=BceCredentials(AK, SK),
        endpoint=HOST,
        protocol=protocol,
        connection_timeout_in_mills=connection_timeout_in_mills,
        send_buf_size=send_buf_size,
        recv_buf_size=recv_buf_size,
        retry_policy=retry_policy)