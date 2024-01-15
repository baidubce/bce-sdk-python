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
Unit test for rds database manager
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_database_manager as database_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsDataBaseManager(unittest.TestCase):
    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = database_manager.RdsDataBaseManager(config1)
        self.rds_client2 = database_manager.RdsDataBaseManager(config2)

    # 创建数据库
    def test_create_database(self):
        # MHYSQL字符集参考MYSQLCharSet 常量
        # SQLServer字符集使用SQLServerCharSet 常量
        # PG使用PostgresqlCharSet 常量
        character_set_name = rds_enum.PostgresqlCharSet.UTF8
        # 数据库名称 由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 数据库备注
        remark = "123"
        # 账号名称
        account_name = "test_xxx"
        # 账号权限
        auth_type = rds_enum.AccountPrivileges.READ_WRITE
        accountPrivilege = request_param.AccountPrivilege(account_name, auth_type)
        accountPrivileges = [accountPrivilege.to_json()]
        # ===== 下面参数是pg参数必填======
        # PostgreSQL数据库必填参数，其他数据库非必填此参数(非必填设置为None）
        #
        # characterSetName参数为：utf-8,此参数为:zh_CN.utf-8
        #
        # characterSetNam参数为：LATIN1，此参数为:en_US
        #
        # characterSetNam参数为：SQL_ASCII，此参数为:C

        collate = rds_enum.PostgresqlCTypeCharSet.ZH_CN_UTF8
        c_type = rds_enum.PostgresqlCTypeCharSet.ZH_CN_UTF8
        # 账号所属
        owner = account_name
        # 创建createDataBase对象
        createDataBase = request_param.CreateDataBase(character_set_name, db_name, remark,
                                                      accountPrivileges, collate, c_type,
                                                      owner)
        # 调用接口
        self.rds_client1.create_database(self.instance_id, createDataBase.to_json())

    # 获取数据库列表
    def test_query_database_list(self):
        # 调用接口
        self.rds_client1.query_database_list(self.instance_id)

    # 修改描述信息
    def test_update_database_remark(self):
        # postgresql 不支持修改备注
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 数据库备注
        remark = "123"
        # 调用接口
        self.rds_client1.update_database_remark(self.instance_id, db_name, remark)

    # 修改数据库端口
    def test_update_database_port(self):
        # 数据库端口（sqlserver、postgresql数据库端口不支持修改）
        db_port = 3306
        # 调用接口
        self.rds_client1.update_database_port(self.instance_id, db_port)

    # 删除数据库
    def test_delete_database(self):
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 调用接口
        self.rds_client1.delete_database(self.instance_id, db_name)
