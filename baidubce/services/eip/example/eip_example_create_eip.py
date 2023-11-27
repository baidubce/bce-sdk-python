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

def test_create_eip(eip_client, bandwidth_in_mbps, name, billing):
    """
    Create an eip with the specified options.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type bandwidth_in_mbps: int
        :param bandwidth_in_mbps: specify the bandwidth in Mbps

        :type name: string
        :param name: name of eip. The optional parameter

        :type billing: Billing
        :param billing: billing information.

    Return:
        created eip address, for example,{"eip":"x.x.x.x"}
    
    Raises:
        BceHttpClientError: http request failed
    """
    try:
        res = eip_client.create_eip(bandwidth_in_mbps, name, billing)
        eip_addr_str = res.eip
        return eip_addr_str
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 创建EIPClient
    eip_client = EipClient(eip_example_conf.config)
    # 1M带宽
    test_bw = 1
    # EIP名字                
    test_name = "test-sdk-eip"     
    # 创建后付费EIP
    test_post_billing = Billing(payment_timing="Postpaid", billing_method="ByBandwidth")
    post_eipstr = test_create_eip(eip_client, bandwidth_in_mbps = test_bw, name = test_name, 
                                  billing = test_post_billing)
    # 创建预付费EIP，周期为1个月
    test_pre_billing = Billing(payment_timing="Prepaid", reservation_length = 1, reservation_time_unit = "Month")
    pre_eipstr = test_create_eip(eip_client, bandwidth_in_mbps = test_bw, name = test_name, 
                                 billing = test_pre_billing)