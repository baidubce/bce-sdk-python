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

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_bp_client import EipBpClient

def test_list_eip_bps(eip_bp_client, id=None, name=None, bind_type=None,
                     marker=None, max_keys=1000):
    """
    Get a list of eip_bp owned by the authenticated user and specified conditions. 
    This interface can also be used to get a single eip_bp function through the eip_bp condition.

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type id: string
        :param id: eip_bp's id condition.

        :type name: string
        :param name: eip_bp's name condition.

        :type bind_type: string
        :param bind_type: eip_bp's bind_type condition, 'eip' or 'eipgroup'.

        :type marker: string
        :param marker: The optional parameter marker specified in the original request 
                    to specify where in the results to begin listing.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number of list 
                        result to return. The default value is 1000.

    Return:
        :type: dict
        A dictionary containing a list of eip_bp model, for example:
            {
                "marker": "bw-5fb3ce39",
                "maxKeys": 1000,
                "nextMarker": null,
                "bpList": [
                    {
                        "autoReleaseTime": "2020-05-30T06:46:44Z",
                        "name": "EIP_BP1588821183401",
                        "instanceId": "ip-9340430e",
                        "createTime": "2020-05-07T03:13:03Z",
                        "id": "bw-5fb3ce39",
                        "eips": ["100.88.9.120"],
                        "bandwidthInMbps": 2,
                        "bindType": "eip"
                    }
                    // ... 更多 eip_bp 条目
                ],
                "isTruncated": false
            }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_bp_client.list_eip_bps(id=id, name=name, bind_type=bind_type,
                                         marker=marker, max_keys=max_keys)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化eip_bp client
    eip_bp_client = EipBpClient(example_conf.config)
    # 获取eip_bp详情
    eip_bp_list = test_list_eip_bps(eip_bp_client, id=None, name=None, bind_type=None,
                     marker=None, max_keys=1000)
    print(eip_bp_list)