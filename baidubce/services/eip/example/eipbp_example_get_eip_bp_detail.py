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
Example fir eip bp client.
"""

import eip_example_conf
from baidubce import exception
from baidubce.services.eip.eip_bp_client import EipBpClient

def test_get_eip_bp_detail(eip_bp_client, id):
    """
    Get eip_bp's detail owned by the authenticated user and given eip_bp_id.

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type id: string
        :param id: eip_bp's id.

    Return:
        :rtype: dict
        A dictionary containing the detail of eip_bp, for example:
            {
                "autoReleaseTime": "2020-05-30T06:46:44Z",
                "name": "EIP_BP1588821183401",
                "instanceId": "ip-9340430e",
                "createTime": "2020-05-07T03:13:03Z",
                "id": "bw-5fb3ce39",
                "eips": ["100.88.9.120"],
                "instanceBandwidthInMbps": 1,
                "bandwidthInMbps": 2,
                "bindType": "eip"
            }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_bp_client.get_eip_bp_detail(id=id)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化eip_bp client
    eip_bp_client = EipBpClient(eip_example_conf.config)
    # 指定eip_bp id
    id = "bw-xxxxxxxx"
    # 获取eip_bp详情
    eip_bp_detail = test_get_eip_bp_detail(eip_bp_client, id)
    print(eip_bp_detail)