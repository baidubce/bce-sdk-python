# -*- coding: utf-8 -*-
# !/usr/bin/env python

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
Samples for endpoint client.
"""

from baidubce import exception
import sample.endpoint.endpoint_sample_conf as sample_conf
from baidubce.services.endpoint.endpoint_client import EndpointClient


def test_update_endpoint_sg(endpoint_client, endpoint_id, security_group_list):
    """
    Update endpoint's security_group_list with a specified endpoint_id

    Args:
        :type endpoint_client: EndpointClient
        :param endpoint_client: endpoint client

        :type endpoint_id: str
        :param endpoint_id: endpoint's id

        :type security_group_list: list
        :param security_group_list: the security group list to be bound

    Returns:
        None

    Raise:
        BceHttpClientError: http request error
    """
    try:
        response = endpoint_client.update_endpoint_sg(endpoint_id, security_group_list)
        print(response)
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None


if __name__ == '__main__':
    # 初始化EndpointClient
    endpoint_client = EndpointClient(sample_conf.config)
    # 服务网卡的ID
    endpoint_id = b'endpoint-xxx'
    # 普通安全组的ID列表，需和服务网卡在同一VPC下
    security_group_list = [
        b'sg-xxx',
        b'sg-xxxx'
    ]
    # 更新服务网卡绑定的普通安全组的列表
    test_update_endpoint_sg(endpoint_client, endpoint_id, security_group_list)
