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
Example for eip group client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_group_client import EipGroupClient

def test_update_eip_group(eip_group_client, id, name):
    """
    Update the name of specified EIP group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of specified EIP group.

        :type name: string
        :param name: The new name of the EIP group.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_group_client.update_eip_group(id=id, name=name)
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
    # 更新eipgroup的name
    name = "new_eipgroup"
    # 列出对应id的eipgroup信息
    test_update_eip_group(eipgroup_client, id, name)
