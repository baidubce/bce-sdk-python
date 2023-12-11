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

def test_eip_group_move_out(eip_group_client, id, move_out_args):
    """
    Move out an EIP from a group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The ID of the EIP group.

        :type move_out_args: List[dict]
        :param move_out_args: List of dictionaries for moving out the EIPs, 
                            each dict containing 'eip', 'bandwidth_in_mbps', 
                            and 'billing' keys.

    Return:
        :rtype: baidubce.bce_response.BceResponse
        A BceResponse object.

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """

    try:
        res = eip_group_client.eip_group_move_out(id=id, move_out_args=move_out_args)
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
    # EIPGroup的id
    test_id = "eg-xxxxxxxx"
    # 创建移出dict
    move_out_args = []
    # 构造第一个移出的EIP
    move_out_arg_1 = {}
    # eip 
    move_out_arg_1["eip"] = "x.x.x.x"
    # 添加至dict
    move_out_args.append(move_out_arg_1)
    # 构造第二个移出的EIP
    move_out_arg_2 = {}
    # eip
    move_out_arg_2["eip"] = "y.y.y.y"
    # 带宽
    move_out_arg_2["bandwidthInMbps"] = 100
    # 创建后付费EIPGroup billing
    move_out_arg_2["billing"] = Billing(paymentTiming="Postpaid", billingMethod="ByBandwidth")
    # 添加至dict
    move_out_args.append(move_out_arg_2)

    test_eip_group_move_out(eip_group_client=eip_group_client, id=test_id, move_out_args=move_out_args)