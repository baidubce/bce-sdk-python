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
Example for creating EIP transfer task.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient


def test_create_eip_transfer(eip_client, transfer_type, transfer_resource_list, to_user_id):
    """
    Create an EIP resource transfer task.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type transfer_type: string
        :param transfer_type: Transfer resource type, should be 'eip'

        :type transfer_resource_list: list
        :param transfer_resource_list: List of resource short IDs to transfer, max 30 items

        :type to_user_id: string
        :param to_user_id: Target account ID

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_client.create_eip_transfer(
            transfer_type=transfer_type,
            transfer_resource_list=transfer_resource_list,
            to_user_id=to_user_id
        )
        print(res)
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)


if __name__ == '__main__':
    # 初始化EIP client
    eip_client = EipClient(example_conf.config)
    # 转移资源类型
    transfer_type = "eip"
    # 要转移的EIP资源ID列表（最多30个）
    transfer_resource_list = ["ip-4vuz5gko"]
    # 目标账号ID
    to_user_id = "xxxxxx"
    # 创建EIP转移任务
    test_create_eip_transfer(eip_client, transfer_type, transfer_resource_list, to_user_id)