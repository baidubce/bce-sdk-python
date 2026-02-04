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
Example for updating EIP delete protection.
"""

import example_conf
from baidubce import exception
from baidubce.services.eip.eip_client import EipClient

def test_update_eip_delete_protect(eip_client, eip, delete_protect):
    """
    Update EIP delete protection setting.

    Args:
        :type eip_client: EipClient
        :param eip_client: EipClient

        :type eip: string
        :param eip: eip address to update

        :type delete_protect: bool
        :param delete_protect: enable or disable delete protection

    Return:
        BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = eip_client.update_eip_delete_protect(eip, delete_protect)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None

if __name__ == '__main__':
    # 初始化EipClient
    eip_client = EipClient(example_conf.config)

    # EIP地址
    eip = "x.x.x.x"
    test_update_eip_delete_protect(eip_client, eip, delete_protect=False)