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
Sample for rds readonly group example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
import baidubce.services.rds.rds_readonly_group_manager as readonly_group
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample_read_only_group.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = readonly_group.RdsReadOnlyGroupManager(CONF.config)

    try:

        # 实例id
        instance_id = 'rds-rWLm6n4e'
        # 只读组id
        ro_group_id = "rdsmrg-rn6xw3h2"

        # 只读组创建后，由于只读组状态在短时间内无法为正常状态，因此
        # 其他只读组创建的时候出错，这里建议用test目录单侧
        # create_readonly_group
        LOG.debug('\n\n\nSample 1: create readonly group\n\n\n')
        # vpcId
        vpc_id = "vpc-70pxg3pmv8rv"
        # 子网Id
        subnet_id = "sbn-dqafncqsy3y4"
        # 只读组名称（可选参数）
        ro_group_name = "test_name"
        # 是否启用延迟剔除，默认为关闭（可选参数）
        enable_delay_off = True
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1（可选参数）
        least_app_amount = 5
        # 是否启用重新负载均衡开关（可选参数）
        balance_reload = True
        # 分配到共享集群还是专属集群（可选参数）
        bgw_group_exclusive = False
        # 集群id（可选参数）
        bgw_groupId = None
        # 服务端口,MySQL默认为3306（可选参数）
        entry_port = 3306
        # 内网ip（可选参数，建议获取同一个子网的内网IP，否则创建后在控制台不可见）
        vnet_ip = None
        # 延迟阈值，取值为大于等于0的整数，默认为10（可选参数）
        delay_threshold = 11
        # 调用接口
        response = rds_client.create_readonly_group(instance_id,
                                                    vpc_id,
                                                    subnet_id,
                                                    ro_group_name,
                                                    enable_delay_off,
                                                    least_app_amount,
                                                    balance_reload,
                                                    bgw_group_exclusive,
                                                    bgw_groupId,
                                                    entry_port,
                                                    vnet_ip,
                                                    delay_threshold)
        # 日志输出
        LOG.debug('\n%s', response)

        # master_instance_associated_readonly_List
        LOG.debug('\n\n\nSample 2: readonly_group_detail\n\n\n')
        # 调用接口
        response = rds_client.readonly_group_detail(instance_id, ro_group_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # master_instance_associated_readonly_List
        LOG.debug('\n\n\nSample 3: master instance associated readonly List\n\n\n')
        # 调用接口
        response = rds_client.master_instance_associated_readonly_List(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # join_readonly_group
        LOG.debug('\n\n\nSample 4: join readonly group\n\n\n')
        # 只实例短id或者长id都可以
        app_id = "rds-ewfD4Bts"
        # 只读实例短id
        app_id_short = "rds-ewfD4Bts"
        # app_name
        app_name = "test"
        # 权重
        weight = 1
        # 主实例id
        source_app_id = "rds-rWLm6n4e"
        # 只读实例状态
        status = "available"
        # 创建时间
        create_time = "2023-12-11T15:15:00Z"
        # 更新时间
        update_time = "2023-12-11T15:15:00Z"
        # 只读组状态
        app_status = "online"
        # App
        app = request_param.App(app_id, app_name, weight, ro_group_id, source_app_id,
                                status, create_time, update_time, app_status,
                                app_id_short)
        # 只读实例组
        readReplicaList = [app.to_json()]
        # 调用接口
        response = rds_client.join_readonly_group(instance_id, ro_group_id, readReplicaList)
        # 日志输出
        LOG.debug('\n%s', response)

        # readonly_group_load_balance
        LOG.debug('\n\n\nSample 5: readonly group load balance\n\n\n')
        # 调用接口
        response = rds_client.readonly_group_load_balance(instance_id, ro_group_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # batch_modify_readonly_group_properties
        LOG.debug('\n\n\nSample 6: batch modify readonly group properties\n\n\n')
        # 只读组名称（可选参数）
        ro_group_name = None
        # 只读组的延迟自动剔除开关（可选参数）
        enable_delay_off = False
        # 延迟阈值，取值为大于等于0的整数，范围1-2147483646,enable_delay_off开启有效（可选参数）
        delay_threshold = 90
        # 只读组的重新负载均衡开关（可选参数）
        balance_reload = None
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1（可选参数）
        least_app_amount = None
        # 只读实例短id或者长id都可以
        app_id = "rds-ewfD4Bts"
        # 权重
        weight = 1
        # 要修改权重的只读实例对象
        readReplica = request_param.ReadReplica(app_id, weight)
        # 要修改权重的只读实例列表,不传递填（可选参数）
        readReplicaList = [readReplica.to_json()]
        read_replica_list = None
        # 调用接口
        response = rds_client.batch_modify_readonly_group_properties(instance_id,
                                                                     ro_group_id,
                                                                     ro_group_name,
                                                                     enable_delay_off,
                                                                     delay_threshold,
                                                                     balance_reload,
                                                                     least_app_amount,
                                                                     read_replica_list)
        # 日志输出
        LOG.debug('\n%s', response)

        # update_publicly_accessible
        LOG.debug('\n\n\nSample 7: update publicly accessible\n\n\n')
        # 是否开启状态，true：开启，false：关闭
        publicly_accessible = False
        # 调用接口
        response = rds_client.update_publicly_accessible(instance_id, ro_group_id,
                                                         publicly_accessible)
        # 日志输出
        LOG.debug('\n%s', response)

        # update_endpoint
        LOG.debug('\n\n\nSample 8: update endpoint\n\n\n')
        # 只读组名没，（可选参数）
        ro_group_name = "test_name"
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1，（可选参数）
        least_app_amount = 1
        # 延迟阈值，取值为大于等于0的整数，默认为10（可选参数）
        delay_threshold = 10
        # 连接信息，address必填,其他参数选填
        endpoint = request_param.Endpoint(None, "127.0.0.1", None, "dmxmk")
        # 调用接口
        response = rds_client.update_endpoint(instance_id, ro_group_id, endpoint,
                                              ro_group_name, least_app_amount,
                                              delay_threshold)
        # 日志输出
        LOG.debug('\n%s', response)

        # level_readonly_group
        LOG.debug('\n\n\nSample 9: level readonly group\n\n\n')
        # 只读组id，要离开的只读实例id列表 ,多个逗号分隔
        read_replica_list = ["rds-ewfD4Bts"]
        # 调用接口
        response = rds_client.level_readonly_group(instance_id, ro_group_id,
                                                   read_replica_list)
        # 日志输出
        LOG.debug('\n%s', response)

        # delete_readonly_group
        LOG.debug('\n\n\nSample 10: delete readonly group\n\n\n')
        # 调用接口
        response = rds_client.delete_readonly_group(instance_id, ro_group_id)
        # 日志输出
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
