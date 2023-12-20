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
from baidubce.services.eip.eip_group_model import Billing

def test_create_eip_group(eip_group_client, eip_count, bandwidth_in_mbps, name, 
                          billing):
    """
    Create a shared bandwidth EIP group with specified options.
    Real-name authentication is required before creating EIP groups.
    Only prepaid EIP groups are supported.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type eip_count: int
        :param eip_count: Numbers of EIP addresses in the EIP group.
                        The minimum number of public IP addresses is two,
                        and the maximum number multiplies 5Mbps mustn't exceed the
                        total amount of shared bandwidth package.

        :type bandwidth_in_mbps: int
        :param bandwidth_in_mbps: Public Internet bandwidth in unit Mbps.
                                For Prepaid EIP groups, this value must be an 
                                integer between 10 and 200.

        :type billing: eip_group_model.Billing
        :param billing: Billing information.

        :type name: string
        :param name: The name of EIP group that will be created.
                    The name, beginning with a letter, should have a length 
                    between 1 and 65 bytes, and can contain alphabets, numbers 
                    or '-_/.'. If not specified, the service will generate it 
                    automatically.

    Return:
        id of the created EIP group, for example:
        {id: "eg-xxxxxxxx"}


    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_group_client.create_eip_group(eip_count=eip_count, bandwidth_in_mbps=bandwidth_in_mbps, 
                                               name=name, billing=billing)
        eip_group_id = res.id
        return eip_group_id
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 创建EIPGroupClient
    eip_group_client = EipGroupClient(example_conf.config)
    # eip数量
    test_eip_count = 3
    # 10M带宽
    test_bw = 10
    # EIPGroup名字                
    test_name = "test-sdk-eipgroup"     
    # 创建后付费EIPGroup
    test_post_billing = Billing(paymentTiming="Postpaid", billingMethod="ByBandwidth")
    post_eipgroup_id = test_create_eip_group(eip_group_client, eip_count = test_eip_count, 
                                             bandwidth_in_mbps = test_bw, name = test_name, billing = test_post_billing)

    # 创建预付费EIPGroup，周期为1个月
    test_pre_billing = Billing(paymentTiming="Prepaid", reservationLength = 1, 
                               reservationTimeUnit = "Month")
    pre_eipgroup_id = test_create_eip_group(eip_group_client, eip_count = test_eip_count, 
                                            bandwidth_in_mbps = test_bw, name = test_name, billing = test_pre_billing)