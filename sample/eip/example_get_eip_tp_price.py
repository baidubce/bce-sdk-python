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
Example for eip tp price inquiry.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_tp_client import EipTpClient

def test_get_eip_tp_price(eip_tp_client, reservation_length, capacity,
                          deduct_policy=None, package_type=None):
    """
    Get the price of creating an eip_tp with the specified options.

    Args:
        :type eip_tp_client: EipTpClient
        :param eip_tp_client: EipTpClient

        :type reservation_length: int
        :param reservation_length: The reservation length of the eip_tp
                                   including 1, 6, and 12 months.

        :type capacity: string
        :param capacity: The capacity of the eip_tp.

        :type deduct_policy: string
        :param deduct_policy: The deduct policy of the eip_tp (optional).

        :type package_type: string
        :param package_type: The eip_tp package type (optional).

    Return:
        :type: dict
        A dictionary containing the price, for example, {"price": "7.20000"}.

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_tp_client.get_eip_tp_price(
            reservation_length=reservation_length,
            capacity=capacity,
            deduct_policy=deduct_policy,
            package_type=package_type
        )
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化eip_tp client
    eip_tp_client = EipTpClient(example_conf.config)

    # 指定时长
    reservation_length = 1
    # 指定容量
    capacity = "10G"
    # 指定扣费策略
    deduct_policy = "FullTimeDurationPackage"
    # 指定共享流量包的线路类型
    package_type = "WebOutBytes"

    # 查询价格
    price_result = test_get_eip_tp_price(
        eip_tp_client, reservation_length, capacity,
        deduct_policy, package_type
    )
    print(price_result)