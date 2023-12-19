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
Example for eip bp client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_bp_client import EipBpClient

def test_create_eip_bp(eip_bp_client, eip, eip_group_Id, bandwidth_in_mbps, name=None, autoReleaseTime=None):
    """
    Create an eip_bp with the specified options.

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type eip: string
        :param eip: The EIP address that the eip_bp will attach. Only one of 
                    "eip" and "eip_group_Id" parameters will take effect.

        :type eip_group_Id: string
        :param eip_group_Id: The eipGroupId that the eip_bp will attach. Only one of 
                            "eip" and "eip_group_Id" parameters will take effect.

        :type bandwidth_in_mbps: int
        :param bandwidth_in_mbps: The bandwidth of eip_bp in Mbps.

        :type name: string
        :param name: The name of eipbp. This is an optional parameter.

        :type auto_release_time: string
        :param auto_release_time: The auto release time of eipbp in UTC format 
                                (like yyyy:mm:ddThh:mm:ssZ). This is an optional 
                                parameter.

    Return:
        :type: dict
        A dictionary containing the created eip_bp id, for example, {"id": "bw-xxxxxxxx"}.

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_bp_client.create_eip_bp(eip=eip, eip_group_Id=eip_group_Id, bandwidth_in_mbps = bandwidth_in_mbps,
                                           name=name, autoReleaseTime=autoReleaseTime)
        eip_bp_id = res.id
        return eip_bp_id
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化eip_group_client
    eip_bp_client = EipBpClient(example_conf.config)
    # 初始化eip
    eip = "ip-xxxxxxxx"
    # 初始化移入eip group id
    eip_group_Id = "eg-xxxxxxxx"
    # 初始化带宽
    bandwidth_in_mbps = 10
    # 初始化名称
    name_eip = "test_eip_bp_eip"
    name_eipgroup = "test_eip_bp_eipgroup"
    # 初始化自动释放时间
    autoReleaseTime = "2023-12-30T16:45:00Z"
    # 创建绑定EIP的eip_bp
    eip_bp_id_by_eip = test_create_eip_bp(eip_bp_client=eip_bp_client, eip=eip, eip_group_Id=None, 
                       bandwidth_in_mbps=bandwidth_in_mbps, name=name_eip, autoReleaseTime=autoReleaseTime)
    # 创建绑定eip group的eip_bp
    eip_bp_id_by_eipgroup = test_create_eip_bp(eip_bp_client=eip_bp_client, eip=None, eip_group_Id=eip_group_Id, 
                       bandwidth_in_mbps=bandwidth_in_mbps, name=name_eipgroup, autoReleaseTime=autoReleaseTime)