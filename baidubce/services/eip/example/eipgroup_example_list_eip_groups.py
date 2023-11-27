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

import eip_example_conf
from baidubce import exception
from baidubce.services.eip.eip_group_client import EipGroupClient

def test_list_eip_groups(eip_group_client, id, name, status, marker, max_keys):
    """
    Return a list of EIP groups, according to the ID, name or status of EIP group. 
    If not specified, returns a full list of EIP groups in VPC.

    Args:
        :type eip_group_client: EipGroupClient
        :param eip_group_client: EipGroupClient

        :type id: string
        :param id: The id of specified EIP group.

        :type name: string
        :param name: The name of specified EIP group.

        :type status: string
        :param status: The status of specified EIP group.

        :type marker: string
        :param marker: The optional parameter marker specified in the original request 
                    to specify where in the results to begin listing. Together with 
                    the marker, specifies the list result which listing should begin. 
                    If the marker is not specified, the list result will listing from 
                    the first one.

        :type max_keys: int
        :param max_keys: The optional parameter to specifies the max number of list 
                        result to return. The default value is 1000.

    Return: list of eipgroup model, for example:
    {
        "eipgroups": [
            {
                id:"eg-xxxxxxxx",
                name:"test",
                eips:[
                    {
                        name:"EIPxxxxxxxxxxxxx",
                        eip:"x.x.x.x",
                        eip_id:"ip-xxxxxxxx",
                        status:"available",
                        instance_type:None,
                        instance_id:None,
                        route_type:"BGP",
                        bw_bandwidth_in_mbps:0,
                        domestic_bw_bandwidth_in_mbps:0,
                        bandwidth_in_mbps:20,
                        payment_timing:None,
                        billing_method:None,
                        create_time:"2023-08-29T09:53:48Z",
                        expire_time:None,
                        share_group_id:"eg-xxxxxxxx",
                        eip_instance_type:u"shared",
                        tags:None,
                        region:"bj",
                        pool_type:"public"
                    }
                ],
                bandwidth_in_mbps:20,
                status:"available",
                route_type:"BGP",
                tags:None,
                region:"bj",
                bw_bandwidth_in_mbps:0,
                domestic_bw_bandwidth_in_mbps:0,
                payment_timing:"Postpaid",
                billing_method:"ByBandwidth",
                create_time:"2023-08-29T09:53:48Z",
                expire_time:None
            }
        ]
    }

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """

    try:
        res = eip_group_client.list_eip_groups(id=id, name=name, status=status,
                                               marker=marker, max_keys=max_keys)
        eip_group_list = res.eipgroups
        return eip_group_list
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 创建EIPGroupClient
    eipgroup_client = EipGroupClient(eip_example_conf.config)
    # 列出所有eipgroup
    eip_group_list = test_list_eip_groups(eipgroup_client, None, None, None, None, None)
    # eipgroupid
    id = "eg-xxxxxxxx"
    # 列出指定id的eipgroup
    eip_group_list = test_list_eip_groups(eipgroup_client, id, None, None, None, None)  