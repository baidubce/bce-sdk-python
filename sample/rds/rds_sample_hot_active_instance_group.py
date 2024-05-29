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
Sample for rds hot active instance group example.
"""

import os
import sys
import logging

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_hot_active_instance_group_manager as hot_active_instance_group

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG,
                    filename='./rds_sample_hot_active_instance_group.log',
                    filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = hot_active_instance_group.\
        RdsHotActiveInstanceGroupManager(CONF.config)

    try:

        # 热活实例组id
        group_id = "rdcn8z8f8n8"
        # 主角色 实例id
        leader_id = "rds-Ow4u3xBM"
        # 从角色 实例id
        follower_id = 'rds-qfsugnmr'

        # check_gtid_group
        LOG.debug('\n\n\nSample 1: check gtid group\n\n\n')
        # 检查gtid的实例短id
        instance_id = leader_id
        # 调用接口
        response = rds_client.check_gtid_group(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # check_ping_group
        LOG.debug('\n\n\nSample 2: check ping group\n\n\n')
        # source_id实例短id
        source_id = leader_id
        # target_id实例短id
        target_id = follower_id
        # 调用接口
        response = rds_client.check_ping_group(source_id, target_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # check_data_group
        LOG.debug('\n\n\nSample 3: check data group\n\n\n')
        # 连通性检查（数据检查）的实例短id
        instance_id = leader_id
        # 调用接口
        response = rds_client.check_data_group(instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # create_group
        LOG.debug('\n\n\nSample 4: create group\n\n\n')
        # 创建热活实例组名称
        name = "test_hot_rds"
        # 主角色短实例id
        leader_id = leader_id
        # 调用接口
        response = rds_client.create_group(name, leader_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # group_batch_join
        LOG.debug('\n\n\nSample 5: group batch join\n\n\n')
        # leader_id和 follower_ids 的 id都不加入任何实例组中慢，方可成功
        # 从角色短实例id列表
        follower_ids = [follower_id]
        # 热活实例组名称
        name = "test_hot_rds"
        # 调用接口
        response = rds_client.group_batch_join(follower_ids, name, leader_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # add_instance_to_group
        LOG.debug('\n\n\nSample 6: add instance to group\n\n\n')
        # 从角色短实例id
        follower_id = "rds-6SSrsqxG"
        # 调用接口
        response = rds_client.add_instance_to_group(group_id, follower_id)
        # 输出日志
        LOG.debug('\n%s', response)

        # group_list
        LOG.debug('\n\n\nSample 7: group list\n\n\n')
        # 排序规则：asc(升序)/desc（降序）
        order = rds_enum.Order.ASC
        # 排序字段
        order_by = "name"
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 过滤字符串 从groupId、groupName、instanceStatus 三个key过滤
        # filter_map_str = "{\"groupId\":\"rdcqzga9i4s\"}"
        # filter_map_str = "{\"groupName\":\"acount-test\"}"
        # filter_map_str = "{\"instanceStatus\":\"topoModifying\"}"
        filter_map_str = None
        # 截止日期
        days_to_expiration = -1
        # 调用接口
        response = rds_client.group_list(order, order_by, page_no, page_size, filter_map_str,
                                         days_to_expiration)
        # 输出日志
        LOG.debug('\n%s', response)

        # detail_group
        LOG.debug('\n\n\nSample 8: detail group\n\n\n')
        # 热活实例组id
        group_id = group_id
        # 调用接口
        response = rds_client.detail_group(group_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # force_change_instance
        LOG.debug('\n\n\nSample 9: force change instance\n\n\n')
        # force：0 - 非故障（非故障状态时使用）1 - 故障
        force = 1
        # 最大允许备库Behind_Master值（0 表示要求备库和故障主库数据完全一致，
        # 建议业务从0开始逐步增加，直至最大容忍值，force=0时，该参数不生效 ）
        max_behind = 10
        # 调用接口
        response = rds_client.force_change_instance(group_id, "rds-6SSrsqxG", force, max_behind)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify_instances_group_name
        LOG.debug('\n\n\nSample 10: modify_instances_group_name\n\n\n')
        # 修改热活实例组的id
        group_id = group_id
        # 修改的热活实例组名称
        group_name = "test_hot_rds_group"
        # 调用接口
        response = rds_client.modify_instances_group_name(group_id, group_name)
        # 输出日志
        LOG.debug('\n%s', response)

        # master_role_change
        LOG.debug('\n\n\nSample 11: master role change\n\n\n')
        # 调用接口
        response = rds_client.master_role_change(group_id, leader_id)
        # 输出日志
        LOG.debug('\n%s', response)

        # quit_instances_group
        LOG.debug('\n\n\nSample 12: quit instances group\n\n\n')
        # 调用接口
        response = rds_client.quit_instances_group(group_id, "rds-6SSrsqxG")
        # 输出日志
        LOG.debug('\n%s', response)

        # delete_instances_group
        LOG.debug('\n\n\nSample 13: delete instances group\n\n\n')
        # 调用接口
        response = rds_client.delete_instances_group(group_id)
        # 输出日志
        LOG.debug('\n%s', response)

        # check_min_version
        LOG.debug('\n\n\nSample 14: check min version\n\n\n')
        # 调用接口
        response = rds_client.check_min_version(leader_id, follower_id)
        # 输出日志
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
