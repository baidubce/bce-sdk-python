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

def test_delete_recycle_eip(eip_client, eip):
    """
    Delete an EIP from the recycle bin.

    Args:
        :type eip_client: EipClient
        :param eip_client: EIPClient

        :type eip: string
        :param eip: eip address to be delete from recycle bin.

    Return: 
        None
    Raise:
        BceHttpClientError: http request failed
    """
    try:
        res = eip_client.delete_recycle_eip(eip)
        print(res)
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 创建EIPClient
    eip_client = EipClient(example_conf.config)
    # 指定EIP
    eip = "x.x.x.x"
    # 释放EIP
    test_delete_recycle_eip(eip_client, eip)