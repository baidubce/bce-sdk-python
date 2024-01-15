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
Unit test for  rds users manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_users_manager as users_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsUsersManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = users_manager.RdsUsersManager(config1)
        self.rds_client2 = users_manager.RdsUsersManager(config2)
        self.access_key = config1.credentials.access_key_id

    # 创建账号
    def test_create_account(self):
        # 实例id
        instance_id = self.instance_id
        # 账号名称 [a-z][a-z0-9_]{0,14}[a-z0-9]
        account_name = 'test_xxxx'
        # 密码，秘文，md5加密后字符串，长度为32位
        password = 'xxxxxxxxx'
        # 账号类型 Common为普通用户，Super为超级用户
        account_type = rds_enum.AccountType.COMMON
        # 数据库权限
        databasePrivilege = request_param.DatabasePrivilege("test_db", rds_enum.AccountPrivileges.READ_WRITE)
        database_privileges_arrays = [
            databasePrivilege.to_json()
        ]
        # 数据库描述
        desc = "test_db"
        # 数据库类型
        type = rds_enum.AccountOwnershipInstance.ONLY_MASTER
        # 调用接口
        self.rds_client1.create_account(self.access_key, instance_id, account_name, password, account_type,
                                        database_privileges_arrays, desc, type)

    # 查询账号列表
    def test_query_account(self):
        # 实例id
        instance_id = self.instance_id
        # 接口调用
        self.rds_client1.query_account(instance_id)

    # 查询账号详情
    def test_query_account_detail(self):
        # 实例id
        instance_id = self.instance_id
        # 账号名称
        account_name = 'test_xxxx'
        # 接口调用
        self.rds_client1.query_account_detail(instance_id, account_name)

    # 修改密码
    def test_modify_account_password(self):
        # 实例id
        instance_id = self.instance_id
        # 账号名称
        account_name = 'test_xxxx'
        # 密码，秘文，md5加密后字符串，长度为32位
        password = 'xxxxxxx'
        # 调用接口
        self.rds_client1.modify_account_password(self.access_key, instance_id, account_name, password)

    # 修改账号权限
    def test_modify_account_privileges(self):
        # 实例id
        instance_id = self.instance_id
        # 账号名称
        account_name = 'test_xxxx'
        # 修改版本号,从查询账号详情返回结果的查询账号详情的ETag字段获取
        e_tag = 'v1'
        # 数据库名称
        db_name = 'test_tb'
        # 数据库权限
        database_privilege = request_param.DatabasePrivilege(db_name, rds_enum.AccountPrivileges.READ_ONLY)
        privileges_arrays = [
            database_privilege.to_json()
        ]
        # 调用接口
        self.rds_client1.modify_account_privileges(self.access_key, e_tag, instance_id, account_name,
                                                   privileges_arrays)

    # 修改账号备注
    def test_modify_account_remark(self):
        # postgresql要求账户没有绑定数据库，是独立账户
        # 实例id
        instance_id = self.instance_id
        # 账号名称
        account_name = 'test_xxxx'
        # 修改账号备注
        remark = '账号test'
        # 调用接口
        self.rds_client1.modify_account_remark(instance_id, account_name, remark)

    # 删除账号
    def test_delete_account(self):
        #  postgresql要求账户没有绑定数据库，是独立账户
        # 实例id
        instance_id = self.instance_id
        # 账号详情
        account_name = 'test_xxxx'
        # 调用接口
        self.rds_client1.delete_account(instance_id, account_name)
