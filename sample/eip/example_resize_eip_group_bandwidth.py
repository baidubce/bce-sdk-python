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
Example fir eip group client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_group_client import EipGroupClient

def test_resize_eip_group_bandwidth(eip_group_client, id, bandwidth_in_mbps):
    """
    Resize the bandwidth of a specified EIP group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of specified EIP group.

        :type bandwidth_in_mbps: int
        :param bandwidth_in_mbps: The new bandwidth of EIP group. For prepaid EIP 
                                groups, this value must be an integer between 10 
                                and 200.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_group_client.resize_eip_group_bandwidth(id=id, bandwidth_in_mbps=bandwidth_in_mbps)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 创建EIPGroupClient
    eipgroup_client = EipGroupClient(example_conf.config)
    # 指定eipgroup的id
    id = "eg-xxxxxxxx"
    # 重设eipgroup的bandwidth，单位M
    bandwidth = 10
    # 列出对应id的eipgroup信息
    test_resize_eip_group_bandwidth(eipgroup_client, id, bandwidth)