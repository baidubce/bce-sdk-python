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

def test_list_recycle_eip(eip_client, eip, name, marker, max_keys):
    """
    List all EIP in the recycle bin with the specific parameters.

    Args:
        :type eip_client: EipClient
        :param eip_client: EIPClient

        :type eip: string
        :param eip: eip address condition

        :type name: string
        :param name: eip name condition

        :type marker: string
        :param marker: The optional parameter marker specified in the original
         request to specify where in the results to begin listing.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number
         of list result to return. The default value is 1000.

    Return: list of eip model, for example:
            {
                "eip_list": [
                    {
                        "name":"eip-xxxxxxx-1",
                        "eip": "x.x.x.x",
                        "eip_id":"ip-xxxxxxxx",
                        "status": "paused",
                        "route_type": "BGP",
                        "bandwidth_in_mbps": 5,
                        "payment_timing":"Prepaid",
                        "billing_method":"ByBandwidth",
                        "recycle_time":"2016-03-08T08:13:09Z",
                        "scheduled_delete_time":"2016-04-08T08:13:09Z"
                    },
                    {
                        "name":"eip-xxxxxxx-2",
                        "eip": "x.x.x.x",
                        "eip_id":"ip-xxxxxxxx",
                        "status": "paused",
                        "route_type": "BGP",
                        "bandwidth_in_mbps": 10,
                        "payment_timing":"Postpaid",
                        "billing_method":"ByBandwidth",
                        "recycle_time":"2016-03-08T08:13:09Z",
                        "scheduled_delete_time":"2016-04-08T08:13:09Z"
                    },
                ],
                "marker":"ip-xxxxxxxx",
                "is_truncated": true,
                "max_keys": 1000
            }
    
    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = eip_client.list_eip_recycle(eip, name, marker, max_keys)
        eip_list = res.eip_list
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
    eip_list = test_list_recycle_eip(eip_client, None, None, None, None)
    print(eip_list)