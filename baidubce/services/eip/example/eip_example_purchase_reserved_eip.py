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
Example fir eip client.
"""

import eip_example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient
from baidubce.services.eip.model import Billing

def test_purchase_reserved_eip(eip_client, eip, billing):
    """
    PurchaseReserved eip with fixed duration,only Prepaid eip can do this

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type eip: string
        :param eip: eip address to be renewed

        :type billing: Billing
        :param billing: billing information.

    Return: 
        None
    
    Raise:
        BceHttpClientError: http request failed
    """
    try:
        res = eip_client.purchase_reserved_eip(eip, billing)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化EipClient
    eip_client = EipClient(eip_example_conf.config)
    # 续费的EIP
    eip = 'x.x.x.x'
    # 续费，不指定billing默认续费一个月
    test_purchase_reserved_eip(eip_client, eip, None)
    # 初始化billing
    billing = Billing(reservation_length=2, reservation_time_unit='Month')
    # 续费，指定billing
    test_purchase_reserved_eip(eip_client, eip, billing)