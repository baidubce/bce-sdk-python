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
Sample for rds database example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_database_manager as database_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_database.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = database_manager.RdsDataBaseManager(CONF.config)
    try:

        # 获取access_key
        access_key = rds_client.config.credentials.access_key_id
        # 实例id
        instance_id = "rds-Ow4u3xBM"

        # delete_database
        LOG.debug('\n\n\nSample 1: delete database\n\n\n')
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 调用接口
        response = rds_client.delete_database(instance_id, db_name)
        # 日志输出
        LOG.debug('\n%s', response)

        # create_database
        LOG.debug('\n\n\nSample 2: create_database\n\n\n')
        # MHYSQL字符集参考MYSQLCharSet 常量
        # SQLServer字符集使用SQLServerCharSet 常量
        # PG使用PostgresqlCharSet 常量
        character_set_name = rds_enum.MYSQLCharSet.UTF8
        # 数据库名称 由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 数据库备注
        remark = "test_db"
        # 账号名称
        account_name = "test_xxx"
        # 账号权限
        auth_type = rds_enum.AccountPrivileges.READ_WRITE
        accountPrivilege = request_param.AccountPrivilege(account_name, auth_type)
        accountPrivileges = [accountPrivilege.to_json()]
        # ===== 下面参数是pg参数必填======
        # PostgreSQL数据库必填参数，其他数据库非必填此参数(非必填设置为None）
        # characterSetName参数为：utf-8,此参数为:zh_CN.utf-8
        # characterSetNam参数为：LATIN1，此参数为:en_US
        # characterSetNam参数为：SQL_ASCII，此参数为:C
        collate = None
        c_type = None
        # 账号所属
        owner = account_name
        # 创建createDataBase对象
        createDataBase = request_param.CreateDataBase(character_set_name, db_name, remark,
                                                      accountPrivileges, collate, c_type,
                                                      owner)
        # 调用接口
        response = rds_client.create_database(instance_id, createDataBase.to_json())
        # 日志输出
        LOG.debug('\n%s', response)

        # query_database_list
        LOG.debug('\n\n\nSample 3: query database list\n\n\n')
        # 调用接口
        response = rds_client.query_database_list(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # update_database_port
        LOG.debug('\n\n\nSample 4: update database port\n\n\n')
        # 数据库端口（sqlserver、postgresql数据库端口不支持修改）
        db_port = 3306
        # 调用接口
        response = rds_client.update_database_port(instance_id, db_port)
        # 日志输出
        LOG.debug('\n%s', response)

        # update_database_remark
        LOG.debug('\n\n\nSample 5: update database remark\n\n\n')
        # postgresql 不支持修改备注(没有此功能）
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 数据库备注
        remark = "test_db_remark"
        # 调用接口
        response = rds_client.update_database_remark(instance_id, db_name, remark)
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
