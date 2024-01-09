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
Unit test for rds parameter manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_parameter_manager as parameter_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsParameterManager(unittest.TestCase):
    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = parameter_manager.RdsParameterManager(config1)
        self.rds_client2 = parameter_manager.RdsParameterManager(config2)

    # 获取参数列表
    def test_parameter_list(self):
        # 搜索参数关键字，可以为空，非必须传
        keyword = None
        # keyword = "wait_timeout"
        # 调用接口
        self.rds_client1.parameter_list(self.instance_id, keyword)

    # 修改配置参数
    def test_modify_config_parameter(self):
        effective_time = rds_enum.EffectiveTime.IMMEDIATE
        # 参数名称
        parameter_name = "wait_timeout"
        # 参数值
        parameter_value = "86300"
        # 修改版本号，从获取参数列表的返回结果项中的etag字段获取
        e_tag = "v6"
        # 建议参数生效方式：立即执行（immediate）、维护时间执行（timewindow）。
        # 默认applyMethod参数值为immediate
        # 设置执行方式
        applyMethod = effective_time
        parameter_object_model = request_param.ParameterObject(parameter_name,parameter_value,
                                                               e_tag, applyMethod)
        # 修改参数列表
        ParameterList = [parameter_object_model.to_json()]
        # 调用接口
        self.rds_client1.modify_config_parameter(self.instance_id, e_tag, effective_time,
                                                 ParameterList)

    # 查询修改参数历史
    def test_query_modify_parameter_history_list(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.query_modify_parameter_history_List(instance_id)

    # 查询参数模板列表
    def test_query_parameter_template_list(self):
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 模板类型，支持user/system，不传默认为user。user：返回自定义参数列表；
        # system：返回系统参数列表
        template_type = rds_enum.TemplateType.USER
        # 数据库引擎 支持MySQL (驼峰命名）
        # db_type = None
        db_type = rds_enum.DbType.MYSQL
        # 数据库版本 如：mysql(5.0, 5.6, 5.7, 8.0)等
        db_version = rds_enum.DBVersion.MYSQL_57
        # db_version = None
        # 调用接口
        self.rds_client1.query_parameter_template_list(page_no, page_size, template_type, db_type,
                                                       db_version)

    # 查询参数模板详情
    def test_query_parameter_detail(self):
        # 模版id
        template_id = "503"
        # 调用接口
        self.rds_client1.query_parameter_template_detail(template_id)

    # 复制参数模版
    def test_copy_parameter_template(self):
        # 模版名称
        name = "503_template_copy"
        # 模版描述
        desc = ""
        # 模板id
        template_id = "503"
        # 调用接口
        self.rds_client1.copy_parameter_template(template_id, name, desc)

    # 参数模板应用历史
    def test_parameter_template_apply_history(self):
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 应用模版id
        template_id = "364"
        # 调用接口
        self.rds_client1.parameter_template_apply_history(template_id, page_no, page_size)

    # 参数模板应用详情
    def test_parameter_template_apply_detail(self):
        # 应用模版id
        apply_id = "2235"
        # 调用接口
        self.rds_client1.parameter_template_apply_detail(apply_id)

    # 创建参数模板
    def test_create_parameter_template(self):
        # 模版名称
        name = "param_test_zc"
        # 数据类型 Mysql
        db_type = rds_enum.DbType.MYSQL
        # 数据库版本 5.5、5.6、5.7、8.0
        db_version = rds_enum.DBVersion.MYSQL_57
        # 模版描述
        desc = None
        # 创建参数值
        paraTemplates = request_param.ParaTemplates("auto_increment_offset", "1")
        # 模版参数集合对象
        parameters = [paraTemplates.to_json()]
        # 调用接口
        self.rds_client1.create_parameter_template(name, db_type, db_version, parameters, desc)

    # 删参数模版
    def test_delete_parameter_template(self):
        # 模版id
        template_id = "363"
        # 调用接口
        self.rds_client1.delete_parameter_template(template_id)

    # 修改参数模版
    def test_modify_parameter_template(self):
        # 模版id
        template_id = "364"
        # 修改的模版名称
        name = "364_test"
        # 修改参数对象
        paraTemplateUpdate = request_param.ParaTemplateUpdate("auto_increment_offset", "1", "2")
        # 修改参数列表
        update_list = [paraTemplateUpdate.to_json()]
        # 调用接口
        self.rds_client1.modify_parameter_template(template_id, name, update_list)

    # 应用模版
    def test_parameter_template_apply(self):
        # 应用模版id
        template_id = "364"
        # 操作执行方式，有两种取值：timewindow、immediate。
        # 其中timewindow表示在时间窗口内执行，immediate表示立即执行
        effective_time = rds_enum.EffectiveTime.IMMEDIATE
        # 是否进行切换重启。
        switchover = False
        # 短实例id列表
        instance_ids = [self.instance_id]
        # 模版列表
        apply_template = request_param.ApplyTemplate(effective_time, switchover, instance_ids)
        # 调用接口
        self.rds_client1.parameter_template_apply(template_id, apply_template.to_json())

    # 查询可应用参数模版列表
    def test_parameter_template_can_apply_instance_list(self):
        # 数据库引擎
        engine = rds_enum.DbType.MYSQL
        # 数据库引擎版本
        engine_version = rds_enum.DBVersion.MYSQL_57
        # 调用接口
        self.rds_client1.parameter_template_can_apply_instance_list(engine, engine_version)

    # 模版比较
    def test_compare_parameter_template(self):
        # 模版id
        template_id = "364"
        # 短实例id
        instance_id = self.instance_id
        # 接口调用
        self.rds_client1.compare_parameter_template(template_id, instance_id)

    # 查询数据库参数
    def test_query_database_parameter(self):
        # 数据库类型
        db_type = rds_enum.DbType.MYSQL
        # 数据库版本
        db_version = rds_enum.DBVersion.MYSQL_57
        # 模版id
        template_id = "364"
        # 调用接口
        self.rds_client1.query_database_parameter(db_type, db_version, template_id)
