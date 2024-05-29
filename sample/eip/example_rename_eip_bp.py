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

def test_rename_eip_bp(eip_bp_client, id, name):
    """
    Update eip_bp's name.

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type id: string
        :param id: eip_bp's id.

        :type name: string
        :param name: The new name for the eip_bp.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_bp_client.rename_eip_bp(id=id, name=name)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None
    
if __name__ == '__main__':
    # 初始化EipBpClient
    eip_bp_client = EipBpClient(example_conf.config)
    # 被更新名称的eip_bp id
    id = "bw-xxxxxxxx"
    # 新名称
    name = "newname"
    # 更新eip_bp的名称
    test_rename_eip_bp(eip_bp_client, id=id, name=name)
