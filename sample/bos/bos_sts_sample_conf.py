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
Configuration for bos samples.
"""

#!/usr/bin/env python
#coding=utf-8

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.sts.sts_client import StsClient

sts_host = "Fill STS host here"
access_key_id = "Fill AK here"
secret_access_key = "Fill SK here"

logger = logging.getLogger('baidubce.services.sts.stsclient')
fh = logging.FileHandler("sample.log")
fh.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
__logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

sts_config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=sts_host)
# get StsClient
sts_client = StsClient(sts_config)

duration_seconds = 3600
# you can specify limited permissions with ACL
access_dict = {}
access_dict["service"] = "bce:bos"
access_dict["region"] = "bj"   
access_dict["effect"] = "Allow"
resource = ["*"]
access_dict["resource"] = resource
permission = ["READ"]
access_dict["permission"] = permission

access_control_list = {"accessControlList": [access_dict]}

# 新建StsClient
response = sts_client.get_session_token(acl=access_control_list, duration_seconds=duration_seconds)

sts_ak = str(response.access_key_id)
sts_sk = str(response.secret_access_key)
token = response.session_token
bos_host = "Fill host here"
#配置BceClientConfiguration
config = BceClientConfiguration(credentials=BceCredentials(sts_ak, sts_sk), endpoint = bos_host, security_token=token)