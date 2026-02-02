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
Example for changing EIP billing from postpaid to prepaid.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient

def test_change_eip_to_prepay(eip_client, eip, purchase_length, bandwidth):
    """
    Change EIP billing method from postpay to prepay.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type eip: string
        :param eip: eip address to change billing method

        :type purchase_length: int
        :param purchase_length: purchase duration in months (1-9, 12, 24, 36)

        :type bandwidth: int
        :param bandwidth: bandwidth for prepaid EIP

    Return:
        BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = eip_client.change_eip_to_prepay(eip, purchase_length, bandwidth)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化EipClient
    eip_client = EipClient(example_conf.config)

    # EIP地址
    eip = "x.x.x.x"
    # 购买时长(月)
    purchase_length = 1
    # 带宽(Mbps)
    bandwidth = 50

    # 执行计费方式变更
    test_change_eip_to_prepay(eip_client, eip, purchase_length, bandwidth)