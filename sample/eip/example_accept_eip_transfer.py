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
Example for accepting EIP transfer tasks.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient


def test_accept_eip_transfer(eip_client, transfer_id_list):
    """
    Accept EIP resource transfer tasks.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type transfer_id_list: list
        :param transfer_id_list: List of transfer task IDs to accept, max 30 items

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_client.accept_eip_transfer(transfer_id_list=transfer_id_list)
        print(res)
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)


if __name__ == '__main__':
    # 初始化EIP client
    eip_client = EipClient(example_conf.config)
    # 要接收的转移任务ID列表（最多30个）
    transfer_id_list = ["tf-5z41ejys"]
    # 接收转移任务
    test_accept_eip_transfer(eip_client, transfer_id_list)