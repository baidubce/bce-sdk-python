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
Example fir eip tp client.
"""

import eip_example_conf
from baidubce import exception
from baidubce.services.eip.eip_tp_client import EipTpClient

def test_create_eip_tp(eip_tp_client, reservation_length, capacity, deduct_policy=None, package_type=None):
    """
    Create an eip_tp with the specified options.

    Args:
        :type eip_tp_client: EipTpClient
        :param eip_tp_client: EipTpClient

        :type reservation_length: int
        :param reservation_length: The reservation length of the eip_tp including 1, 6, and 12 months.

        :type capacity: string
        :param capacity: The capacity of the eip_tp. Different capacities are available based on 
                        the reservation length:
                        - When reservationLength = 1, capacity options include "10G", "50G", "100G", 
                        "500G", "1T", "5T", "10T", "50T".
                        - When reservationLength = 6, capacity options include "60G", "300G", "600G",
                        "3T", "6T", "30T", "60T", "300T".
                        - When reservationLength = 12, capacity options include "1T", "10T", "50T", 
                        "100T", "500T", "1P".

        :type deduct_policy: string
        :param deduct_policy: The deduct policy of the eip_tp, including 'FullTimeDurationPackage'
                            and 'TimeDurationPackage'. The default deduct policy is 
                            'FullTimeDurationPackage'. This is an optional parameter.

        :type package_type: string
        :param package_type: The eip_tp package type. The default package type is 'WebOutBytes'.
                            This is an optional parameter.

    Return:
        :type: dict
        A dictionary containing the created eip_tp id, for example, {"id": "tp-xxxxxxxxxx"}.

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_tp_client.create_eip_tp(reservation_length=reservation_length,
                                          capacity=capacity, deduct_policy=deduct_policy, 
                                          package_type=package_type)
        eip_tp_id = res.id
        return eip_tp_id
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化eip_tp client
    eip_tp_client = EipTpClient(eip_example_conf.config)
    # 指定时长
    reservation_length = 1
    # 指定容量
    capacity = "10G"
    # 指定扣费策略
    deduct_policy = "FullTimeDurationPackage"
    # 指定共享流量包的线路类型
    package_type = "WebOutBytes"
    # 创建eip_tp
    eip_tp_id = test_create_eip_tp(eip_tp_client, reservation_length, capacity, 
                                   deduct_policy, package_type)
    print(eip_tp_id)
