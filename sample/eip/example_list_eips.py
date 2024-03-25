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
Example for eip client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient

def test_list_eips(eip_client, eip, instance_type, instance_id, status, marker, max_keys):
    """
    Get a list of eip owned by the authenticated user and specified
    conditions. we can Also get a single eip function  through this
    interface by eip condition

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type eip: string
        :param eip: eip address condition

        :type instance_type: string
        :param instance_type: bound instance type condition

        :type instance_id: string
        :param instance_id: bound instance id condition
        if query by the instanceId or instanceType condition, must provides
         both of them at the same time

        :type status: string
        :param status of eip condition
        if query by the status condition, must provides

        :type marker: string
        :param marker: The optional parameter marker specified in the original
         request to specify where in the results to begin listing.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number
         of list result to return. The default value is 1000.

    Return: list of eip model, for example:
        {
            "eipList": [
                {
                    "name":"eip-xxxxxxx-1",
                    "eip": "x.x.x.x",
                    "status":"binded",
                    "instanceType": "BCC",
                    "instanceId": "i-xxxxxxx",
                    "bandwidthInMbps": 5,
                    "paymentTiming":"Prepaid",
                    "billingMethod":"ByBandwidth",
                    "createTime":"2016-03-08T08:13:09Z",
                    "expireTime":"2016-04-08T08:13:09Z"
                },
                {
                    "name":"eip-xxxxxxx-1",
                    "eip": "x.x.x.x",
                    "status":"binded",
                    "instanceType": "BCC",
                    "instanceId": "i-xxxxxxx",
                    "bandwidthInMbps": 1,
                    "paymentTiming":"Postpaid",
                    "billingMethod":"ByTraffic",
                    "createTime":"2016-03-08T08:13:09Z",
                    "expireTime":null
                },
            ],
            "marker":"eip-xxxxxxx-1",
            "isTruncated": true,
            "nextMarker": "eip-DCB50387",
            "maxKeys": 2
        }

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = eip_client.list_eips(eip, instance_type, instance_id, status, marker, max_keys)
        eip_list  = res.eip_list
        return eip_list
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 创建EIPClient
    eip_client = EipClient(example_conf.config)
    # 获取所有EIP列表
    eip_list = test_list_eips(eip_client, None, None, None, None, None, None)
    print(eip_list)
   