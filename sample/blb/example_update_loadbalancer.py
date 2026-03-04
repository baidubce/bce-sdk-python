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
example for update load balancer
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.blb import blb_client

if __name__ == '__main__':
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "Your Endpoint"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    blb_client = blb_client.BlbClient(config)  # 初始化client
    try:
        # 基本更新（名称和描述）
        resp = blb_client.update_loadbalancer("lb-xxxx", name="testblb", desc="justForTest")
        print("[example] update loadbalancer (basic) response :%s" % resp)
        
        # 更新删除保护设置
        resp_delete = blb_client.update_loadbalancer("lb-xxxx", allow_delete=False)
        print("[example] update loadbalancer (allow_delete) response :%s" % resp_delete)
        
        # 启用IPv6支持
        resp_ipv6 = blb_client.update_loadbalancer("lb-xxxx", allocate_ipv6=True)
        print("[example] update loadbalancer (allocate_ipv6) response :%s" % resp_ipv6)
        
        # 完整更新（包含所有参数）
        resp_full = blb_client.update_loadbalancer(
            blb_id="lb-xxxx",
            name="new-blb-name",
            desc="Updated description",
            allow_delete=True,
            allocate_ipv6=True
        )
        print("[example] update loadbalancer (full) response :%s" % resp_full)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
