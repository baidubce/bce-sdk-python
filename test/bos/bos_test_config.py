#!/usr/bin/env python
#coding=utf8

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
The configuration for bos test.
"""
from builtins import str
from builtins import bytes
import logging
import baidubce
from baidubce.auth import bce_credentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.retry.retry_policy import NoRetryPolicy

# online
HOST=""
ACCESS_KEY=""
SECRET_KEY=""
DISPLAY_NAME = 'PASSPORT:1504517149'
OWNER_ID = ""


# sandbox
#HOST="bos.qasandbox.bcetest.baidu.com"
#ACCESS_KEY=""
#SECRET_KEY=""


ALIGNED_SIZE = 10 * 1024 * 1024


logger = logging.getLogger("baidubce.http.bce_http_client")
fh = logging.FileHandler("test_client.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
    datefmt="%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

config = BceClientConfiguration(
    bce_credentials.BceCredentials(ACCESS_KEY,
    SECRET_KEY),
    HOST,
    baidubce.protocol.HTTP,
    retry_policy=NoRetryPolicy())
