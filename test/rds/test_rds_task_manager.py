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
Unit test for rds task manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds import rds_task_manager as task_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsTaskManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = task_manager.RdsTaskManager(config1)
        self.rds_client2 = task_manager.RdsTaskManager(config2)

    # 查询任务列表
    def test_instance_task(self):
        # 调用接口
        self.rds_client1.task_instance()
