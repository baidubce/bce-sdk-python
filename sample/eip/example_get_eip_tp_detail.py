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
Example for eip tp client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_tp_client import EipTpClient

def test_get_eip_tp_detail(eip_tp_client, id):
    """
    Get the eip_tp's detail owned by the authenticated user by the passed eip_tp_id.

    Args:
        :type eip_tp_client: EipTpClient
        :param eip_tp_client: EipTpClient

        :type id: string
        :param id: eip_tp's id.

    Return:
        :type: dict
        A dictionary containing the detail of eip_tp, for example:
            {
                "id": "tp-87V5cnkwqO",
                "deductPolicy": "TimeDurationPackage",
                "packageType": "WebOutBytes",
                "status": "RUNNING",
                "capacity": 10737418240,
                "usedCapacity": 0,
                "createTime": "2021-04-10T11:40:57Z",
                "activeTime": "2021-04-10T11:41:16Z",
                "expireTime": "2021-05-10T11:41:16Z"
            }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_tp_client.get_eip_tp_detail(id=id)
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
    # 指定id
    id = 'tp-xxxxxxxxxx'
    # 获取eiptp详情
    eip_tp_detail = test_get_eip_tp_detail(eip_tp_client, id)
    print(eip_tp_detail)