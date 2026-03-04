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
example for create load balancer
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
        # 基本创建（仅必填参数）
        resp = blb_client.create_loadbalancer(vpc_id="vpc-xxxx", subnet_id="sbn-xxxx")
        print("[example] create loadbalancer (basic) response :%s" % resp)
        
        # 完整创建（包含所有可选参数）
        resp_full = blb_client.create_loadbalancer(
            vpc_id="vpc-xxxx",
            subnet_id="sbn-xxxx",
            name="my-blb",
            desc="My Load Balancer",
            address="192.168.1.10",
            blb_type="application",
            eip="1.2.3.4",
            tags=[
                {"tagKey": "env", "tagValue": "prod"},
                {"tagKey": "team", "tagValue": "backend"}
            ],
            billing={
                "paymentTiming": "Postpaid",
                "billingMethod": "ByTraffic"
            },
            performance_level="small",
            auto_renew_length=1,
            auto_renew_time_unit="month",
            resource_group_id="rg-xxxx",
            allow_delete=True,
            allocate_ipv6=True
        )
        print("[example] create loadbalancer (full) response :%s" % resp_full)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
