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

def test_eip_group_move_in(eip_group_client, id, eips):
    """
    Move in an EIP to a group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The ID of the EIP group.

        :type eips: List[str]
        :param eips: The list of EIPs to move in.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """

    try:
        res = eip_group_client.eip_group_move_in(id=id, eips=eips)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化eip_group_client
    eip_group_client = EipGroupClient(example_conf.config)
    # 初始化eipGroupId
    id = "eg-xxxxxxxx"
    # 初始化移入eipList
    eips = ["x.x.x.x"]
    # 调用move_in
    test_eip_group_move_in(eip_group_client, id, eips)