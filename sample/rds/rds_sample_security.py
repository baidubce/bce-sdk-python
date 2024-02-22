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
Sample for rds security example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds import rds_security_manager as security_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_security.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = security_manager.RdsSecurityManager(CONF.config)
    try:

        # 获取access_key
        access_key = rds_client.config.credentials.access_key_id
        # 实例id
        instance_id = "rds-rWLm6n4e"

        # whit_list
        LOG.debug('\n\n\nSample 1: whit list\n\n\n')
        # 调用接口
        response = rds_client.whit_list(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # update_whit_list
        LOG.debug('\n\n\nSample 2: update whit list\n\n\n')
        # 创建白名单
        security_ips = ['127.0.0.1']
        # 修改版本号, 这个参数值是从查询白名单的返回头域字段x-bce-if-match获取
        # 或者从返回结果的etag字段获取
        e_tag = "v5"
        # 调用接口
        response = rds_client.update_whit_list(instance_id, security_ips, e_tag)
        # 日志输出
        LOG.debug('\n%s', response)

        # set_ssl_status
        LOG.debug('\n\n\nSample 3: set ssl status\n\n\n')
        # 公网状态
        status = True
        # 调用接口
        response = rds_client.set_ssl_status(instance_id, status)
        # 日志输出
        LOG.debug('\n%s', response)

        # obtain_ssl_encrypted_info
        LOG.debug('\n\n\nSample 4: obtain ssl encrypted info\n\n\n')
        # 调用接口
        response = rds_client.obtain_ssl_encrypted_info(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # obtain_ssl_ca
        LOG.debug('\n\n\nSample 5: obtain ssl ca\n\n\n')
        # 调用接口
        response = rds_client.obtain_ssl_ca()
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
