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

def test_get_eip_group(eip_group_client, id):
    """
    Get the detail information of specified EIP group.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of specified EIP group.

    Return:
        list of eipgroup model, for example:
        {
            "id": "eg-xxxxxxxx",
            "name": "test-eipgroup",
            "eips":[
                {
                    name:u"EIP1693302827987",
                    eip:u"100.88.0.217",
                    eip_id:u"ip-d9c57824",
                    status:u"available",
                    instance_type:None,
                    instance_id:None,
                    route_type:u"BGP",
                    bw_bandwidth_in_mbps:0,
                    domestic_bw_bandwidth_in_mbps:0,
                    bandwidth_in_mbps:20,
                    payment_timing:None,
                    billing_method:None,
                    create_time:u"2023-08-29T09:53:48Z",
                    expire_time:None,
                    share_group_id:u"eg-e9cc0d33",
                    eip_instance_type:u"shared",
                    tags:None,region:u"bj",
                    pool_type:u"public"}
            ],
            bandwidth_in_mbps:20,
            status:u"available",
            route_type:u"BGP",
            tags:None,
            region:"bj",
            bw_bandwidth_in_mbps:0,
            domestic_bw_bandwidth_in_mbps:0,
            payment_timing:"Postpaid",
            billing_method:"ByBandwidth",
            create_time:"2023-08-29T09:53:48Z",
            expire_time:None
        }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """

    try:
        res = eip_group_client.get_eip_group(id=id)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 创建EIPGroupClient
    eipgroup_client = EipGroupClient(example_conf.config)
    # eipgroupid
    id = "eg-xxxxxxxx"
    # 列出对应id的eipgroup信息
    eip_group_info = test_get_eip_group(eipgroup_client, id)