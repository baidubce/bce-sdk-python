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
from baidubce.services.endpoint import model


def test_create_endpoint(endpoint_client, vpc_id, subnet_id, name, service, billing, bandwidth,
                         description=None, ip_address=None, tags=None, resource_group_id=None):
    """
    Create endpoint in vpc subnet with specified name, service and billing

    Args:
        :type endpoint_client: EndpointClient
        :param endpoint_client: endpoint_client

        :type vpc_id: str
        :param vpc_id: id of vpc which endpoint belongs to

        :type subnet_id: str
        :param subnet_id: id of subnet which endpoint belongs to

        :type name: str
        :param name: endpoint's name

        :type service: str
        :param service: domain name to be bounded

        :type billing: Billing
        :param billing: the endpoint creation order configuration

        :type bandwidth: int
        :param bandwidth: the bandwidth of endpoint

        :type description: str
        :param description: endpoint's description

        :type ip_address: str
        :param ip_address: ipv4 address

        :type tags: list
        :param tags: the list of tags to be bound

        :type resource_group_id: str
        :param resource_group_id: the id of resource group

    Returns:
        None

    Raise:
        BceHttpClientError: http request error
    """
    try:
        response = endpoint_client.create_endpoint(vpc_id, subnet_id, name, service, billing, bandwidth,
                                                   description=description, ip_address=ip_address,
                                                   tags=tags, resource_group_id=resource_group_id)
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
    # 初始化Billing
    billing = model.Billing(payment_timing=b'Prepaid')
    # 所属VPC的ID
    vpc_id = b'vpc-xxx'
    # 所在子网的ID
    subnet_id = b'subnet-xxx'
    # 服务网卡的名称
    name = b'test-endpoint'
    # 挂载的服务域名
    service = b'www.test-endpoint-service.com'
    # 服务网卡带宽
    bandwidth = 20
    
    # Example 1: 基础创建服务网卡（不使用可选参数）
    print("Example 1 - Basic creation:")
    test_create_endpoint(endpoint_client, vpc_id, subnet_id, name, service, billing, bandwidth)
    
    # Example 2: 创建服务网卡并指定标签、资源组等可选参数
    print("\nExample 2 - Creation with tags and resource_group_id:")
    name2 = b'test-endpoint-with-tags'
    tags = [
        {
            'tagKey': 'project',
            'tagValue': 'test'
        },
        {
            'tagKey': 'env',
            'tagValue': 'production'
        }
    ]
    resource_group_id = b'RESG-UoMgbkuLNjj'
    ip_address = b'192.168.0.100'
    description = b'Test endpoint with tags'
    
    test_create_endpoint(endpoint_client, vpc_id, subnet_id, name2, service, billing, bandwidth,
                        description=description, ip_address=ip_address, 
                        tags=tags, resource_group_id=resource_group_id)
