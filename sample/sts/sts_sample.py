# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Samples for sts client.
"""

import os
import random
import string

import sts_sample_conf
from baidubce import exception
from baidubce.services.sts.sts_client import StsClient

if __name__ == "__main__":
    import logging
    
    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    sts_client = StsClient(sts_sample_conf.config)

    duration_seconds = 3600
    access_dict = {}
    access_dict["service"] = "bce:bos"
    access_dict["region"] = "bj"
    access_dict["effect"] = "Allow"
    resource = ["*"]
    access_dict["resource"] = resource
    permission = ["READ"]
    access_dict["permission"] = permission

    access_control_list = [access_dict]

    acl = {"accessControlList": access_control_list}
    response = sts_client.get_session_token(acl=acl,
                                            duration_seconds=duration_seconds)

    print response.session_token

