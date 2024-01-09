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
Sample for rds log example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds import rds_log_manager as log_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_logs.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = log_manager.RdsLogManager(CONF.config)
    try:

        # 获取access_key
        access_key = rds_client.config.credentials.access_key_id
        # 实例id
        instance_id = "rds-rWLm6n4e"

        # slow_logs_detail
        LOG.debug('\n\n\nSample 1: slow logs detail\n\n\n')
        # 开始时间  格式：2017-06-08T13:45:00Z
        start_time = "2023-12-10T09:50:04Z"
        # 结束时间  格式：2017-06-08T13:45:00Z
        end_time = "2023-12-10T09:59:04Z"
        # 当前页数
        page_no = 1
        # 每页大小
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
        response = rds_client.slow_log_detail(instance_id, start_time, end_time, page_no,
                                              page_size, db_name, host_ip, user_name, sql)
        # 日志输出
        LOG.debug('\n%s', response)

        # query_account
        LOG.debug('\n\n\nSample 2: error logs detail\n\n\n')
        # 开始时间  格式：YYYY-MM-DDTHH:mm:ssZ
        start_time = "2023-12-13T06:00:00Z"
        # 结束时间  格式：YYYY-MM-DDTHH:mm:ssZ
        end_time = "2023-12-13T18:00:00Z"
        # 当前页数
        page_no = 3
        # 每页条数
        page_size = 10
        # 搜索关键词 ，模糊条件
        key_word = "test_name1"
        # 调用接口
        response = rds_client.error_log_detail(instance_id, start_time, end_time, page_no,
                                               page_size, key_word)
        # 日志输出
        LOG.debug('\n%s', response)

        # slow_logs_list
        LOG.debug('\n\n\nSample 3: slow logs list\n\n\n')
        # 慢日志时间点
        datetime = "2023-12-10T19:48:05Z"
        # 调用接口
        response = rds_client.slow_log_list(instance_id, datetime)
        # 日志输出
        LOG.debug('\n%s', response)

        # slow_logs_download_detail
        LOG.debug('\n\n\nSample 4: slow logs download detail\n\n\n')
        # 慢日志id
        log_id = "slowlog.202312130005"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = 1800
        # 调用接口
        response = rds_client.slow_log_download_detail(instance_id, log_id,
                                                       download_valid_time_in_sec)
        # 日志输出
        LOG.debug('\n%s', response)

        # error_logs_list
        LOG.debug('\n\n\nSample 5: error logs list\n\n\n')
        # 慢日志时间点
        datetime = "2023-12-13T15:50:12Z"
        # 调用接口
        response = rds_client.error_log_list(instance_id, datetime)
        # 日志输出
        LOG.debug('\n%s', response)

        # error_logs_download_detail
        LOG.debug('\n\n\nSample 6: error logs download detail\n\n\n')
        # 慢日志id
        log_id = "errorlog.202312131549"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = "1800"
        # 调用接口
        response = rds_client.error_log_download_detail(instance_id, log_id,
                                                        download_valid_time_in_sec)
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
