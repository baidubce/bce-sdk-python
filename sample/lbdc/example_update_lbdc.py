# -*- coding: utf-8 -*-
# !/usr/bin/env python

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
Samples for lbdc client.
"""

import lbdc_sample_conf as sample_conf
from baidubce.services.lbdc.lbdc_client import LbdcClient
from baidubce import exception


def test_update_lbdc(lbdc_client, lbdc_id, lbdc_name, description):
    """
    Update the lbdc cluster with specified lbdc_id, lbdc_name and description

    Args:
        :type lbdc_client: LbdcClient
        :param lbdc_client: lbdc sdk client

        :type lbdc_id: str
        :param lbdc_type: id of lbdc to be update

        :type lbdc_name: str
        :param lbdc_name: name of lbdc to be created

        :type description: str
        :param description: description of the lbdc

    Return:
        None

    Raise:
        BceHttpClientError: http request error
    """
    try:
        response = lbdc_client.update_lbdc(lbdc_id=lbdc_id, name=lbdc_name, desc=description)
        print(response)
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None


if __name__ == '__main__':
    # 初始化LbdcClient
    lbdc_client = LbdcClient(sample_conf.config)
    # lbdc的集群ID
    lbdc_id = b'lbdc-xxx'
    # lbdc的集群名称
    lbdc_name = b'test-lbdc-new'
    # lbdc的集群描述
    description = b'this is a new test lbdc'
    # 更新lbdc集群
    test_update_lbdc(lbdc_client, lbdc_id, lbdc_name, description)
