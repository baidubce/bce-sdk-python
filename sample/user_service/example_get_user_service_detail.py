# -*- coding: utf-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Example for get user service detail information.
"""

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.exception import BceHttpClientError

from baidubce.services.blb import user_service_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号AK
    sk = "Your SK"  # 账号AK
    endpoint = 'Your Endpoint'  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak,
                                    secret_access_key=sk), endpoint=endpoint)
    client = user_service_client.UserServiceClient(config)
    try:
        service = 'Your Service Domain'   # 服务发布点的域名
        resp = client.get_user_service_detail(service, None, config)
        print("[example] get user service detail response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
