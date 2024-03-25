#!/usr/bin/env python
# coding=utf8

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
from baidubce.services.rds.models import rds_instance_model
from baidubce.services.rds import rds_instance_manager as instance_manager

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsInstanceManager(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.vpc_id = 'vpc-ph7237ym686c'
        self.subnets = [
            rds_instance_model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        self.post_billing = rds_instance_model.Billing(pay_method='Postpaid')
        self.engine = 'MySql'
        self.engine_version = '5.7'
        self.category = 'Standard'
        self.cpu_count = 1
        self.memory_capacity = 2
        self.volume_capacity = 100
        self.disk_io_type = 'cloud_enha'
        self.rds_client1 = instance_manager.RdsInstanceManager(config1)
        self.rds_client2 = instance_manager.RdsInstanceManager(config2)

    # 创建实例
    def test_create_instance(self):
        # 设置实例名称
        instance_name = 'rds-py-create'
        # 支付方式
        billing = self.post_billing
        # 批量创建云数据库 RDS 实例个数, 最大不超过10个， 默认为1
        purchase_count = 1
        # 数据库类型
        engine = self.engine
        # 数据库版本
        engine_version = self.engine_version
        # 实例类别，basic：单机版本，Standard：双机高可用版本
        category = self.category
        # cpu 核数
        cpu_count = self.cpu_count
        # 内存大小 单位GB
        memory_capacity = self.memory_capacity
        # 磁盘大小 单位GB
        volume_capacity = self.volume_capacity
        # 磁盘类型，cloud_ssd：SSD云硬盘，cloud_essd：ESSD云硬盘，local_hdd_pro：本地
        disk_io_type = self.disk_io_type
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        # tags = [
        #    model.Tag(u'key', u'value'),
        #    model.Tag(u'zyh', u'haha')
        # ]
        # parameter_template_id = "167"
        # initial_data_reference = model.InitialDataReference(instance_id='rds-gvQDRheI',
        #                                                     reference_type='snapshot',
        #                                                     snapshot_id='1681225244867371501')
        # data = [
        #    model.RecoveryToSourceInstanceModel(db_name='test2',
        #                                        new_dbname='test22',
        #                                        restore_mode='table',
        #                                        tables=[
        #                                            model.Tables(table_name='table1',
        #                                                         new_tablename='table11')
        #                                        ]
        #                                        )
        # ]
        # 调用接口
        response = self.rds_client1.create_instance(instance_name=instance_name,
                                                    billing=billing,
                                                    purchase_count=purchase_count,
                                                    engine=engine,
                                                    engine_version=engine_version,
                                                    category=category,
                                                    cpu_count=cpu_count,
                                                    memory_capacity=memory_capacity,
                                                    volume_capacity=volume_capacity,
                                                    disk_io_type=disk_io_type,
                                                    vpc_id=vpc_id, subnets=subnets,
                                                    is_direct_pay=is_direct_pay)
        # 设置实例节点id
        self.instance_id = response.instance_ids[0]

    # 创建只读实例
    def test_create_read_instance(self):
        # 设置只读实例名称
        instance_name = 'rds-py-create-read'
        # 主实例id
        source_instance_id = self.instance_id
        # 支付方式
        billing = self.post_billing
        # cpu 核数
        cpu_count = self.cpu_count
        # 内存大小 单位GB
        memory_capacity = self.memory_capacity
        # 磁盘大小 单位GB
        volume_capacity = self.volume_capacity
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        # 调用接口
        response = self.rds_client1.create_read_instance(instance_name=instance_name,
                                                         source_instance_id=source_instance_id,
                                                         billing=billing,
                                                         vpc_id=vpc_id,
                                                         is_direct_pay=is_direct_pay,
                                                         subnets=subnets,
                                                         cpu_count=cpu_count,
                                                         memory_capacity=memory_capacity,
                                                         volume_capacity=volume_capacity)
        # 设置只读节点id
        instance_read_id = response.instance_ids[0]

    def test_create_proxy_instance(self):
        # 创建代理实例
        instance_name = 'rds-py-create-proxy'
        # 主实例id
        source_instance_id = self.instance_id
        # 支付方式
        billing = self.post_billing
        # 节点数量
        node_amount = 2
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        # 调用接口
        response = self.rds_client1.create_proxy_instance(instance_name=instance_name,
                                                          source_instance_id=source_instance_id,
                                                          billing=billing,
                                                          vpc_id=vpc_id,
                                                          is_direct_pay=is_direct_pay,
                                                          subnets=subnets,
                                                          node_amount=node_amount)
        # 设置代理节点id
        instance_proxy_id = response.instance_ids[0]

    def test_instance_detail(self):
        # 实例详情
        self.rds_client1.get_instance_detail(self.instance_id)

    def test_instance(self):
        # 实例列表
        self.rds_client1.list_instances(max_keys=10)

    # 变配实例
    def test_resize_instance(self):
        # 实例id
        instance_id = self.instance_id
        # cpu 核数
        cpu_count = 1
        # 内存大小 单位GB
        memory_capacity = 4
        # 磁盘大小 单位GB
        volume_capacity = 100
        # node_amount = 4
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 调用接口
        self.rds_client1.resize_instance(instance_id=instance_id,
                                         cpu_count=cpu_count,
                                         memory_capacity=memory_capacity,
                                         volume_capacity=volume_capacity,
                                         is_direct_pay=is_direct_pay)

    # 重启实例
    def test_reboot_instance(self):
        # 调用接口
        self.rds_client1.reboot_instance(self.instance_id)

    # 更新实例名称
    def test_rename_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 实例名称
        instance_name = "py-test"
        # 调用接口
        self.rds_client1.rename_instance(instance_id=instance_id,
                                         instance_name=instance_name)

    # 更新实例同步模式
    def test_modify_sync_mode_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 同步模式（异步复制：Async，半同步复制：Semi_sync）
        sync_mode = "Semi_sync"
        # 调用接口
        self.rds_client1.modify_sync_mode_instance(instance_id=instance_id,
                                                   sync_mode=sync_mode)

    def test_modify_endpoint_instance(self):
        # 更新实例连接信息
        instance_id = self.instance_id
        # 地址
        address = "python"
        # 调用接口
        self.rds_client1.modify_endpoint_instance(instance_id=instance_id,
                                                  address=address)

    def test_modify_public_access_instance(self):
        # 更新实例公网访问状态
        instance_id = self.instance_id
        # 公网访问状态 0：关闭公网访问，1：开启公网访问
        public_access = bool(1)
        # 调用接口
        self.rds_client1.modify_public_access_instance(instance_id=instance_id,
                                                       public_access=public_access)

    # 实例开启自动续费
    def test_auto_renew_instance(self):
        # 实例id
        instance_ids = [self.instance_id]
        # 自动续费周期单位（年：year；月：month）
        auto_renew_time_unit = "month"
        # 续费周期按月（不超过9个月）按年付费（不超过3年）
        auto_renew_time = 1
        # 调用接口
        self.rds_client1.auto_renew_instance(instance_ids=instance_ids,
                                             auto_renew_time_unit=auto_renew_time_unit,
                                             auto_renew_time=auto_renew_time)

    # 查询可用区列表
    def test_zone_list(self):
        # 调用接口
        self.rds_client1.zone()

    # 查询查询子网列表
    def test_subnet_list(self):
        # 调用接口
        self.rds_client1.subnet()

    # 获取价格
    def test_price_instance(self):
        instance = rds_instance_model.Instance(engine='sqlserver',
                                               engine_version='2016',
                                               cpu_count=2,
                                               allocated_memory_in_g_b=8,
                                               allocated_storage_in_g_b=50,
                                               category='Singleton',
                                               disk_io_type='cloud_enha')
        # 时长。支付方式为后支付时不需要设置，预支付时必须设置。时间单位默认为month。
        duration = 1
        # 购买数量，默认值为1。
        number = 1
        # 支付类型
        product_type = "prepay"
        # 调用接口
        self.rds_client1.price_instance(instance=instance,
                                        duration=duration,
                                        number=number,
                                        product_type=product_type)

    # 暂停实例
    def test_suspend_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.suspend_instance(instance_id=instance_id)

    # 启动实例
    def test_start_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.start_instance(instance_id=instance_id)

    # 释放实例
    def test_delete_instance(self):
        # 调用接口
        self.rds_client1.delete_instance(self.instance_id)

    # 更新时间窗口
    def test_maintaintime_instance(self):
        # 实例id
        self.instance_id = "rds-RAFJszBj"
        # 实例维护时间窗口的持续时间，单位是小时，如：1；
        maintain_duration = 1
        # 维护时间
        maintain_start_time = "05:00:00"
        # 调用接口
        self.rds_client1.maintaintime_instance(self.instance_id, maintain_start_time, maintain_duration)


if __name__ == '__main__':
    unittest.main()
