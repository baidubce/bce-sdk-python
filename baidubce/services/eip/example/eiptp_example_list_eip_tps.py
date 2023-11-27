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

def test_list_eip_tps(eip_tp_client, id=None, deduct_policy=None, status=None,
                     marker=None, max_keys=1000):
    """
    Get a list of eip_tp owned by the authenticated user, filtered by specific conditions.

    Args:
        :type eip_tp_client: EipTpClient
        :param eip_tp_client: EipTpClient

        :type id: string
        :param id: eip_tp's id, the optional parameter.

        :type deduct_policy: string
        :param deduct_policy: eip_tp's deduct policy, options include 'FullTimeDurationPackage' 
                            or 'TimeDurationPackage'. This is an optional parameter.

        :type status: string
        :param status: eip_tp's status, options include 'RUNNING', 'EXPIRED', or 'USED_UP'. 
                    This is an optional parameter.

        :type marker: string
        :param marker: The optional parameter marker specified in the original request to 
                    specify where in the results to begin listing.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number of list result 
                        to return. The default value is 1000.

    Return:
        :type: dict
        A dictionary containing a list of eip_tp model, for example:
            {
                "marker": "tp-87V5cnkwqO",
                "maxKeys": 1,
                "nextMarker": "tp-Qn65tYXAx3",
                "isTruncated": true,
                "packageList": [
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
                    // ... 更多 eip_tp 条目
                ]
            }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_tp_client.list_eip_tps(id=id, deduct_policy=deduct_policy, status=status,
                                         marker=marker, max_keys=max_keys)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化eip_tp client
    eip_tp_client = EipTpClient(eip_example_conf.config)
    # 获取eip_tp列表
    eip_tps = test_list_eip_tps(eip_tp_client, id=None, deduct_policy=None, status=None,
                     marker=None, max_keys=1000)
    print(eip_tps)