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
The configuration for tsdb test.
"""
import logging
import baidubce
from baidubce.auth import bce_credentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.retry.retry_policy import NoRetryPolicy


HOST = '<database_name>.tsdb.iot.<region>.baidubce.com'
ACCESS_KEY = '<your ak>'
SECRET_KEY = '<your sk>'

logger = logging.getLogger("baidubce.services.tsdb")
fh = logging.FileHandler("tsdb_test_client.log")
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
