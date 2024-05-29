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
Sample for rds parameter example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_parameter_manager as parameter_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_parameter.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = parameter_manager.RdsParameterManager(CONF.config)
    try:

        # 获取access_key
        access_key = rds_client.config.credentials.access_key_id
        # 短实例id
        instance_id = "rds-rWLm6n4e"

        # parameter_list
        LOG.debug('\n\n\nSample 1: parameter list\n\n\n')
        # 搜索参数关键字，可以为空，非必须传
        keyword = None
        # keyword = "wait_timeout"
        # 调用接口
        response = rds_client.parameter_list(instance_id, keyword)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify_config_parameter
        LOG.debug('\n\n\nSample 2: modify config parameter\n\n\n')
        # 参数生效方式：立即执行（immediate）、维护时间执行（timewindow）
        effective_time = rds_enum.EffectiveTime.IMMEDIATE
        # 参数名称
        parameter_name = "auto_increment_offset"
        # 参数值
        parameter_value = "2"
        # 修改版本号，从获取参数列表的返回结果项中的etag字段获取
        e_tag = "v3"
        # 建议参数生效方式：立即执行（immediate）、维护时间执行（timewindow）
        # 默认applyMethod参数值为immediate
        # 设置执行方式
        applyMethod = effective_time
        parameter_object_model = request_param.ParameterObject(parameter_name, parameter_value,
                                                               e_tag, applyMethod)
        # 修改参数列表
        ParameterList = [parameter_object_model.to_json()]
        # 调用接口
        response = rds_client.modify_config_parameter(instance_id, e_tag, effective_time,
                                                      ParameterList)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_modify_parameter_history_List
        LOG.debug('\n\n\nSample 3: query modify parameter history List\n\n\n')
        # 调用接口
        response = rds_client.query_modify_parameter_history_List(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_modify_parameter_history_List
        LOG.debug('\n\n\nSample 4: query modify parameter history List\n\n\n')
        # 调用接口
        response = rds_client.query_modify_parameter_history_List(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_parameter_template_detail
        LOG.debug('\n\n\nSample 5: query parameter template detail\n\n\n')
        # 模版id
        template_id = "503"
        # 调用接口
        response = rds_client.query_parameter_template_detail(template_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_parameter_template_list
        LOG.debug('\n\n\nSample 6: query parameter template list\n\n\n')
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 模板类型，支持user/system，不传默认为user。user：返回自定义参数列表；system：返回系统参数列表
        template_type = rds_enum.TemplateType.USER
        # 数据库引擎 支持MySQL (驼峰命名）
        # db_type = None
        db_type = rds_enum.DbType.MYSQL
        # 数据库版本 如：mysql(5.0, 5.6, 5.7, 8.0)等
        db_version = rds_enum.DBVersion.MYSQL_57
        # db_version = None
        # 调用接口
        response = rds_client.query_parameter_template_list(page_no, page_size, template_type,
                                                            db_type, db_version)
        # 日志输出
        LOG.debug('\n%s', response)

        # copy parameter template
        LOG.debug('\n\n\nSample 7: copy parameter template\n\n\n')
        # 模版名称
        name = "503_template_copy1"
        # 模版描述
        desc = ""
        # 模板id
        template_id = "503"
        # 调用接口
        response = rds_client.copy_parameter_template(template_id, name, desc)
        # 日志输出
        LOG.debug('\n%s', response)

        # parameter_template_apply_history
        LOG.debug('\n\n\nSample 8: parameter template apply history\n\n\n')
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 应用模版id
        template_id = "503"
        # 调用接口
        response = rds_client.parameter_template_apply_history(template_id, page_no, page_size)
        # 日志输出
        LOG.debug('\n%s', response)

        # create_parameter_template
        LOG.debug('\n\n\nSample 9: create parameter template\n\n\n')
        # 模版名称
        name = "503_template_copy1"
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
        response = rds_client.create_parameter_template(name, db_type, db_version, parameters,
                                                        desc)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify_parameter_template
        LOG.debug('\n\n\nSample 10: modify parameter template\n\n\n')
        # 修改参数对象
        paraTemplateUpdate = request_param.ParaTemplateUpdate("auto_increment_offset", "1", "2")
        # 修改参数列表
        update_list = [paraTemplateUpdate.to_json()]
        # 调用接口
        response = rds_client.modify_parameter_template("502", "502_test", update_list)
        # 日志输出
        LOG.debug('\n%s', response)

        # parameter_template_apply
        LOG.debug('\n\n\nSample 11: parameter template apply\n\n\n')
        # 应用模版id
        template_id = "502"
        # 操作执行方式，有两种取值：timewindow、immediate。其中timewindow表示在时间窗口内执行，immediate表示立即执行
        effective_time = rds_enum.EffectiveTime.IMMEDIATE
        # 是否进行切换重启。
        switchover = False
        # 短实例id列表
        instance_ids = [instance_id]
        # 模版列表
        apply_template = request_param.ApplyTemplate(effective_time, switchover, instance_ids)
        # 调用接口
        response = rds_client.parameter_template_apply(template_id, apply_template.to_json())
        # 日志输出
        LOG.debug('\n%s', response)

        # parameter_template_can_apply_instance_list
        LOG.debug('\n\n\nSample 12: parameter template can apply instance list\n\n\n')
        # 数据库引擎
        engine = rds_enum.DbType.MYSQL
        # 数据库引擎版本
        engine_version = rds_enum.DBVersion.MYSQL_57
        # 调用接口
        response = rds_client.parameter_template_can_apply_instance_list(engine, engine_version)
        # 日志输出
        LOG.debug('\n%s', response)

        # compare_parameter_template
        LOG.debug('\n\n\nSample 13: compare parameter template\n\n\n')
        # 模版id
        template_id = "498"
        # 调用接口
        response = rds_client.compare_parameter_template(template_id, instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_database_parameter
        LOG.debug('\n\n\nSample 14: query database parameter\n\n\n')
        # 调用接口
        response = rds_client.query_database_parameter(rds_enum.DbType.MYSQL,
                                                       rds_enum.DBVersion.MYSQL_57, "498")
        # 日志输出
        LOG.debug('\n%s', response)

        # delete_parameter_template
        LOG.debug('\n\n\nSample 15: delete parameter template\n\n\n')
        # 调用接口
        response = rds_client.delete_parameter_template("503")
        # 日志输出
        LOG.debug('\n%s', response)

        # parameter_template_apply_detail
        LOG.debug('\n\n\nSample 16: parameter template apply detail\n\n\n')
        # 应用模版id
        apply_id = "2862"
        # 调用接口
        response = rds_client.parameter_template_apply_detail(apply_id)
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
