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
from baidubce.services.lbdc import model
from baidubce import exception


def test_create_lbdc(lbdc_client, lbdc_name, lbdc_type, ccu_count, billing):
    """
    Create the lbdc cluster with specified name, type, ccu_count and billing

    Args:
        :type lbdc_client: LbdcClient
        :param lbdc_client: lbdc sdk client

        :type lbdc_name: str
        :param lbdc_name: name of lbdc to be created

        :type lbdc_type: str
        :param lbdc_type: type of lbdc to be created(4Layer 7Layer et.)

        :type ccu_count: int
        :param ccu_count: number of cluster capacity unit

        :type billing: Billing
        :param billing: the endpoint creation order configuration

    Return:
        None

    Raise:
        BceHttpClientError: http request error
    """
    try:
        response = lbdc_client.create_lbdc(name=lbdc_name, type=lbdc_type, ccu_count=ccu_count, billing=billing)
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
    # 初始化Billing
    billing = model.Billing(payment_timing=b'Prepaid')
    # lbdc的集群名称
    lbdc_name = b'test-lbdc'
    # lbdc的集群类型, 4/7层
    lbdc_type = b'7Layer'
    # lbdc的集群性能容量单位CCU数（Cluster Capacity Unit）
    ccu_count = 1
    # 创建lbdc集群
    test_create_lbdc(lbdc_client, lbdc_name, lbdc_type, ccu_count, billing)
