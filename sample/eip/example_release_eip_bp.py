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

def test_release_eip_bp(eip_bp_client, id):
    """
    Release the eip_bp (delete operation).

    Args:
        :type eip_bp_client: EipBpClient
        :param eip_bp_client: EipBpClient

        :type id: string
        :param id: eip_bp's id to be released.

    Return:
        None

    Raises:
        BceHttpClientError: If the HTTP request fails.
    """
    try:
        res = eip_bp_client.release_eip_bp(id=id)
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
    # 被释放的eip_bp id
    id = "bw-xxxxxxxx"
    # 释放eip_bp
    test_release_eip_bp(eip_bp_client, id=id)