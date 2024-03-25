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

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_hot_active_instance_group_manager as hot_active_instance_group

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsHotActiveInstanceGroupManager(unittest.TestCase):
    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.group_id = 'rdcdp0hqwp7'
        self.leader_id = 'rds-Ow4u3xBM'
        self.follower_id = 'rds-qfsugnmr'
        self.rds_client1 = hot_active_instance_group.RdsHotActiveInstanceGroupManager(config1)
        self.rds_client2 = hot_active_instance_group.RdsHotActiveInstanceGroupManager(config2)

    # 强制切换热活实例组id
    def test_force_change_instance(self):
        # 热活实例组id
        group_id = self.group_id
        # 需要切换的主角色的实例id
        leader_id = self.leader_id
        # force：0 - 非故障（非故障状态时使用）1 - 故障
        force = 1
        # 最大允许备库Behind_Master值（0 表示要求备库和故障主库数据完全一致，
        # 建议业务从0开始逐步增加，直至最大容忍值，force=0时，该参数不生效 ）
        max_behind = 10
        # 调用接口
        self.rds_client1.force_change_instance(group_id, leader_id, force, max_behind)

    # 批量加入热活实例组
    def test_group_batch_join(self):
        # leader_id和 follower_ids 的 id都不加入任何实例组中慢，方可成功
        # 从角色短实例ids列表
        follower_ids = [self.follower_id]
        # 热活实例组名称
        name = "test_hot_rds"
        # 主角色短实例id
        leader_id = self.leader_id
        # 调用接口
        self.rds_client1.group_batch_join(follower_ids, name, leader_id)

    # 创建热活实例组
    def test_create_group(self):
        # 创建热活实例组名称
        name = "test_hot_rds"
        # 主角色短实例id
        leader_id = self.leader_id
        # 调用接口
        self.rds_client1.create_group(name, leader_id)

    # 查询热活实例组列表（需要修改参数）
    def test_group_list(self):
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
        self.rds_client1.group_list(order, order_by, page_no, page_size, filter_map_str,
                                    days_to_expiration)

    # 热活实例组详情
    def test_detail_group(self):
        # 热活实例组id
        group_id = self.group_id
        # 调用接口
        self.rds_client1.detail_group(group_id)

    # 实例组前置检查（GTID检查）
    # 双角色ID不在任何实例组中，且在同一地域，返回结果才是true
    def test_check_gtid_group(self):
        # 短实例id
        instance_id = self.follower_id
        # 调用接口
        self.rds_client1.check_gtid_group(instance_id)

    # 实例组前置检查（实例连通性检查）
    # 双角色id不在任何实例组中，且在同一地域，返回结果才是true
    def test_check_ping_group(self):
        # source_id实例短id
        source_id = self.leader_id
        # target_id实例短id
        target_id = self.follower_id
        # 调用接口
        self.rds_client1.check_ping_group(source_id, target_id)

    # 实例组前置检查（数据检查）
    # 双角色id不在任何实例组中，且在同一地域，返回结果才是true
    def test_check_data_group(self):
        # 实例短id
        instance_id = self.leader_id
        # 调用接口
        self.rds_client1.check_data_group(instance_id)

    # 加入某个实例组
    def test_add_instance_to_group(self):
        # 热活实例组的id
        group_id = self.group_id
        # 从角色短实例id
        follower_id = self.follower_id
        # 调用接口
        self.rds_client1.add_instance_to_group(group_id, follower_id)

    # 修改热活实例组名称
    def test_modify_instances_group_name(self):
        # 修改热活实例组的id
        group_id = self.group_id
        # 修改的热活实例组名称
        group_name = "test_hot_rds_group"
        # 调用接口
        self.rds_client1.modify_instances_group_name(group_id, group_name)

    # 删除热活实例组
    def test_delete_instances_group(self):
        # 热活实例组id
        group_id = self.group_id
        # 调用接口
        self.rds_client1.delete_instances_group(group_id)

    # 主角色变更
    def test_master_role_change(self):
        # 热活实例组id
        group_id = self.group_id
        # 主角色短实例id
        leader_id = self.leader_id
        # 调用接口
        self.rds_client1.master_role_change(group_id, leader_id)

    # 退出某个实例组
    def test_quit_instance_to_group(self):
        # 热活实例组id
        group_id = self.group_id
        # 退出热活实例组中的短实例id
        instance_id = self.follower_id
        # 调用接口
        self.rds_client1.quit_instances_group(group_id, instance_id)

    # 小版本前置检查
    def test_check_min_version(self):
        # 主角色短实例id
        leader_id = self.leader_id
        # 从角色短实例id
        follower_id = self.follower_id
        # 调用接口
        self.rds_client1.check_min_version(leader_id, follower_id)
