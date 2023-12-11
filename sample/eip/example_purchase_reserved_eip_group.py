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
Example fir eip group client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_group_client import EipGroupClient
from baidubce.services.eip.eip_group_model import Billing

def test_eip_group_purchase_reserved_eip_group(eip_group_client, id, billing):
    """
    Renew specified EIP group.
    EIP groups cannot be renewed during the resizing process.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of the EIP group.

        :type billing: eip_group_model.Billing
        :param billing: Billing information.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_group_client.purchase_reserved_eip_group(id=id, billing=billing)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 创建EIPGroupClient
    eip_group_client = EipGroupClient(example_conf.config)
    # 续费eipgroup的id，必须是预付费eipgroup
    id = "eg-xxxxxxxx"
    # 创建billing对象，必须是预付费
    test_pre_billing = Billing(paymentTiming="Prepaid", reservationLength = 1, 
                               reservationTimeUnit = "Month")
    # 续费
    test_eip_group_purchase_reserved_eip_group(eip_group_client, id = id, billing = None)