#!/usr/bin/env python
# coding=utf8

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
Unite test for rds recycler manager interface
"""

import sys
import unittest
from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds import rds_recycler_manager as recycler_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsRecyclerManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-5xmvRHEm'
        self.rds_client1 = recycler_manager.RdsRecyclerManager(config1)
        self.rds_client2 = recycler_manager.RdsRecyclerManager(config2)
        self.ACCESS_KEY = config1.credentials.access_key_id

    # 回收站列表
    def test_recycler_list(self):
        # 调用接口
        self.rds_client1.recycler_list()

    # 从回收站恢复实例（单个、批量均通过同一个接口）
    def test_recycler_recover(self):
        # 从回收站恢复的实例id，多个用英文逗号分隔开
        instance_ids = ["rds-dWRnnVn9", "rds-V9Crmhez"]
        # 调用接口
        self.rds_client1.recycler_recover(instance_ids)

    # 从回收站中释放单个实例
    def test_delete_recycler(self):
        # 从回收站释放单个实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.delete_recycler(instance_id)

    # 从回收站中释放批量实例
    def test_delete_recycler_batch(self):
        # 从回收站批量释放的实例id，多个用英文逗号分隔
        instance_ids = 'rds-6k24UUIR,rds-6k24UUIR'
        # 调用接口
        self.rds_client1.delete_recycler_batch(instance_ids)
