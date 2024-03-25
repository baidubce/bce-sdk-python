#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
Unit test for rds security manager interface.
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds import rds_security_manager as security_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsSecurityManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = security_manager.RdsSecurityManager(config1)
        self.rds_client2 = security_manager.RdsSecurityManager(config2)
        self.ACCESS_KEY = config1.credentials.access_key_id

    # 查询白名单列表
    def test_whit_list(self):
        # 调用接口
        self.rds_client1.whit_list(self.instance_id)

    # 更新白名单
    def test_update_whit_list(self):
        # 创建白名单
        security_ips = ['127.0.0.1']
        # 修改版本号, 这个参数值是从查询白名单的返回头域字段x-bce-if-match获取
        # 或者从返回结果的etag字段获取
        e_tag = "v1"
        # 调用接口
        self.rds_client1.update_whit_list(self.instance_id, security_ips, e_tag)

    # 设置SSL状态
    def test_set_ssl_status(self):
        # 实例id
        instance_id = self.instance_id
        # 公网状态
        status = False
        # 调用接口
        self.rds_client1.set_ssl_status(instance_id, status)

    # 获取SSL加密信息
    def test_obtain_ssl_encrypted_info(self):
        #  实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.obtain_ssl_encrypted_info(instance_id)

    # 获取ca证书
    def test_obtain_ssl_ca(self):
        # 调用接口
        self.rds_client2.obtain_ssl_ca()
