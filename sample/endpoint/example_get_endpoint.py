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


def test_get_endpoint(endpoint_client, endpoint_id):
    """
    Get endpoint detail info with specified endpointId

    Args:
        :type endpoint_client: EndpointClient
        :param endpoint_client: endpoint_client

        :type endpoint_id: str
        :param endpoint_id: endpoint's id

    Returns:
        None

    Raise:
        BceHttpClientError: http request error
    """
    try:
        response = endpoint_client.get_endpoint(endpoint_id)
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
    # 创建服务网卡
    test_get_endpoint(endpoint_client, endpoint_id)
