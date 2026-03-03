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
example for describe load balancer
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
        # 查询所有BLB实例
        resp = blb_client.describe_loadbalancers()
        print("[example] describe all loadbalancers response :%s" % resp)
        
        # 按名称模糊查询
        resp_by_name = blb_client.describe_loadbalancers(name="my-blb")
        print("[example] describe loadbalancers by name response :%s" % resp_by_name)
        
        # 按名称精确匹配查询
        resp_exact = blb_client.describe_loadbalancers(name="my-blb", exactly_match=True)
        print("[example] describe loadbalancers (exact match) response :%s" % resp_exact)
        
        # 按类型查询
        resp_by_type = blb_client.describe_loadbalancers(blb_type="application")
        print("[example] describe loadbalancers by type response :%s" % resp_by_type)
        
        # 组合查询
        resp_combined = blb_client.describe_loadbalancers(
            name="my-blb",
            blb_type="application",
            exactly_match=True,
            max_keys=50
        )
        print("[example] describe loadbalancers (combined filters) response :%s" % resp_combined)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
