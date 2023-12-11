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
Example fir eip client.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient

def test_optional_delete_eip(eip_client, eip, releaseToRecycle):
    """
    Delete an EIP with additional options.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient 

        :type eip: string
        :param eip: The EIP address to delete.
        
        :type release_to_recycle: bool
        :param release_to_recycle: flag to release EIP to recycle bin.

    Return: 
        None
    
    Raise:
        BceHttpClientError: http request failed
    """
    try:
        res = eip_client.optional_delete_eip(eip, releaseToRecycle)
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
    # 指定是否释放到回收站
    releaseToRecycle = False
    # 释放EIP
    test_optional_delete_eip(eip_client, eip, releaseToRecycle)