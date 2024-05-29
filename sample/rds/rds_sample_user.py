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
Sample for rds user example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_users_manager as users_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_user.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = users_manager.RdsUsersManager(CONF.config)
    try:

        # 获取access_key
        access_key = rds_client.config.credentials.access_key_id
        # 实例id
        instance_id = "rds-LnK2kTHr"

        # delete_account
        LOG.debug('\n\n\nSample 1: delete account\n\n\n')
        # postgresql要求账户没有绑定数据库，是独立账户
        # 账号名称
        account_name = 'test_name1'
        # 调用接口
        response = rds_client.delete_account(instance_id, account_name)
        # 日志输出
        LOG.debug('\n%s', response)

        # create_account
        LOG.debug('\n\n\nSample 2: create account\n\n\n')
        # 账号名称 [a-z][a-z0-9_]{0,14}[a-z0-9]
        account_name = 'test_xxxx'
        # 密码，秘文，md5加密后字符串，长度为32位
        password = 'xxxxxxxx'
        # 账号类型 Common为普通用户，Super为超级用户
        account_type = rds_enum.AccountType.COMMON
        # 数据库权限
        databasePrivilege = request_param.DatabasePrivilege("test_db", rds_enum.AccountPrivileges.READ_ONLY)
        database_privileges_arrays = [
            databasePrivilege.to_json()
        ]
        # 数据库描述
        desc = "test_db"
        # 数据库类型
        type = rds_enum.AccountOwnershipInstance.ONLY_MASTER
        # 调用接口
        response = rds_client.create_account(access_key, instance_id, account_name, password, account_type,
                                             database_privileges_arrays, desc, type)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_account
        LOG.debug('\n\n\nSample 3: query account\n\n\n')
        # 调用接口
        response = rds_client.query_account(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_account_detail
        LOG.debug('\n\n\nSample 4: query account detail\n\n\n')
        # 账号名称
        account_name = 'test_xxxx'
        # 调用接口
        response = rds_client.query_account_detail(instance_id, account_name)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify_account_password
        LOG.debug('\n\n\nSample 5: modify account password\n\n\n')
        # 账号名称
        account_name = 'test_xxxx'
        # 密码，秘文，md5加密后字符串，长度为32位
        password = 'xxxxxxxxx'
        # 调用接口
        response = rds_client.modify_account_password(access_key, instance_id, account_name, password)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify account remark
        LOG.debug('\n\n\nSample 6: modify account remark\n\n\n')
        # postgresql要求账户没有绑定数据库，是独立账户
        # 账号详情
        account_name = 'test_xxxx'
        # 修改账号备注
        remark = '账号test'
        # 调用接口
        response = rds_client.modify_account_remark(instance_id, account_name, remark)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify account privileges
        LOG.debug('\n\n\nSample 7: modify account privileges\n\n\n')
        # 账号详情
        account_name = 'test_xxxx'
        # 修改版本号,从查询账号详情返回结果的查询账号详情的ETag字段获取
        e_tag = 'v1'
        # 数据库名称
        db_name = 'test_db'
        # 数据库权限
        database_privilege = request_param.DatabasePrivilege(db_name, rds_enum.AccountPrivileges.READ_ONLY)
        privileges_arrays = [
            database_privilege.to_json()
        ]
        # 调用接口
        response = rds_client.modify_account_privileges(
            access_key, e_tag, instance_id, account_name, privileges_arrays)
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
