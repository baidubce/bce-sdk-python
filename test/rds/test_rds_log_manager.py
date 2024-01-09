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
Unit test for rds log manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds import rds_log_manager as log_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsLogManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = log_manager.RdsLogManager(config1)
        self.rds_client2 = log_manager.RdsLogManager(config2)

    # 慢日志详情
    def test_slow_log_detail(self):
        # 开始时间
        start_time = "2023-12-10T09:50:04Z"
        # 结束时间
        end_time = "2023-12-10T09:59:04Z"
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 数据库名称，数组
        db_name = []
        # IP地址，数组
        host_ip = ["127.0.0.1"]
        # 用户名，数组
        user_name = ["test_name1"]
        # SQL语句 ，模糊条件
        sql = "select"
        # 调用接口
        self.rds_client1.slow_log_detail(self.instance_id, start_time, end_time, page_no,
                                         page_size, db_name, host_ip, user_name, sql)

    # 错日志详情
    def test_error_log_detail(self):
        # 开始时间
        start_time = "2023-12-13T06:00:00Z"
        # 结束时间
        end_time = "2023-12-13T18:00:00Z"
        # 当前页码
        page_no = 3
        # 每页条数
        page_size = 10
        # 搜索关键词 ，模糊条件
        key_word = "test_name1"
        # 调用接口
        self.rds_client1.error_log_detail(self.instance_id, start_time, end_time,
                                          page_no, page_size, key_word)

    # 慢日志列表
    def test_slow_log_list(self):
        # 慢日志时间点
        datetime = "2023-12-10T19:48:05Z"
        # 调用接口
        self.rds_client1.slow_log_list(self.instance_id, datetime)

    # 慢日志下载详情
    def test_slow_log_download_detail(self):
        # 慢日志id
        log_id = "slowlog.202312130005"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = 1800
        # 调用接口
        self.rds_client1.slow_log_download_detail(self.instance_id, log_id,
                                                  download_valid_time_in_sec)

    # 错误日志列表
    def test_error_log_list(self):
        # 慢日志时间点
        datetime = "2023-12-13T15:50:12Z"
        # 调用接口
        self.rds_client1.error_log_list(self.instance_id, datetime)

    # 错误日志下载详情
    def test_error_log_download_detail(self):
        # 慢日志id
        log_id = "errorlog.202312131549"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = "1800"
        # 调用接口
        self.rds_client1.error_log_download_detail(self.instance_id, log_id,
                                                   download_valid_time_in_sec)
