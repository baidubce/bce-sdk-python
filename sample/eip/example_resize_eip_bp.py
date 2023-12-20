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

def test_resize_eip_bp(eip_bp_client, id, new_bandwidth_in_mbps):
    """
    Resizing eip_bp.

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type id: string
        :param id: eip_bp's id to be resized.

        :type new_bandwidth_in_mbps: int
        :param new_bandwidth_in_mbps: Specify new bandwidth in Mbps for eip_bp.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """

    try:
        res = eip_bp_client.resize_eip_bp(id=id, new_bandwidth_in_mbps=new_bandwidth_in_mbps)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化eip_bp client
    eip_bp_client = EipBpClient(example_conf.config)
    # 指定eip_bp id
    id = "bw-xxxxxxxx"
    # 指定新带宽
    new_bandwidth_in_mbps = 30
    # 重设eip_bp带宽
    test_resize_eip_bp(eip_bp_client, id, new_bandwidth_in_mbps)