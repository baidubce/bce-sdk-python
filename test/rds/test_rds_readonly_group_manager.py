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
Unit test for rds readonly group manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds import rds_readonly_group_manager as readonly_group_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsReadOnlyGroupManager(unittest.TestCase):
    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = readonly_group_manager.RdsReadOnlyGroupManager(config1)
        self.rds_client2 = readonly_group_manager.RdsReadOnlyGroupManager(config2)
        self.ACCESS_KEY = config1.credentials.access_key_id

    # 创建实例组(只读实例组存在2个以上接口执行会提示错误）
    def test_create_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # vpcId
        vpc_id = "vpc-70pxg3pmv8rv"
        # 子网Id
        subnet_id = "sbn-dqafncqsy3y4"
        # 只读组名称（可选参数）
        ro_group_name = "test_name_group"
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
        self.rds_client1.create_readonly_group(instance_id,
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
                                               delay_threshold
                                               )
    # 只读组详情

    def test_readonly_group_detail(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-rn6xw3h2"
        # 调用接口
        self.rds_client1.readonly_group_detail(instance_id, ro_group_id)

    # 只读实例组列表
    def test_master_instance_associated_readonly_List(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.master_instance_associated_readonly_List(instance_id)

    # 加入只读组
    def test_join_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-rn6xw3h2"
        # 只实例短id或者长id都可以
        app_id = "rds-ewfD4Bts"
        # 只实例短id
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
        app = request_param.App(
            app_id,
            app_name,
            weight,
            ro_group_id,
            source_app_id,
            status,
            create_time,
            update_time,
            app_status,
            app_id_short)
        # 只读实例组
        readReplicaList = [app.to_json()]
        # 调用接口
        self.rds_client1.join_readonly_group(instance_id, ro_group_id,
                                             readReplicaList)

    # 负载重新均衡
    def test_readonly_group_load_balance(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 调用接口
        self.rds_client1.readonly_group_load_balance(instance_id, ro_group_id)

    # 批量修改只读组名称、延迟剔除开关、延迟阈值、重新负载均衡开关、组内只读实例权重。
    def test_batch_modify_readonly_group_properties(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
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
        self.rds_client1.batch_modify_readonly_group_properties(instance_id,
                                                                ro_group_id,
                                                                ro_group_name,
                                                                enable_delay_off,
                                                                delay_threshold,
                                                                balance_reload,
                                                                least_app_amount,
                                                                read_replica_list)

    # 只读组开启/关闭公网
    def test_update_publicly_accessible(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 是否开启状态，true：开启，false：关闭
        publicly_accessible = False
        # 调用接口
        self.rds_client1.update_publicly_accessible(instance_id, ro_group_id,
                                                    publicly_accessible)

    # 只读组修改连接信息
    def test_update_endpoint(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 只读组名，（可选参数）
        ro_group_name = "test_name"
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1，（可选参数）
        least_app_amount = 1
        # 延迟阈值，取值为大于等于0的整数，默认为10（可选参数）
        delay_threshold = 10
        # 连接信息，address必填,其他参数选填
        endpoint = request_param.Endpoint(None, "xxx.xxx.xxx.xxx", None, "dmxmk")
        # 调用接口
        self.rds_client1.update_endpoint(instance_id,
                                         ro_group_id,
                                         endpoint,
                                         ro_group_name,
                                         least_app_amount,
                                         delay_threshold)

    # 只读实例离开只读组（离开字读组后，只读组没有只读实例，将自动删除只读组）
    def test_level_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 要离开的只读实例id列表 ,多个逗号分隔
        read_replica_list = ["rds-ewfD4Bts"]
        # 调用接口
        self.rds_client1.level_readonly_group(instance_id, ro_group_id,
                                              read_replica_list)

    # 删除只读组
    def test_delete_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-zyhrfm3j"
        # 调用接口
        self.rds_client1.delete_readonly_group(instance_id, ro_group_id)
