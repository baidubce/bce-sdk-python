# -*- coding: utf-8 -*-
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
example for create app load balancer
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.blb import app_blb_client


if __name__ == '__main__':
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "Your Endpoint"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    app_blb_client = app_blb_client.AppBlbClient(config)  # 初始化client
    try:
        resp = app_blb_client.create_app_loadbalancer(vpc_id="vpc-xxxx", subnet_id="sbn-xxxx")  # 创建app blb
        print("[example] create app loadbalancer response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
