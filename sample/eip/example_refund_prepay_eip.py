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
Example for refunding prepaid EIP.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient

def test_refund_prepay_eip(eip_client, eip):
    """
    Refund a prepay EIP.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type eip: string
        :param eip: eip address to refund

    Return:
        BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = eip_client.refund_prepay_eip(eip)
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

    # 预付费EIP地址
    eip = "x.x.x.x"

    # 执行退订
    test_refund_prepay_eip(eip_client, eip)