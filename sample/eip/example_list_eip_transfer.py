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
Example for listing EIP transfer tasks.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient


def test_list_eip_transfers(eip_client, max_keys=None, marker=None, direction=None,
                            transfer_id=None, status=None,
                            fuzzy_transfer_id=None, fuzzy_instance_id=None,
                            fuzzy_instance_name=None, fuzzy_instance_ip=None):
    """
    List EIP resource transfer tasks.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type max_keys: int
        :param max_keys: Maximum number of items per page, default 10

        :type marker: string
        :param marker: Pagination marker

        :type direction: string
        :param direction: 'sent' for initiated by me, 'received' for received by me

        :type transfer_type: string
        :param transfer_type: Transfer resource type

        :type transfer_id: string
        :param transfer_id: Transfer ID for exact query, multiple IDs separated by '_'

        :type status: string
        :param status: Status filter

        :type fuzzy_transfer_id: string
        :param fuzzy_transfer_id: Transfer ID fuzzy query

        :type fuzzy_instance_id: string
        :param fuzzy_instance_id: Instance ID fuzzy query

        :type fuzzy_instance_name: string
        :param fuzzy_instance_name: Instance name fuzzy query

        :type fuzzy_instance_ip: string
        :param fuzzy_instance_ip: Instance IP fuzzy query

    Return:
        :type: dict
        A dictionary containing the list of transfer tasks

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_client.list_eip_transfer(
            max_keys=max_keys,
            marker=marker,
            direction=direction,
            transfer_id=transfer_id,
            status=status,
            fuzzy_transfer_id=fuzzy_transfer_id,
            fuzzy_instance_id=fuzzy_instance_id,
            fuzzy_instance_name=fuzzy_instance_name,
            fuzzy_instance_ip=fuzzy_instance_ip
        )
        print("EIP transfer tasks list:")
        print(res)
        return res
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None


if __name__ == "__main__":
    # 初始化EIP client
    eip_client = EipClient(example_conf.config)
    all_transfers = test_list_eip_transfers(eip_client, 10, "tf-1l4m5etb", "sent",
                                            "tf-1l4m5etb", "success", "tf-1l4m5etb",
                                            "ip-3pblsyay", "EIP1768387961009",
                                            "100.88.8.139")