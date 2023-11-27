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


import eip_example_conf
from baidubce import exception
from baidubce.services.eip.eip_group_client import EipGroupClient

def test_resize_eip_group_count(eip_group_client, id, eip_add_count):
    """
    Resize the EIP count of a specified EIP group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of specified EIP group.

        :type eip_add_count: int
        :param eip_add_count: The increase number of EIP addresses in the EIP group.
                            This value must be larger than zero, and the maximum 
                            number multiplies 5Mbps mustn't exceed the total amount 
                            of shared bandwidth package.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_group_client.resize_eip_group_count(id=id, eip_add_count=eip_add_count)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 创建EIPGroupClient
    eipgroup_client = EipGroupClient(eip_example_conf.config)
    # 指定eipgroup的id
    id = "eg-xxxxxxxx"
    # 重设eipgroup的bandwidth，单位M
    eip_add_count = 1
    # 列出对应id的eipgroup信息
    test_resize_eip_group_count(eipgroup_client, id, eip_add_count)
